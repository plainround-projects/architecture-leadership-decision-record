# Environment variables and .env files

## What it is

An **environment variable** is a named text value that every program started from a shell can read. Programs use
them for settings that change between machines (a folder, a limit, a port) without changing code. A **`.env` file** is
a plain file of `NAME=value` lines that a tool loads into the environment. It is a convention, not a standard
program.

## Why this repository uses it

The lesson's twelve-factor rule: configuration lives in the environment, validated once at start-up. The settings
here are only limits and folders (nothing secret), and the defaults work with no `.env` at all. `.env.example`
documents each setting.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `.env.example` | Committed. Lists every setting with a comment and the default value. |
| `.env` | Local copy created by `make env`; ignored by git. |
| `Makefile` | `-include .env` and `export` pass the values to the program. |
| `src/adr_toolkit/infrastructure/settings.py` | Reads `os.environ` and checks the values. |
| `tests/unit/interfaces/test_cli.py` | Sets variables with `monkeypatch.setenv`. |

## How it works underneath

- Make reads `.env` as variable assignments and, because of `export`, copies them into the environment of each
  command it starts. A value assigned in the Makefile or an included file takes priority over a variable of the same
  name that your shell already had (the option `make -e` reverses that).
- The program receives its environment at start-up. In Python, `os.environ` is a dictionary-like view of it. Every
  value is a string.
- If a variable is missing, the code supplies a default. If a value cannot be used (`ADR_MAX_LINES=lots`), the
  program stops with exit code 2 and a message that names the variable.

## Walkthrough of this repository's use

`.env.example`:

```ini
# Where the documents live (the repository root by default).
ADR_ROOT=.
# Where `make report` writes report.md.
REPORT_DIR=build
# One page: the most non-blank lines and words a decision record may have.
ADR_MAX_LINES=70
ADR_MAX_WORDS=600
# Records that must come with audience versions, a reaction log and (if present) a talk. Comma-separated numbers.
ADR_REQUIRED_COMMUNICATION=7
```

Each setting has a comment line above it. `#` starts a comment in both Make and shell syntax. The file is
`NAME=value` with no spaces around `=` and no quotes.

`src/adr_toolkit/infrastructure/settings.py`:

```python
class SettingsError(ValueError):
    """An environment variable holds a value the program cannot use."""
```

`src/adr_toolkit/infrastructure/settings.py`:

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
```

The function receives the environment as a mapping (`Mapping[str, str]`), so tests can pass a plain dictionary. It
reads each name with `env.get(NAME, default)`, converts to a number, and raises `SettingsError` for a value it
cannot accept. `cli.py` catches that error, prints `configuration error: ...` to stderr and returns exit code 2.

### The complete file `.env.example`, line by line

`.env.example` lines 1 to 9:

```ini
# Where the documents live (the repository root by default).
ADR_ROOT=.
# Where `make report` writes report.md.
REPORT_DIR=build
# One page: the most non-blank lines and words a decision record may have.
ADR_MAX_LINES=70
ADR_MAX_WORDS=600
# Records that must come with audience versions, a reaction log and (if present) a talk. Comma-separated numbers.
ADR_REQUIRED_COMMUNICATION=7
```

> **In plain words.** A `.env` file is a list of `NAME=value` lines that become settings (environment variables) for the programs; a line starting with `#` is a comment.

- `ADR_ROOT` is set to `.`. The author's comment: Where the documents live (the repository root by default).
- `REPORT_DIR` is set to `build`. The author's comment: Where `make report` writes report.md.
- `ADR_MAX_LINES` is set to `70`. The author's comment: One page: the most non-blank lines and words a decision record may have.
- `ADR_MAX_WORDS` is set to `600`.
- `ADR_REQUIRED_COMMUNICATION` is set to `7`. The author's comment: Records that must come with audience versions, a reaction log and (if present) a talk. Comma-separated numbers.

## Try it yourself

```bash
cat .env.example
```
Prints the settings and their comments.

```bash
ADR_MAX_LINES=lots .venv/bin/adr-toolkit check; echo "exit: $?"
```
Calls the program directly with a bad value. It prints `configuration error: ...` naming the variable, then `exit: 2`.

```bash
ADR_MAX_LINES=lots make run; echo "exit: $?"
```
Surprise: this **passes** (`exit: 0`). `.env` sets `ADR_MAX_LINES` and an assignment in a Makefile beats a value inherited
from your shell. Add `-e` (`make -e run`) to let the shell's value win; now the program reports the bad value and
`make` fails.

```bash
git check-ignore -v .env
```
Prints the `.gitignore` line that ignores `.env`.

```bash
env | grep -c '^ADR_ROOT=' ; make -n run | head -2
```
Shows that the variable is not set in your shell by default: Make supplies it only to the commands it runs.

## Mistakes people make

- **Committing `.env`.** It is in `.gitignore`. Only `.env.example` is committed. (There are no secrets in this
  repository's settings; for a real secret you would never commit it either.)
- **Expecting the shell to override `.env`.** Inside `make`, the value in `.env` wins over `NAME=value make ...`
  unless you use `make -e`. To change a setting for one run, edit `.env` or run the program directly.
- **Spaces or quotes** in `NAME = "value"`: Make and shell read them differently.
- **Forgetting that every value is a string**, so numbers must be converted and checked.
- **Defaults that hide errors.** The code rejects unusable values instead of falling back silently.

## Check yourself

1. What does `export` in the Makefile do?
   **Answer:** It passes every Make variable, including those from `.env`, to the commands Make runs.
2. Why is `.env.example` committed but `.env` not?
   **Answer:** The example documents the settings for everyone; the real `.env` is local to a machine.
3. What type is every value in `os.environ`?
   **Answer:** A string.
4. What exit code means a bad setting?
   **Answer:** 2.
5. Why does `load_settings` take a mapping instead of reading `os.environ` itself?
   **Answer:** So tests can pass a plain dictionary.

## Further reading

- The Twelve-Factor App, III. Config: <https://12factor.net/config>
- Python `os.environ` (3.12): <https://docs.python.org/3.12/library/os.html#os.environ>
- GNU Make, `include` and `export`: <https://www.gnu.org/software/make/manual/make.html#Include>
