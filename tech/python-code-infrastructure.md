# Infrastructure layer code

## What it is

The adapters: the code that really reads files, talks to a database or a network, and reads the environment. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

This is where the repository's infrastructure work happens. Reading it file by file, with every line explained, is how a reader sees the work that was done.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/infrastructure/__init__.py` | 1 lines. Adapters: the file system, the Markdown parsers, the environment and the report writer. |
| `src/adr_toolkit/infrastructure/filesystem.py` | 31 lines. The document store on the local file system. |
| `src/adr_toolkit/infrastructure/markdown.py` | 144 lines. Parse the Markdown of each document type into the domain's values. |
| `src/adr_toolkit/infrastructure/settings.py` | 42 lines. Settings from the environment, validated once at start-up (twelve-factor). |

## How it works underneath

Each adapter implements a port from the application layer using a real technology (the file system, SQLite or PostgreSQL, HTTP, the environment). They are kept thin, so that swapping one changes nothing above. Tests exercise them on real temporary files or a real database.

## Walkthrough of this repository's use

### `src/adr_toolkit/infrastructure/__init__.py`

`src/adr_toolkit/infrastructure/__init__.py` lines 1 to 1:

```python
"""Adapters: the file system, the Markdown parsers, the environment and the report writer."""
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.

**Module description.** Adapters: the file system, the Markdown parsers, the environment and the report writer.

### `src/adr_toolkit/infrastructure/filesystem.py`

`src/adr_toolkit/infrastructure/filesystem.py` lines 1 to 5:

```python
"""The document store on the local file system."""

from __future__ import annotations

from pathlib import Path
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The document store on the local file system.

Imports:

- From `__future__` it takes `annotations`.
- From `pathlib` it takes `Path`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 8 to 9:

```python
class FileSystemStore:
    """Reads the repository's documents under one root. Paths are relative and may not leave the root."""
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.

**Class `FileSystemStore`**. Reads the repository's documents under one root. Paths are relative and may not leave the root.

`src/adr_toolkit/infrastructure/filesystem.py` lines 11 to 12:

```python
    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.

**Method `__init__` of class `FileSystemStore`.**

It takes: `root` (a `Path`).

It gives back a `None`.

Step by step:

- Stores the result of calling `root.resolve()` in `self._root`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 14 to 18:

```python
    def _resolve(self, path: str) -> Path:
        resolved = (self._root / path).resolve()
        if self._root != resolved and self._root not in resolved.parents:
            raise ValueError(f"path escapes the repository root: {path}")
        return resolved
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `raise Error(...)` stops the current function by signalling an error. `raise ... from None` hides the earlier error, so the user sees only the new, clearer message.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Method `_resolve` of class `FileSystemStore`.**

It takes: `path` (a `str`).

It gives back a `Path`.

Step by step:

- Stores the result of calling `(self._root / path).resolve()` in `resolved`.
- If `self._root` is different from `resolved` and `self._root` is not in `resolved.parents`:
  - Stops here by raising `ValueError(f'path escapes the repository root: {path}')`.
- Gives back `resolved`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 20 to 27:

```python
    def list_paths(self, folder: str) -> list[str]:
        """Markdown files directly inside the folder, sorted."""
        directory = self._resolve(folder)
        if not directory.is_dir():
            return []
        return sorted(
            f"{folder}/{entry.name}" for entry in directory.iterdir() if entry.suffix == ".md" and entry.is_file()
        )
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Method `list_paths` of class `FileSystemStore`.** Markdown files directly inside the folder, sorted.

It takes: `folder` (a `str`).

It gives back a `list[str]`.

Step by step:

- Stores the result of calling `self._resolve(folder)` in `directory`.
- If not (`directory.is_dir()`):
  - Gives back the list `[]`.
- Gives back the result of calling `sorted((f'{folder}/{entry.name}' for entry in directory.iterdir() if entry.suffix == '.md…`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 29 to 31:

