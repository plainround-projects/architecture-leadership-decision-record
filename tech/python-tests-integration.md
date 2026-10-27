# The tests (integration)

## What it is

The pytest tests in `tests/integration`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/integration/test_done_when.py` | 84 lines. One test per 'Done when' line of the lesson, run over copies of the repository's own documents. |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/integration/test_done_when.py`

`tests/integration/test_done_when.py` lines 1 to 13:

```python
"""One test per 'Done when' line of the lesson, run over copies of the repository's own documents."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from adr_toolkit.application.check_documents import CheckSettings, check_documents
from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import REPOSITORY_ROOT
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** One test per 'Done when' line of the lesson, run over copies of the repository's own documents.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `shutil`.
- From `pathlib` it takes `Path`.
- It imports module `pytest`.
- From `adr_toolkit.application.check_documents` it takes `CheckSettings, check_documents`.
- From `adr_toolkit.infrastructure.filesystem` it takes `FileSystemStore`.
- From `adr_toolkit.infrastructure.markdown` it takes `MarkdownRecordReader`.
- From `tests.conftest` it takes `REPOSITORY_ROOT`.

`tests/integration/test_done_when.py` lines 15 to 17:

```python
ADR = "docs/adr/0007-announce-paid-orders.md"
AUDIENCES = "docs/communication/0007-audiences.md"
REACTION = "docs/review/0007-reaction.md"
```

> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the text `'docs/adr/0007-announce-paid-orders.md'` in `ADR`.
- Stores the text `'docs/communication/0007-audiences.md'` in `AUDIENCES`.
- Stores the text `'docs/review/0007-reaction.md'` in `REACTION`.

`tests/integration/test_done_when.py` lines 20 to 23:

```python
@pytest.fixture
def docs(tmp_path: Path) -> Path:
    shutil.copytree(REPOSITORY_ROOT / "docs", tmp_path / "docs")
    return tmp_path
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `tmp_path` is a built-in pytest fixture: a fresh, empty temporary folder (a `Path`) that is removed after the test.

**Function `docs`.**

It takes: `tmp_path` (a `Path`).

It gives back a `Path`.

Decorators: `@pytest.fixture`.

Step by step:

- Calls `shutil.copytree(REPOSITORY_ROOT / 'docs', tmp_path / 'docs')`.
- Gives back `tmp_path`.

`tests/integration/test_done_when.py` lines 26 to 29:

```python
def codes(root: Path) -> set[str]:
    store = FileSystemStore(root)
    report = check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=(7,)))
    return {finding.code for finding in report.errors}
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Function `codes`.**

It takes: `root` (a `Path`).

It gives back a `set[str]`.

Step by step:

- Stores the result of calling `FileSystemStore(root)` in `store`.
- Stores the result of calling `check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=(7,)))` in `report`.
- Gives back a new set made by a loop (`{finding.code for finding in report.errors}`).

`tests/integration/test_done_when.py` lines 32 to 36:

```python
def edit(root: Path, path: str, old: str, new: str) -> None:
    file = root / path
    text = file.read_text()
    assert old in text, f"{old!r} not in {path}"
    file.write_text(text.replace(old, new))
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `edit`.**

It takes: `root` (a `Path`); `path` (a `str`); `old` (a `str`); `new` (a `str`).

It gives back a `None`.

Step by step:

- Stores `root / path` in `file`.
- Stores the result of calling `file.read_text()` in `text`.
- Checks that `old` is in `text` with the message `f'{old!r} not in {path}'`; if not, the test fails.
- Calls `file.write_text(text.replace(old, new))`.

`tests/integration/test_done_when.py` lines 39 to 40:

```python
def test_the_repository_as_committed_passes(docs: Path) -> None:
    assert codes(docs) == set()
```

> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_the_repository_as_committed_passes`** checks: the repository as committed passes.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Checks that `codes(docs)` equals `set()`; if not, the test fails.

`tests/integration/test_done_when.py` lines 43 to 48:

```python
def test_done_when_1_two_options_each_with_a_real_advantage(docs: Path) -> None:
    record = MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)
    assert len(record.options) >= 2
    assert all(len(option.advantage.split()) >= 4 for option in record.options)
    edit(docs, ADR, "Advantage: nothing new to run; it ships this week.", "Advantage:")
    assert "ADR007" in codes(docs)
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Test `test_done_when_1_two_options_each_with_a_real_advantage`** checks: done when 1 two options each with a real advantage.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)` in `record`.
- Checks that `len(record.options)` is at least `2`; if not, the test fails.
- Checks that `all((len(option.advantage.split()) >= 4 for option in record.options))`; if not, the test fails.
- Calls `edit(docs, ADR, 'Advantage: nothing new to run; it ships this week.', 'Advantage:')`.
- Checks that `'ADR007'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 51 to 55:

```python
def set_context(root: Path, text: str) -> None:
    record = (root / ADR).read_text()
    start = record.index("## Context") + len("## Context\n")
    end = record.index("## Options considered")
    (root / ADR).write_text(record[:start] + text + "\n\n" + record[end:])
```

> **In plain words.** A **slice** such as `text[:7]` or `items[1:]` takes part of a sequence: `[:7]` the first seven items, `[1:]` everything after the first.

**Function `set_context`.**

It takes: `root` (a `Path`); `text` (a `str`).

It gives back a `None`.

Step by step:

- Stores the result of calling `(root / ADR).read_text()` in `record`.
- Stores `record.index('## Context') + len('## Context\n')` in `start`.
- Stores the result of calling `record.index('## Options considered')` in `end`.
- Calls `(root / ADR).write_text(record[:start] + text + '\n\n' + record[end:])`.

`tests/integration/test_done_when.py` lines 58 to 60:

```python
def test_done_when_2_a_context_that_argues_for_an_answer_is_rejected(docs: Path) -> None:
    set_context(docs, "The team has 6 engineers, so we need a simple tool. Option C is the one.")
    assert "ADR010" in codes(docs)
```

**Test `test_done_when_2_a_context_that_argues_for_an_answer_is_rejected`** checks: done when 2 a context that argues for an answer is rejected.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Calls `set_context(docs, 'The team has 6 engineers, so we need a simple tool. Option C is the one.')`.
- Checks that `'ADR010'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 63 to 65:

```python
def test_done_when_2_a_context_with_no_numbers_is_rejected(docs: Path) -> None:
    set_context(docs, "Emails are late and the database is busy.")
    assert "ADR009" in codes(docs)
```

**Test `test_done_when_2_a_context_with_no_numbers_is_rejected`** checks: done when 2 a context with no numbers is rejected.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Calls `set_context(docs, 'Emails are late and the database is busy.')`.
- Checks that `'ADR009'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 68 to 75:

```python
def test_done_when_3_each_option_is_described_by_the_same_three_lines(docs: Path) -> None:
    record = MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)
    for option in record.options:
        assert option.advantage
        assert option.main_cost
        assert option.pick_if
    edit(docs, ADR, "Pick it if: more consumers are coming and a clean boundary matters.", "")
    assert "ADR007" in codes(docs)
```

> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.

**Test `test_done_when_3_each_option_is_described_by_the_same_three_lines`** checks: done when 3 each option is described by the same three lines.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)` in `record`.
- For each `option` in `record.options`:
  - Checks that `option.advantage`; if not, the test fails.
  - Checks that `option.main_cost`; if not, the test fails.
  - Checks that `option.pick_if`; if not, the test fails.
- Calls `edit(docs, ADR, 'Pick it if: more consumers are coming and a clean boundary matters.', '')`.
- Checks that `'ADR007'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 78 to 88:

```python
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
```

**Test `test_done_when_4_a_bad_consequence_and_an_observable_trigger`** checks: done when 4 a bad consequence and an observable trigger.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `MarkdownRecordReader(FileSystemStore(docs)).read_adr(ADR)` in `record`.
- Checks that `record.bad`; if not, the test fails.
- Checks that `'1,000 events'` is in `record.revisit_when`; if not, the test fails.
- Calls `edit(docs, ADR, "the relay's backlog is over 1,000 events for more than 5 minutes, or a third consumer needs …`.
- Checks that `'ADR015'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 91 to 94:

```python
def test_done_when_4_a_record_with_only_good_consequences_is_rejected(docs: Path) -> None:
    text = (docs / ADR).read_text()
    (docs / ADR).write_text("\n".join(line for line in text.splitlines() if not line.startswith("Bad:")) + "\n")
    assert "ADR013" in codes(docs)
