# Interfaces layer code

## What it is

The entry points: the command line, the web routes and the wiring that builds everything from settings. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

This is where the repository's interfaces work happens. Reading it file by file, with every line explained, is how a reader sees the work that was done.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/interfaces/__init__.py` | 1 lines. The command-line program. Nothing depends on this package. |
| `src/adr_toolkit/interfaces/cli.py` | 48 lines. `adr-toolkit check | log | report`. Wires the adapters into the use cases and owns the exit codes. |

## How it works underneath

This outermost layer turns requests (a typed command, an HTTP call) into use-case calls and turns errors into exit codes or status codes. It is also where the adapters are created and connected (the composition root). Nothing depends on it.

## Walkthrough of this repository's use

### `src/adr_toolkit/interfaces/__init__.py`

`src/adr_toolkit/interfaces/__init__.py` lines 1 to 1:

```python
"""The command-line program. Nothing depends on this package."""
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.

**Module description.** The command-line program. Nothing depends on this package.

### `src/adr_toolkit/interfaces/cli.py`

`src/adr_toolkit/interfaces/cli.py` lines 1 to 14:

```python
"""`adr-toolkit check | log | report`. Wires the adapters into the use cases and owns the exit codes."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

from adr_toolkit.application.check_documents import check_documents, current_log, write_log
from adr_toolkit.application.reporting import render_markdown, render_text
from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from adr_toolkit.infrastructure.settings import SettingsError, load_settings
```

> **In plain words.** A **docstring** is a text in triple quotes as the first thing in a module, class or function. Python keeps it as the thing's description, and ruff requires one on public code.
> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.
> **In plain words.** `from __future__ import annotations` makes every type hint in the file lazy text. Python no longer evaluates a hint when the file loads, so a hint may name a class defined further down.

**Module description.** `adr-toolkit check | log | report`. Wires the adapters into the use cases and owns the exit codes.

Imports:

- From `__future__` it takes `annotations`.
- It imports module `argparse`.
- It imports module `os`.
- It imports module `sys`.
- From `collections.abc` it takes `Sequence`.
- From `adr_toolkit.application.check_documents` it takes `check_documents, current_log, write_log`.
- From `adr_toolkit.application.reporting` it takes `render_markdown, render_text`.
- From `adr_toolkit.infrastructure.filesystem` it takes `FileSystemStore`.
- From `adr_toolkit.infrastructure.markdown` it takes `MarkdownRecordReader`.
- From `adr_toolkit.infrastructure.settings` it takes `SettingsError, load_settings`.

`src/adr_toolkit/interfaces/cli.py` lines 17 to 27:

```python
def build_parser() -> argparse.ArgumentParser:
    """The command line: three subcommands, no options of their own."""
    parser = argparse.ArgumentParser(
        prog="adr-toolkit", description="Check decision records and the documents that carry them."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="run every rule; exit 1 on any error")
    log = commands.add_parser("log", help="print the decision log")
    log.add_argument("--write", action="store_true", help="write docs/decision-log.md instead of printing")
    commands.add_parser("report", help="write the Markdown report under REPORT_DIR")
    return parser
```

> **In plain words.** A **type hint** such as `x: int` or `-> str` says what kind of value a name holds or a function gives back. Python does not enforce hints when the program runs; the type checker mypy reads them before.
> **In plain words.** `return value` ends the function and gives the value back to whoever called it.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Function `build_parser`.** The command line: three subcommands, no options of their own.

It gives back a `argparse.ArgumentParser`.

Step by step:

- Stores the result of calling `argparse.ArgumentParser(prog='adr-toolkit', description='Check decision records and the d…` in `parser`.
- Stores the result of calling `parser.add_subparsers(dest='command', required=True)` in `commands`.
- Calls `commands.add_parser('check', help='run every rule; exit 1 on any error')`.
- Stores the result of calling `commands.add_parser('log', help='print the decision log')` in `log`.
- Calls `log.add_argument('--write', action='store_true', help='write docs/decision-log.md instead of printing')`.
- Calls `commands.add_parser('report', help='write the Markdown report under REPORT_DIR')`.
- Gives back `parser`.

`src/adr_toolkit/interfaces/cli.py` lines 30 to 53:

```python
def main(argv: Sequence[str] | None = None) -> int:
    """Run one command and return the exit code: 0 ok, 1 findings, 2 bad configuration."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(os.environ)
    except SettingsError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2
    store = FileSystemStore(settings.root)
    reader = MarkdownRecordReader(store)
    if args.command == "log":
        if args.write:
            write_log(store, reader)
            print("wrote docs/decision-log.md")
        else:
            print(current_log(store, reader), end="")
        return 0
    report = check_documents(store, reader, settings.check)
    if args.command == "report":
        store.write_text(f"{settings.report_dir}/report.md", render_markdown(report))
        print(f"wrote {settings.report_dir}/report.md")
        return 0 if report.ok else 1
    print(render_text(report))
    return 0 if report.ok else 1
