# Domain layer code

## What it is

The rules and values: plain Python that decides things and never touches a file, a network or a database. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

This is where the repository's domain work happens. Reading it file by file, with every line explained, is how a reader sees the work that was done.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/__init__.py` | 2 lines. Lints architecture decision records and the documents that carry them to their readers. |
| `src/adr_toolkit/domain/__init__.py` | 1 lines. Pure rules over parsed documents. Depends on the standard library only. |
| `src/adr_toolkit/domain/adr.py` | 179 lines. The architecture decision record as a value, and the rules a record must satisfy. |
| `src/adr_toolkit/domain/audiences.py` | 111 lines. The same decision told three ways, and the rules that keep each version for its reader. |
| `src/adr_toolkit/domain/decision_log.py` | 79 lines. The links between records: which one superseded which, and the log that shows it. |
| `src/adr_toolkit/domain/findings.py` | 38 lines. The result of a rule: a finding with a code, a severity and the document it is about. |
| `src/adr_toolkit/domain/reaction.py` | 61 lines. The reaction log: what a reader got wrong, and the proof the record changed because of it. |
| `src/adr_toolkit/domain/text.py` | 24 lines. Small text helpers shared by the rules. |

## How it works underneath

The domain layer is the centre of the design. Because it imports nothing from the outer layers, every rule can be tested with plain values, fast, without setting anything up. import-linter fails the build if a domain file imports an outer layer.

## Walkthrough of this repository's use

### `src/adr_toolkit/__init__.py`

`src/adr_toolkit/__init__.py` lines 1 to 1:

```python
"""Lints architecture decision records and the documents that carry them to their readers."""
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.

**Module description.** Lints architecture decision records and the documents that carry them to their readers.

`src/adr_toolkit/__init__.py` lines 3 to 3:

```python
__version__ = "0.1.0"
```

These module-level lines:

- Stores the text `'0.1.0'` in `__version__`.

### `src/adr_toolkit/domain/__init__.py`

`src/adr_toolkit/domain/__init__.py` lines 1 to 1:

```python
"""Pure rules over parsed documents. Depends on the standard library only."""
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.

**Module description.** Pure rules over parsed documents. Depends on the standard library only.

### `src/adr_toolkit/domain/adr.py`

`src/adr_toolkit/domain/adr.py` lines 1 to 10:

