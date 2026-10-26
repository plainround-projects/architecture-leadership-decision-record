"""Shared builders: a valid record, an in-memory document store, and the repository's own root."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from adr_toolkit.domain.adr import Adr, Option

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def valid_adr(**changes: object) -> Adr:
    """A record that passes every rule; tests change one field to break one rule."""
    base = Adr(
        path="docs/adr/0007-x.md",
        number=7,
        title="How the orders service announces paid orders",
        status="Accepted",
        superseded_by=None,
        supersedes=None,
        date_text="2026-10-22",
        deciders="Orders tech lead, database owner",
        sections=("Context", "Options considered", "Decision", "Consequences"),
        context="Volume grew from 2,000 to 40,000 orders a day and a scan takes 6 seconds.",
        options=(
            Option(
                "keep polling",
                "nothing new to run; it ships this week",
                "load grows with every new reader",
                "the team has no time to learn",
            ),
            Option(
                "an outbox table with a relay",
                "the event is written in the same transaction as the order",
                "one more table and a relay process to run",
                "events must never be lost",
            ),
        ),
        decision=(
            "We will write an event row beside the order in an outbox table and forward it with a relay, "
            "because it never loses an event."
        ),
        good="emails arrive in under 2 seconds",
        bad="we own one more table and one relay process",
        revisit_when="the relay backlog is over 1,000 events for more than 5 minutes",
        line_count=30,
        word_count=300,
    )
    return replace(base, **changes)  # type: ignore[arg-type]


class MemoryStore:
    """A DocumentStore held in a dict, for tests that need no disk."""

    def __init__(self, files: dict[str, str] | None = None) -> None:
        self.files = dict(files or {})

    def list_paths(self, folder: str) -> list[str]:
        return sorted(
            path for path in self.files if path.startswith(f"{folder}/") and "/" not in path[len(folder) + 1 :]
        )

    def read_text(self, path: str) -> str:
        return self.files[path]

    def exists(self, path: str) -> bool:
        return path in self.files

    def write_text(self, path: str, text: str) -> None:
        self.files[path] = text


@pytest.fixture
def repository_root() -> Path:
    return REPOSITORY_ROOT
