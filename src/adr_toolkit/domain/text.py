"""Small text helpers shared by the rules."""

from __future__ import annotations

import re

_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")


def squash(text: str) -> str:
    """Collapse every run of whitespace to one space."""
    return " ".join(text.split())


def sentences(text: str) -> list[str]:
    """Split prose into sentences. Lists and labels in the documents end with a full stop on purpose."""
    flat = squash(text)
    return [part for part in _SENTENCE_BREAK.split(flat) if part] if flat else []


def words(text: str) -> list[str]:
    """The words of a text, lower-cased."""
    return [match.lower() for match in _WORD.findall(text)]


def has_figure(text: str) -> bool:
    """True when the text holds at least one digit: a number, a date or a count."""
    return any(character.isdigit() for character in text)


def similarity(first: str, second: str) -> float:
    """Jaccard similarity of the two texts' word sets, from 0 (nothing shared) to 1 (the same words)."""
    left, right = set(words(first)), set(words(second))
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
