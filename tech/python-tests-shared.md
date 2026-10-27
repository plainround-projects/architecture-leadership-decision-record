# The tests (shared)

## What it is

The pytest tests in `tests/shared`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/conftest.py` | 62 lines. Shared builders: a valid record, an in-memory document store, and the repository's own root. |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/conftest.py`

`tests/conftest.py` lines 1 to 10:

```python
"""Shared builders: a valid record, an in-memory document store, and the repository's own root."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from adr_toolkit.domain.adr import Adr, Option
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** Shared builders: a valid record, an in-memory document store, and the repository's own root.

Imports:

- From `__future__` it takes `annotations`.
- From `dataclasses` it takes `replace`.
- From `pathlib` it takes `Path`.
- It imports module `pytest`.
- From `adr_toolkit.domain.adr` it takes `Adr, Option`.

`tests/conftest.py` lines 12 to 12:

```python
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores `Path(__file__).resolve().parents[1]` in `REPOSITORY_ROOT`.

`tests/conftest.py` lines 15 to 52:

```python
def valid_adr(**changes: object) -> Adr:
    """A record that passes every rule; tests change one field to break one rule."""
    base = Adr(
        path="docs/adr/0007-x.md",
        number=7,
        title="How the orders service announces paid orders",
        status="Accepted",
        superseded_by=None,
        supersedes=None,
        date_text="2026-10-22",
        deciders="Orders tech lead, database owner",
        sections=("Context", "Options considered", "Decision", "Consequences"),
        context="Volume grew from 2,000 to 40,000 orders a day and a scan takes 6 seconds.",
        options=(
            Option(
                "keep polling",
                "nothing new to run; it ships this week",
                "load grows with every new reader",
                "the team has no time to learn",
            ),
            Option(
                "an outbox table with a relay",
                "the event is written in the same transaction as the order",
                "one more table and a relay process to run",
                "events must never be lost",
            ),
        ),
        decision=(
            "We will write an event row beside the order in an outbox table and forward it with a relay, "
            "because it never loses an event."
        ),
        good="emails arrive in under 2 seconds",
        bad="we own one more table and one relay process",
        revisit_when="the relay backlog is over 1,000 events for more than 5 minutes",
        line_count=30,
        word_count=300,
    )
    return replace(base, **changes)  # type: ignore[arg-type]
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Function `valid_adr`.** A record that passes every rule; tests change one field to break one rule.

It takes: `**changes` (any extra named values).

It gives back a `Adr`.

Step by step:

- Stores the result of calling `Adr(path='docs/adr/0007-x.md', number=7, title='How the orders service announces paid ord…` in `base`.
- Gives back the result of calling `replace(base, **changes)`.

`tests/conftest.py` lines 55 to 73:

```python
class MemoryStore:
    """A DocumentStore held in a dict, for tests that need no disk."""

    def __init__(self, files: dict[str, str] | None = None) -> None:
        self.files = dict(files or {})

    def list_paths(self, folder: str) -> list[str]:
        return sorted(
            path for path in self.files if path.startswith(f"{folder}/") and "/" not in path[len(folder) + 1 :]
        )

    def read_text(self, path: str) -> str:
        return self.files[path]

    def exists(self, path: str) -> bool:
        return path in self.files

    def write_text(self, path: str, text: str) -> None:
        self.files[path] = text
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.
> **In plain words.** A **dictionary** `{key: value}` maps keys to values.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.
> **In plain words.** A **slice** such as `text[:7]` or `items[1:]` takes part of a sequence: `[:7]` the first seven items, `[1:]` everything after the first.

**Class `MemoryStore`**. A DocumentStore held in a dict, for tests that need no disk.

Its methods, in order:

**Method `__init__` of class `MemoryStore`.**

It takes: `files` (a `dict[str, str] | None`), default `None`.

It gives back a `None`.

Step by step:

- Stores the result of calling `dict(files or {})` in `self.files`.

**Method `list_paths` of class `MemoryStore`.**

It takes: `folder` (a `str`).

It gives back a `list[str]`.

Step by step:

- Gives back the result of calling `sorted((path for path in self.files if path.startswith(f'{folder}/') and '/' not in path[…`.

**Method `read_text` of class `MemoryStore`.**

It takes: `path` (a `str`).

It gives back a `str`.

Step by step:

- Gives back `self.files[path]`.

**Method `exists` of class `MemoryStore`.**

It takes: `path` (a `str`).

It gives back a `bool`.

Step by step:

- Gives back whether `path` is in `self.files`.

**Method `write_text` of class `MemoryStore`.**

It takes: `path` (a `str`); `text` (a `str`).

It gives back a `None`.

Step by step:

- Stores `text` in `self.files[path]`.

`tests/conftest.py` lines 76 to 78:

```python
@pytest.fixture
def repository_root() -> Path:
    return REPOSITORY_ROOT
```

**Function `repository_root`.**

It gives back a `Path`.

Decorators: `@pytest.fixture`.

Step by step:

- Gives back `REPOSITORY_ROOT`.

## Try it yourself

```bash
.venv/bin/pytest -q tests
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/conftest.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `valid_adr` check?
   **Answer:** A record that passes every rule; tests change one field to break one rule.
2. What does the test `MemoryStore` check?
   **Answer:** A DocumentStore held in a dict, for tests that need no disk.
3. What is a docstring?
   **Answer:** A text in triple quotes at the start of a module, class or function that describes it.
4. What does `frozen=True` do on a dataclass?
   **Answer:** It forbids changing a field after the object is created.
5. What does a type hint do at run time?
   **Answer:** Nothing; mypy reads hints before the program runs.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
