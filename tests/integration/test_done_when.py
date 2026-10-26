"""One test per 'Done when' line of the lesson, run over copies of the repository's own documents."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from adr_toolkit.application.check_documents import CheckSettings, check_documents
from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import REPOSITORY_ROOT

ADR = "docs/adr/0007-announce-paid-orders.md"
AUDIENCES = "docs/communication/0007-audiences.md"
REACTION = "docs/review/0007-reaction.md"


@pytest.fixture
def docs(tmp_path: Path) -> Path:
    shutil.copytree(REPOSITORY_ROOT / "docs", tmp_path / "docs")
    return tmp_path


def codes(root: Path) -> set[str]:
    store = FileSystemStore(root)
    report = check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=(7,)))
    return {finding.code for finding in report.errors}


def edit(root: Path, path: str, old: str, new: str) -> None:
    file = root / path
    text = file.read_text()
    assert old in text, f"{old!r} not in {path}"
    file.write_text(text.replace(old, new))


def test_the_repository_as_committed_passes(docs: Path) -> None:
    assert codes(docs) == set()


def test_done_when_1_two_options_each_with_a_real_advantage(docs: Path) -> None:
    record = MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)
    assert len(record.options) >= 2
    assert all(len(option.advantage.split()) >= 4 for option in record.options)
    edit(docs, ADR, "Advantage: nothing new to run; it ships this week.", "Advantage:")
    assert "ADR007" in codes(docs)


def set_context(root: Path, text: str) -> None:
    record = (root / ADR).read_text()
    start = record.index("## Context") + len("## Context\n")
    end = record.index("## Options considered")
    (root / ADR).write_text(record[:start] + text + "\n\n" + record[end:])


def test_done_when_2_a_context_that_argues_for_an_answer_is_rejected(docs: Path) -> None:
    set_context(docs, "The team has 6 engineers, so we need a simple tool. Option C is the one.")
    assert "ADR010" in codes(docs)


def test_done_when_2_a_context_with_no_numbers_is_rejected(docs: Path) -> None:
    set_context(docs, "Emails are late and the database is busy.")
    assert "ADR009" in codes(docs)


def test_done_when_3_each_option_is_described_by_the_same_three_lines(docs: Path) -> None:
    record = MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)
    for option in record.options:
        assert option.advantage
        assert option.main_cost
        assert option.pick_if
    edit(docs, ADR, "Pick it if: more consumers are coming and a clean boundary matters.", "")
    assert "ADR007" in codes(docs)


def test_done_when_4_a_bad_consequence_and_an_observable_trigger(docs: Path) -> None:
    record = MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)
    assert record.bad
    assert "1,000 events" in record.revisit_when
    edit(
        docs,
        ADR,
        "the relay's backlog is over 1,000 events for more than 5 minutes, or a third consumer needs ordering",
        "it stops working well, ordering",
    )
    assert "ADR015" in codes(docs)


def test_done_when_4_a_record_with_only_good_consequences_is_rejected(docs: Path) -> None:
    text = (docs / ADR).read_text()
    (docs / ADR).write_text("\n".join(line for line in text.splitlines() if not line.startswith("Bad:")) + "\n")
    assert "ADR013" in codes(docs)


def test_done_when_5_three_versions_that_answer_three_first_questions(docs: Path) -> None:
    versions = MarkdownRecordReader(FileSystemStore(docs)).read_audiences(AUDIENCES)
    assert versions.manager
    assert versions.engineers
    assert versions.sibling
    manager_text = versions.manager
    edit(docs, AUDIENCES, manager_text, versions.sibling)
    assert "AUD008" in codes(docs)


def test_done_when_5_jargon_in_the_manager_version_is_rejected(docs: Path) -> None:
    edit(docs, AUDIENCES, "The risk is 1 new process to run", "The risk is 1 new relay to run")
    assert "AUD006" in codes(docs)


def test_done_when_6_the_record_changed_after_a_real_reading(docs: Path) -> None:
    reaction = MarkdownRecordReader(FileSystemStore(docs)).read_reaction(REACTION)
    assert reaction.misunderstood
    assert reaction.after in " ".join((docs / ADR).read_text().split())
    edit(docs, ADR, "so consumers must ignore repeats by order id.", "so be careful.")
    assert "REA002" in codes(docs)