```python
    def read_text(self, path: str) -> str:
        """The text of a file."""
        return self._resolve(path).read_text(encoding="utf-8")
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Method `read_text` of class `FileSystemStore`.** The text of a file.

It takes: `path` (a `str`).

It gives back a `str`.

Step by step:

- Gives back the result of calling `self._resolve(path).read_text(encoding='utf-8')`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 33 to 35:

```python
    def exists(self, path: str) -> bool:
        """True when the file exists."""
        return self._resolve(path).is_file()
```

**Method `exists` of class `FileSystemStore`.** True when the file exists.

It takes: `path` (a `str`).

It gives back a `bool`.

Step by step:

- Gives back the result of calling `self._resolve(path).is_file()`.

`src/adr_toolkit/infrastructure/filesystem.py` lines 37 to 41:

```python
    def write_text(self, path: str, text: str) -> None:
        """Replace a file, creating its folder."""
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
```

**Method `write_text` of class `FileSystemStore`.** Replace a file, creating its folder.

It takes: `path` (a `str`); `text` (a `str`).

It gives back a `None`.

Step by step:

- Stores the result of calling `self._resolve(path)` in `target`.
- Calls `target.parent.mkdir(parents=True, exist_ok=True)`.
- Calls `target.write_text(text, encoding='utf-8')`.

### `src/adr_toolkit/infrastructure/markdown.py`

`src/adr_toolkit/infrastructure/markdown.py` lines 1 to 10:

```python
"""Parse the Markdown of each document type into the domain's values."""

from __future__ import annotations

import re

from adr_toolkit.application.ports import DocumentStore
from adr_toolkit.domain.adr import Adr, Option
from adr_toolkit.domain.audiences import AudienceVersions
from adr_toolkit.domain.reaction import Reaction
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** Parse the Markdown of each document type into the domain's values.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `re`.
- From `adr_toolkit.application.ports` it takes `DocumentStore`.
- From `adr_toolkit.domain.adr` it takes `Adr, Option`.
- From `adr_toolkit.domain.audiences` it takes `AudienceVersions`.
- From `adr_toolkit.domain.reaction` it takes `Reaction`.

`src/adr_toolkit/infrastructure/markdown.py` lines 12 to 18:

```python
_TITLE = re.compile(r"^# ADR (\d+): (.+?)\s*$")
_META = re.compile(r"^(Status|Date|Deciders|Supersedes):\s*(.*?)\s*$")
_SUPERSEDED_BY = re.compile(r"^Superseded by ADR (\d+)$")
_ADR_REF = re.compile(r"^ADR (\d+)$")
_HEADING2 = re.compile(r"^## (.+?)\s*$")
_HEADING3 = re.compile(r"^### (.+?)\s*$")
_OPTION_NAME = re.compile(r"^Option [A-Z]: (.+)$")
```

> **In plain words.** A **regular expression** is a short pattern for text, such as `^## (.+)$` for "a line starting with ## ". `re.compile` prepares it once; `.match` tries it at the start of a string and returns a match object or `None`.
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the result of calling `re.compile('^# ADR (\\d+): (.+?)\\s*$')` in `_TITLE`.
- Stores the result of calling `re.compile('^(Status|Date|Deciders|Supersedes):\\s*(.*?)\\s*$')` in `_META`.
- Stores the result of calling `re.compile('^Superseded by ADR (\\d+)$')` in `_SUPERSEDED_BY`.
- Stores the result of calling `re.compile('^ADR (\\d+)$')` in `_ADR_REF`.
- Stores the result of calling `re.compile('^## (.+?)\\s*$')` in `_HEADING2`.
- Stores the result of calling `re.compile('^### (.+?)\\s*$')` in `_HEADING3`.
- Stores the result of calling `re.compile('^Option [A-Z]: (.+)$')` in `_OPTION_NAME`.

`src/adr_toolkit/infrastructure/markdown.py` lines 21 to 32:

```python
def _sections(lines: list[str]) -> dict[str, list[str]]:
    """Group lines under their `##` heading, in file order. Lines before the first heading go under ''."""
    grouped: dict[str, list[str]] = {"": []}
    current = ""
    for line in lines:
        match = _HEADING2.match(line)
        if match:
            current = match.group(1)
            grouped[current] = []
        else:
            grouped[current].append(line)
    return grouped
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **dictionary** `{key: value}` maps keys to values.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Function `_sections`.** Group lines under their `##` heading, in file order. Lines before the first heading go under ''.