```

> **In plain words.** A **`try` / `except` block** runs the steps under `try`. If an error of the named kind happens, Python jumps to the matching `except` steps instead of stopping the program. `finally` steps always run.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** `A if test else B` is a **conditional expression**: its value is A when the test is true, otherwise B.
> **In plain words.** `A | B` in a type hint means "either A or B". `X | None` means a value that may be missing.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** An **f-string** `f"...{value}..."` is text with Python expressions in braces; Python replaces each by its value. `{x!r}` shows the value the way Python would write it, with quotes.

**Function `main`.** Run one command and return the exit code: 0 ok, 1 findings, 2 bad configuration.

It takes: `argv` (a `Sequence[str] | None`), default `None`.

It gives back a `int`.

Step by step:

- Stores the result of calling `build_parser().parse_args(argv)` in `args`.
- Tries:
  - Stores the result of calling `load_settings(os.environ)` in `settings`.
- If `SettingsError` happens (named `error`):
  - Calls `print(f'configuration error: {error}', file=sys.stderr)`.
  - Gives back the number `2`.
- Stores the result of calling `FileSystemStore(settings.root)` in `store`.
- Stores the result of calling `MarkdownRecordReader(store)` in `reader`.
- If `args.command` equals `'log'`:
  - If `args.write`:
    - Calls `write_log(store, reader)`.
    - Calls `print('wrote docs/decision-log.md')`.
  - Otherwise:
    - Calls `print(current_log(store, reader), end='')`.
  - Gives back the number `0`.
- Stores the result of calling `check_documents(store, reader, settings.check)` in `report`.
- If `args.command` equals `'report'`:
  - Calls `store.write_text(f'{settings.report_dir}/report.md', render_markdown(report))`.
  - Calls `print(f'wrote {settings.report_dir}/report.md')`.
  - Gives back `0` if `report.ok`, otherwise `1`.
- Calls `print(render_text(report))`.
- Gives back `0` if `report.ok`, otherwise `1`.

`src/adr_toolkit/interfaces/cli.py` lines 56 to 57:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

> **In plain words.** `if __name__ == "__main__":` runs its steps only when the file is started directly, not when another file imports it.
> **In plain words.** `raise Error(...)` stops the current function by signalling an error. `raise ... from None` hides the earlier error, so the user sees only the new, clearer message.

This statement:

- If `__name__` equals `'__main__'`:
  - Stops here by raising `SystemExit(main())`.

## Try it yourself

```bash
.venv/bin/python -c "import adr_toolkit.interfaces.cli; print(adr_toolkit.interfaces.cli.__doc__)"
```
Prints the module's description: ``adr-toolkit check | log | report`. Wires the adapters into the use cases and owns the exit codes.`

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check src/adr_toolkit/interfaces/__init__.py src/adr_toolkit/interfaces/cli.py
```
Prints `All checks passed!`.

```bash
grep -c "^def \|^class \|    def " src/adr_toolkit/interfaces/cli.py
```
Counts the functions, methods and classes in `src/adr_toolkit/interfaces/cli.py`.

## Mistakes people make

- Putting rules in a route or a command handler. They call the use cases.
- Returning raw error text to the caller. Named errors map to fixed messages and codes.
- Creating adapters deep inside the code instead of here, which makes testing hard.

## Check yourself

1. What is `build_parser` for?
   **Answer:** The command line: three subcommands, no options of their own.
2. What is `main` for?
   **Answer:** Run one command and return the exit code: 0 ok, 1 findings, 2 bad configuration.
3. What is a docstring?
   **Answer:** A text in triple quotes at the start of a module, class or function that describes it.
4. What does `frozen=True` do on a dataclass?
   **Answer:** It forbids changing a field after the object is created.
5. What does a type hint do at run time?
   **Answer:** Nothing; mypy reads hints before the program runs.

## Further reading

- Python 3.12 tutorial, classes: <https://docs.python.org/3.12/tutorial/classes.html>
- Python 3.12 language reference: <https://docs.python.org/3.12/reference/>
- Type hints: <https://docs.python.org/3.12/library/typing.html>
