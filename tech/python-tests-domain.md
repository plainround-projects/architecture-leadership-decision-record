# The tests (domain)

## What it is

The pytest tests in `tests/unit/domain`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/unit/domain/test_adr_rules.py` | 62 lines.  |
| `tests/unit/domain/test_audiences.py` | 51 lines.  |
| `tests/unit/domain/test_decision_log.py` | 33 lines.  |
| `tests/unit/domain/test_reaction.py` | 31 lines.  |
| `tests/unit/domain/test_text.py` | 16 lines.  |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/unit/domain/test_adr_rules.py`

`tests/unit/domain/test_adr_rules.py` lines 1 to 4:

```python
from dataclasses import replace

from adr_toolkit.domain.adr import AdrLimits, Option, check_adr
from tests.conftest import valid_adr
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `dataclasses` it takes `replace`.
- From `adr_toolkit.domain.adr` it takes `AdrLimits, Option, check_adr`.
- From `tests.conftest` it takes `valid_adr`.

`tests/unit/domain/test_adr_rules.py` lines 7 to 8:

```python
def codes(**changes):
    return sorted({finding.code for finding in check_adr(valid_adr(**changes))})
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.

**Function `codes`.**

It takes: `**changes` (any extra named values).

Step by step:

- Gives back the result of calling `sorted({finding.code for finding in check_adr(valid_adr(**changes))})`.

`tests/unit/domain/test_adr_rules.py` lines 11 to 12:

```python
def test_a_complete_record_has_no_findings():
    assert check_adr(valid_adr()) == []
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_a_complete_record_has_no_findings`** checks: a complete record has no findings.

Step by step:

- Checks that `check_adr(valid_adr())` equals `[]`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 15 to 16:

```python
def test_a_missing_title_is_reported():
    assert "ADR001" in codes(number=None, title="")
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Test `test_a_missing_title_is_reported`** checks: a missing title is reported.

Step by step:

- Checks that `'ADR001'` is in `codes(number=None, title='')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 19 to 20:

```python
def test_an_unknown_status_is_reported():
    assert "ADR002" in codes(status="Maybe")
```

**Test `test_an_unknown_status_is_reported`** checks: an unknown status is reported.

Step by step:

- Checks that `'ADR002'` is in `codes(status='Maybe')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 23 to 24:

```python
def test_superseded_must_name_its_successor():
    assert "ADR002" in codes(status="Superseded", superseded_by=None)
```

**Test `test_superseded_must_name_its_successor`** checks: superseded must name its successor.

Step by step:

- Checks that `'ADR002'` is in `codes(status='Superseded', superseded_by=None)`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 27 to 28:

```python
def test_a_bad_date_is_reported():
    assert "ADR003" in codes(date_text="22 October")
```

**Test `test_a_bad_date_is_reported`** checks: a bad date is reported.

Step by step:

- Checks that `'ADR003'` is in `codes(date_text='22 October')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 31 to 32:

```python
def test_placeholder_deciders_are_reported():
    assert "ADR004" in codes(deciders="<names>")
```

**Test `test_placeholder_deciders_are_reported`** checks: placeholder deciders are reported.

Step by step:

- Checks that `'ADR004'` is in `codes(deciders='<names>')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 35 to 36:

```python
def test_sections_out_of_order_are_reported():
    assert "ADR005" in codes(sections=("Decision", "Context", "Options considered", "Consequences"))
