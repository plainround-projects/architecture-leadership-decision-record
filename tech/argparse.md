# argparse (the command line)

## What it is

A **command-line program** is started by typing its name and some words: `adr-toolkit check`. Those words are its
**arguments**. `argparse` is the standard Python module that reads them, checks them, builds the `--help` text and
reports mistakes. An **exit code** is the number a program returns to the shell when it ends: 0 means success, other
numbers mean different failures.

## Why this repository uses it

`make run` and CI decide pass or fail from the exit code, so the command must return the right number. `argparse`
gives subcommands (`check`, `report`...) and a free help text, with no extra packages.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/interfaces/cli.py` | `build_parser()` and `main()`. |
| `pyproject.toml` `[project.scripts]` | Registers `adr-toolkit` as a command that calls `main`. |
| `Makefile` | `$(CLI) check`, `$(CLI) report`. |
| `tests/unit/interfaces/test_cli.py` | Calls `main([...])` directly and checks the exit code. |

## How it works underneath

1. The shell starts the program with a list of words. Python puts them in `sys.argv`.
2. `parser.parse_args(argv)` walks that list: the first word picks a subcommand; options like `--write` are matched by
   name. Unknown words make `argparse` print an error and exit with code 2.
3. The result is a `Namespace` object whose attributes are the answers (`args.command`).
4. The program does its work and returns an integer. `raise SystemExit(main())` turns the integer into the process
   exit code. The shell stores it in `$?`.

## Walkthrough of this repository's use

`src/adr_toolkit/interfaces/cli.py`:

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

- `argparse.ArgumentParser(prog=..., description=...)` creates the parser. `prog` is the name shown in usage text.
- `add_subparsers(dest="command", required=True)` creates the group of subcommands. `dest="command"` stores which
  one the user typed in `args.command`. `required=True` makes it an error to give none.
- `commands.add_parser("check", help=...)` adds one subcommand and its help line.

- `log.add_argument("--write", action="store_true", help=...)` adds the option `--write` to the `log` subcommand.
  `action="store_true"` makes `args.write` `True` when the option is given and `False` otherwise.

`src/adr_toolkit/interfaces/cli.py`:

```python
def main(argv: Sequence[str] | None = None) -> int:
    """Run one command and return the exit code: 0 ok, 1 findings, 2 bad configuration."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(os.environ)
    except SettingsError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2
```

- `argv: Sequence[str] | None = None`: when `None`, `parse_args` reads the real command line. Tests pass a list.
- `load_settings(os.environ)` reads the environment (see `env-files.md`).
- A bad setting prints to **stderr** (`file=sys.stderr`) and returns 2: the three exit codes are 0 (ok), 1 (the
  documents have errors) and 2 (the program was set up wrongly).

`src/adr_toolkit/interfaces/cli.py`:

```python
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


if __name__ == "__main__":
    raise SystemExit(main())
```

The three subcommands: `log` prints or (with `--write`) writes `docs/decision-log.md`; `report` writes `build/report.md`; `check` prints the findings. `0 if report.ok else 1` is a **conditional expression**: the value is 0 when the report has no errors, otherwise 1.

## Try it yourself

```bash
.venv/bin/adr-toolkit --help
```
Prints the usage line and the list of subcommands with their help text.

```bash
.venv/bin/adr-toolkit nonsense; echo "exit: $?"
```
`argparse` prints `error: argument command: invalid choice: 'nonsense'` and the shell shows `exit: 2`.

```bash
make run > /dev/null; echo "exit: $?"
```
Prints `exit: 0` when every document passes.

```bash
ADR_MAX_LINES=lots .venv/bin/adr-toolkit check; echo "exit: $?"
```
Prints `configuration error: ...` naming the variable, then `exit: 2`.

```bash
.venv/bin/python -c "from adr_toolkit.interfaces.cli import main; print(main(['report']))"
```
Calls `main` as a function, as the tests do; prints `wrote build/report.md` and then `0`.

## Mistakes people make

- **Printing errors to stdout.** Errors belong on stderr so scripts can separate them.
- **Always exiting 0**, so CI cannot tell a failure. This program returns 1 for findings and 2 for bad setup.
- **Reading `sys.argv` by hand.** `argparse` handles quoting, options and help.
- **Calling `sys.exit` deep inside the code.** Only `main` decides the exit code; the rest returns values.

## Check yourself

1. What are the exit codes of `adr-toolkit`?
   **Answer:** 0 for success, 1 when the checks find errors, 2 for a bad configuration (and argparse uses 2 for a bad command line).
2. Why does `main` take `argv` as a parameter?
   **Answer:** So tests can call it with a list instead of the real command line.
3. What does `required=True` on `add_subparsers` do?
   **Answer:** It makes giving no subcommand an error.
4. Where do error messages go and why?
   **Answer:** To stderr, so scripts can separate them from normal output.
5. What turns `main`'s return value into the exit status?
   **Answer:** `raise SystemExit(main())`.

## Further reading

- `argparse` (Python 3.12): <https://docs.python.org/3.12/library/argparse.html>
- Argparse tutorial: <https://docs.python.org/3.12/howto/argparse.html>
