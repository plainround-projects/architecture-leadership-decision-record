"""The same decision told three ways, and the rules that keep each version for its reader."""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import combinations

from adr_toolkit.domain.findings import Finding, error
from adr_toolkit.domain.text import has_figure, sentences, similarity, words

MANAGER_JARGON = frozenset(
    {
        *("outbox", "relay", "idempotent", "idempotency", "broker", "kafka", "rabbitmq", "partition"),
        *("offset", "transaction", "consumer", "consumers", "publish", "publishes", "schema", "payload"),
        *("table", "index", "replica"),
    }
)
SIBLING_JARGON = frozenset(("outbox", "relay", "idempotent", "idempotency", "transaction", "broker"))
SIBLING_ACTIONS = frozenset(
    ("subscribe", "read", "stop", "switch", "migrate", "use", "update", "change", "move", "call", "send", "replace")
)
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_PATTERN = re.compile(rf"\b\d{{1,2}} (?:{_MONTHS})\b|\b\d{{4}}-\d{{2}}-\d{{2}}\b")


@dataclass(frozen=True)
class AudienceVersions:
    """The three short versions of one decision, keyed to the record they tell."""

    path: str
    adr_number: int | None
    engineers: str
    manager: str
    sibling: str
    sibling_name: str


def check_audiences(versions: AudienceVersions, decision: str) -> list[Finding]:
    """Apply AUD001 to AUD009. The decision text is the record's, so the engineer version can be tied to it."""
    found: list[Finding] = []
    for label, text in (
        ("engineers", versions.engineers),
        ("manager", versions.manager),
        ("sibling team", versions.sibling),
    ):
        if not sentences(text):
            found.append(error("AUD001", versions.path, f"the {label} version is missing"))
    if found:
        return found
    found += _engineers(versions, decision)
    found += _manager(versions)
    found += _sibling(versions)
    found += _no_copying(versions)
    return found


def _engineers(versions: AudienceVersions, decision: str) -> list[Finding]:
    found: list[Finding] = []
    count = len(sentences(versions.engineers))
    if not 3 <= count <= 8:
        found.append(
            error("AUD002", versions.path, f"engineers get the mechanism in about five sentences, not {count}")
        )
    wanted = {word for word in words(decision.split(" because ")[0]) if len(word) >= 5}
    if len(wanted & set(words(versions.engineers))) < 2:
        found.append(
            error("AUD003", versions.path, "the engineer version does not describe the mechanism the decision chose")
        )
    return found


def _manager(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    parts = sentences(versions.manager)
    if len(parts) > 2:
        found.append(
            error("AUD004", versions.path, f"the manager version is {len(parts)} sentences; two, with a number in each")
        )
    if not all(has_figure(part) for part in parts):
        found.append(
            error(
                "AUD005",
                versions.path,
                "every manager sentence carries a number: the first question is cost, risk or time",
            )
        )
    jargon = sorted(MANAGER_JARGON & set(words(versions.manager)))
    if jargon:
        found.append(error("AUD006", versions.path, f"jargon in the manager version: {', '.join(jargon)}"))
    return found


def _sibling(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    first = sentences(versions.sibling)[0]
    if not DATE_PATTERN.search(first):
        found.append(
            error("AUD007", versions.path, "the sibling team's first question is when: the first sentence needs a date")
        )
    if not SIBLING_ACTIONS & set(words(versions.sibling)):
        found.append(error("AUD007", versions.path, "the sibling note names no action (subscribe, read, switch, ...)"))
    jargon = sorted(SIBLING_JARGON & set(words(versions.sibling)))
    if jargon:
        found.append(error("AUD006", versions.path, f"internal jargon in the sibling note: {', '.join(jargon)}"))
    if len(sentences(versions.sibling)) < 2:
        found.append(
            error(
                "AUD007", versions.path, "the sibling note is too thin to tell the team what changes for them and when"
            )
        )
    return found


def _no_copying(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    texts = {"engineers": versions.engineers, "manager": versions.manager, "sibling team": versions.sibling}
    for (left_name, left), (right_name, right) in combinations(texts.items(), 2):
        shared = set(sentences(left)) & set(sentences(right))
        if shared or similarity(left, right) > 0.6:
            found.append(
                error(
                    "AUD008",
                    versions.path,
                    f"the {left_name} and {right_name} versions repeat each other; none answers its own reader",
                )
            )
    return found
