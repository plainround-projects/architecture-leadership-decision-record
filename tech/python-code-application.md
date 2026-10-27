# Application layer code

## What it is

The use cases: the steps that join domain rules to the outside world through small interfaces (ports). (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

This is where the repository's application work happens. Reading it file by file, with every line explained, is how a reader sees the work that was done.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/application/__init__.py` | 1 lines. Use cases and the ports they need. Depends on the domain only. |
| `src/adr_toolkit/application/check_documents.py` | 74 lines. The use case behind `adr-toolkit check`: every rule over every document. |
| `src/adr_toolkit/application/ports.py` | 31 lines. What the use cases need from the outside world. |
| `src/adr_toolkit/application/reporting.py` | 34 lines. Format a report as text for the terminal and as Markdown for the build artifact. |

## How it works underneath

The application layer says *what* happens in what order (check every document, export a person's data, collect the evidence) and asks the outside world for what it needs only through `ports.py`, a list of `Protocol` classes. It imports the domain and nothing outer.

## Walkthrough of this repository's use

### `src/adr_toolkit/application/__init__.py`

`src/adr_toolkit/application/__init__.py` lines 1 to 1:

```python
"""Use cases and the ports they need. Depends on the domain only."""
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.

**Module description.** Use cases and the ports they need. Depends on the domain only.

### `src/adr_toolkit/application/check_documents.py`

`src/adr_toolkit/application/check_documents.py` lines 1 to 12:

```python
"""The use case behind `adr-toolkit check`: every rule over every document."""

from __future__ import annotations

from dataclasses import dataclass, field

from adr_toolkit.application.ports import DocumentStore, RecordReader
from adr_toolkit.domain.adr import Adr, AdrLimits, check_adr
from adr_toolkit.domain.audiences import check_audiences
from adr_toolkit.domain.decision_log import check_links, render_log
from adr_toolkit.domain.findings import Finding, Report, error
from adr_toolkit.domain.reaction import check_reaction, check_talk
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The use case behind `adr-toolkit check`: every rule over every document.

Imports:

- From `__future__` it takes `annotations`.
- From `dataclasses` it takes `dataclass, field`.
- From `adr_toolkit.application.ports` it takes `DocumentStore, RecordReader`.
- From `adr_toolkit.domain.adr` it takes `Adr, AdrLimits, check_adr`.
- From `adr_toolkit.domain.audiences` it takes `check_audiences`.
- From `adr_toolkit.domain.decision_log` it takes `check_links, render_log`.
- From `adr_toolkit.domain.findings` it takes `Finding, Report, error`.
- From `adr_toolkit.domain.reaction` it takes `check_reaction, check_talk`.

`src/adr_toolkit/application/check_documents.py` lines 14 to 18:

```python
ADR_FOLDER = "docs/adr"
COMMUNICATION_FOLDER = "docs/communication"
REVIEW_FOLDER = "docs/review"
TALK_FOLDER = "docs/talk"
LOG_PATH = "docs/decision-log.md"
```

> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the text `'docs/adr'` in `ADR_FOLDER`.
- Stores the text `'docs/communication'` in `COMMUNICATION_FOLDER`.
- Stores the text `'docs/review'` in `REVIEW_FOLDER`.
- Stores the text `'docs/talk'` in `TALK_FOLDER`.
- Stores the text `'docs/decision-log.md'` in `LOG_PATH`.

`src/adr_toolkit/application/check_documents.py` lines 21 to 26:

```python
@dataclass(frozen=True)
class CheckSettings:
    """Which records must come with audience versions, a reaction log and a talk."""

    limits: AdrLimits = field(default_factory=AdrLimits)
    required_adrs: tuple[int, ...] = ()
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `CheckSettings`**. Which records must come with audience versions, a reaction log and a talk. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `limits`: a `AdrLimits`, default `field(default_factory=AdrLimits)`.
- Field `required_adrs`: a `tuple[int, ...]`, default `()`.

`src/adr_toolkit/application/check_documents.py` lines 29 to 31:

```python
def load_records(store: DocumentStore, reader: RecordReader) -> list[Adr]:
    """Every decision record in `docs/adr`, parsed."""
    return [reader.read_adr(path) for path in store.list_paths(ADR_FOLDER)]
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.

**Function `load_records`.** Every decision record in `docs/adr`, parsed.

It takes: `store` (a `DocumentStore`); `reader` (a `RecordReader`).

It gives back a `list[Adr]`.

Step by step:

- Gives back a new list made by a loop (`[reader.read_adr(path) for path in store.list_paths(ADR_FOLDER)]`).

`src/adr_toolkit/application/check_documents.py` lines 34 to 50:

```python
def check_documents(store: DocumentStore, reader: RecordReader, settings: CheckSettings) -> Report:
    """Check the records, the links between them, the audience versions, the reaction logs, the talks and the log."""
    records = load_records(store, reader)
    findings: list[Finding] = []
    subjects = [record.path for record in records]
    for record in records:
        findings.extend(check_adr(record, settings.limits))
    findings.extend(check_links(records))
    by_number = {record.number: record for record in records if record.number is not None}
    for number in settings.required_adrs:
        required = by_number.get(number)
        if required is None:
            findings.append(error("DOC001", f"ADR {number:04d}", "a required record does not exist"))
            continue
        findings.extend(_companions(store, reader, required, subjects))
    findings.extend(_log_is_current(store, records))
    return Report(tuple(subjects), tuple(findings))
```

> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** A **dictionary comprehension** `{k: v for ...}` builds a dictionary with a loop written inside braces.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `check_documents`.** Check the records, the links between them, the audience versions, the reaction logs, the talks and the log.

It takes: `store` (a `DocumentStore`); `reader` (a `RecordReader`); `settings` (a `CheckSettings`).

It gives back a `Report`.

Step by step:

- Stores the result of calling `load_records(store, reader)` in `records`.
- Declares `findings` as a `list[Finding]` and stores the list `[]` in it.
- Stores a new list made by a loop (`[record.path for record in records]`) in `subjects`.
- For each `record` in `records`:
  - Calls `findings.extend(check_adr(record, settings.limits))`.
- Calls `findings.extend(check_links(records))`.
- Stores a new dictionary made by a loop (`{record.number: record for record in records if record.number is not …`) in `by_number`.
- For each `number` in `settings.required_adrs`:
  - Stores the result of calling `by_number.get(number)` in `required`.
  - If `required` is the same object as `None`:
    - Calls `findings.append(error('DOC001', f'ADR {number:04d}', 'a required record does not exist'))`.
    - Skips to the next item (`continue`).
  - Calls `findings.extend(_companions(store, reader, required, subjects))`.
- Calls `findings.extend(_log_is_current(store, records))`.
- Gives back the result of calling `Report(tuple(subjects), tuple(findings))`.

`src/adr_toolkit/application/check_documents.py` lines 53 to 73:

```python
def _companions(store: DocumentStore, reader: RecordReader, record: Adr, subjects: list[str]) -> list[Finding]:
    assert record.number is not None
    prefix = f"{record.number:04d}"
    record_text = store.read_text(record.path)
    found: list[Finding] = []
    audiences = f"{COMMUNICATION_FOLDER}/{prefix}-audiences.md"
    reaction = f"{REVIEW_FOLDER}/{prefix}-reaction.md"
    talk = f"{TALK_FOLDER}/{prefix}-three-minute-talk.md"
    for path in (audiences, reaction):
        if not store.exists(path):
            found.append(error("DOC002", record.path, f"ADR {prefix} has no {path}"))
    if store.exists(audiences):
        subjects.append(audiences)
        found.extend(check_audiences(reader.read_audiences(audiences), record.decision))
    if store.exists(reaction):
        subjects.append(reaction)
        found.extend(check_reaction(reader.read_reaction(reaction), record_text))
    if store.exists(talk):
        subjects.append(talk)
        found.extend(check_talk(talk, store.read_text(talk)))
    return found
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.

**Function `_companions`.**

It takes: `store` (a `DocumentStore`); `reader` (a `RecordReader`); `record` (a `Adr`); `subjects` (a `list[str]`).

It gives back a `list[Finding]`.

Step by step:

- Checks that `record.number` is not the same object as `None`; if not, the test fails.
- Stores a text built with values filled in (`f'{record.number:04d}'`) in `prefix`.
- Stores the result of calling `store.read_text(record.path)` in `record_text`.
- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores a text built with values filled in (`f'{COMMUNICATION_FOLDER}/{prefix}-audiences.md'`) in `audiences`.
- Stores a text built with values filled in (`f'{REVIEW_FOLDER}/{prefix}-reaction.md'`) in `reaction`.
- Stores a text built with values filled in (`f'{TALK_FOLDER}/{prefix}-three-minute-talk.md'`) in `talk`.
- For each `path` in the tuple `(audiences, reaction)`:
  - If not (`store.exists(path)`):
    - Calls `found.append(error('DOC002', record.path, f'ADR {prefix} has no {path}'))`.
- If `store.exists(audiences)`:
  - Calls `subjects.append(audiences)`.
  - Calls `found.extend(check_audiences(reader.read_audiences(audiences), record.decision))`.
- If `store.exists(reaction)`:
  - Calls `subjects.append(reaction)`.
  - Calls `found.extend(check_reaction(reader.read_reaction(reaction), record_text))`.
- If `store.exists(talk)`:
  - Calls `subjects.append(talk)`.
  - Calls `found.extend(check_talk(talk, store.read_text(talk)))`.
- Gives back `found`.

`src/adr_toolkit/application/check_documents.py` lines 76 to 81:

```python
def _log_is_current(store: DocumentStore, records: list[Adr]) -> list[Finding]:
    if not store.exists(LOG_PATH):
        return [error("LOG001", LOG_PATH, "the decision log does not exist; run `adr-toolkit log --write`")]
    if store.read_text(LOG_PATH) != render_log(records):
        return [error("LOG001", LOG_PATH, "the decision log is out of date; run `adr-toolkit log --write`")]
    return []
```

**Function `_log_is_current`.**

It takes: `store` (a `DocumentStore`); `records` (a `list[Adr]`).

It gives back a `list[Finding]`.

Step by step:

- If not (`store.exists(LOG_PATH)`):
  - Gives back the list `[error('LOG001', LOG_PATH, 'the decision log does not exist; run `adr…`.
- If `store.read_text(LOG_PATH)` is different from `render_log(records)`:
  - Gives back the list `[error('LOG001', LOG_PATH, 'the decision log is out of date; run `adr…`.
- Gives back the list `[]`.

`src/adr_toolkit/application/check_documents.py` lines 84 to 86:

```python
def current_log(store: DocumentStore, reader: RecordReader) -> str:
    """The decision log as the records say it should read today."""
    return render_log(load_records(store, reader))
```

**Function `current_log`.** The decision log as the records say it should read today.

It takes: `store` (a `DocumentStore`); `reader` (a `RecordReader`).

It gives back a `str`.

Step by step:

- Gives back the result of calling `render_log(load_records(store, reader))`.

`src/adr_toolkit/application/check_documents.py` lines 89 to 93:

```python
def write_log(store: DocumentStore, reader: RecordReader) -> str:
    """Regenerate `docs/decision-log.md` and return its text."""
    text = current_log(store, reader)
    store.write_text(LOG_PATH, text)
    return text
```

**Function `write_log`.** Regenerate `docs/decision-log.md` and return its text.

It takes: `store` (a `DocumentStore`); `reader` (a `RecordReader`).

It gives back a `str`.

Step by step:

- Stores the result of calling `current_log(store, reader)` in `text`.
- Calls `store.write_text(LOG_PATH, text)`.
- Gives back `text`.

### `src/adr_toolkit/application/ports.py`

`src/adr_toolkit/application/ports.py` lines 1 to 9:

```python
"""What the use cases need from the outside world."""

from __future__ import annotations

from typing import Protocol

from adr_toolkit.domain.adr import Adr
from adr_toolkit.domain.audiences import AudienceVersions
from adr_toolkit.domain.reaction import Reaction
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** What the use cases need from the outside world.

Imports:

- From `__future__` it takes `annotations`.
- From `typing` it takes `Protocol`.
- From `adr_toolkit.domain.adr` it takes `Adr`.
- From `adr_toolkit.domain.audiences` it takes `AudienceVersions`.
- From `adr_toolkit.domain.reaction` it takes `Reaction`.

`src/adr_toolkit/application/ports.py` lines 12 to 29:

```python
class DocumentStore(Protocol):
    """Reads and writes the repository's documents by path relative to its root."""

    def list_paths(self, folder: str) -> list[str]:
        """Markdown files directly inside the folder, sorted; empty when the folder is missing."""
        ...

    def read_text(self, path: str) -> str:
        """The text of a file."""
        ...

    def exists(self, path: str) -> bool:
        """True when the file exists."""
        ...

    def write_text(self, path: str, text: str) -> None:
        """Replace a file, creating its folder."""
        ...
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A **Protocol** describes the methods an object must have, without requiring inheritance. Any class with those methods fits. A body of `...` means "no code here, only the shape".
> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `obj[key]` looks a value up by key or position.

**Class `DocumentStore`**, a kind of `Protocol`. Reads and writes the repository's documents by path relative to its root.

Its methods, in order:

**Method `list_paths` of class `DocumentStore`.** Markdown files directly inside the folder, sorted; empty when the folder is missing.

It takes: `folder` (a `str`).

It gives back a `list[str]`.

**Method `read_text` of class `DocumentStore`.** The text of a file.

It takes: `path` (a `str`).

It gives back a `str`.

**Method `exists` of class `DocumentStore`.** True when the file exists.

It takes: `path` (a `str`).

It gives back a `bool`.

**Method `write_text` of class `DocumentStore`.** Replace a file, creating its folder.

It takes: `path` (a `str`); `text` (a `str`).

It gives back a `None`.

`src/adr_toolkit/application/ports.py` lines 32 to 45:

```python
class RecordReader(Protocol):
    """Turns the Markdown of each document type into the domain's values."""

    def read_adr(self, path: str) -> Adr:
        """Parse a decision record."""
        ...

    def read_audiences(self, path: str) -> AudienceVersions:
        """Parse the three audience versions."""
        ...

    def read_reaction(self, path: str) -> Reaction:
        """Parse a reaction log."""
        ...
```

**Class `RecordReader`**, a kind of `Protocol`. Turns the Markdown of each document type into the domain's values.

Its methods, in order:

**Method `read_adr` of class `RecordReader`.** Parse a decision record.

It takes: `path` (a `str`).

It gives back a `Adr`.

**Method `read_audiences` of class `RecordReader`.** Parse the three audience versions.

It takes: `path` (a `str`).

It gives back a `AudienceVersions`.

**Method `read_reaction` of class `RecordReader`.** Parse a reaction log.

It takes: `path` (a `str`).

It gives back a `Reaction`.

### `src/adr_toolkit/application/reporting.py`

`src/adr_toolkit/application/reporting.py` lines 1 to 5:

```python
"""Format a report as text for the terminal and as Markdown for the build artifact."""

from __future__ import annotations

from adr_toolkit.domain.findings import Report
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** Format a report as text for the terminal and as Markdown for the build artifact.

Imports:

- From `__future__` it takes `annotations`.
- From `adr_toolkit.domain.findings` it takes `Report`.

`src/adr_toolkit/application/reporting.py` lines 8 to 17:

```python
def render_text(report: Report) -> str:
    """One line per finding, then the verdict."""
    lines = [
        f"{finding.severity.value.upper():7} {finding.code} {finding.subject}: {finding.message}"
        for finding in report.findings
    ]
    verdict = "OK" if report.ok else "FAILED"
    counts = f"{len(report.subjects)} documents checked, {len(report.errors)} errors, {len(report.warnings)} warnings"
    lines.append(f"{verdict}: {counts}")
    return "\n".join(lines)
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `render_text`.** One line per finding, then the verdict.

It takes: `report` (a `Report`).

It gives back a `str`.

Step by step:

- Stores a new list made by a loop (`[f'{finding.severity.value.upper():7} {finding.code} {finding.subject…`) in `lines`.
- Stores `'OK'` if `report.ok`, otherwise `'FAILED'` in `verdict`.
- Stores a text built with values filled in (`f'{len(report.subjects)} documents checked, {len(report.errors)} erro…`) in `counts`.
- Calls `lines.append(f'{verdict}: {counts}')`.
- Gives back the result of calling `'\n'.join(lines)`.

`src/adr_toolkit/application/reporting.py` lines 20 to 40:

```python
def render_markdown(report: Report) -> str:
    """The report the CI run uploads: verdict, documents checked, findings."""
    verdict = "OK" if report.ok else "FAILED"
    lines = [
        "# Decision record report",
        "",
        f"**Verdict:** {verdict} ({len(report.errors)} errors, {len(report.warnings)} warnings)",
        "",
        "## Documents checked",
        "",
        *[f"- `{subject}`" for subject in report.subjects],
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        lines += ["| Severity | Code | Document | Message |", "| --- | --- | --- | --- |"]
        lines += [f"| {f.severity.value} | {f.code} | `{f.subject}` | {f.message} |" for f in report.findings]
    else:
        lines.append("None.")
    return "\n".join(lines) + "\n"
```

> **In plain words.** `*items` **unpacks** a sequence into separate values; `**options` does the same for a dictionary's keys and values.

**Function `render_markdown`.** The report the CI run uploads: verdict, documents checked, findings.

It takes: `report` (a `Report`).

It gives back a `str`.

Step by step:

- Stores `'OK'` if `report.ok`, otherwise `'FAILED'` in `verdict`.
- Stores the list `['# Decision record report', '', f'**Verdict:** {verdict} ({len(repor…` in `lines`.
- If `report.findings`:
  - Adds the list `['| Severity | Code | Document | Message |', '| --- | --- | --- | ---…` to `lines`.
  - Adds a new list made by a loop (`[f'| {f.severity.value} | {f.code} | `{f.subject}` | {f.message} |' f…`) to `lines`.
- Otherwise:
  - Calls `lines.append('None.')`.
- Gives back `'\n'.join(lines) + '\n'`.

## Try it yourself

```bash
.venv/bin/python -c "import adr_toolkit.application.check_documents; print(adr_toolkit.application.check_documents.__doc__)"
```
Prints the module's description: `The use case behind `adr-toolkit check`: every rule over every document.`

```bash
.venv/bin/python -c "import adr_toolkit.application.ports; print(adr_toolkit.application.ports.__doc__)"
```
Prints the module's description: `What the use cases need from the outside world.`

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check src/adr_toolkit/application/__init__.py src/adr_toolkit/application/check_documents.py src/adr_toolkit/application/ports.py src/adr_toolkit/application/reporting.py
```
Prints `All checks passed!`.

```bash
grep -c "^def \|^class \|    def " src/adr_toolkit/application/check_documents.py
```
Counts the functions, methods and classes in `src/adr_toolkit/application/check_documents.py`.

## Mistakes people make

- Importing an adapter directly. Use the port; the adapter is passed in from the outside.
- Putting a rule here that belongs in the domain, where it can be tested without any setup.
- Catching an error too early. Use cases let named errors travel up to the interfaces layer.

## Check yourself

1. What is `CheckSettings` for?
   **Answer:** Which records must come with audience versions, a reaction log and a talk.
2. What is `load_records` for?
   **Answer:** Every decision record in `docs/adr`, parsed.
3. What is `check_documents` for?
   **Answer:** Check the records, the links between them, the audience versions, the reaction logs, the talks and the log.
4. What is `current_log` for?
   **Answer:** The decision log as the records say it should read today.
5. What is `write_log` for?
   **Answer:** Regenerate `docs/decision-log.md` and return its text.

## Further reading

- Python 3.12 tutorial, classes: <https://docs.python.org/3.12/tutorial/classes.html>
- Python 3.12 language reference: <https://docs.python.org/3.12/reference/>
- Type hints: <https://docs.python.org/3.12/library/typing.html>
