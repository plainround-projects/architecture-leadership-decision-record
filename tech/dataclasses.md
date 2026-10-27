# dataclasses

## What it is

A **dataclass** is a class that mainly holds data. You list the fields with their types, and Python writes the
boring methods for you: `__init__` (to create the object), `__repr__` (to print it) and `__eq__` (to compare two
objects by their fields). The decorator `@dataclass` does the work. `frozen=True` makes the object read-only after it
is created.

## Why this repository uses it

Everything the program passes around is a value: a finding, a report, a parsed record, a set of settings. Frozen
values cannot be changed behind your back, are easy to compare in tests, and print readably when a test fails.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/domain/findings.py` | `Finding`, `Report`. |
| `src/adr_toolkit/domain/*.py` | `Adr`, `Option`, `AdrLimits`, `AudienceVersions`, `Reaction`: the parsed documents. |
| `src/adr_toolkit/application/check_documents.py` | `CheckSettings`. |
| `src/adr_toolkit/infrastructure/settings.py` | `Settings`. |
| `tests/conftest.py` and tests | `dataclasses.replace` to change one field of a sample. |

## How it works underneath

At import time, `@dataclass` looks at the class's annotated fields and **generates source code** for `__init__`,
`__repr__` and `__eq__` and attaches it to the class. With `frozen=True` it also generates `__setattr__` and
`__delattr__` methods that raise `FrozenInstanceError`, and a `__hash__`, so frozen objects can be dictionary keys or
set members. The fields are stored in the object like ordinary attributes.

## Walkthrough of this repository's use

`src/adr_toolkit/domain/findings.py`:

```python
@dataclass(frozen=True)
class Finding:
    """One rule violation. The code names the rule so a test and a reader can point at it."""

    code: str
    severity: Severity
    subject: str
    message: str
```

- `@dataclass(frozen=True)` is the decorator with an option.
- The four lines `code: str`, `severity: Severity`, ... are **fields**: a name, a colon and a type. There is no
  `__init__` to write: `Finding("ADR001", Severity.ERROR, "a.md", "text")` works.
- The docstring explains what the class is.

`src/adr_toolkit/domain/findings.py`:

```python
@dataclass(frozen=True)
class Report:
    """Every finding from one run, plus the subjects that were checked."""

    subjects: tuple[str, ...]
    findings: tuple[Finding, ...]
```

`tuple[str, ...]` fields hold immutable sequences; using tuples instead of lists keeps the whole object unchangeable.
The methods and properties below read those fields but never change them.

`src/adr_toolkit/application/check_documents.py`:

```python
@dataclass(frozen=True)
class CheckSettings:
    """Which records must come with audience versions, a reaction log and a talk."""

    limits: AdrLimits = field(default_factory=AdrLimits)
    required_adrs: tuple[int, ...] = ()
```

`field(default_factory=AdrLimits)` is the safe way to give a dataclass field a default that is an object: each `CheckSettings` gets its own new `AdrLimits`. (`from dataclasses import dataclass, field` imports both names.)

`tests/conftest.py`:

```python
    return replace(base, **changes)  # type: ignore[arg-type]
```

`replace` (imported with `from dataclasses import replace`) makes a **copy** of a frozen object with some fields
changed. The tests build one valid sample, then change one field to break exactly one rule.

## Try it yourself

```bash
.venv/bin/python - <<'EOF'
from adr_toolkit.domain.findings import Finding, Severity
f = Finding("X1", Severity.ERROR, "a.md", "oops")
print(f == Finding("X1", Severity.ERROR, "a.md", "oops"))
try:
    f.code = "Y"
except Exception as e:
    print(type(e).__name__)
EOF
```
Prints `True` (equal by fields) and then `FrozenInstanceError`.

```bash
.venv/bin/python -c "from dataclasses import fields; from adr_toolkit.domain.findings import Finding; print([x.name for x in fields(Finding)])"
```
Prints `['code', 'severity', 'subject', 'message']`.

```bash
.venv/bin/python -c "from dataclasses import replace; from adr_toolkit.domain.findings import Finding, Severity; f = Finding('A', Severity.ERROR, 's', 'm'); print(replace(f, code='B').code, f.code)"
```
Prints `B A`: a changed copy, the original untouched.

```bash
grep -rn "@dataclass" src | wc -l
```
Counts how many dataclasses the code defines.

## Mistakes people make

- **A mutable default** such as `items: list = []`. Dataclasses reject it; use `field(default_factory=list)` or an
  immutable tuple.
- **Forgetting `frozen=True`** and letting values change by accident.
- **Assuming frozen means deeply frozen.** A frozen dataclass holding a list can still have the list changed. These
  classes hold tuples.
- **Comparing floats by `==`** in a dataclass field. Use a tolerance in tests.

## Check yourself

1. What does `@dataclass` write for you?
   **Answer:** `__init__`, `__repr__` and `__eq__` (and more, with options).
2. What does `frozen=True` do?
   **Answer:** It makes assigning to a field after creation raise `FrozenInstanceError`.
3. How do you change one field of a frozen object?
   **Answer:** Make a copy with `dataclasses.replace(obj, field=value)`.
4. Why use `tuple[str, ...]` rather than `list[str]` in a frozen class?
   **Answer:** A tuple cannot be changed, so the object stays unchangeable.
5. When does `__post_init__` run?
   **Answer:** Right after the generated `__init__`, to validate the fields.

## Further reading

- `dataclasses` (Python 3.12): <https://docs.python.org/3.12/library/dataclasses.html>
