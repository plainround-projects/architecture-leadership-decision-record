# The tests (application)

## What it is

The pytest tests in `tests/unit/application`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/unit/application/test_check_documents.py` | 58 lines.  |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/unit/application/test_check_documents.py`

`tests/unit/application/test_check_documents.py` lines 1 to 7:

```python
from pathlib import Path

from adr_toolkit.application.check_documents import CheckSettings, check_documents, current_log, write_log
from adr_toolkit.application.reporting import render_markdown, render_text
from adr_toolkit.domain.findings import Report
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import REPOSITORY_ROOT, MemoryStore
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `pathlib` it takes `Path`.
- From `adr_toolkit.application.check_documents` it takes `CheckSettings, check_documents, current_log, write_log`.
- From `adr_toolkit.application.reporting` it takes `render_markdown, render_text`.
- From `adr_toolkit.domain.findings` it takes `Report`.
- From `adr_toolkit.infrastructure.markdown` it takes `MarkdownRecordReader`.
- From `tests.conftest` it takes `REPOSITORY_ROOT, MemoryStore`.

`tests/unit/application/test_check_documents.py` lines 10 to 14:

```python
def repo_files() -> dict[str, str]:
    files: dict[str, str] = {}
    for path in REPOSITORY_ROOT.glob("docs/**/*.md"):
        files[path.relative_to(REPOSITORY_ROOT).as_posix()] = Path(path).read_text()
    return files
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **dictionary** `{key: value}` maps keys to values.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Function `repo_files`.**

It gives back a `dict[str, str]`.

Step by step:

- Declares `files` as a `dict[str, str]` and stores the dictionary `{}` in it.
- For each `path` in the result of calling `REPOSITORY_ROOT.glob('docs/**/*.md')`:
  - Stores the result of calling `Path(path).read_text()` in `files[path.relative_to(REPOSITORY_ROOT).as_posix()]`.
- Gives back `files`.

`tests/unit/application/test_check_documents.py` lines 17 to 19:

```python
def run(files: dict[str, str], required=(7,)):
    store = MemoryStore(files)
    return check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=required))
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Function `run`.**

It takes: `files` (a `dict[str, str]`); `required`, default `(7,)`.

Step by step:

- Stores the result of calling `MemoryStore(files)` in `store`.
- Gives back the result of calling `check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=required))`.

`tests/unit/application/test_check_documents.py` lines 22 to 23:

```python
def codes(report) -> set[str]:
    return {finding.code for finding in report.findings}
```

> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.

**Function `codes`.**

It takes: `report`.

It gives back a `set[str]`.

Step by step:

- Gives back a new set made by a loop (`{finding.code for finding in report.findings}`).

`tests/unit/application/test_check_documents.py` lines 26 to 30:

```python
def test_the_repository_documents_pass():
    report = run(repo_files())
    assert report.ok
    assert {f.code for f in report.warnings} == {"REA004"}
    assert len(report.subjects) == 6
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_the_repository_documents_pass`** checks: the repository documents pass.

Step by step:

- Stores the result of calling `run(repo_files())` in `report`.
- Checks that `report.ok`; if not, the test fails.
- Checks that `{f.code for f in report.warnings}` equals `{'REA004'}`; if not, the test fails.
- Checks that `len(report.subjects)` equals `6`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 33 to 34:

```python
def test_a_required_record_that_does_not_exist_is_reported():
    assert "DOC001" in codes(run(repo_files(), required=(9,)))
```

**Test `test_a_required_record_that_does_not_exist_is_reported`** checks: a required record that does not exist is reported.

Step by step:

- Checks that `'DOC001'` is in `codes(run(repo_files(), required=(9,)))`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 37 to 41:

```python
def test_missing_companions_are_reported():
    files = repo_files()
    del files["docs/communication/0007-audiences.md"]
    del files["docs/review/0007-reaction.md"]
    assert codes(run(files)) == {"DOC002"}
```

**Test `test_missing_companions_are_reported`** checks: missing companions are reported.

Step by step:

- Stores the result of calling `repo_files()` in `files`.
- Removes `files['docs/communication/0007-audiences.md']`.
- Removes `files['docs/review/0007-reaction.md']`.
- Checks that `codes(run(files))` equals `{'DOC002'}`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 44 to 47:

```python
def test_a_missing_log_is_reported():
    files = repo_files()
    del files["docs/decision-log.md"]
    assert codes(run(files)) == {"LOG001", "REA004"}
