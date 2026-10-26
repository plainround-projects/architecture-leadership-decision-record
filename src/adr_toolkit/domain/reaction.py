"""The reaction log: what a reader got wrong, and the proof the record changed because of it."""

from __future__ import annotations

from dataclasses import dataclass

from adr_toolkit.domain.findings import Finding, error, warning
from adr_toolkit.domain.text import squash


@dataclass(frozen=True)
class Reaction:
    """One reading of a record by someone who was not in the room."""

    path: str
    adr_number: int | None
    reader: str
    reader_kind: str
    said_back: str
    misunderstood: str
    before: str
    after: str


def check_reaction(reaction: Reaction, adr_text: str) -> list[Finding]:
    """REA001 to REA004. The record text is searched for the fix, so a log cannot claim a change that never happened."""
    found: list[Finding] = []
    for label, value in (
        ("Reader", reaction.reader),
        ("Said back", reaction.said_back),
        ("Misunderstood", reaction.misunderstood),
    ):
        if not squash(value):
            found.append(error("REA001", reaction.path, f"'{label}' is empty"))
    if not reaction.before or not reaction.after:
        found.append(error("REA001", reaction.path, "the log must quote the sentence before and after the fix"))
        return found
    flat = squash(adr_text)
    if squash(reaction.after) not in flat:
        found.append(
            error("REA002", reaction.path, "the 'After' sentence is not in the record: the record was not updated")
        )
    if squash(reaction.before) in flat:
        found.append(
            error(
                "REA003",
                reaction.path,
                "the 'Before' sentence is still in the record: the misunderstanding is not fixed",
            )
        )
    if reaction.reader_kind != "real":
        found.append(
            warning(
                "REA004",
                reaction.path,
                f"reader kind is {reaction.reader_kind!r}: this is a worked example; replace it with a real reading",
            )
        )
    return found


def check_talk(path: str, text: str, max_words: int = 400) -> list[Finding]:
    """TLK001: three minutes of speech is about 400 words."""
    count = len(text.split())
    if count > max_words:
        return [error("TLK001", path, f"{count} words; three minutes is about {max_words}")]
    if count < 150:
        return [
            error("TLK001", path, f"{count} words is under a minute; the talk needs the options and the consequence")
        ]
    return []