```

**Test `test_done_when_4_a_record_with_only_good_consequences_is_rejected`** checks: done when 4 a record with only good consequences is rejected.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `(docs / ADR).read_text()` in `text`.
- Calls `(docs / ADR).write_text('\n'.join((line for line in text.splitlines() if not line.startswith('Bad:'))) + '\n')`.
- Checks that `'ADR013'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 97 to 104:

```python
def test_done_when_5_three_versions_that_answer_three_first_questions(docs: Path) -> None:
    versions = MarkdownRecordReader(FileSystemStore(docs)).read_audiences(AUDIENCES)
    assert versions.manager
    assert versions.engineers
    assert versions.sibling
    manager_text = versions.manager
    edit(docs, AUDIENCES, manager_text, versions.sibling)
    assert "AUD008" in codes(docs)
```

**Test `test_done_when_5_three_versions_that_answer_three_first_questions`** checks: done when 5 three versions that answer three first questions.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `MarkdownRecordReader(FileSystemStore(docs)).read_audiences(AUDIENCES)` in `versions`.
- Checks that `versions.manager`; if not, the test fails.
- Checks that `versions.engineers`; if not, the test fails.
- Checks that `versions.sibling`; if not, the test fails.
- Stores `versions.manager` in `manager_text`.
- Calls `edit(docs, AUDIENCES, manager_text, versions.sibling)`.
- Checks that `'AUD008'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 107 to 109:

```python
def test_done_when_5_jargon_in_the_manager_version_is_rejected(docs: Path) -> None:
    edit(docs, AUDIENCES, "The risk is 1 new process to run", "The risk is 1 new relay to run")
    assert "AUD006" in codes(docs)
```

**Test `test_done_when_5_jargon_in_the_manager_version_is_rejected`** checks: done when 5 jargon in the manager version is rejected.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Calls `edit(docs, AUDIENCES, 'The risk is 1 new process to run', 'The risk is 1 new relay to run')`.
- Checks that `'AUD006'` is in `codes(docs)`; if not, the test fails.

`tests/integration/test_done_when.py` lines 112 to 117:

```python
def test_done_when_6_the_record_changed_after_a_real_reading(docs: Path) -> None:
    reaction = MarkdownRecordReader(FileSystemStore(docs)).read_reaction(REACTION)
    assert reaction.misunderstood
    assert reaction.after in " ".join((docs / ADR).read_text().split())
    edit(docs, ADR, "so consumers must ignore repeats by order id.", "so be careful.")
    assert "REA002" in codes(docs)
```

**Test `test_done_when_6_the_record_changed_after_a_real_reading`** checks: done when 6 the record changed after a real reading.

It takes: `docs` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `MarkdownRecordReader(FileSystemStore(docs)).read_reaction(REACTION)` in `reaction`.
- Checks that `reaction.misunderstood`; if not, the test fails.
- Checks that `reaction.after` is in `' '.join((docs / ADR).read_text().split())`; if not, the test fails.
- Calls `edit(docs, ADR, 'so consumers must ignore repeats by order id.', 'so be careful.')`.
- Checks that `'REA002'` is in `codes(docs)`; if not, the test fails.

## Try it yourself

```bash
.venv/bin/pytest -q tests/integration
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/integration/test_done_when.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `test_the_repository_as_committed_passes` check?
   **Answer:** it checks: the repository as committed passes.
2. What does the test `test_done_when_1_two_options_each_with_a_real_advantage` check?
   **Answer:** it checks: done when 1 two options each with a real advantage.
3. What does the test `test_done_when_2_a_context_that_argues_for_an_answer_is_rejected` check?
   **Answer:** it checks: done when 2 a context that argues for an answer is rejected.
4. What does the test `test_done_when_2_a_context_with_no_numbers_is_rejected` check?
   **Answer:** it checks: done when 2 a context with no numbers is rejected.
5. What does the test `test_done_when_3_each_option_is_described_by_the_same_three_lines` check?
   **Answer:** it checks: done when 3 each option is described by the same three lines.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
