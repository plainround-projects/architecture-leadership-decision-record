# The tests (interfaces)

## What it is

The pytest tests in `tests/unit/interfaces`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/unit/interfaces/test_cli.py` | 33 lines.  |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/unit/interfaces/test_cli.py`

`tests/unit/interfaces/test_cli.py` lines 1 to 7:

```python
import shutil
from pathlib import Path

import pytest

from adr_toolkit.interfaces.cli import main
from tests.conftest import REPOSITORY_ROOT
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- It imports module `shutil`.
- From `pathlib` it takes `Path`.
- It imports module `pytest`.
- From `adr_toolkit.interfaces.cli` it takes `main`.
- From `tests.conftest` it takes `REPOSITORY_ROOT`.

`tests/unit/interfaces/test_cli.py` lines 10 to 16:

```python
@pytest.fixture
def copy_of_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    shutil.copytree(REPOSITORY_ROOT / "docs", tmp_path / "docs")
    monkeypatch.setenv("ADR_ROOT", str(tmp_path))
    monkeypatch.setenv("ADR_REQUIRED_COMMUNICATION", "7")
    monkeypatch.setenv("REPORT_DIR", "build")
    return tmp_path
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `tmp_path` is a built-in pytest fixture: a fresh, empty temporary folder (a `Path`) that is removed after the test.
> **In plain words.** `monkeypatch` is a built-in pytest fixture that changes something (an environment variable, an attribute) for this test only and undoes it afterwards.

**Function `copy_of_repo`.**

It takes: `tmp_path` (a `Path`); `monkeypatch` (a `pytest.MonkeyPatch`).

It gives back a `Path`.

Decorators: `@pytest.fixture`.

Step by step:

- Calls `shutil.copytree(REPOSITORY_ROOT / 'docs', tmp_path / 'docs')`.
- Calls `monkeypatch.setenv('ADR_ROOT', str(tmp_path))`.
- Calls `monkeypatch.setenv('ADR_REQUIRED_COMMUNICATION', '7')`.
- Calls `monkeypatch.setenv('REPORT_DIR', 'build')`.
- Gives back `tmp_path`.

`tests/unit/interfaces/test_cli.py` lines 19 to 21:

```python
def test_check_passes_on_the_repository_documents(copy_of_repo, capsys):
    assert main(["check"]) == 0
    assert capsys.readouterr().out.splitlines()[-1].startswith("OK: 6 documents")
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.
> **In plain words.** `capsys` is a built-in pytest fixture that captures what the program prints, so the test can read it with `capsys.readouterr()`.

**Test `test_check_passes_on_the_repository_documents`** checks: check passes on the repository documents.

It takes: `copy_of_repo`; `capsys`.

Step by step:

- Checks that `main(['check'])` equals `0`; if not, the test fails.
- Checks that `capsys.readouterr().out.splitlines()[-1].startswith('OK: 6 documents')`; if not, the test fails.

`tests/unit/interfaces/test_cli.py` lines 24 to 28:

```python
def test_check_fails_when_the_bad_consequence_is_removed(copy_of_repo, capsys):
    adr = copy_of_repo / "docs/adr/0007-announce-paid-orders.md"
    adr.write_text("\n".join(line for line in adr.read_text().splitlines() if not line.startswith("Bad:")) + "\n")
    assert main(["check"]) == 1
    assert "ADR013" in capsys.readouterr().out
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Test `test_check_fails_when_the_bad_consequence_is_removed`** checks: check fails when the bad consequence is removed.

It takes: `copy_of_repo`; `capsys`.

Step by step:

- Stores `copy_of_repo / 'docs/adr/0007-announce-paid-orders.md'` in `adr`.
- Calls `adr.write_text('\n'.join((line for line in adr.read_text().splitlines() if not line.startswith('Bad:'))) + '\…`.
- Checks that `main(['check'])` equals `1`; if not, the test fails.
- Checks that `'ADR013'` is in `capsys.readouterr().out`; if not, the test fails.

`tests/unit/interfaces/test_cli.py` lines 31 to 33:

```python
def test_report_writes_markdown(copy_of_repo, capsys):
    assert main(["report"]) == 0
    assert (copy_of_repo / "build/report.md").read_text().startswith("# Decision record report")
```

**Test `test_report_writes_markdown`** checks: report writes markdown.

It takes: `copy_of_repo`; `capsys`.

Step by step:

- Checks that `main(['report'])` equals `0`; if not, the test fails.
- Checks that `(copy_of_repo / 'build/report.md').read_text().startswith('# Decision…`; if not, the test fails.

`tests/unit/interfaces/test_cli.py` lines 36 to 41:

```python
def test_log_prints_and_writes(copy_of_repo, capsys):
    assert main(["log"]) == 0
    assert "# Decision log" in capsys.readouterr().out
    (copy_of_repo / "docs/decision-log.md").write_text("stale\n")
    assert main(["log", "--write"]) == 0
    assert "stale" not in (copy_of_repo / "docs/decision-log.md").read_text()
```

**Test `test_log_prints_and_writes`** checks: log prints and writes.

It takes: `copy_of_repo`; `capsys`.

Step by step:

- Checks that `main(['log'])` equals `0`; if not, the test fails.
- Checks that `'# Decision log'` is in `capsys.readouterr().out`; if not, the test fails.
- Calls `(copy_of_repo / 'docs/decision-log.md').write_text('stale\n')`.
- Checks that `main(['log', '--write'])` equals `0`; if not, the test fails.
- Checks that `'stale'` is not in `(copy_of_repo / 'docs/decision-log.md').read_text…`; if not, the test fails.

`tests/unit/interfaces/test_cli.py` lines 44 to 47:

```python
def test_a_bad_setting_exits_with_2(monkeypatch, capsys):
    monkeypatch.setenv("ADR_MAX_LINES", "lots")
    assert main(["check"]) == 2
    assert "ADR_MAX_LINES" in capsys.readouterr().err
```

**Test `test_a_bad_setting_exits_with_2`** checks: a bad setting exits with 2.

It takes: `monkeypatch`; `capsys`.

Step by step:

- Calls `monkeypatch.setenv('ADR_MAX_LINES', 'lots')`.
- Checks that `main(['check'])` equals `2`; if not, the test fails.
- Checks that `'ADR_MAX_LINES'` is in `capsys.readouterr().err`; if not, the test fails.

## Try it yourself

```bash
.venv/bin/pytest -q tests/unit/interfaces
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/unit/interfaces/test_cli.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `test_check_passes_on_the_repository_documents` check?
   **Answer:** it checks: check passes on the repository documents.
2. What does the test `test_check_fails_when_the_bad_consequence_is_removed` check?
   **Answer:** it checks: check fails when the bad consequence is removed.
3. What does the test `test_report_writes_markdown` check?
   **Answer:** it checks: report writes markdown.
4. What does the test `test_log_prints_and_writes` check?
   **Answer:** it checks: log prints and writes.
5. What does the test `test_a_bad_setting_exits_with_2` check?
   **Answer:** it checks: a bad setting exits with 2.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