```

> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Test `test_sections_out_of_order_are_reported`** checks: sections out of order are reported.

Step by step:

- Checks that `'ADR005'` is in `codes(sections=('Decision', 'Context', 'Options c…`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 39 to 41:

```python
def test_missing_section_is_named():
    messages = [f.message for f in check_adr(valid_adr(sections=("Context", "Decision", "Consequences")))]
    assert any("missing Options considered" in message for message in messages)
```

> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Test `test_missing_section_is_named`** checks: missing section is named.

Step by step:

- Stores a new list made by a loop (`[f.message for f in check_adr(valid_adr(sections=('Context', 'Decisio…`) in `messages`.
- Checks that `any(('missing Options considered' in message for message in messages))`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 44 to 46:

```python
def test_one_option_is_not_a_decision():
    only = valid_adr().options[:1]
    assert "ADR006" in codes(options=only)
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **slice** such as `text[:7]` or `items[1:]` takes part of a sequence: `[:7]` the first seven items, `[1:]` everything after the first.

**Test `test_one_option_is_not_a_decision`** checks: one option is not a decision.

Step by step:

- Stores `valid_adr().options[:1]` in `only`.
- Checks that `'ADR006'` is in `codes(options=only)`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 49 to 52:

```python
def test_an_option_without_an_advantage_is_a_straw_man():
    weak = Option("keep polling", "", "load grows with every new reader", "the team has no time to learn")
    second = valid_adr().options[1]
    assert "ADR007" in codes(options=(weak, second))
```

**Test `test_an_option_without_an_advantage_is_a_straw_man`** checks: an option without an advantage is a straw man.

Step by step:

- Stores the result of calling `Option('keep polling', '', 'load grows with every new reader', 'the team has no time to l…` in `weak`.
- Stores `valid_adr().options[1]` in `second`.
- Checks that `'ADR007'` is in `codes(options=(weak, second))`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 55 to 58:

```python
def test_two_options_with_one_advantage_are_the_same_choice():
    first, second = valid_adr().options
    clone = replace(second, advantage=first.advantage)
    assert "ADR008" in codes(options=(first, clone))
```

**Test `test_two_options_with_one_advantage_are_the_same_choice`** checks: two options with one advantage are the same choice.

Step by step:

- Unpacks `valid_adr().options` into `(first, second)`.
- Stores the result of calling `replace(second, advantage=first.advantage)` in `clone`.
- Checks that `'ADR008'` is in `codes(options=(first, clone))`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 61 to 62:

```python
def test_a_context_without_a_number_is_a_feeling():
    assert "ADR009" in codes(context="Emails are late and the database is busy.")
```

**Test `test_a_context_without_a_number_is_a_feeling`** checks: a context without a number is a feeling.

Step by step:

- Checks that `'ADR009'` is in `codes(context='Emails are late and the database i…`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 65 to 67:

```python
def test_a_context_that_argues_is_reported():
    assert "ADR010" in codes(context="We have 6 engineers, so we need a queue.")
    assert "ADR010" in codes(context="We have 6 engineers and Option A is cheap.")
```

**Test `test_a_context_that_argues_is_reported`** checks: a context that argues is reported.

Step by step:

- Checks that `'ADR010'` is in `codes(context='We have 6 engineers, so we need a …`; if not, the test fails.
- Checks that `'ADR010'` is in `codes(context='We have 6 engineers and Option A i…`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 70 to 71:

```python
def test_a_decision_must_use_the_we_will_because_form():
    assert "ADR011" in codes(decision="Use the outbox.")
```

**Test `test_a_decision_must_use_the_we_will_because_form`** checks: a decision must use the we will because form.

Step by step:

- Checks that `'ADR011'` is in `codes(decision='Use the outbox.')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 74 to 76:

```python
def test_two_reasons_hide_the_real_one():
    decision = "We will write an outbox table with a relay, because it is safe because it is simple."
    assert "ADR012" in codes(decision=decision)
```

**Test `test_two_reasons_hide_the_real_one`** checks: two reasons hide the real one.

Step by step:

- Stores the text `'We will write an outbox table with a relay, because it is …` in `decision`.
- Checks that `'ADR012'` is in `codes(decision=decision)`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 79 to 80:

```python
def test_the_decision_must_name_an_option_considered():
    assert "ADR017" in codes(decision="We will buy a bigger database server, because it is quick.")
```

**Test `test_the_decision_must_name_an_option_considered`** checks: the decision must name an option considered.

Step by step:

- Checks that `'ADR017'` is in `codes(decision='We will buy a bigger database ser…`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 83 to 85:

```python
def test_consequences_need_a_bad_result():
    assert "ADR013" in codes(bad="")
    assert "ADR013" in codes(good="")
```

**Test `test_consequences_need_a_bad_result`** checks: consequences need a bad result.

Step by step:

- Checks that `'ADR013'` is in `codes(bad='')`; if not, the test fails.
- Checks that `'ADR013'` is in `codes(good='')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 88 to 89:

```python
def test_a_missing_trigger_is_reported():
    assert "ADR014" in codes(revisit_when="")
```

**Test `test_a_missing_trigger_is_reported`** checks: a missing trigger is reported.

Step by step:

- Checks that `'ADR014'` is in `codes(revisit_when='')`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 92 to 94:

```python
def test_a_vague_trigger_is_not_observable():
    assert "ADR015" in codes(revisit_when="if it stops working")
    assert "ADR015" in codes(revisit_when="when the team feels it is slow")
```

**Test `test_a_vague_trigger_is_not_observable`** checks: a vague trigger is not observable.

Step by step:

- Checks that `'ADR015'` is in `codes(revisit_when='if it stops working')`; if not, the test fails.
- Checks that `'ADR015'` is in `codes(revisit_when='when the team feels it is slo…`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 97 to 99:

```python
def test_a_record_longer_than_a_page_is_reported():
    assert "ADR016" in codes(line_count=71)
    assert "ADR016" in codes(word_count=601)
```

**Test `test_a_record_longer_than_a_page_is_reported`** checks: a record longer than a page is reported.

Step by step:

- Checks that `'ADR016'` is in `codes(line_count=71)`; if not, the test fails.
- Checks that `'ADR016'` is in `codes(word_count=601)`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 102 to 104:

```python
def test_limits_are_configurable():
    findings = check_adr(valid_adr(line_count=30), AdrLimits(max_lines=20, max_words=600))
    assert [f.code for f in findings] == ["ADR016"]
```

**Test `test_limits_are_configurable`** checks: limits are configurable.

Step by step:

- Stores the result of calling `check_adr(valid_adr(line_count=30), AdrLimits(max_lines=20, max_words=600))` in `findings`.
- Checks that `[f.code for f in findings]` equals `['ADR016']`; if not, the test fails.

`tests/unit/domain/test_adr_rules.py` lines 107 to 109:

```python
def test_a_proposed_record_is_a_warning_not_an_error():
    findings = check_adr(valid_adr(status="Proposed"))
    assert [(f.code, f.severity.value) for f in findings] == [("ADR018", "warning")]
```

**Test `test_a_proposed_record_is_a_warning_not_an_error`** checks: a proposed record is a warning not an error.

Step by step:

- Stores the result of calling `check_adr(valid_adr(status='Proposed'))` in `findings`.
- Checks that `[(f.code, f.severity.value) for f in findings]` equals `[('ADR018', 'warning')]`; if not, the test fails.

### `tests/unit/domain/test_audiences.py`

`tests/unit/domain/test_audiences.py` lines 1 to 3:

```python
from dataclasses import replace

from adr_toolkit.domain.audiences import AudienceVersions, check_audiences
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `dataclasses` it takes `replace`.
- From `adr_toolkit.domain.audiences` it takes `AudienceVersions, check_audiences`.

`tests/unit/domain/test_audiences.py` lines 5 to 28:

```python
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
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the text `'We will write an event row in the same transaction as the …` in `DECISION`.
- Stores the result of calling `AudienceVersions(path='docs/communication/0007-audiences.md', adr_number=7, engineers='Th…` in `GOOD`.

`tests/unit/domain/test_audiences.py` lines 31 to 32:

```python
def codes(versions: AudienceVersions) -> set[str]:
    return {finding.code for finding in check_audiences(versions, DECISION)}
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.

**Function `codes`.**

It takes: `versions` (a `AudienceVersions`).

It gives back a `set[str]`.

Step by step:

- Gives back a new set made by a loop (`{finding.code for finding in check_audiences(versions, DECISION)}`).

`tests/unit/domain/test_audiences.py` lines 35 to 36:

```python
def test_three_good_versions_pass():
    assert check_audiences(GOOD, DECISION) == []
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_three_good_versions_pass`** checks: three good versions pass.

Step by step:

- Checks that `check_audiences(GOOD, DECISION)` equals `[]`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 39 to 40:

```python
def test_a_missing_version_is_reported_alone():
    assert codes(replace(GOOD, manager="")) == {"AUD001"}
```

> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.

**Test `test_a_missing_version_is_reported_alone`** checks: a missing version is reported alone.

Step by step:

- Checks that `codes(replace(GOOD, manager=''))` equals `{'AUD001'}`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 43 to 44:

```python
def test_engineers_get_about_five_sentences():
    assert "AUD002" in codes(replace(GOOD, engineers="It uses a relay. It is fine."))
```

**Test `test_engineers_get_about_five_sentences`** checks: engineers get about five sentences.

Step by step:

- Checks that `'AUD002'` is in `codes(replace(GOOD, engineers='It uses a relay. I…`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 47 to 49:

```python
def test_engineers_must_get_the_chosen_mechanism():
    text = "We bought a bigger server. It has more memory. It is faster for everyone. Nothing else changes."
    assert "AUD003" in codes(replace(GOOD, engineers=text))
```

**Test `test_engineers_must_get_the_chosen_mechanism`** checks: engineers must get the chosen mechanism.

Step by step:

- Stores the text `'We bought a bigger server. It has more memory. It is faste…` in `text`.
- Checks that `'AUD003'` is in `codes(replace(GOOD, engineers=text))`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 52 to 54:

```python
def test_manager_gets_two_sentences_with_numbers():
    assert "AUD004" in codes(replace(GOOD, manager="Cheaper by 5 percent. Safer by 2 points. Done in 3 weeks."))
    assert "AUD005" in codes(replace(GOOD, manager="Emails get faster before Black Friday. The risk is small."))
```

**Test `test_manager_gets_two_sentences_with_numbers`** checks: manager gets two sentences with numbers.

Step by step:

- Checks that `'AUD004'` is in `codes(replace(GOOD, manager='Cheaper by 5 percent…`; if not, the test fails.
- Checks that `'AUD005'` is in `codes(replace(GOOD, manager='Emails get faster be…`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 57 to 58:

```python
def test_manager_version_has_no_jargon():
    assert "AUD006" in codes(replace(GOOD, manager="Emails drop to 2 seconds. The outbox relay is 1 new process."))
```

**Test `test_manager_version_has_no_jargon`** checks: manager version has no jargon.

Step by step:

- Checks that `'AUD006'` is in `codes(replace(GOOD, manager='Emails drop to 2 sec…`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 61 to 63:

```python
def test_sibling_note_starts_with_a_date_and_an_action():
    assert "AUD007" in codes(replace(GOOD, sibling="We changed how orders are announced. Please read the ADR."))
    assert "AUD007" in codes(replace(GOOD, sibling="From 3 November the queue exists. It carries orders."))
```

**Test `test_sibling_note_starts_with_a_date_and_an_action`** checks: sibling note starts with a date and an action.

Step by step:

- Checks that `'AUD007'` is in `codes(replace(GOOD, sibling='We changed how order…`; if not, the test fails.
- Checks that `'AUD007'` is in `codes(replace(GOOD, sibling='From 3 November the …`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 66 to 67:

```python
def test_sibling_note_has_no_internal_jargon():
    assert "AUD006" in codes(replace(GOOD, sibling="From 3 November, subscribe to the queue. The outbox is ours."))
```

**Test `test_sibling_note_has_no_internal_jargon`** checks: sibling note has no internal jargon.

Step by step:

- Checks that `'AUD006'` is in `codes(replace(GOOD, sibling='From 3 November, sub…`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 70 to 71:

```python
def test_a_thin_sibling_note_is_reported():
    assert "AUD007" in codes(replace(GOOD, sibling="From 3 November, subscribe to the queue."))
```

**Test `test_a_thin_sibling_note_is_reported`** checks: a thin sibling note is reported.

Step by step:

- Checks that `'AUD007'` is in `codes(replace(GOOD, sibling='From 3 November, sub…`; if not, the test fails.

`tests/unit/domain/test_audiences.py` lines 74 to 76:

```python
def test_copying_one_paragraph_into_two_versions_is_reported():
    copied = replace(GOOD, manager=GOOD.sibling)
    assert "AUD008" in codes(copied)
```

**Test `test_copying_one_paragraph_into_two_versions_is_reported`** checks: copying one paragraph into two versions is reported.

Step by step:

- Stores the result of calling `replace(GOOD, manager=GOOD.sibling)` in `copied`.
- Checks that `'AUD008'` is in `codes(copied)`; if not, the test fails.

### `tests/unit/domain/test_decision_log.py`

`tests/unit/domain/test_decision_log.py` lines 1 to 2:

```python
from adr_toolkit.domain.decision_log import check_links, render_log
from tests.conftest import valid_adr
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `adr_toolkit.domain.decision_log` it takes `check_links, render_log`.
- From `tests.conftest` it takes `valid_adr`.

`tests/unit/domain/test_decision_log.py` lines 5 to 6:

```python
def old():
    return valid_adr(number=5, path="docs/adr/0005-a.md", status="Superseded", superseded_by=7)
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Function `old`.**

Step by step:

- Gives back the result of calling `valid_adr(number=5, path='docs/adr/0005-a.md', status='Superseded', superseded_by=7)`.

`tests/unit/domain/test_decision_log.py` lines 9 to 10:

```python
def new():
    return valid_adr(number=7, path="docs/adr/0007-b.md", supersedes=5)
```

**Function `new`.**

Step by step:

- Gives back the result of calling `valid_adr(number=7, path='docs/adr/0007-b.md', supersedes=5)`.

`tests/unit/domain/test_decision_log.py` lines 13 to 14:

```python
def test_a_consistent_pair_has_no_findings():
    assert check_links([old(), new()]) == []
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_a_consistent_pair_has_no_findings`** checks: a consistent pair has no findings.

Step by step:

- Checks that `check_links([old(), new()])` equals `[]`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 17 to 18:

```python
def test_superseded_by_a_missing_record_is_reported():
    assert [f.code for f in check_links([old()])] == ["ADR101"]
```

> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.

**Test `test_superseded_by_a_missing_record_is_reported`** checks: superseded by a missing record is reported.

Step by step:

- Checks that `[f.code for f in check_links([old()])]` equals `['ADR101']`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 21 to 22:

```python
def test_the_successor_must_say_what_it_replaces():
    assert [f.code for f in check_links([old(), valid_adr(number=7, path="docs/adr/0007-b.md")])] == ["ADR102"]
```

**Test `test_the_successor_must_say_what_it_replaces`** checks: the successor must say what it replaces.

Step by step:

- Checks that `[f.code for f in check_links([old(), valid_adr(nu…` equals `['ADR102']`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 25 to 27:

```python
def test_the_predecessor_must_say_it_was_replaced():
    still_accepted = valid_adr(number=5, path="docs/adr/0005-a.md")
    assert [f.code for f in check_links([still_accepted, new()])] == ["ADR103"]
```

**Test `test_the_predecessor_must_say_it_was_replaced`** checks: the predecessor must say it was replaced.

Step by step:

- Stores the result of calling `valid_adr(number=5, path='docs/adr/0005-a.md')` in `still_accepted`.
- Checks that `[f.code for f in check_links([still_accepted, new…` equals `['ADR103']`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 30 to 31:

```python
def test_supersedes_a_missing_record_is_reported():
    assert [f.code for f in check_links([new()])] == ["ADR101"]
```

**Test `test_supersedes_a_missing_record_is_reported`** checks: supersedes a missing record is reported.

Step by step:

- Checks that `[f.code for f in check_links([new()])]` equals `['ADR101']`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 34 to 36:

```python
def test_duplicate_numbers_are_reported():
    copy = valid_adr(number=7, path="docs/adr/0007-c.md")
    assert "ADR100" in {f.code for f in check_links([new(), copy])}
```

> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.

**Test `test_duplicate_numbers_are_reported`** checks: duplicate numbers are reported.

Step by step:

- Stores the result of calling `valid_adr(number=7, path='docs/adr/0007-c.md')` in `copy`.
- Checks that `'ADR100'` is in `{f.code for f in check_links([new(), copy])}`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 39 to 43:

```python
def test_the_log_lists_every_record_and_the_chain():
    text = render_log([new(), old()])
    assert text.index("0005") < text.index("0007")
    assert "ADR 0007 supersedes ADR 0005" in text
    assert "(adr/0005-a.md)" in text
```

**Test `test_the_log_lists_every_record_and_the_chain`** checks: the log lists every record and the chain.

Step by step:

- Stores the result of calling `render_log([new(), old()])` in `text`.
- Checks that `text.index('0005')` is less than `text.index('0007')`; if not, the test fails.
- Checks that `'ADR 0007 supersedes ADR 0005'` is in `text`; if not, the test fails.
- Checks that `'(adr/0005-a.md)'` is in `text`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 46 to 51:

```python
def test_a_chain_of_three_reads_newest_first():
    middle = valid_adr(number=6, path="docs/adr/0006-m.md", status="Superseded", superseded_by=7, supersedes=5)
    first = valid_adr(number=5, path="docs/adr/0005-a.md", status="Superseded", superseded_by=6)
    last = valid_adr(number=7, path="docs/adr/0007-b.md", supersedes=6)
    text = render_log([first, middle, last])
    assert "ADR 0007 supersedes ADR 0006 supersedes ADR 0005" in text
```

**Test `test_a_chain_of_three_reads_newest_first`** checks: a chain of three reads newest first.

Step by step:

- Stores the result of calling `valid_adr(number=6, path='docs/adr/0006-m.md', status='Superseded', superseded_by=7, supe…` in `middle`.
- Stores the result of calling `valid_adr(number=5, path='docs/adr/0005-a.md', status='Superseded', superseded_by=6)` in `first`.
- Stores the result of calling `valid_adr(number=7, path='docs/adr/0007-b.md', supersedes=6)` in `last`.
- Stores the result of calling `render_log([first, middle, last])` in `text`.
- Checks that `'ADR 0007 supersedes ADR 0006 supersedes ADR 0005'` is in `text`; if not, the test fails.

`tests/unit/domain/test_decision_log.py` lines 54 to 55:

```python
def test_a_record_without_a_number_still_renders():
    assert "| ?" in render_log([valid_adr(number=None)])
```

**Test `test_a_record_without_a_number_still_renders`** checks: a record without a number still renders.

Step by step:

- Checks that `'| ?'` is in `render_log([valid_adr(number=None)])`; if not, the test fails.

### `tests/unit/domain/test_reaction.py`

`tests/unit/domain/test_reaction.py` lines 1 to 4:

```python
from dataclasses import replace

from adr_toolkit.domain.findings import Severity
from adr_toolkit.domain.reaction import Reaction, check_reaction, check_talk
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `dataclasses` it takes `replace`.
- From `adr_toolkit.domain.findings` it takes `Severity`.
- From `adr_toolkit.domain.reaction` it takes `Reaction, check_reaction, check_talk`.

`tests/unit/domain/test_reaction.py` lines 6 to 16:

```python
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
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the result of calling `Reaction(path='docs/review/0007-reaction.md', adr_number=7, reader='engineer', reader_kin…` in `REACTION`.
- Stores the text `'Bad: the relay can publish an event twice.'` in `RECORD`.

`tests/unit/domain/test_reaction.py` lines 19 to 20:

```python
def test_a_logged_fix_that_is_in_the_record_passes():
    assert check_reaction(REACTION, RECORD) == []
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_a_logged_fix_that_is_in_the_record_passes`** checks: a logged fix that is in the record passes.

Step by step:

- Checks that `check_reaction(REACTION, RECORD)` equals `[]`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 23 to 24:

```python
def test_an_empty_field_is_reported():
    assert {f.code for f in check_reaction(replace(REACTION, misunderstood=""), RECORD)} == {"REA001"}
```

> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.
> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.

**Test `test_an_empty_field_is_reported`** checks: an empty field is reported.

Step by step:

- Checks that `{f.code for f in check_reaction(replace(REACTION,…` equals `{'REA001'}`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 27 to 28:

```python
def test_a_log_without_before_and_after_is_reported():
    assert {f.code for f in check_reaction(replace(REACTION, after=""), RECORD)} == {"REA001"}
```

**Test `test_a_log_without_before_and_after_is_reported`** checks: a log without before and after is reported.

Step by step:

- Checks that `{f.code for f in check_reaction(replace(REACTION,…` equals `{'REA001'}`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 31 to 32:

```python
def test_a_fix_that_is_not_in_the_record_is_reported():
    assert "REA002" in {f.code for f in check_reaction(REACTION, "Bad: nothing.")}
```

**Test `test_a_fix_that_is_not_in_the_record_is_reported`** checks: a fix that is not in the record is reported.

Step by step:

- Checks that `'REA002'` is in `{f.code for f in check_reaction(REACTION, 'Bad: n…`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 35 to 36:

```python
def test_a_sentence_that_is_still_in_the_record_is_reported():
    assert "REA003" in {f.code for f in check_reaction(REACTION, RECORD + " a stuck relay delays every consumer.")}
```

**Test `test_a_sentence_that_is_still_in_the_record_is_reported`** checks: a sentence that is still in the record is reported.

Step by step:

- Checks that `'REA003'` is in `{f.code for f in check_reaction(REACTION, RECORD …`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 39 to 41:

```python
def test_a_worked_example_is_a_warning():
    findings = check_reaction(replace(REACTION, reader_kind="worked-example"), RECORD)
    assert [(f.code, f.severity) for f in findings] == [("REA004", Severity.WARNING)]
```

> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Test `test_a_worked_example_is_a_warning`** checks: a worked example is a warning.

Step by step:

- Stores the result of calling `check_reaction(replace(REACTION, reader_kind='worked-example'), RECORD)` in `findings`.
- Checks that `[(f.code, f.severity) for f in findings]` equals `[('REA004', Severity.WARNING)]`; if not, the test fails.

`tests/unit/domain/test_reaction.py` lines 44 to 47:

```python
def test_a_talk_must_fit_three_minutes():
    assert check_talk("t.md", "word " * 399) == []
    assert [f.code for f in check_talk("t.md", "word " * 401)] == ["TLK001"]
    assert [f.code for f in check_talk("t.md", "word " * 20)] == ["TLK001"]
```

**Test `test_a_talk_must_fit_three_minutes`** checks: a talk must fit three minutes.

Step by step:

- Checks that `check_talk('t.md', 'word ' * 399)` equals `[]`; if not, the test fails.
- Checks that `[f.code for f in check_talk('t.md', 'word ' * 401…` equals `['TLK001']`; if not, the test fails.
- Checks that `[f.code for f in check_talk('t.md', 'word ' * 20)]` equals `['TLK001']`; if not, the test fails.

### `tests/unit/domain/test_text.py`

`tests/unit/domain/test_text.py` lines 1 to 1:

```python
from adr_toolkit.domain.text import has_figure, sentences, similarity, squash, words
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `adr_toolkit.domain.text` it takes `has_figure, sentences, similarity, squash, words`.

`tests/unit/domain/test_text.py` lines 4 to 5:

```python
def test_squash_collapses_whitespace():
    assert squash("a \n b\t c") == "a b c"
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_squash_collapses_whitespace`** checks: squash collapses whitespace.

Step by step:

- Checks that `squash('a \n b\t c')` equals `'a b c'`; if not, the test fails.

`tests/unit/domain/test_text.py` lines 8 to 9:

```python
def test_sentences_split_on_full_stops_before_a_capital_or_digit():
    assert sentences("One. Two! Three? four") == ["One.", "Two!", "Three? four"]
```

**Test `test_sentences_split_on_full_stops_before_a_capital_or_digit`** checks: sentences split on full stops before a capital or digit.

Step by step:

- Checks that `sentences('One. Two! Three? four')` equals `['One.', 'Two!', 'Three? four']`; if not, the test fails.

`tests/unit/domain/test_text.py` lines 12 to 13:

```python
def test_sentences_of_nothing_is_empty():
    assert sentences("   ") == []
```

**Test `test_sentences_of_nothing_is_empty`** checks: sentences of nothing is empty.

Step by step:

- Checks that `sentences(' ')` equals `[]`; if not, the test fails.

`tests/unit/domain/test_text.py` lines 16 to 17:

```python
def test_words_are_lower_case_and_keep_apostrophes():
    assert words("The relay's Backlog, 1,000") == ["the", "relay's", "backlog", "1", "000"]
```

**Test `test_words_are_lower_case_and_keep_apostrophes`** checks: words are lower case and keep apostrophes.

Step by step:

- Checks that `words("The relay's Backlog, 1,000")` equals `['the', "relay's", 'backlog', '1', '000']`; if not, the test fails.

`tests/unit/domain/test_text.py` lines 20 to 22:

```python
def test_has_figure_finds_a_digit():
    assert has_figure("40,000 orders")
    assert not has_figure("many orders")
```

**Test `test_has_figure_finds_a_digit`** checks: has figure finds a digit.

Step by step:

- Checks that `has_figure('40,000 orders')`; if not, the test fails.
- Checks that not (`has_figure('many orders')`); if not, the test fails.

`tests/unit/domain/test_text.py` lines 25 to 28:

```python
def test_similarity_runs_from_zero_to_one():
    assert similarity("a b c", "a b c") == 1.0
    assert similarity("a b", "c d") == 0.0
    assert similarity("", "a") == 0.0
```

**Test `test_similarity_runs_from_zero_to_one`** checks: similarity runs from zero to one.

Step by step:

- Checks that `similarity('a b c', 'a b c')` equals `1.0`; if not, the test fails.
- Checks that `similarity('a b', 'c d')` equals `0.0`; if not, the test fails.
- Checks that `similarity('', 'a')` equals `0.0`; if not, the test fails.

## Try it yourself

```bash
.venv/bin/pytest -q tests/unit/domain
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/unit/domain/test_adr_rules.py tests/unit/domain/test_audiences.py tests/unit/domain/test_decision_log.py tests/unit/domain/test_reaction.py tests/unit/domain/test_text.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `test_a_complete_record_has_no_findings` check?
   **Answer:** it checks: a complete record has no findings.
2. What does the test `test_a_missing_title_is_reported` check?
   **Answer:** it checks: a missing title is reported.
3. What does the test `test_an_unknown_status_is_reported` check?
   **Answer:** it checks: an unknown status is reported.
4. What does the test `test_superseded_must_name_its_successor` check?
   **Answer:** it checks: superseded must name its successor.
5. What does the test `test_a_bad_date_is_reported` check?
   **Answer:** it checks: a bad date is reported.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