It takes: `lines` (a `list[str]`).

It gives back a `dict[str, list[str]]`.

Step by step:

- Declares `grouped` as a `dict[str, list[str]]` and stores the dictionary `{'': []}` in it.
- Stores the text `''` in `current`.
- For each `line` in `lines`:
  - Stores the result of calling `_HEADING2.match(line)` in `match`.
  - If `match`:
    - Stores the result of calling `match.group(1)` in `current`.
    - Stores the list `[]` in `grouped[current]`.
  - Otherwise:
    - Calls `grouped[current].append(line)`.
- Gives back `grouped`.

`src/adr_toolkit/infrastructure/markdown.py` lines 35 to 47:

```python
def _fields(lines: list[str], labels: tuple[str, ...]) -> dict[str, str]:
    """`Label: text` fields whose text may continue on the following lines until the next label."""
    pattern = re.compile(rf"^({'|'.join(re.escape(label) for label in labels)}):\s*(.*)$")
    values: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            current = match.group(1)
            values[current] = [match.group(2)]
        elif current is not None and line.strip():
            values[current].append(line.strip())
    return {label: " ".join(parts).strip() for label, parts in values.items()}
```

> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** A **dictionary comprehension** `{k: v for ...}` builds a dictionary with a loop written inside braces.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Function `_fields`.** `Label: text` fields whose text may continue on the following lines until the next label.

It takes: `lines` (a `list[str]`); `labels` (a `tuple[str, ...]`).

It gives back a `dict[str, str]`.

Step by step:

- Stores the result of calling `re.compile(f"^({'|'.join((re.escape(label) for label in labels))}):\\s*(.*)$")` in `pattern`.
- Declares `values` as a `dict[str, list[str]]` and stores the dictionary `{}` in it.
- Declares `current` as a `str | None` and stores nothing (`None`) in it.
- For each `line` in `lines`:
  - Stores the result of calling `pattern.match(line.strip())` in `match`.
  - If `match`:
    - Stores the result of calling `match.group(1)` in `current`.
    - Stores the list `[match.group(2)]` in `values[current]`.
  - Otherwise, if `current` is not the same object as `None` and `line.strip()`:
    - Calls `values[current].append(line.strip())`.
- Gives back a new dictionary made by a loop (`{label: ' '.join(parts).strip() for label, parts in values.items()}`).

`src/adr_toolkit/infrastructure/markdown.py` lines 50 to 51:

```python
def _paragraph(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip())
```

**Function `_paragraph`.**

It takes: `lines` (a `list[str]`).

It gives back a `str`.

Step by step:

- Gives back the result of calling `' '.join((line.strip() for line in lines if line.strip()))`.

`src/adr_toolkit/infrastructure/markdown.py` lines 54 to 55:

```python
class MarkdownRecordReader:
    """Reads the repository's three document types from a store."""
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.

**Class `MarkdownRecordReader`**. Reads the repository's three document types from a store.

`src/adr_toolkit/infrastructure/markdown.py` lines 57 to 58:

```python
    def __init__(self, store: DocumentStore) -> None:
        self._store = store