```

**Test `test_a_missing_log_is_reported`** checks: a missing log is reported.

Step by step:

- Stores the result of calling `repo_files()` in `files`.
- Removes `files['docs/decision-log.md']`.
- Checks that `codes(run(files))` equals `{'LOG001', 'REA004'}`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 50 to 58:

```python
def test_a_stale_log_is_reported_and_write_log_repairs_it():
    files = repo_files()
    files["docs/decision-log.md"] = "old\n"
    store = MemoryStore(files)
    reader = MarkdownRecordReader(store)
    assert "LOG001" in codes(check_documents(store, reader, CheckSettings(required_adrs=(7,))))
    write_log(store, reader)
    assert store.files["docs/decision-log.md"] == current_log(store, reader)
    assert "LOG001" not in codes(check_documents(store, reader, CheckSettings(required_adrs=(7,))))
```

**Test `test_a_stale_log_is_reported_and_write_log_repairs_it`** checks: a stale log is reported and write log repairs it.

Step by step:

- Stores the result of calling `repo_files()` in `files`.
- Stores the text `'old\n'` in `files['docs/decision-log.md']`.
- Stores the result of calling `MemoryStore(files)` in `store`.
- Stores the result of calling `MarkdownRecordReader(store)` in `reader`.
- Checks that `'LOG001'` is in `codes(check_documents(store, reader, CheckSetting…`; if not, the test fails.
- Calls `write_log(store, reader)`.
- Checks that `store.files['docs/decision-log.md']` equals `current_log(store, reader)`; if not, the test fails.
- Checks that `'LOG001'` is not in `codes(check_documents(store, reader, CheckSetting…`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 61 to 68:

```python
def test_a_fix_logged_but_not_made_is_reported():
    files = repo_files()
    files["docs/adr/0007-announce-paid-orders.md"] = files["docs/adr/0007-announce-paid-orders.md"].replace(
        "a stuck relay delays every consumer, and the relay can publish an event twice, "
        "so consumers must ignore repeats by order id.",
        "and a stuck relay delays every consumer.",
    )
    assert {"REA002", "REA003"} <= codes(run(files))
```

**Test `test_a_fix_logged_but_not_made_is_reported`** checks: a fix logged but not made is reported.

Step by step:

- Stores the result of calling `repo_files()` in `files`.
- Stores the result of calling `files['docs/adr/0007-announce-paid-orders.md'].replace('a stuck relay delays every consum…` in `files['docs/adr/0007-announce-paid-orders.md']`.
- Checks that `{'REA002', 'REA003'}` is at most `codes(run(files))`; if not, the test fails.

`tests/unit/application/test_check_documents.py` lines 71 to 79:

```python
def test_text_and_markdown_reports_carry_the_verdict():
    report = run(repo_files())
    assert render_text(report).splitlines()[-1] == "OK: 6 documents checked, 0 errors, 1 warnings"
    markdown = render_markdown(report)
    assert "**Verdict:** OK" in markdown
    assert "REA004" in markdown
    broken = run({})
    assert "FAILED" in render_text(broken)
    assert "None." in render_markdown(Report(subjects=(), findings=()))
```

**Test `test_text_and_markdown_reports_carry_the_verdict`** checks: text and markdown reports carry the verdict.

Step by step:

- Stores the result of calling `run(repo_files())` in `report`.
- Checks that `render_text(report).splitlines()[-1]` equals `'OK: 6 documents checked, 0 errors, 1 warnings'`; if not, the test fails.
- Stores the result of calling `render_markdown(report)` in `markdown`.
- Checks that `'**Verdict:** OK'` is in `markdown`; if not, the test fails.
- Checks that `'REA004'` is in `markdown`; if not, the test fails.
- Stores the result of calling `run({})` in `broken`.
- Checks that `'FAILED'` is in `render_text(broken)`; if not, the test fails.
- Checks that `'None.'` is in `render_markdown(Report(subjects=(), findings=()))`; if not, the test fails.

## Try it yourself

```bash
.venv/bin/pytest -q tests/unit/application
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/unit/application/test_check_documents.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `test_the_repository_documents_pass` check?
   **Answer:** it checks: the repository documents pass.
2. What does the test `test_a_required_record_that_does_not_exist_is_reported` check?
   **Answer:** it checks: a required record that does not exist is reported.
3. What does the test `test_missing_companions_are_reported` check?
   **Answer:** it checks: missing companions are reported.
4. What does the test `test_a_missing_log_is_reported` check?
   **Answer:** it checks: a missing log is reported.
5. What does the test `test_a_stale_log_is_reported_and_write_log_repairs_it` check?
   **Answer:** it checks: a stale log is reported and write log repairs it.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
