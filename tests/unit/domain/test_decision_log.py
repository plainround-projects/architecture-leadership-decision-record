from adr_toolkit.domain.decision_log import check_links, render_log
from tests.conftest import valid_adr


def old():
    return valid_adr(number=5, path="docs/adr/0005-a.md", status="Superseded", superseded_by=7)


def new():
    return valid_adr(number=7, path="docs/adr/0007-b.md", supersedes=5)


def test_a_consistent_pair_has_no_findings():
    assert check_links([old(), new()]) == []


def test_superseded_by_a_missing_record_is_reported():
    assert [f.code for f in check_links([old()])] == ["ADR101"]


def test_the_successor_must_say_what_it_replaces():
    assert [f.code for f in check_links([old(), valid_adr(number=7, path="docs/adr/0007-b.md")])] == ["ADR102"]


def test_the_predecessor_must_say_it_was_replaced():
    still_accepted = valid_adr(number=5, path="docs/adr/0005-a.md")
    assert [f.code for f in check_links([still_accepted, new()])] == ["ADR103"]


def test_supersedes_a_missing_record_is_reported():
    assert [f.code for f in check_links([new()])] == ["ADR101"]


def test_duplicate_numbers_are_reported():
    copy = valid_adr(number=7, path="docs/adr/0007-c.md")
    assert "ADR100" in {f.code for f in check_links([new(), copy])}


def test_the_log_lists_every_record_and_the_chain():
    text = render_log([new(), old()])
    assert text.index("0005") < text.index("0007")
    assert "ADR 0007 supersedes ADR 0005" in text
    assert "(adr/0005-a.md)" in text


def test_a_chain_of_three_reads_newest_first():
    middle = valid_adr(number=6, path="docs/adr/0006-m.md", status="Superseded", superseded_by=7, supersedes=5)
    first = valid_adr(number=5, path="docs/adr/0005-a.md", status="Superseded", superseded_by=6)
    last = valid_adr(number=7, path="docs/adr/0007-b.md", supersedes=6)
    text = render_log([first, middle, last])
    assert "ADR 0007 supersedes ADR 0006 supersedes ADR 0005" in text


def test_a_record_without_a_number_still_renders():
    assert "| ?" in render_log([valid_adr(number=None)])