```

**Method `__init__` of class `MarkdownRecordReader`.**

It takes: `store` (a `DocumentStore`).

It gives back a `None`.

Step by step:

- Stores `store` in `self._store`.

`src/adr_toolkit/infrastructure/markdown.py` lines 60 to 88:

```python
    def read_adr(self, path: str) -> Adr:
        """Parse a decision record; whatever is missing stays empty for the rules to report."""
        text = self._store.read_text(path)
        lines = text.splitlines()
        title_match = _TITLE.match(lines[0]) if lines else None
        meta = {m.group(1): m.group(2) for line in lines if (m := _META.match(line))}
        sections = _sections(lines)
        status, superseded_by = _status(meta.get("Status", ""))
        supersedes = _adr_number(meta.get("Supersedes", ""))
        consequences = _fields(sections.get("Consequences", []), ("Good", "Bad", "Revisit when"))
        return Adr(
            path=path,
            number=int(title_match.group(1)) if title_match else None,
            title=title_match.group(2) if title_match else "",
            status=status,
            superseded_by=superseded_by,
            supersedes=supersedes,
            date_text=meta.get("Date", ""),
            deciders=meta.get("Deciders", ""),
            sections=tuple(name for name in sections if name),
            context=_paragraph(sections.get("Context", [])),
            options=_options(sections.get("Options considered", [])),
            decision=_paragraph(sections.get("Decision", [])),
            good=consequences.get("Good", ""),
            bad=consequences.get("Bad", ""),
            revisit_when=consequences.get("Revisit when", ""),
            line_count=len([line for line in lines if line.strip()]),
            word_count=len(text.split()),
        )
