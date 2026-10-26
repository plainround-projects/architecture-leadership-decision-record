from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import MemoryStore

ADR = """# ADR 0009: Pick a thing

Status: Superseded by ADR 0010
Date: 2026-01-02
Deciders: Tech lead
Supersedes: ADR 0004

## Context
Facts: 5 of them,
on two lines.

## Options considered
### Option A: first way
Advantage: it is fast
and cheap.
Main cost: it is new
Pick it if: you are in a hurry

### Option B: second way
Advantage: it is old

## Decision
We will do the first way, because it is fast.

## Consequences
Good: fast
Bad: new
Revisit when: 3 users complain
"""


def reader(files):
    return MarkdownRecordReader(MemoryStore(files))


def test_an_adr_is_parsed_into_its_parts():
    adr = reader({"a.md": ADR}).read_adr("a.md")
    assert (adr.number, adr.title, adr.status, adr.superseded_by, adr.supersedes) == (
        9,
        "Pick a thing",
        "Superseded",
        10,
        4,
    )
    assert adr.context == "Facts: 5 of them, on two lines."
    assert adr.sections == ("Context", "Options considered", "Decision", "Consequences")
    assert [option.name for option in adr.options] == ["first way", "second way"]
    assert adr.options[0].advantage == "it is fast and cheap."
    assert adr.options[1].main_cost == ""
    assert (adr.good, adr.bad, adr.revisit_when) == ("fast", "new", "3 users complain")
    assert adr.decision.startswith("We will do")


def test_a_file_that_is_not_an_adr_parses_to_empty_parts():
    adr = reader({"a.md": "just words\n"}).read_adr("a.md")
    assert (adr.number, adr.title, adr.status, adr.options, adr.sections) == (None, "", "", (), ())


def test_a_plain_status_is_kept_as_written():
    adr = reader({"a.md": ADR.replace("Superseded by ADR 0010", "Accepted")}).read_adr("a.md")
    assert (adr.status, adr.superseded_by) == ("Accepted", None)


def test_audience_versions_use_the_third_heading_as_the_sibling_team():
    text = "# Audience versions: ADR 0007\n\n## Engineers\nOne.\n\n## Manager\nTwo.\n\n## Billing team\nThree.\nMore.\n"
    versions = reader({"a.md": text}).read_audiences("a.md")
    assert (versions.adr_number, versions.engineers, versions.manager) == (7, "One.", "Two.")
    assert (versions.sibling_name, versions.sibling) == ("Billing team", "Three. More.")


def test_missing_audience_sections_parse_to_empty_text():
    versions = reader({"a.md": "# nothing\n"}).read_audiences("a.md")
    assert (versions.adr_number, versions.engineers, versions.sibling, versions.sibling_name) == (None, "", "", "")


def test_a_reaction_log_is_parsed():
    text = (
        "# Reaction log: ADR 0007\n\nReader: an engineer\nReader kind: real\nADR: 0007\n\n"
        "## Said back\n> They send it once.\n> Always.\n\n## Misunderstood\nThey missed repeats.\n\n"
        '## Fix\nBefore: "old words."\nAfter: "new words."\n'
    )
    reaction = reader({"a.md": text}).read_reaction("a.md")
    assert (reaction.reader, reaction.reader_kind, reaction.adr_number) == ("an engineer", "real", 7)
    assert reaction.said_back == "They send it once. Always."
    assert (reaction.before, reaction.after) == ("old words.", "new words.")
