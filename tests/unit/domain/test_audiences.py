from dataclasses import replace

from adr_toolkit.domain.audiences import AudienceVersions, check_audiences

DECISION = (
    "We will write an event row in the same transaction as the order (an outbox) "
    "and forward it to a managed queue with a small relay, because it is safe."
)

GOOD = AudienceVersions(
    path="docs/communication/0007-audiences.md",
    adr_number=7,
    engineers=(
        "The order and its event row are written in one transaction. "
        "A relay reads the unsent rows and publishes them to the queue. "
        "It then marks them sent. Consumers must ignore a repeat by order id. "
        "We chose an outbox over publishing from the service."
    ),
    manager=(
        "Emails drop from 25 seconds to 2 seconds in 10 weeks. "
        "The risk is 1 new process, with an alert at 1,000 events."
    ),
    sibling=(
        "From 3 November, subscribe to the queue instead of polling our table. "
        "Expect an occasional duplicate, so ignore repeats by order id."
    ),
    sibling_name="Warehouse team",
)


def codes(versions: AudienceVersions) -> set[str]:
    return {finding.code for finding in check_audiences(versions, DECISION)}


def test_three_good_versions_pass():
    assert check_audiences(GOOD, DECISION) == []


def test_a_missing_version_is_reported_alone():
    assert codes(replace(GOOD, manager="")) == {"AUD001"}


def test_engineers_get_about_five_sentences():
    assert "AUD002" in codes(replace(GOOD, engineers="It uses a relay. It is fine."))


def test_engineers_must_get_the_chosen_mechanism():
    text = "We bought a bigger server. It has more memory. It is faster for everyone. Nothing else changes."
    assert "AUD003" in codes(replace(GOOD, engineers=text))


def test_manager_gets_two_sentences_with_numbers():
    assert "AUD004" in codes(replace(GOOD, manager="Cheaper by 5 percent. Safer by 2 points. Done in 3 weeks."))
    assert "AUD005" in codes(replace(GOOD, manager="Emails get faster before Black Friday. The risk is small."))


def test_manager_version_has_no_jargon():
    assert "AUD006" in codes(replace(GOOD, manager="Emails drop to 2 seconds. The outbox relay is 1 new process."))


def test_sibling_note_starts_with_a_date_and_an_action():
    assert "AUD007" in codes(replace(GOOD, sibling="We changed how orders are announced. Please read the ADR."))
    assert "AUD007" in codes(replace(GOOD, sibling="From 3 November the queue exists. It carries orders."))


def test_sibling_note_has_no_internal_jargon():
    assert "AUD006" in codes(replace(GOOD, sibling="From 3 November, subscribe to the queue. The outbox is ours."))


def test_a_thin_sibling_note_is_reported():
    assert "AUD007" in codes(replace(GOOD, sibling="From 3 November, subscribe to the queue."))


def test_copying_one_paragraph_into_two_versions_is_reported():
    copied = replace(GOOD, manager=GOOD.sibling)
    assert "AUD008" in codes(copied)