```python
"""The architecture decision record as a value, and the rules a record must satisfy."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from adr_toolkit.domain.findings import Finding, error, warning
from adr_toolkit.domain.text import has_figure, squash, words
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The architecture decision record as a value, and the rules a record must satisfy.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `re`.
- From `dataclasses` it takes `dataclass`.
- From `datetime` it takes `date`.
- From `adr_toolkit.domain.findings` it takes `Finding, error, warning`.
- From `adr_toolkit.domain.text` it takes `has_figure, squash, words`.

`src/adr_toolkit/domain/adr.py` lines 12 to 23:

```python
REQUIRED_SECTIONS = ("Context", "Options considered", "Decision", "Consequences")
STATUSES = ("Proposed", "Accepted", "Superseded")
VAGUE_TRIGGERS = (
    "if it stops working",
    "if needed",
    "when appropriate",
    "if there are problems",
    "if problems",
    "later",
)
DECISION_LANGUAGE = ("we will", "we should", "so we need", "we need to", "we must")
STOP_WORDS = frozenset({"with", "that", "this", "from", "into", "than", "then", "have", "will", "make", "keep"})
```

> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the tuple `('Context', 'Options considered', 'Decision', 'Consequences')` in `REQUIRED_SECTIONS`.
- Stores the tuple `('Proposed', 'Accepted', 'Superseded')` in `STATUSES`.
- Stores the tuple `('if it stops working', 'if needed', 'when appropriate', 'if there ar…` in `VAGUE_TRIGGERS`.
- Stores the tuple `('we will', 'we should', 'so we need', 'we need to', 'we must')` in `DECISION_LANGUAGE`.
- Stores the result of calling `frozenset({'with', 'that', 'this', 'from', 'into', 'than', 'then', 'have', 'will', 'make'…` in `STOP_WORDS`.

`src/adr_toolkit/domain/adr.py` lines 26 to 33:

```python
@dataclass(frozen=True)
class Option:
    """One option, described by the same three lines for every option."""

    name: str
    advantage: str
    main_cost: str
    pick_if: str
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `Option`**. One option, described by the same three lines for every option. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `name`: a `str`.
- Field `advantage`: a `str`.
- Field `main_cost`: a `str`.
- Field `pick_if`: a `str`.

`src/adr_toolkit/domain/adr.py` lines 36 to 56:

```python
@dataclass(frozen=True)
class Adr:
    """A parsed decision record. Missing parts are empty strings or None, and the rules report them."""

    path: str
    number: int | None
    title: str
    status: str
    superseded_by: int | None
    supersedes: int | None
    date_text: str
    deciders: str
    sections: tuple[str, ...]
    context: str
    options: tuple[Option, ...]
    decision: str
    good: str
    bad: str
    revisit_when: str
    line_count: int
    word_count: int
```

> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** `obj[key]` looks a value up by key or position.

**Class `Adr`**. A parsed decision record. Missing parts are empty strings or None, and the rules report them. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `path`: a `str`.
- Field `number`: a `int | None`.
- Field `title`: a `str`.
- Field `status`: a `str`.
- Field `superseded_by`: a `int | None`.
- Field `supersedes`: a `int | None`.
- Field `date_text`: a `str`.
- Field `deciders`: a `str`.
- Field `sections`: a `tuple[str, ...]`.
- Field `context`: a `str`.
- Field `options`: a `tuple[Option, ...]`.
- Field `decision`: a `str`.
- Field `good`: a `str`.
- Field `bad`: a `str`.
- Field `revisit_when`: a `str`.
- Field `line_count`: a `int`.
- Field `word_count`: a `int`.

`src/adr_toolkit/domain/adr.py` lines 59 to 64:

```python
@dataclass(frozen=True)
class AdrLimits:
    """The size of one page."""

    max_lines: int = 70
    max_words: int = 600
```

**Class `AdrLimits`**. The size of one page. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `max_lines`: a `int`, default `70`.
- Field `max_words`: a `int`, default `600`.

`src/adr_toolkit/domain/adr.py` lines 67 to 84:

```python
def check_adr(adr: Adr, limits: AdrLimits | None = None) -> list[Finding]:
    """Apply every rule to one record. The codes ADR001 to ADR018 are listed in the README."""
    limits = limits or AdrLimits()
    findings: list[Finding] = []
    for rule in (_header, _sections, _options, _context, _decision, _consequences):
        findings.extend(rule(adr))
    if adr.status == "Proposed":
        findings.append(warning("ADR018", adr.path, "still Proposed: accept it or withdraw it before the work starts"))
    if adr.line_count > limits.max_lines or adr.word_count > limits.max_words:
        findings.append(
            error(
                "ADR016",
                adr.path,
                f"longer than one page: {adr.line_count} lines and {adr.word_count} words "
                f"(limit {limits.max_lines} lines and {limits.max_words} words)",
            )
        )
    return findings
```

> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `check_adr`.** Apply every rule to one record. The codes ADR001 to ADR018 are listed in the README.

It takes: `adr` (a `Adr`); `limits` (a `AdrLimits | None`), default `None`.

It gives back a `list[Finding]`.

Step by step:

- Stores whether `limits` or `AdrLimits()` in `limits`.
- Declares `findings` as a `list[Finding]` and stores the list `[]` in it.
- For each `rule` in the tuple `(_header, _sections, _options, _context, _decision, _consequences)`:
  - Calls `findings.extend(rule(adr))`.
- If `adr.status` equals `'Proposed'`:
  - Calls `findings.append(warning('ADR018', adr.path, 'still Proposed: accept it or withdraw it before the work starts'…`.
- If `adr.line_count` is more than `limits.max_lines` or `adr.word_count` is more than `limits.max_words`:
  - Calls `findings.append(error('ADR016', adr.path, f'longer than one page: {adr.line_count} lines and {adr.word_count}…`.
- Gives back `findings`.

`src/adr_toolkit/domain/adr.py` lines 87 to 105:

```python
def _header(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if adr.number is None or not adr.title:
        found.append(error("ADR001", adr.path, "the first line must read '# ADR NNNN: title'"))
    if adr.status not in STATUSES:
        found.append(
            error(
                "ADR002", adr.path, f"status must be Proposed, Accepted or Superseded by ADR NNNN, got {adr.status!r}"
            )
        )
    if adr.status == "Superseded" and adr.superseded_by is None:
        found.append(error("ADR002", adr.path, "a Superseded record must say which one: 'Superseded by ADR NNNN'"))
    try:
        date.fromisoformat(adr.date_text)
    except ValueError:
        found.append(error("ADR003", adr.path, f"date must be an ISO date (YYYY-MM-DD), got {adr.date_text!r}"))
    if not adr.deciders or re.search(r"<.*>", adr.deciders):
        found.append(error("ADR004", adr.path, "name the deciders; a placeholder is not a name"))
    return found
```

> **In plain words.** A **`try` / `except` block** runs the steps under `try`. If an error of the named kind happens, Python jumps to the matching `except` steps instead of stopping the program. `finally` steps always run.
> **In plain words.** A **regular expression** is a short pattern for text, such as `^## (.+)$` for "a line starting with ## ". `re.compile` prepares it once; `.match` tries it at the start of a string and returns a match object or `None`.

**Function `_header`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- If `adr.number` is the same object as `None` or not (`adr.title`):
  - Calls `found.append(error('ADR001', adr.path, "the first line must read '# ADR NNNN: title'"))`.
- If `adr.status` is not in `STATUSES`:
  - Calls `found.append(error('ADR002', adr.path, f'status must be Proposed, Accepted or Superseded by ADR NNNN, got {ad…`.
- If `adr.status` equals `'Superseded'` and `adr.superseded_by` is the same object as `None`:
  - Calls `found.append(error('ADR002', adr.path, "a Superseded record must say which one: 'Superseded by ADR NNNN'"))`.
- Tries:
  - Calls `date.fromisoformat(adr.date_text)`.
- If `ValueError` happens:
  - Calls `found.append(error('ADR003', adr.path, f'date must be an ISO date (YYYY-MM-DD), got {adr.date_text!r}'))`.
- If not (`adr.deciders`) or `re.search('<.*>', adr.deciders)`:
  - Calls `found.append(error('ADR004', adr.path, 'name the deciders; a placeholder is not a name'))`.
- Gives back `found`.

`src/adr_toolkit/domain/adr.py` lines 108 to 113:

```python
def _sections(adr: Adr) -> list[Finding]:
    if adr.sections == REQUIRED_SECTIONS:
        return []
    missing = [name for name in REQUIRED_SECTIONS if name not in adr.sections]
    detail = f"missing {', '.join(missing)}" if missing else "out of order"
    return [error("ADR005", adr.path, f"sections must be {' / '.join(REQUIRED_SECTIONS)}: {detail}")]
```

> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.

**Function `_sections`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- If `adr.sections` equals `REQUIRED_SECTIONS`:
  - Gives back the list `[]`.
- Stores a new list made by a loop (`[name for name in REQUIRED_SECTIONS if name not in adr.sections]`) in `missing`.
- Stores `f"missing {', '.join(missing)}"` if `missing`, otherwise `'out of order'` in `detail`.
- Gives back the list `[error('ADR005', adr.path, f"sections must be {' / '.join(REQUIRED_SE…`.

`src/adr_toolkit/domain/adr.py` lines 116 to 136:

```python
def _options(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if len(adr.options) < 2:
        found.append(error("ADR006", adr.path, f"{len(adr.options)} option(s); a real decision has at least two"))
    for option in adr.options:
        for label, text in (
            ("Advantage", option.advantage),
            ("Main cost", option.main_cost),
            ("Pick it if", option.pick_if),
        ):
            if len(words(text)) < 4:
                found.append(
                    error("ADR007", adr.path, f"option '{option.name}': '{label}' is missing or too short to be fair")
                )
    names = [squash(option.name).lower() for option in adr.options]
    advantages = [squash(option.advantage).lower() for option in adr.options]
    if len(set(names)) < len(names) or len(set(advantages)) < len(advantages):
        found.append(
            error("ADR008", adr.path, "two options share a name or an advantage: one is the same choice renamed")
        )
    return found
```

**Function `_options`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- If `len(adr.options)` is less than `2`:
  - Calls `found.append(error('ADR006', adr.path, f'{len(adr.options)} option(s); a real decision has at least two'))`.
- For each `option` in `adr.options`:
  - For each `(label, text)` in the tuple `(('Advantage', option.advantage), ('Main cost', option.main_cost), ('…`:
    - If `len(words(text))` is less than `4`:
      - Calls `found.append(error('ADR007', adr.path, f"option '{option.name}': '{label}' is missing or too short to be fair…`.
- Stores a new list made by a loop (`[squash(option.name).lower() for option in adr.options]`) in `names`.
- Stores a new list made by a loop (`[squash(option.advantage).lower() for option in adr.options]`) in `advantages`.
- If `len(set(names))` is less than `len(names)` or `len(set(advantages))` is less than `len(advantages)`:
  - Calls `found.append(error('ADR008', adr.path, 'two options share a name or an advantage: one is the same choice rena…`.
- Gives back `found`.

`src/adr_toolkit/domain/adr.py` lines 139 to 154:

```python
def _context(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if not has_figure(adr.context):
        found.append(error("ADR009", adr.path, "the context has no number: facts, not feelings"))
    lowered = squash(adr.context).lower()
    leaks = [phrase for phrase in DECISION_LANGUAGE if phrase in lowered]
    leaks += [match.group(0) for match in re.finditer(r"\boption [a-z]\b", lowered)]
    if leaks:
        found.append(
            error(
                "ADR010",
                adr.path,
                f"the context argues for an answer ({', '.join(leaks)}); that belongs in the decision",
            )
        )
    return found
```

**Function `_context`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- If not (`has_figure(adr.context)`):
  - Calls `found.append(error('ADR009', adr.path, 'the context has no number: facts, not feelings'))`.
- Stores the result of calling `squash(adr.context).lower()` in `lowered`.
- Stores a new list made by a loop (`[phrase for phrase in DECISION_LANGUAGE if phrase in lowered]`) in `leaks`.
- Adds a new list made by a loop (`[match.group(0) for match in re.finditer('\\boption [a-z]\\b', lowere…`) to `leaks`.
- If `leaks`:
  - Calls `found.append(error('ADR010', adr.path, f"the context argues for an answer ({', '.join(leaks)}); that belongs …`.
- Gives back `found`.

`src/adr_toolkit/domain/adr.py` lines 157 to 183:

```python
def _decision(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    text = squash(adr.decision)
    if not re.match(r"We will .+ because .+", text):
        found.append(
            error("ADR011", adr.path, "the decision must read 'We will <choice>, because <the deciding reason>.'")
        )
        return found
    if text.lower().count("because") > 1:
        found.append(
            error(
                "ADR012",
                adr.path,
                "more than one 'because': if two reasons are needed, the real reason is still hiding",
            )
        )
    choice = {word for word in words(text.split(" because ")[0]) if len(word) >= 4 and word not in STOP_WORDS}
    shared = [
        option.name
        for option in adr.options
        if len({word for word in words(option.name) if len(word) >= 4 and word not in STOP_WORDS} & choice) >= 2
    ]
    if adr.options and not shared:
        found.append(
            error("ADR017", adr.path, "the decision does not name any option considered; say which one was chosen")
        )
    return found
```

> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.
> **In plain words.** On sets, `a | b` is the union (everything in either) and `a & b` the intersection (what both have).

**Function `_decision`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores the result of calling `squash(adr.decision)` in `text`.
- If not (`re.match('We will .+ because .+', text)`):
  - Calls `found.append(error('ADR011', adr.path, "the decision must read 'We will <choice>, because <the deciding reaso…`.
  - Gives back `found`.
- If `text.lower().count('because')` is more than `1`:
  - Calls `found.append(error('ADR012', adr.path, "more than one 'because': if two reasons are needed, the real reason i…`.
- Stores a new set made by a loop (`{word for word in words(text.split(' because ')[0]) if len(word) >= 4…`) in `choice`.
- Stores a new list made by a loop (`[option.name for option in adr.options if len({word for word in words…`) in `shared`.
- If `adr.options` and not (`shared`):
  - Calls `found.append(error('ADR017', adr.path, 'the decision does not name any option considered; say which one was c…`.
- Gives back `found`.

`src/adr_toolkit/domain/adr.py` lines 186 to 206:

```python
def _consequences(adr: Adr) -> list[Finding]:
    found: list[Finding] = []
    if not adr.good:
        found.append(error("ADR013", adr.path, "the consequences list no good result"))
    if not adr.bad:
        found.append(
            error("ADR013", adr.path, "the consequences list no bad result: the record then reads as advertising")
        )
    if not adr.revisit_when:
        found.append(error("ADR014", adr.path, "no 'Revisit when:' trigger"))
    else:
        lowered = adr.revisit_when.lower()
        if not has_figure(lowered) or any(vague in lowered for vague in VAGUE_TRIGGERS):
            found.append(
                error(
                    "ADR015",
                    adr.path,
                    f"the revisit trigger must be observable (a number, a date or an event): {adr.revisit_when!r}",
                )
            )
    return found
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Function `_consequences`.**

It takes: `adr` (a `Adr`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- If not (`adr.good`):
  - Calls `found.append(error('ADR013', adr.path, 'the consequences list no good result'))`.
- If not (`adr.bad`):
  - Calls `found.append(error('ADR013', adr.path, 'the consequences list no bad result: the record then reads as adverti…`.
- If not (`adr.revisit_when`):
  - Calls `found.append(error('ADR014', adr.path, "no 'Revisit when:' trigger"))`.
- Otherwise:
  - Stores the result of calling `adr.revisit_when.lower()` in `lowered`.
  - If not (`has_figure(lowered)`) or `any((vague in lowered for vague in VAGUE_TRIGGERS))`:
    - Calls `found.append(error('ADR015', adr.path, f'the revisit trigger must be observable (a number, a date or an event…`.
- Gives back `found`.

### `src/adr_toolkit/domain/audiences.py`

`src/adr_toolkit/domain/audiences.py` lines 1 to 10:

```python
"""The same decision told three ways, and the rules that keep each version for its reader."""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import combinations

from adr_toolkit.domain.findings import Finding, error
from adr_toolkit.domain.text import has_figure, sentences, similarity, words
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The same decision told three ways, and the rules that keep each version for its reader.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `re`.
- From `dataclasses` it takes `dataclass`.
- From `itertools` it takes `combinations`.
- From `adr_toolkit.domain.findings` it takes `Finding, error`.
- From `adr_toolkit.domain.text` it takes `has_figure, sentences, similarity, words`.

`src/adr_toolkit/domain/audiences.py` lines 12 to 24:

```python
MANAGER_JARGON = frozenset(
    {
        *("outbox", "relay", "idempotent", "idempotency", "broker", "kafka", "rabbitmq", "partition"),
        *("offset", "transaction", "consumer", "consumers", "publish", "publishes", "schema", "payload"),
        *("table", "index", "replica"),
    }
)
SIBLING_JARGON = frozenset(("outbox", "relay", "idempotent", "idempotency", "transaction", "broker"))
SIBLING_ACTIONS = frozenset(
    ("subscribe", "read", "stop", "switch", "migrate", "use", "update", "change", "move", "call", "send", "replace")
)
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_PATTERN = re.compile(rf"\b\d{{1,2}} (?:{_MONTHS})\b|\b\d{{4}}-\d{{2}}-\d{{2}}\b")
```

> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.
> **In plain words.** `*items` **unpacks** a sequence into separate values; `**options` does the same for a dictionary's keys and values.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** A **regular expression** is a short pattern for text, such as `^## (.+)$` for "a line starting with ## ". `re.compile` prepares it once; `.match` tries it at the start of a string and returns a match object or `None`.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the result of calling `frozenset({*('outbox', 'relay', 'idempotent', 'idempotency', 'broker', 'kafka', 'rabbitmq…` in `MANAGER_JARGON`.
- Stores the result of calling `frozenset(('outbox', 'relay', 'idempotent', 'idempotency', 'transaction', 'broker'))` in `SIBLING_JARGON`.
- Stores the result of calling `frozenset(('subscribe', 'read', 'stop', 'switch', 'migrate', 'use', 'update', 'change', '…` in `SIBLING_ACTIONS`.
- Stores the text `'January|February|March|April|May|June|July|August|Septembe…` in `_MONTHS`.
- Stores the result of calling `re.compile(f'\\b\\d{{1,2}} (?:{_MONTHS})\\b|\\b\\d{{4}}-\\d{{2}}-\\d{{2}}\\b')` in `DATE_PATTERN`.

`src/adr_toolkit/domain/audiences.py` lines 27 to 36:

```python
@dataclass(frozen=True)
class AudienceVersions:
    """The three short versions of one decision, keyed to the record they tell."""

    path: str
    adr_number: int | None
    engineers: str
    manager: str
    sibling: str
    sibling_name: str
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `AudienceVersions`**. The three short versions of one decision, keyed to the record they tell. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `path`: a `str`.
- Field `adr_number`: a `int | None`.
- Field `engineers`: a `str`.
- Field `manager`: a `str`.
- Field `sibling`: a `str`.
- Field `sibling_name`: a `str`.

`src/adr_toolkit/domain/audiences.py` lines 39 to 55:

```python
def check_audiences(versions: AudienceVersions, decision: str) -> list[Finding]:
    """Apply AUD001 to AUD009. The decision text is the record's, so the engineer version can be tied to it."""
    found: list[Finding] = []
    for label, text in (
        ("engineers", versions.engineers),
        ("manager", versions.manager),
        ("sibling team", versions.sibling),
    ):
        if not sentences(text):
            found.append(error("AUD001", versions.path, f"the {label} version is missing"))
    if found:
        return found
    found += _engineers(versions, decision)
    found += _manager(versions)
    found += _sibling(versions)
    found += _no_copying(versions)
    return found
```

> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.

**Function `check_audiences`.** Apply AUD001 to AUD009. The decision text is the record's, so the engineer version can be tied to it.

It takes: `versions` (a `AudienceVersions`); `decision` (a `str`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- For each `(label, text)` in the tuple `(('engineers', versions.engineers), ('manager', versions.manager), ('…`:
  - If not (`sentences(text)`):
    - Calls `found.append(error('AUD001', versions.path, f'the {label} version is missing'))`.
- If `found`:
  - Gives back `found`.
- Adds the result of calling `_engineers(versions, decision)` to `found`.
- Adds the result of calling `_manager(versions)` to `found`.
- Adds the result of calling `_sibling(versions)` to `found`.
- Adds the result of calling `_no_copying(versions)` to `found`.
- Gives back `found`.

`src/adr_toolkit/domain/audiences.py` lines 58 to 70:

```python
def _engineers(versions: AudienceVersions, decision: str) -> list[Finding]:
    found: list[Finding] = []
    count = len(sentences(versions.engineers))
    if not 3 <= count <= 8:
        found.append(
            error("AUD002", versions.path, f"engineers get the mechanism in about five sentences, not {count}")
        )
    wanted = {word for word in words(decision.split(" because ")[0]) if len(word) >= 5}
    if len(wanted & set(words(versions.engineers))) < 2:
        found.append(
            error("AUD003", versions.path, "the engineer version does not describe the mechanism the decision chose")
        )
    return found
```

> **In plain words.** A **set comprehension** `{x for ...}` builds a set (a collection with no duplicates) with a loop.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** On sets, `a | b` is the union (everything in either) and `a & b` the intersection (what both have).

**Function `_engineers`.**

It takes: `versions` (a `AudienceVersions`); `decision` (a `str`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores the result of calling `len(sentences(versions.engineers))` in `count`.
- If not (`3` is at most `count` is at most `8`):
  - Calls `found.append(error('AUD002', versions.path, f'engineers get the mechanism in about five sentences, not {count…`.
- Stores a new set made by a loop (`{word for word in words(decision.split(' because ')[0]) if len(word) …`) in `wanted`.
- If `len(wanted & set(words(versions.engineers)))` is less than `2`:
  - Calls `found.append(error('AUD003', versions.path, 'the engineer version does not describe the mechanism the decisio…`.
- Gives back `found`.

`src/adr_toolkit/domain/audiences.py` lines 73 to 91:

```python
def _manager(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    parts = sentences(versions.manager)
    if len(parts) > 2:
        found.append(
            error("AUD004", versions.path, f"the manager version is {len(parts)} sentences; two, with a number in each")
        )
    if not all(has_figure(part) for part in parts):
        found.append(
            error(
                "AUD005",
                versions.path,
                "every manager sentence carries a number: the first question is cost, risk or time",
            )
        )
    jargon = sorted(MANAGER_JARGON & set(words(versions.manager)))
    if jargon:
        found.append(error("AUD006", versions.path, f"jargon in the manager version: {', '.join(jargon)}"))
    return found
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Function `_manager`.**

It takes: `versions` (a `AudienceVersions`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores the result of calling `sentences(versions.manager)` in `parts`.
- If `len(parts)` is more than `2`:
  - Calls `found.append(error('AUD004', versions.path, f'the manager version is {len(parts)} sentences; two, with a numb…`.
- If not (`all((has_figure(part) for part in parts))`):
  - Calls `found.append(error('AUD005', versions.path, 'every manager sentence carries a number: the first question is c…`.
- Stores the result of calling `sorted(MANAGER_JARGON & set(words(versions.manager)))` in `jargon`.
- If `jargon`:
  - Calls `found.append(error('AUD006', versions.path, f"jargon in the manager version: {', '.join(jargon)}"))`.
- Gives back `found`.

`src/adr_toolkit/domain/audiences.py` lines 94 to 112:

```python
def _sibling(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    first = sentences(versions.sibling)[0]
    if not DATE_PATTERN.search(first):
        found.append(
            error("AUD007", versions.path, "the sibling team's first question is when: the first sentence needs a date")
        )
    if not SIBLING_ACTIONS & set(words(versions.sibling)):
        found.append(error("AUD007", versions.path, "the sibling note names no action (subscribe, read, switch, ...)"))
    jargon = sorted(SIBLING_JARGON & set(words(versions.sibling)))
    if jargon:
        found.append(error("AUD006", versions.path, f"internal jargon in the sibling note: {', '.join(jargon)}"))
    if len(sentences(versions.sibling)) < 2:
        found.append(
            error(
                "AUD007", versions.path, "the sibling note is too thin to tell the team what changes for them and when"
            )
        )
    return found
```

**Function `_sibling`.**

It takes: `versions` (a `AudienceVersions`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores `sentences(versions.sibling)[0]` in `first`.
- If not (`DATE_PATTERN.search(first)`):
  - Calls `found.append(error('AUD007', versions.path, "the sibling team's first question is when: the first sentence ne…`.
- If not (`SIBLING_ACTIONS & set(words(versions.sibling))`):
  - Calls `found.append(error('AUD007', versions.path, 'the sibling note names no action (subscribe, read, switch, ...)'…`.
- Stores the result of calling `sorted(SIBLING_JARGON & set(words(versions.sibling)))` in `jargon`.
- If `jargon`:
  - Calls `found.append(error('AUD006', versions.path, f"internal jargon in the sibling note: {', '.join(jargon)}"))`.
- If `len(sentences(versions.sibling))` is less than `2`:
  - Calls `found.append(error('AUD007', versions.path, 'the sibling note is too thin to tell the team what changes for t…`.
- Gives back `found`.

`src/adr_toolkit/domain/audiences.py` lines 115 to 128:

```python
def _no_copying(versions: AudienceVersions) -> list[Finding]:
    found: list[Finding] = []
    texts = {"engineers": versions.engineers, "manager": versions.manager, "sibling team": versions.sibling}
    for (left_name, left), (right_name, right) in combinations(texts.items(), 2):
        shared = set(sentences(left)) & set(sentences(right))
        if shared or similarity(left, right) > 0.6:
            found.append(
                error(
                    "AUD008",
                    versions.path,
                    f"the {left_name} and {right_name} versions repeat each other; none answers its own reader",
                )
            )
    return found
```

> **In plain words.** A **dictionary** `{key: value}` maps keys to values.

**Function `_no_copying`.**

It takes: `versions` (a `AudienceVersions`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- Stores the dictionary `{'engineers': versions.engineers, 'manager': versions.manager, 'sibli…` in `texts`.
- For each `((left_name, left), (right_name, right))` in the result of calling `combinations(texts.items(), 2)`:
  - Stores `set(sentences(left)) & set(sentences(right))` in `shared`.
  - If `shared` or `similarity(left, right)` is more than `0.6`:
    - Calls `found.append(error('AUD008', versions.path, f'the {left_name} and {right_name} versions repeat each other; no…`.
- Gives back `found`.

### `src/adr_toolkit/domain/decision_log.py`

`src/adr_toolkit/domain/decision_log.py` lines 1 to 8:

```python
"""The links between records: which one superseded which, and the log that shows it."""

from __future__ import annotations

from collections import Counter

from adr_toolkit.domain.adr import Adr
from adr_toolkit.domain.findings import Finding, error
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The links between records: which one superseded which, and the log that shows it.

Imports:

- From `__future__` it takes `annotations`.
- From `collections` it takes `Counter`.
- From `adr_toolkit.domain.adr` it takes `Adr`.
- From `adr_toolkit.domain.findings` it takes `Finding, error`.

`src/adr_toolkit/domain/decision_log.py` lines 11 to 48:

```python
def check_links(records: list[Adr]) -> list[Finding]:
    """Supersession must point at a real record, and the record it replaces must point back."""
    findings: list[Finding] = []
    by_number = {record.number: record for record in records if record.number is not None}
    for number, count in Counter(record.number for record in records if record.number is not None).items():
        if count > 1:
            findings.append(error("ADR100", f"ADR {number:04d}", f"{count} records share the number {number:04d}"))
    for record in records:
        if record.superseded_by is not None:
            successor = by_number.get(record.superseded_by)
            if successor is None:
                findings.append(
                    error("ADR101", record.path, f"superseded by ADR {record.superseded_by:04d}, which does not exist")
                )
            elif successor.supersedes != record.number:
                findings.append(
                    error(
                        "ADR102",
                        successor.path,
                        f"ADR {record.number:04d} was replaced by this record, "
                        f"which lacks 'Supersedes: ADR {record.number:04d}'",
                    )
                )
        if record.supersedes is not None:
            predecessor = by_number.get(record.supersedes)
            if predecessor is None:
                findings.append(
                    error("ADR101", record.path, f"supersedes ADR {record.supersedes:04d}, which does not exist")
                )
            elif predecessor.superseded_by != record.number:
                findings.append(
                    error(
                        "ADR103",
                        predecessor.path,
                        f"replaced by ADR {record.number:04d} but its status does not say so",
                    )
                )
    return findings
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **dictionary comprehension** `{k: v for ...}` builds a dictionary with a loop written inside braces.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `check_links`.** Supersession must point at a real record, and the record it replaces must point back.

It takes: `records` (a `list[Adr]`).

It gives back a `list[Finding]`.

Step by step:

- Declares `findings` as a `list[Finding]` and stores the list `[]` in it.
- Stores a new dictionary made by a loop (`{record.number: record for record in records if record.number is not …`) in `by_number`.
- For each `(number, count)` in the result of calling `Counter((record.number for record in records if record.number is not None)).items()`:
  - If `count` is more than `1`:
    - Calls `findings.append(error('ADR100', f'ADR {number:04d}', f'{count} records share the number {number:04d}'))`.
- For each `record` in `records`:
  - If `record.superseded_by` is not the same object as `None`:
    - Stores the result of calling `by_number.get(record.superseded_by)` in `successor`.
    - If `successor` is the same object as `None`:
      - Calls `findings.append(error('ADR101', record.path, f'superseded by ADR {record.superseded_by:04d}, which does not e…`.
    - Otherwise, if `successor.supersedes` is different from `record.number`:
      - Calls `findings.append(error('ADR102', successor.path, f"ADR {record.number:04d} was replaced by this record, which …`.
  - If `record.supersedes` is not the same object as `None`:
    - Stores the result of calling `by_number.get(record.supersedes)` in `predecessor`.
    - If `predecessor` is the same object as `None`:
      - Calls `findings.append(error('ADR101', record.path, f'supersedes ADR {record.supersedes:04d}, which does not exist'))`.
    - Otherwise, if `predecessor.superseded_by` is different from `record.number`:
      - Calls `findings.append(error('ADR103', predecessor.path, f'replaced by ADR {record.number:04d} but its status does n…`.
- Gives back `findings`.

`src/adr_toolkit/domain/decision_log.py` lines 51 to 71:

```python
def render_log(records: list[Adr]) -> str:
    """The decision log as Markdown: one row per record, oldest first, with what replaced what."""
    rows = ["| ADR | Title | Status | Date | Replaces | Replaced by |", "| --- | --- | --- | --- | --- | --- |"]
    for record in sorted(records, key=lambda item: item.number or 0):
        rows.append(
            "| {num} | [{title}]({path}) | {status} | {date} | {replaces} | {replaced} |".format(
                num=f"{record.number:04d}" if record.number is not None else "?",
                title=record.title,
                path=record.path.removeprefix("docs/"),
                status=record.status,
                date=record.date_text,
                replaces=f"{record.supersedes:04d}" if record.supersedes is not None else "",
                replaced=f"{record.superseded_by:04d}" if record.superseded_by is not None else "",
            )
        )
    chains = _chains(records)
    lines = ["# Decision log", "", "Generated by `adr-toolkit log --write`; do not edit by hand.", "", *rows]
    if chains:
        lines += ["", "## Supersession chains", ""]
        lines += [f"- {chain}" for chain in chains]
    return "\n".join(lines) + "\n"
```

> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** `*items` **unpacks** a sequence into separate values; `**options` does the same for a dictionary's keys and values.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** A **lambda** is a small function written in one line: `lambda x: x + 1`.
> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.

**Function `render_log`.** The decision log as Markdown: one row per record, oldest first, with what replaced what.

It takes: `records` (a `list[Adr]`).

It gives back a `str`.

Step by step:

- Stores the list `['| ADR | Title | Status | Date | Replaces | Replaced by |', '| --- |…` in `rows`.
- For each `record` in the result of calling `sorted(records, key=lambda item: item.number or 0)`:
  - Calls `rows.append('| {num} | [{title}]({path}) | {status} | {date} | {replaces} | {replaced} |'.format(num=f'{recor…`.
- Stores the result of calling `_chains(records)` in `chains`.
- Stores the list `['# Decision log', '', 'Generated by `adr-toolkit log --write`; do no…` in `lines`.
- If `chains`:
  - Adds the list `['', '## Supersession chains', '']` to `lines`.
  - Adds a new list made by a loop (`[f'- {chain}' for chain in chains]`) to `lines`.
- Gives back `'\n'.join(lines) + '\n'`.

`src/adr_toolkit/domain/decision_log.py` lines 74 to 88:

```python
def _chains(records: list[Adr]) -> list[str]:
    by_number = {record.number: record for record in records if record.number is not None}
    chains: list[str] = []
    for record in sorted(records, key=lambda item: item.number or 0):
        if record.supersedes is None or record.number is None:
            continue
        trail = [record.number]
        cursor = by_number.get(record.supersedes)
        seen = {record.number}
        while cursor is not None and cursor.number is not None and cursor.number not in seen:
            trail.append(cursor.number)
            seen.add(cursor.number)
            cursor = by_number.get(cursor.supersedes) if cursor.supersedes is not None else None
        chains.append(" supersedes ".join(f"ADR {number:04d}" for number in trail))
    return chains
```

> **In plain words.** A **`while` loop** repeats its steps as long as its condition stays true.
> **In plain words.** A **set** `{a, b}` holds items without duplicates; `frozenset` is a set that cannot be changed.

**Function `_chains`.**

It takes: `records` (a `list[Adr]`).

It gives back a `list[str]`.

Step by step:

- Stores a new dictionary made by a loop (`{record.number: record for record in records if record.number is not …`) in `by_number`.
- Declares `chains` as a `list[str]` and stores the list `[]` in it.
- For each `record` in the result of calling `sorted(records, key=lambda item: item.number or 0)`:
  - If `record.supersedes` is the same object as `None` or `record.number` is the same object as `None`:
    - Skips to the next item (`continue`).
  - Stores the list `[record.number]` in `trail`.
  - Stores the result of calling `by_number.get(record.supersedes)` in `cursor`.
  - Stores `{record.number}` in `seen`.
  - While `cursor` is not the same object as `None` and `cursor.number` is not the same object as `None` and `cursor.number` is not in `seen`:
    - Calls `trail.append(cursor.number)`.
    - Calls `seen.add(cursor.number)`.
    - Stores `by_number.get(cursor.supersedes)` if `cursor.supersedes` is not the same object as `None`, otherwise `None` in `cursor`.
  - Calls `chains.append(' supersedes '.join((f'ADR {number:04d}' for number in trail)))`.
- Gives back `chains`.

### `src/adr_toolkit/domain/findings.py`

`src/adr_toolkit/domain/findings.py` lines 1 to 6:

```python
"""The result of a rule: a finding with a code, a severity and the document it is about."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The result of a rule: a finding with a code, a severity and the document it is about.

Imports:

- From `__future__` it takes `annotations`.
- From `dataclasses` it takes `dataclass`.
- From `enum` it takes `Enum`.

`src/adr_toolkit/domain/findings.py` lines 9 to 13:

```python
class Severity(Enum):
    """ERROR fails the check; WARNING is reported and does not."""

    ERROR = "error"
    WARNING = "warning"
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** An **Enum** is a class whose members are the only allowed values of a fixed set, such as `Severity.ERROR` and `Severity.WARNING`.

**Class `Severity`**, a kind of `Enum`. ERROR fails the check; WARNING is reported and does not.

Its parts:

- Class value `ERROR` set to the text `'error'`.
- Class value `WARNING` set to the text `'warning'`.

`src/adr_toolkit/domain/findings.py` lines 16 to 23:

```python
@dataclass(frozen=True)
class Finding:
    """One rule violation. The code names the rule so a test and a reader can point at it."""

    code: str
    severity: Severity
    subject: str
    message: str
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `Finding`**. One rule violation. The code names the rule so a test and a reader can point at it. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `code`: a `str`.
- Field `severity`: a `Severity`.
- Field `subject`: a `str`.
- Field `message`: a `str`.

`src/adr_toolkit/domain/findings.py` lines 26 to 28:

```python
def error(code: str, subject: str, message: str) -> Finding:
    """Build an ERROR finding."""
    return Finding(code, Severity.ERROR, subject, message)
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.

**Function `error`.** Build an ERROR finding.

It takes: `code` (a `str`); `subject` (a `str`); `message` (a `str`).

It gives back a `Finding`.

Step by step:

- Gives back the result of calling `Finding(code, Severity.ERROR, subject, message)`.

`src/adr_toolkit/domain/findings.py` lines 31 to 33:

```python
def warning(code: str, subject: str, message: str) -> Finding:
    """Build a WARNING finding."""
    return Finding(code, Severity.WARNING, subject, message)
```

**Function `warning`.** Build a WARNING finding.

It takes: `code` (a `str`); `subject` (a `str`); `message` (a `str`).

It gives back a `Finding`.

Step by step:

- Gives back the result of calling `Finding(code, Severity.WARNING, subject, message)`.

`src/adr_toolkit/domain/findings.py` lines 36 to 56:

```python
@dataclass(frozen=True)
class Report:
    """Every finding from one run, plus the subjects that were checked."""

    subjects: tuple[str, ...]
    findings: tuple[Finding, ...]

    @property
    def errors(self) -> tuple[Finding, ...]:
        """The findings that fail the check."""
        return tuple(f for f in self.findings if f.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        """The findings that are reported without failing the check."""
        return tuple(f for f in self.findings if f.severity is Severity.WARNING)

    @property
    def ok(self) -> bool:
        """True when no finding is an error."""
        return not self.errors
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.

**Class `Report`**. Every finding from one run, plus the subjects that were checked. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `subjects`: a `tuple[str, ...]`.
- Field `findings`: a `tuple[Finding, ...]`.

Its methods, in order:

**Method `errors` of class `Report`.** The findings that fail the check.

It gives back a `tuple[Finding, ...]`.

Decorators: `@property`.

Step by step:

- Gives back the result of calling `tuple((f for f in self.findings if f.severity is Severity.ERROR))`.

**Method `warnings` of class `Report`.** The findings that are reported without failing the check.

It gives back a `tuple[Finding, ...]`.

Decorators: `@property`.

Step by step:

- Gives back the result of calling `tuple((f for f in self.findings if f.severity is Severity.WARNING))`.

**Method `ok` of class `Report`.** True when no finding is an error.

It gives back a `bool`.

Decorators: `@property`.

Step by step:

- Gives back whether not (`self.errors`).

### `src/adr_toolkit/domain/reaction.py`

`src/adr_toolkit/domain/reaction.py` lines 1 to 8:

```python
"""The reaction log: what a reader got wrong, and the proof the record changed because of it."""

from __future__ import annotations

from dataclasses import dataclass

from adr_toolkit.domain.findings import Finding, error, warning
from adr_toolkit.domain.text import squash
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** The reaction log: what a reader got wrong, and the proof the record changed because of it.

Imports:

- From `__future__` it takes `annotations`.
- From `dataclasses` it takes `dataclass`.
- From `adr_toolkit.domain.findings` it takes `Finding, error, warning`.
- From `adr_toolkit.domain.text` it takes `squash`.

`src/adr_toolkit/domain/reaction.py` lines 11 to 22:

```python
@dataclass(frozen=True)
class Reaction:
    """One reading of a record by someone who was not in the room."""

    path: str
    adr_number: int | None
    reader: str
    reader_kind: str
    said_back: str
    misunderstood: str
    before: str
    after: str
```

> **In plain words.** A **class** is a blueprint for objects that bundle data with the functions that work on it. `class B(A)` means B is a kind of A and starts with everything A has.
> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).
> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** A **dataclass** is a class that mainly holds data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields; `frozen=True` forbids changing a field after the object is created.

**Class `Reaction`**. One reading of a record by someone who was not in the room. Decorators: `@dataclass(frozen=True)`.

Its parts:

- Field `path`: a `str`.
- Field `adr_number`: a `int | None`.
- Field `reader`: a `str`.
- Field `reader_kind`: a `str`.
- Field `said_back`: a `str`.
- Field `misunderstood`: a `str`.
- Field `before`: a `str`.
- Field `after`: a `str`.

`src/adr_toolkit/domain/reaction.py` lines 25 to 59:

```python
def check_reaction(reaction: Reaction, adr_text: str) -> list[Finding]:
    """REA001 to REA004. The record text is searched for the fix, so a log cannot claim a change that never happened."""
    found: list[Finding] = []
    for label, value in (
        ("Reader", reaction.reader),
        ("Said back", reaction.said_back),
        ("Misunderstood", reaction.misunderstood),
    ):
        if not squash(value):
            found.append(error("REA001", reaction.path, f"'{label}' is empty"))
    if not reaction.before or not reaction.after:
        found.append(error("REA001", reaction.path, "the log must quote the sentence before and after the fix"))
        return found
    flat = squash(adr_text)
    if squash(reaction.after) not in flat:
        found.append(
            error("REA002", reaction.path, "the 'After' sentence is not in the record: the record was not updated")
        )
    if squash(reaction.before) in flat:
        found.append(
            error(
                "REA003",
                reaction.path,
                "the 'Before' sentence is still in the record: the misunderstanding is not fixed",
            )
        )
    if reaction.reader_kind != "real":
        found.append(
            warning(
                "REA004",
                reaction.path,
                f"reader kind is {reaction.reader_kind!r}: this is a worked example; replace it with a real reading",
            )
        )
    return found
```

> **In plain words.** A **`for` loop** repeats its steps once for each item of a collection. `range(n)` counts from 0 to n-1.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `check_reaction`.** REA001 to REA004. The record text is searched for the fix, so a log cannot claim a change that never happened.

It takes: `reaction` (a `Reaction`); `adr_text` (a `str`).

It gives back a `list[Finding]`.

Step by step:

- Declares `found` as a `list[Finding]` and stores the list `[]` in it.
- For each `(label, value)` in the tuple `(('Reader', reaction.reader), ('Said back', reaction.said_back), ('Mi…`:
  - If not (`squash(value)`):
    - Calls `found.append(error('REA001', reaction.path, f"'{label}' is empty"))`.
- If not (`reaction.before`) or not (`reaction.after`):
  - Calls `found.append(error('REA001', reaction.path, 'the log must quote the sentence before and after the fix'))`.
  - Gives back `found`.
- Stores the result of calling `squash(adr_text)` in `flat`.
- If `squash(reaction.after)` is not in `flat`:
  - Calls `found.append(error('REA002', reaction.path, "the 'After' sentence is not in the record: the record was not up…`.
- If `squash(reaction.before)` is in `flat`:
  - Calls `found.append(error('REA003', reaction.path, "the 'Before' sentence is still in the record: the misunderstandi…`.
- If `reaction.reader_kind` is different from `'real'`:
  - Calls `found.append(warning('REA004', reaction.path, f'reader kind is {reaction.reader_kind!r}: this is a worked exa…`.
- Gives back `found`.

`src/adr_toolkit/domain/reaction.py` lines 62 to 71:

```python
def check_talk(path: str, text: str, max_words: int = 400) -> list[Finding]:
    """TLK001: three minutes of speech is about 400 words."""
    count = len(text.split())
    if count > max_words:
        return [error("TLK001", path, f"{count} words; three minutes is about {max_words}")]
    if count < 150:
        return [
            error("TLK001", path, f"{count} words is under a minute; the talk needs the options and the consequence")
        ]
    return []
```

**Function `check_talk`.** TLK001: three minutes of speech is about 400 words.

It takes: `path` (a `str`); `text` (a `str`); `max_words` (a `int`), default `400`.

It gives back a `list[Finding]`.

Step by step:

- Stores the result of calling `len(text.split())` in `count`.
- If `count` is more than `max_words`:
  - Gives back the list `[error('TLK001', path, f'{count} words; three minutes is about {max_w…`.
- If `count` is less than `150`:
  - Gives back the list `[error('TLK001', path, f'{count} words is under a minute; the talk ne…`.
- Gives back the list `[]`.

### `src/adr_toolkit/domain/text.py`

`src/adr_toolkit/domain/text.py` lines 1 to 5:

```python
"""Small text helpers shared by the rules."""

from __future__ import annotations

import re
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** Small text helpers shared by the rules.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `re`.

`src/adr_toolkit/domain/text.py` lines 7 to 8:

```python
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
```

> **In plain words.** A **regular expression** is a short pattern for text, such as `^## (.+)$` for "a line starting with ## ". `re.compile` prepares it once; `.match` tries it at the start of a string and returns a match object or `None`.
> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the result of calling `re.compile('(?<=[.!?])\\s+(?=[A-Z0-9\\"\'(])')` in `_SENTENCE_BREAK`.
- Stores the result of calling `re.compile("[A-Za-z0-9][A-Za-z0-9'-]*")` in `_WORD`.

`src/adr_toolkit/domain/text.py` lines 11 to 13:

```python
def squash(text: str) -> str:
    """Collapse every run of whitespace to one space."""
    return " ".join(text.split())
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.

**Function `squash`.** Collapse every run of whitespace to one space.

It takes: `text` (a `str`).

It gives back a `str`.

Step by step:

- Gives back the result of calling `' '.join(text.split())`.

`src/adr_toolkit/domain/text.py` lines 16 to 19:

```python
def sentences(text: str) -> list[str]:
    """Split prose into sentences. Lists and labels in the documents end with a full stop on purpose."""
    flat = squash(text)
    return [part for part in _SENTENCE_BREAK.split(flat) if part] if flat else []
```

> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.

**Function `sentences`.** Split prose into sentences. Lists and labels in the documents end with a full stop on purpose.

It takes: `text` (a `str`).

It gives back a `list[str]`.

Step by step:

- Stores the result of calling `squash(text)` in `flat`.
- Gives back `[part for part in _SENTENCE_BREAK.split…` if `flat`, otherwise `[]`.

`src/adr_toolkit/domain/text.py` lines 22 to 24:

```python
def words(text: str) -> list[str]:
    """The words of a text, lower-cased."""
    return [match.lower() for match in _WORD.findall(text)]
```

**Function `words`.** The words of a text, lower-cased.

It takes: `text` (a `str`).

It gives back a `list[str]`.

Step by step:

- Gives back a new list made by a loop (`[match.lower() for match in _WORD.findall(text)]`).

`src/adr_toolkit/domain/text.py` lines 27 to 29:

```python
def has_figure(text: str) -> bool:
    """True when the text holds at least one digit: a number, a date or a count."""
    return any(character.isdigit() for character in text)
```

> **In plain words.** A **generator expression** `(x for x in items)` is like a list comprehension, but it hands out one value at a time instead of building the whole list; here it is passed straight to a function such as `tuple(...)` or `sum(...)`.

**Function `has_figure`.** True when the text holds at least one digit: a number, a date or a count.

It takes: `text` (a `str`).

It gives back a `bool`.

Step by step:

- Gives back the result of calling `any((character.isdigit() for character in text))`.

`src/adr_toolkit/domain/text.py` lines 32 to 37:

```python
def similarity(first: str, second: str) -> float:
    """Jaccard similarity of the two texts' word sets, from 0 (nothing shared) to 1 (the same words)."""
    left, right = set(words(first)), set(words(second))
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
```

> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** On sets, `a | b` is the union (everything in either) and `a & b` the intersection (what both have).

**Function `similarity`.** Jaccard similarity of the two texts' word sets, from 0 (nothing shared) to 1 (the same words).

It takes: `first` (a `str`); `second` (a `str`).

It gives back a `float`.

Step by step:

- Unpacks the tuple `(set(words(first)), set(words(second)))` into `(left, right)`.
- If not (`left`) or not (`right`):
  - Gives back the number `0.0`.
- Gives back `len(left & right) / len(left | right)`.

## Try it yourself

```bash
.venv/bin/python -c "import adr_toolkit.domain.adr; print(adr_toolkit.domain.adr.__doc__)"
```
Prints the module's description: `The architecture decision record as a value, and the rules a record must satisfy.`

```bash
.venv/bin/python -c "import adr_toolkit.domain.audiences; print(adr_toolkit.domain.audiences.__doc__)"
```
Prints the module's description: `The same decision told three ways, and the rules that keep each version for its reader.`

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check src/adr_toolkit/__init__.py src/adr_toolkit/domain/__init__.py src/adr_toolkit/domain/adr.py src/adr_toolkit/domain/audiences.py src/adr_toolkit/domain/decision_log.py src/adr_toolkit/domain/findings.py
```
Prints `All checks passed!`.

```bash
grep -c "^def \|^class \|    def " src/adr_toolkit/domain/adr.py
```
Counts the functions, methods and classes in `src/adr_toolkit/domain/adr.py`.

## Mistakes people make

- Reading a file or printing from a domain function. Input and output belong to the outer layers.
- Importing a framework (Flask, psycopg) here; the contract in `pyproject.toml` forbids it.
- Changing a value in place. The domain uses frozen values, so a change makes a new value.

## Check yourself

1. What is `Option` for?
   **Answer:** One option, described by the same three lines for every option.
2. What is `Adr` for?
   **Answer:** A parsed decision record. Missing parts are empty strings or None, and the rules report them.
3. What is `AdrLimits` for?
   **Answer:** The size of one page.
4. What is `check_adr` for?
   **Answer:** Apply every rule to one record. The codes ADR001 to ADR018 are listed in the README.
5. What is `AudienceVersions` for?
   **Answer:** The three short versions of one decision, keyed to the record they tell.

## Further reading

- Python 3.12 tutorial, classes: <https://docs.python.org/3.12/tutorial/classes.html>
- Python 3.12 language reference: <https://docs.python.org/3.12/reference/>
- Type hints: <https://docs.python.org/3.12/library/typing.html>
