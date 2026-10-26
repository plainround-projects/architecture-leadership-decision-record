from dataclasses import replace

from adr_toolkit.domain.adr import AdrLimits, Option, check_adr
from tests.conftest import valid_adr


def codes(**changes):
    return sorted({finding.code for finding in check_adr(valid_adr(**changes))})


def test_a_complete_record_has_no_findings():
    assert check_adr(valid_adr()) == []


def test_a_missing_title_is_reported():
    assert "ADR001" in codes(number=None, title="")


def test_an_unknown_status_is_reported():
    assert "ADR002" in codes(status="Maybe")


def test_superseded_must_name_its_successor():
    assert "ADR002" in codes(status="Superseded", superseded_by=None)


def test_a_bad_date_is_reported():
    assert "ADR003" in codes(date_text="22 October")


def test_placeholder_deciders_are_reported():
    assert "ADR004" in codes(deciders="<names>")


def test_sections_out_of_order_are_reported():
    assert "ADR005" in codes(sections=("Decision", "Context", "Options considered", "Consequences"))


def test_missing_section_is_named():
    messages = [f.message for f in check_adr(valid_adr(sections=("Context", "Decision", "Consequences")))]
    assert any("missing Options considered" in message for message in messages)


def test_one_option_is_not_a_decision():
    only = valid_adr().options[:1]
    assert "ADR006" in codes(options=only)


def test_an_option_without_an_advantage_is_a_straw_man():
    weak = Option("keep polling", "", "load grows with every new reader", "the team has no time to learn")
    second = valid_adr().options[1]
    assert "ADR007" in codes(options=(weak, second))


def test_two_options_with_one_advantage_are_the_same_choice():
    first, second = valid_adr().options
    clone = replace(second, advantage=first.advantage)
    assert "ADR008" in codes(options=(first, clone))


def test_a_context_without_a_number_is_a_feeling():
    assert "ADR009" in codes(context="Emails are late and the database is busy.")


def test_a_context_that_argues_is_reported():
    assert "ADR010" in codes(context="We have 6 engineers, so we need a queue.")
    assert "ADR010" in codes(context="We have 6 engineers and Option A is cheap.")


def test_a_decision_must_use_the_we_will_because_form():
    assert "ADR011" in codes(decision="Use the outbox.")


def test_two_reasons_hide_the_real_one():
    decision = "We will write an outbox table with a relay, because it is safe because it is simple."
    assert "ADR012" in codes(decision=decision)


def test_the_decision_must_name_an_option_considered():
    assert "ADR017" in codes(decision="We will buy a bigger database server, because it is quick.")


def test_consequences_need_a_bad_result():
    assert "ADR013" in codes(bad="")
    assert "ADR013" in codes(good="")


def test_a_missing_trigger_is_reported():
    assert "ADR014" in codes(revisit_when="")


def test_a_vague_trigger_is_not_observable():
    assert "ADR015" in codes(revisit_when="if it stops working")
    assert "ADR015" in codes(revisit_when="when the team feels it is slow")


def test_a_record_longer_than_a_page_is_reported():
    assert "ADR016" in codes(line_count=71)
    assert "ADR016" in codes(word_count=601)


def test_limits_are_configurable():
    findings = check_adr(valid_adr(line_count=30), AdrLimits(max_lines=20, max_words=600))
    assert [f.code for f in findings] == ["ADR016"]


def test_a_proposed_record_is_a_warning_not_an_error():
    findings = check_adr(valid_adr(status="Proposed"))
    assert [(f.code, f.severity.value) for f in findings] == [("ADR018", "warning")]
