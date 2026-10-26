from dataclasses import replace

from adr_toolkit.domain.findings import Severity
from adr_toolkit.domain.reaction import Reaction, check_reaction, check_talk

REACTION = Reaction(
    path="docs/review/0007-reaction.md",
    adr_number=7,
    reader="engineer",
    reader_kind="real",
    said_back="They send each order once.",
    misunderstood="The reader thought there are no repeats.",
    before="a stuck relay delays every consumer.",
    after="the relay can publish an event twice.",
)
RECORD = "Bad: the relay can publish an event twice."


def test_a_logged_fix_that_is_in_the_record_passes():
    assert check_reaction(REACTION, RECORD) == []


def test_an_empty_field_is_reported():
    assert {f.code for f in check_reaction(replace(REACTION, misunderstood=""), RECORD)} == {"REA001"}


def test_a_log_without_before_and_after_is_reported():
    assert {f.code for f in check_reaction(replace(REACTION, after=""), RECORD)} == {"REA001"}


def test_a_fix_that_is_not_in_the_record_is_reported():
    assert "REA002" in {f.code for f in check_reaction(REACTION, "Bad: nothing.")}


def test_a_sentence_that_is_still_in_the_record_is_reported():
    assert "REA003" in {f.code for f in check_reaction(REACTION, RECORD + " a stuck relay delays every consumer.")}


def test_a_worked_example_is_a_warning():
    findings = check_reaction(replace(REACTION, reader_kind="worked-example"), RECORD)
    assert [(f.code, f.severity) for f in findings] == [("REA004", Severity.WARNING)]


def test_a_talk_must_fit_three_minutes():
    assert check_talk("t.md", "word " * 399) == []
    assert [f.code for f in check_talk("t.md", "word " * 401)] == ["TLK001"]
    assert [f.code for f in check_talk("t.md", "word " * 20)] == ["TLK001"]