```

> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** The **walrus operator** `:=` stores a value in a name and uses it in the same expression.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.

**Method `read_adr` of class `MarkdownRecordReader`.** Parse a decision record; whatever is missing stays empty for the rules to report.

It takes: `path` (a `str`).

It gives back a `Adr`.

Step by step:

- Stores the result of calling `self._store.read_text(path)` in `text`.
- Stores the result of calling `text.splitlines()` in `lines`.
- Stores `_TITLE.match(lines[0])` if `lines`, otherwise `None` in `title_match`.
- Stores a new dictionary made by a loop (`{m.group(1): m.group(2) for line in lines if (m := _META.match(line))}`) in `meta`.
- Stores the result of calling `_sections(lines)` in `sections`.
- Unpacks the result of calling `_status(meta.get('Status', ''))` into `(status, superseded_by)`.
- Stores the result of calling `_adr_number(meta.get('Supersedes', ''))` in `supersedes`.
- Stores the result of calling `_fields(sections.get('Consequences', []), ('Good', 'Bad', 'Revisit when'))` in `consequences`.
- Gives back the result of calling `Adr(path=path, number=int(title_match.group(1)) if title_match else None, title=title_mat…`.

`src/adr_toolkit/infrastructure/markdown.py` lines 90 to 108:

```python
    def read_audiences(self, path: str) -> AudienceVersions:
        """Parse the audience file: the first two headings are Engineers and Manager, any other is the sibling team."""
        text = self._store.read_text(path)
        lines = text.splitlines()
        sections = _sections(lines)
        first = lines[0] if lines else ""
        number = re.search(r"ADR (\d+)", first)
        engineers = _paragraph(sections.get("Engineers", []))
        manager = _paragraph(sections.get("Manager", []))
        others = [name for name in sections if name and name not in ("Engineers", "Manager")]
        sibling_name = others[0] if others else ""
        return AudienceVersions(
            path=path,
            adr_number=int(number.group(1)) if number else None,
            engineers=engineers,
            manager=manager,
            sibling=_paragraph(sections.get(sibling_name, [])) if sibling_name else "",
            sibling_name=sibling_name,
        )
```

**Method `read_audiences` of class `MarkdownRecordReader`.** Parse the audience file: the first two headings are Engineers and Manager, any other is the sibling team.

It takes: `path` (a `str`).

It gives back a `AudienceVersions`.

Step by step:

- Stores the result of calling `self._store.read_text(path)` in `text`.
- Stores the result of calling `text.splitlines()` in `lines`.
- Stores the result of calling `_sections(lines)` in `sections`.
- Stores `lines[0]` if `lines`, otherwise `''` in `first`.
- Stores the result of calling `re.search('ADR (\\d+)', first)` in `number`.
- Stores the result of calling `_paragraph(sections.get('Engineers', []))` in `engineers`.
- Stores the result of calling `_paragraph(sections.get('Manager', []))` in `manager`.
- Stores a new list made by a loop (`[name for name in sections if name and name not in ('Engineers', 'Man…`) in `others`.
- Stores `others[0]` if `others`, otherwise `''` in `sibling_name`.
- Gives back the result of calling `AudienceVersions(path=path, adr_number=int(number.group(1)) if number else None, engineer…`.

`src/adr_toolkit/infrastructure/markdown.py` lines 110 to 126:

```python
    def read_reaction(self, path: str) -> Reaction:
        """Parse a reaction log."""
        lines = self._store.read_text(path).splitlines()
        sections = _sections(lines)
        header = _fields(sections[""], ("Reader", "Reader kind", "ADR"))
        fix = _fields(sections.get("Fix", []), ("Before", "After"))
        number = re.search(r"\d+", header.get("ADR", ""))
        return Reaction(
            path=path,
            adr_number=int(number.group(0)) if number else None,
            reader=header.get("Reader", ""),
            reader_kind=header.get("Reader kind", ""),
            said_back=_paragraph([line.lstrip("> ") for line in sections.get("Said back", [])]),
            misunderstood=_paragraph(sections.get("Misunderstood", [])),
            before=fix.get("Before", "").strip('"'),
            after=fix.get("After", "").strip('"'),
        )
```

**Method `read_reaction` of class `MarkdownRecordReader`.** Parse a reaction log.

It takes: `path` (a `str`).

It gives back a `Reaction`.

Step by step:

- Stores the result of calling `self._store.read_text(path).splitlines()` in `lines`.
- Stores the result of calling `_sections(lines)` in `sections`.
- Stores the result of calling `_fields(sections[''], ('Reader', 'Reader kind', 'ADR'))` in `header`.
- Stores the result of calling `_fields(sections.get('Fix', []), ('Before', 'After'))` in `fix`.
- Stores the result of calling `re.search('\\d+', header.get('ADR', ''))` in `number`.
- Gives back the result of calling `Reaction(path=path, adr_number=int(number.group(0)) if number else None, reader=header.ge…`.

`src/adr_toolkit/infrastructure/markdown.py` lines 129 to 133:

```python
def _status(raw: str) -> tuple[str, int | None]:
    match = _SUPERSEDED_BY.match(raw)
    if match:
        return "Superseded", int(match.group(1))
    return raw, None
```

**Function `_status`.**

It takes: `raw` (a `str`).

It gives back a `tuple[str, int | None]`.

Step by step:

- Stores the result of calling `_SUPERSEDED_BY.match(raw)` in `match`.
- If `match`:
  - Gives back the tuple `('Superseded', int(match.group(1)))`.
- Gives back the tuple `(raw, None)`.

`src/adr_toolkit/infrastructure/markdown.py` lines 136 to 138:

```python
def _adr_number(raw: str) -> int | None:
    match = _ADR_REF.match(raw)
    return int(match.group(1)) if match else None
```

**Function `_adr_number`.**

It takes: `raw` (a `str`).

It gives back a `int | None`.

Step by step:

- Stores the result of calling `_ADR_REF.match(raw)` in `match`.
- Gives back `int(match.group(1))` if `match`, otherwise `None`.

`src/adr_toolkit/infrastructure/markdown.py` lines 141 to 168:

```python
def _options(lines: list[str]) -> tuple[Option, ...]:
    options: list[Option] = []
    block_name: str | None = None
    block: list[str] = []

    def flush() -> None:
        if block_name is None:
            return
        fields = _fields(block, ("Advantage", "Main cost", "Pick it if"))
        name_match = _OPTION_NAME.match(block_name)
        options.append(
            Option(
                name=name_match.group(1) if name_match else block_name,
                advantage=fields.get("Advantage", ""),
                main_cost=fields.get("Main cost", ""),
                pick_if=fields.get("Pick it if", ""),
            )
        )

    for line in lines:
        heading = _HEADING3.match(line)
        if heading:
            flush()
            block_name, block = heading.group(1), []
        elif block_name is not None:
            block.append(line)
    flush()
    return tuple(options)
```

**Function `_options`.**

It takes: `lines` (a `list[str]`).

It gives back a `tuple[Option, ...]`.

Step by step:

- Declares `options` as a `list[Option]` and stores the list `[]` in it.
- Declares `block_name` as a `str | None` and stores nothing (`None`) in it.
- Declares `block` as a `list[str]` and stores the list `[]` in it.
- Defines a helper function `flush()`.
  - If `block_name` is the same object as `None`:
    - Ends the function and gives back nothing.
  - Stores the result of calling `_fields(block, ('Advantage', 'Main cost', 'Pick it if'))` in `fields`.
  - Stores the result of calling `_OPTION_NAME.match(block_name)` in `name_match`.
  - Calls `options.append(Option(name=name_match.group(1) if name_match else block_name, advantage=fields.get('Advantage…`.
- For each `line` in `lines`:
  - Stores the result of calling `_HEADING3.match(line)` in `heading`.
  - If `heading`:
    - Calls `flush()`.
    - Unpacks the tuple `(heading.group(1), [])` into `(block_name, block)`.
  - Otherwise, if `block_name` is not the same object as `None`:
    - Calls `block.append(line)`.
- Calls `flush()`.
- Gives back the result of calling `tuple(options)`.

### `src/adr_toolkit/infrastructure/settings.py`

`src/adr_toolkit/infrastructure/settings.py` lines 1 to 10:

```python
"""Settings from the environment, validated once at start-up (twelve-factor)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from adr_toolkit.application.check_documents import CheckSettings
from adr_toolkit.domain.adr import AdrLimits
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** Settings from the environment, validated once at start-up (twelve-factor).

Imports:

- From `__future__` it takes `annotations`.
- From `collections.abc` it takes `Mapping`.
- From `dataclasses` it takes `dataclass`.
- From `pathlib` it takes `Path`.
- From `adr_toolkit.application.check_documents` it takes `CheckSettings`.
- From `adr_toolkit.domain.adr` it takes `AdrLimits`.

`src/adr_toolkit/infrastructure/settings.py` lines 13 to 14:

```python
class SettingsError(ValueError):
    """An environment variable holds a value the program cannot use."""
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A class that inherits from `Exception` is a new kind of **error**. `raise` stops the current function with it, and a `try ... except` further up decides what to do.

**Class `SettingsError`**, a kind of `ValueError`. An environment variable holds a value the program cannot use.

`src/adr_toolkit/infrastructure/settings.py` lines 17 to 23:

```python
@dataclass(frozen=True)
class Settings:
    """Where the documents are, where the report goes, and the page limits."""

    root: Path
    report_dir: str
    check: CheckSettings
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `Settings`**. Where the documents are, where the report goes, and the page limits. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `root`: a `Path`.
- Field `report_dir`: a `str`.
- Field `check`: a `CheckSettings`.

`src/adr_toolkit/infrastructure/settings.py` lines 26 to 34:

```python
def _positive_int(env: Mapping[str, str], name: str, default: int) -> int:
    raw = env.get(name, str(default))
    try:
        value = int(raw)
    except ValueError:
        raise SettingsError(f"{name} must be a whole number, got {raw!r}") from None
    if value <= 0:
        raise SettingsError(f"{name} must be positive, got {value}")
    return value
```

> **In plain words.** A **`try` / `except` block** runs the steps under `try`. If an error of the named kind happens, Python jumps to the matching `except` steps instead of stopping the program. `finally` steps always run.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** `raise Error(...)` stops the current function by signalling an error. `raise ... from None` hides the earlier error, so the user sees only the new, clearer message.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `_positive_int`.**

It takes: `env` (a `Mapping[str, str]`); `name` (a `str`); `default` (a `int`).

It gives back a `int`.

Step by step:

- Stores the result of calling `env.get(name, str(default))` in `raw`.
- Tries:
  - Stores the result of calling `int(raw)` in `value`.
- If `ValueError` happens:
  - Stops here by raising `SettingsError(f'{name} must be a whole number, got {raw!r}')` (`from None` hides the earlier error).
- If `value` is at most `0`:
  - Stops here by raising `SettingsError(f'{name} must be positive, got {value}')`.
- Gives back `value`.

`src/adr_toolkit/infrastructure/settings.py` lines 37 to 54:

```python
def load_settings(env: Mapping[str, str]) -> Settings:
    """Read ADR_ROOT, REPORT_DIR, ADR_MAX_LINES, ADR_MAX_WORDS and ADR_REQUIRED_COMMUNICATION."""
    required_raw = env.get("ADR_REQUIRED_COMMUNICATION", "")
    try:
        required = tuple(int(part) for part in required_raw.split(",") if part.strip())
    except ValueError:
        raise SettingsError(
            f"ADR_REQUIRED_COMMUNICATION must be comma-separated numbers, got {required_raw!r}"
        ) from None
    limits = AdrLimits(
        max_lines=_positive_int(env, "ADR_MAX_LINES", 70),
        max_words=_positive_int(env, "ADR_MAX_WORDS", 600),
    )
    return Settings(
        root=Path(env.get("ADR_ROOT", ".")),
        report_dir=env.get("REPORT_DIR", "build"),
        check=CheckSettings(limits=limits, required_adrs=required),
    )
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Function `load_settings`.** Read ADR_ROOT, REPORT_DIR, ADR_MAX_LINES, ADR_MAX_WORDS and ADR_REQUIRED_COMMUNICATION.

It takes: `env` (a `Mapping[str, str]`).

It gives back a `Settings`.

Step by step:

- Stores the result of calling `env.get('ADR_REQUIRED_COMMUNICATION', '')` in `required_raw`.
- Tries:
  - Stores the result of calling `tuple((int(part) for part in required_raw.split(',') if part.strip()))` in `required`.
- If `ValueError` happens:
  - Stops here by raising `SettingsError(f'ADR_REQUIRED_COMMUNICATION must be comma-separated numbers, got {required_raw!r}')` (`from None` hides the earlier error).
- Stores the result of calling `AdrLimits(max_lines=_positive_int(env, 'ADR_MAX_LINES', 70), max_words=_positive_int(env,…` in `limits`.
- Gives back the result of calling `Settings(root=Path(env.get('ADR_ROOT', '.')), report_dir=env.get('REPORT_DIR', 'build'), …`.

## Try it yourself

```bash
.venv/bin/python -c "import adr_toolkit.infrastructure.filesystem; print(adr_toolkit.infrastructure.filesystem.__doc__)"
```
Prints the module's description: `The document store on the local file system.`

```bash
.venv/bin/python -c "import adr_toolkit.infrastructure.markdown; print(adr_toolkit.infrastructure.markdown.__doc__)"
```
Prints the module's description: `Parse the Markdown of each document type into the domain's values.`

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check src/adr_toolkit/infrastructure/__init__.py src/adr_toolkit/infrastructure/filesystem.py src/adr_toolkit/infrastructure/markdown.py src/adr_toolkit/infrastructure/settings.py
```
Prints `All checks passed!`.

```bash
grep -c "^def \|^class \|    def " src/adr_toolkit/infrastructure/filesystem.py
```
Counts the functions, methods and classes in `src/adr_toolkit/infrastructure/filesystem.py`.

## Mistakes people make

- Putting a business rule in an adapter, where the domain tests cannot see it.
- Forgetting to close a connection or file. The adapters use `with` blocks and context managers.
- Trusting input from outside. Adapters check paths, shapes and ranges before handing values inward.

## Check yourself

1. What is `FileSystemStore` for?
   **Answer:** Reads the repository's documents under one root. Paths are relative and may not leave the root.
2. What is `_sections` for?
   **Answer:** Group lines under their `##` heading, in file order. Lines before the first heading go under ''.
3. What is `_fields` for?
   **Answer:** `Label: text` fields whose text may continue on the following lines until the next label.
4. What is `MarkdownRecordReader` for?
   **Answer:** Reads the repository's three document types from a store.
5. What is `SettingsError` for?
   **Answer:** An environment variable holds a value the program cannot use.

## Further reading

- Python 3.12 tutorial, classes: <https://docs.python.org/3.12/tutorial/classes.html>
- Python 3.12 language reference: <https://docs.python.org/3.12/reference/>
- Type hints: <https://docs.python.org/3.12/library/typing.html>
