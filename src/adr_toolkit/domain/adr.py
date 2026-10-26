"""The architecture decision record as a value, and the rules a record must satisfy."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from adr_toolkit.domain.findings import Finding, error, warning
from adr_toolkit.domain.text import has_figure, squash, words

REQUIRED_SECTIONS = ("Context", "Options considered", "Decision", "Consequences")
STATUSES = ("Proposed", "Accepted", "Superseded")
VAGUE_TRIGGERS = (
    "if it stops working",
    "if needed",
    "when appropriate",
    "if there are problems",
    "if problems",
    "later",
)
DECISION_LANGUAGE = ("we will", "we should", "so we need", "we need to", "we must")
STOP_WORDS = frozenset({"with", "that", "this", "from", "into", "than", "then", "have", "will", "make", "keep"})


@dataclass(frozen=True)
class Option:
    """One option, described by the same three lines for every option."""

    name: str
    advantage: str
    main_cost: str
    pick_if: str


@dataclass(frozen=True)
class Adr:
    """A parsed decision record. Missing parts are empty strings or None, and the rules report them."""

    path: str
    number: int | None
    title: str
    status: str
    superseded_by: int | None
    supersedes: int | None
    date_text: str
    deciders: str
    sections: tuple[str, ...]
    context: str
    options: tuple[Option, ...]
    decision: str
    good: str
    bad: str
    revisit_when: str
    line_count: int
    word_count: int


@dataclass(frozen=True)
class AdrLimits:
    """The size of one page."""

    max_lines: int = 70
    max_words: int = 600


def check_adr(adr: Adr, limits: AdrLimits | None = None) -> list[Finding]:
    """Apply every rule to one record. The codes ADR001 to ADR018 are listed in the README."""
    limits = limits or AdrLimits()
    findings: list[Finding] = []
    for rule in (_header, _sections, _options, _context, _decision, _consequences):
        findings.extend(rule(adr))
    if adr.status == "Proposed":
        findings.append(warning("ADR018", adr.path, "still Proposed: accept it or withdraw it before the work starts"))
    if adr.line_count > limits.max_lines or adr.word_count > limits.max_words:
        findings.append(
            error(
                "ADR016",
                adr.path,
                f"longer than one page: {adr.line_count} lines and {adr.word_count} words "
                f"(limit {limits.max_lines} lines and {limits.max_words} words)",
            )
        )
    return findings


def _header(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if adr.number is None or not adr.title:
        found.append(error("ADR001", adr.path, "the first line must read '# ADR NNNN: title'"))
    if adr.status not in STATUSES:
        found.append(
            error(
                "ADR002", adr.path, f"status must be Proposed, Accepted or Superseded by ADR NNNN, got {adr.status!r}"
            )
        )
    if adr.status == "Superseded" and adr.superseded_by is None:
        found.append(error("ADR002", adr.path, "a Superseded record must say which one: 'Superseded by ADR NNNN'"))
    try:
        date.fromisoformat(adr.date_text)
    except ValueError:
        found.append(error("ADR003", adr.path, f"date must be an ISO date (YYYY-MM-DD), got {adr.date_text!r}"))
    if not adr.deciders or re.search(r"<.*>", adr.deciders):
        found.append(error("ADR004", adr.path, "name the deciders; a placeholder is not a name"))
    return found


def _sections(adr: Adr) -> list[Finding]:
    if adr.sections == REQUIRED_SECTIONS:
        return []
    missing = [name for name in REQUIRED_SECTIONS if name not in adr.sections]
    detail = f"missing {', '.join(missing)}" if missing else "out of order"
    return [error("ADR005", adr.path, f"sections must be {' / '.join(REQUIRED_SECTIONS)}: {detail}")]


def _options(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if len(adr.options) < 2:
        found.append(error("ADR006", adr.path, f"{len(adr.options)} option(s); a real decision has at least two"))
    for option in adr.options:
        for label, text in (
            ("Advantage", option.advantage),
            ("Main cost", option.main_cost),
            ("Pick it if", option.pick_if),
        ):
            if len(words(text)) < 4:
                found.append(
                    error("ADR007", adr.path, f"option '{option.name}': '{label}' is missing or too short to be fair")
                )
    names = [squash(option.name).lower() for option in adr.options]
    advantages = [squash(option.advantage).lower() for option in adr.options]
    if len(set(names)) < len(names) or len(set(advantages)) < len(advantages):
        found.append(
            error("ADR008", adr.path, "two options share a name or an advantage: one is the same choice renamed")
        )
    return found


def _context(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if not has_figure(adr.context):
        found.append(error("ADR009", adr.path, "the context has no number: facts, not feelings"))
    lowered = squash(adr.context).lower()
    leaks = [phrase for phrase in DECISION_LANGUAGE if phrase in lowered]
    leaks += [match.group(0) for match in re.finditer(r"\boption [a-z]\b", lowered)]
    if leaks:
        found.append(
            error(
                "ADR010",
                adr.path,
                f"the context argues for an answer ({', '.join(leaks)}); that belongs in the decision",
            )
        )
    return found


def _decision(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    text = squash(adr.decision)
    if not re.match(r"We will .+ because .+", text):
        found.append(
            error("ADR011", adr.path, "the decision must read 'We will <choice>, because <the deciding reason>.'")
        )
        return found
    if text.lower().count("because") > 1:
        found.append(
            error(
                "ADR012",
                adr.path,
                "more than one 'because': if two reasons are needed, the real reason is still hiding",
            )
        )
    choice = {word for word in words(text.split(" because ")[0]) if len(word) >= 4 and word not in STOP_WORDS}
    shared = [
        option.name
        for option in adr.options
        if len({word for word in words(option.name) if len(word) >= 4 and word not in STOP_WORDS} & choice) >= 2
    ]
    if adr.options and not shared:
        found.append(
            error("ADR017", adr.path, "the decision does not name any option considered; say which one was chosen")
        )
    return found


def _consequences(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if not adr.good:
        found.append(error("ADR013", adr.path, "the consequences list no good result"))
    if not adr.bad:
        found.append(
            error("ADR013", adr.path, "the consequences list no bad result: the record then reads as advertising")
        )
    if not adr.revisit_when:
        found.append(error("ADR014", adr.path, "no 'Revisit when:' trigger"))
    else:
        lowered = adr.revisit_when.lower()
        if not has_figure(lowered) or any(vague in lowered for vague in VAGUE_TRIGGERS):
            found.append(
                error(
                    "ADR015",
                    adr.path,
                    f"the revisit trigger must be observable (a number, a date or an event): {adr.revisit_when!r}",
                )
            )
    return found
