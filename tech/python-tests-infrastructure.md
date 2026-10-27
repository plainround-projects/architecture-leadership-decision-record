# The tests (infrastructure)

## What it is

The pytest tests in `tests/unit/infrastructure`. Each function whose name starts with `test_` is one check; pytest finds and runs them. (Every term is explained where it first appears in the walkthrough below.)

## Why this repository uses it

The tests turn every rule, adapter and command of this repository into something that can fail. A rule without a test is only a claim.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `tests/unit/infrastructure/test_filesystem_and_settings.py` | 35 lines.  |
| `tests/unit/infrastructure/test_markdown.py` | 61 lines.  |

## How it works underneath

pytest imports each `test_*.py` file, builds the fixtures a test asks for by parameter name, runs the function, and counts it as passed when no `assert` fails and nothing raises. A fixture such as `tmp_path` or `monkeypatch` is prepared fresh for each test, so tests do not affect each other.

## Walkthrough of this repository's use

### `tests/unit/infrastructure/test_filesystem_and_settings.py`

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 1 to 4:

```python
import pytest

from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.settings import SettingsError, load_settings
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- It imports module `pytest`.
- From `adr_toolkit.infrastructure.filesystem` it takes `FileSystemStore`.
- From `adr_toolkit.infrastructure.settings` it takes `SettingsError, load_settings`.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 7 to 15:

```python
def test_the_store_lists_only_markdown_files_in_one_folder(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "b.md").write_text("b")
    (tmp_path / "docs" / "a.md").write_text("a")
    (tmp_path / "docs" / "c.txt").write_text("c")
    (tmp_path / "docs" / "sub").mkdir()
    store = FileSystemStore(tmp_path)
    assert store.list_paths("docs") == ["docs/a.md", "docs/b.md"]
    assert store.list_paths("missing") == []
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.
> **In plain words.** `tmp_path` is a built-in pytest fixture: a fresh, empty temporary folder (a `Path`) that is removed after the test.

**Test `test_the_store_lists_only_markdown_files_in_one_folder`** checks: the store lists only markdown files in one folder.

It takes: `tmp_path`.

Step by step:

- Calls `(tmp_path / 'docs').mkdir()`.
- Calls `(tmp_path / 'docs' / 'b.md').write_text('b')`.
- Calls `(tmp_path / 'docs' / 'a.md').write_text('a')`.
- Calls `(tmp_path / 'docs' / 'c.txt').write_text('c')`.
- Calls `(tmp_path / 'docs' / 'sub').mkdir()`.
- Stores the result of calling `FileSystemStore(tmp_path)` in `store`.
- Checks that `store.list_paths('docs')` equals `['docs/a.md', 'docs/b.md']`; if not, the test fails.
- Checks that `store.list_paths('missing')` equals `[]`; if not, the test fails.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 18 to 23:

```python
def test_the_store_writes_creates_folders_and_reads_back(tmp_path):
    store = FileSystemStore(tmp_path)
    assert not store.exists("build/report.md")
    store.write_text("build/report.md", "hello")
    assert store.exists("build/report.md")
    assert store.read_text("build/report.md") == "hello"
```

**Test `test_the_store_writes_creates_folders_and_reads_back`** checks: the store writes creates folders and reads back.

It takes: `tmp_path`.

Step by step:

- Stores the result of calling `FileSystemStore(tmp_path)` in `store`.
- Checks that not (`store.exists('build/report.md')`); if not, the test fails.
- Calls `store.write_text('build/report.md', 'hello')`.
- Checks that `store.exists('build/report.md')`; if not, the test fails.
- Checks that `store.read_text('build/report.md')` equals `'hello'`; if not, the test fails.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 26 to 28:

```python
def test_the_store_refuses_to_leave_its_root(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        FileSystemStore(tmp_path).read_text("../secret.md")
```

> **In plain words.** `with pytest.raises(Error):` expects the code inside to raise that error; the test fails if it does not.
> **In plain words.** A call such as `f(a, key=value)` passes `a` by position and `key` by name (a **keyword argument**).

**Test `test_the_store_refuses_to_leave_its_root`** checks: the store refuses to leave its root.

It takes: `tmp_path`.

Step by step:

- Expects the steps inside to raise the error in `pytest.raises(ValueError, match='escapes')`:
  - Calls `FileSystemStore(tmp_path).read_text('../secret.md')`.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 31 to 33:

```python
def test_settings_have_defaults():
    settings = load_settings({})
    assert (settings.report_dir, settings.check.limits.max_lines, settings.check.required_adrs) == ("build", 70, ())
```

> **In plain words.** A **dictionary** `{key: value}` maps keys to values.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.

**Test `test_settings_have_defaults`** checks: settings have defaults.

Step by step:

- Stores the result of calling `load_settings({})` in `settings`.
- Checks that `(settings.report_dir, settings.check.limits.max_l…` equals `('build', 70, ())`; if not, the test fails.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 36 to 39:

```python
def test_settings_read_the_environment():
    env = {"ADR_ROOT": "x", "ADR_MAX_LINES": "40", "ADR_MAX_WORDS": "300", "ADR_REQUIRED_COMMUNICATION": "7, 9"}
    settings = load_settings(env)
    assert (str(settings.root), settings.check.limits.max_words, settings.check.required_adrs) == ("x", 300, (7, 9))
```

**Test `test_settings_read_the_environment`** checks: settings read the environment.

Step by step:

- Stores the dictionary `{'ADR_ROOT': 'x', 'ADR_MAX_LINES': '40', 'ADR_MAX_WORDS': '300', 'ADR…` in `env`.
- Stores the result of calling `load_settings(env)` in `settings`.
- Checks that `(str(settings.root), settings.check.limits.max_wo…` equals `('x', 300, (7, 9))`; if not, the test fails.

`tests/unit/infrastructure/test_filesystem_and_settings.py` lines 42 to 48:

```python
@pytest.mark.parametrize(
    "env",
    [{"ADR_MAX_LINES": "many"}, {"ADR_MAX_WORDS": "0"}, {"ADR_REQUIRED_COMMUNICATION": "seven"}],
)
def test_bad_settings_are_rejected_with_the_name(env):
    with pytest.raises(SettingsError):
        load_settings(env)
```

> **In plain words.** `@pytest.mark.parametrize` runs the same test function once for each row of data given; a failure names the row that broke.

**Test `test_bad_settings_are_rejected_with_the_name`** checks: bad settings are rejected with the name.

It takes: `env`.

Decorators: `@pytest.mark.parametrize('env', [{'ADR_MAX_LINES': 'many'}, {'ADR_MAX_…`.

Step by step:

- Expects the steps inside to raise the error in `pytest.raises(SettingsError)`:
  - Calls `load_settings(env)`.

### `tests/unit/infrastructure/test_markdown.py`

`tests/unit/infrastructure/test_markdown.py` lines 1 to 2:

```python
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import MemoryStore
```

> **In plain words.** An **import** brings a name from another file or from Python's standard library into this file, so this file can use it.

Imports:

- From `adr_toolkit.infrastructure.markdown` it takes `MarkdownRecordReader`.
- From `tests.conftest` it takes `MemoryStore`.

`tests/unit/infrastructure/test_markdown.py` lines 4 to 32:

```python
ADR = """# ADR 0009: Pick a thing

Status: Superseded by ADR 0010
Date: 2026-01-02
Deciders: Tech lead
Supersedes: ADR 0004

## Context
Facts: 5 of them,
on two lines.

## Options considered
### Option A: first way
Advantage: it is fast
and cheap.
Main cost: it is new
Pick it if: you are in a hurry

### Option B: second way
Advantage: it is old

## Decision
We will do the first way, because it is fast.

## Consequences
Good: fast
Bad: new
Revisit when: 3 users complain
"""
```

> **In plain words.** A name written in CAPITAL letters is a **constant** by convention: a value set once, not changed later.

These module-level lines:

- Stores the text `'# ADR 0009: Pick a thing\n\nStatus: Superseded by ADR 0010…` in `ADR`.

`tests/unit/infrastructure/test_markdown.py` lines 35 to 36:

```python
def reader(files):
    return MarkdownRecordReader(MemoryStore(files))
```

> **In plain words.** `return value` ends the function and gives the value back to whoever called it.

**Function `reader`.**

It takes: `files`.

Step by step:

- Gives back the result of calling `MarkdownRecordReader(MemoryStore(files))`.

`tests/unit/infrastructure/test_markdown.py` lines 39 to 54:

```python
def test_an_adr_is_parsed_into_its_parts():
    adr = reader({"a.md": ADR}).read_adr("a.md")
    assert (adr.number, adr.title, adr.status, adr.superseded_by, adr.supersedes) == (
        9,
        "Pick a thing",
        "Superseded",
        10,
        4,
    )
    assert adr.context == "Facts: 5 of them, on two lines."
    assert adr.sections == ("Context", "Options considered", "Decision", "Consequences")
    assert [option.name for option in adr.options] == ["first way", "second way"]
    assert adr.options[0].advantage == "it is fast and cheap."
    assert adr.options[1].main_cost == ""
    assert (adr.good, adr.bad, adr.revisit_when) == ("fast", "new", "3 users complain")
    assert adr.decision.startswith("We will do")
```

> **In plain words.** `assert condition` checks that something is true. In a test, a false condition fails the test and pytest shows both sides of the comparison.
> **In plain words.** `==` tests equality, `is` tests that two names are the very same object (used for `None` and enum members), `in` tests membership.
> **In plain words.** A **tuple** `(a, b)` is a fixed list of values that cannot be changed.
> **In plain words.** A **list comprehension** `[x for x in items if test]` is a loop written inside brackets: it builds a new list from the items that pass the test.
> **In plain words.** `obj[key]` looks a value up by key or position.
> **In plain words.** A **dictionary** `{key: value}` maps keys to values.
> **In plain words.** A **test** is a function whose name starts with `test_`. pytest finds it, runs it, and reports a pass when no `assert` fails and nothing raises.

**Test `test_an_adr_is_parsed_into_its_parts`** checks: an adr is parsed into its parts.

Step by step:

- Stores the result of calling `reader({'a.md': ADR}).read_adr('a.md')` in `adr`.
- Checks that `(adr.number, adr.title, adr.status, adr.supersede…` equals `(9, 'Pick a thing', 'Superseded', 10, 4)`; if not, the test fails.
- Checks that `adr.context` equals `'Facts: 5 of them, on two lines.'`; if not, the test fails.
- Checks that `adr.sections` equals `('Context', 'Options considered', 'Decision', 'Co…`; if not, the test fails.
- Checks that `[option.name for option in adr.options]` equals `['first way', 'second way']`; if not, the test fails.
- Checks that `adr.options[0].advantage` equals `'it is fast and cheap.'`; if not, the test fails.
- Checks that `adr.options[1].main_cost` equals `''`; if not, the test fails.
- Checks that `(adr.good, adr.bad, adr.revisit_when)` equals `('fast', 'new', '3 users complain')`; if not, the test fails.
- Checks that `adr.decision.startswith('We will do')`; if not, the test fails.

`tests/unit/infrastructure/test_markdown.py` lines 57 to 59:

```python
def test_a_file_that_is_not_an_adr_parses_to_empty_parts():
    adr = reader({"a.md": "just words\n"}).read_adr("a.md")
    assert (adr.number, adr.title, adr.status, adr.options, adr.sections) == (None, "", "", (), ())
```

**Test `test_a_file_that_is_not_an_adr_parses_to_empty_parts`** checks: a file that is not an adr parses to empty parts.

Step by step:

- Stores the result of calling `reader({'a.md': 'just words\n'}).read_adr('a.md')` in `adr`.
- Checks that `(adr.number, adr.title, adr.status, adr.options, …` equals `(None, '', '', (), ())`; if not, the test fails.

`tests/unit/infrastructure/test_markdown.py` lines 62 to 64:

```python
def test_a_plain_status_is_kept_as_written():
    adr = reader({"a.md": ADR.replace("Superseded by ADR 0010", "Accepted")}).read_adr("a.md")
    assert (adr.status, adr.superseded_by) == ("Accepted", None)
```

**Test `test_a_plain_status_is_kept_as_written`** checks: a plain status is kept as written.

Step by step:

- Stores the result of calling `reader({'a.md': ADR.replace('Superseded by ADR 0010', 'Accepted')}).read_adr('a.md')` in `adr`.
- Checks that `(adr.status, adr.superseded_by)` equals `('Accepted', None)`; if not, the test fails.

`tests/unit/infrastructure/test_markdown.py` lines 67 to 71:

```python
def test_audience_versions_use_the_third_heading_as_the_sibling_team():
    text = "# Audience versions: ADR 0007\n\n## Engineers\nOne.\n\n## Manager\nTwo.\n\n## Billing team\nThree.\nMore.\n"
    versions = reader({"a.md": text}).read_audiences("a.md")
    assert (versions.adr_number, versions.engineers, versions.manager) == (7, "One.", "Two.")
    assert (versions.sibling_name, versions.sibling) == ("Billing team", "Three. More.")
```

**Test `test_audience_versions_use_the_third_heading_as_the_sibling_team`** checks: audience versions use the third heading as the sibling team.

Step by step:

- Stores the text `'# Audience versions: ADR 0007\n\n## Engineers\nOne.\n\n## …` in `text`.
- Stores the result of calling `reader({'a.md': text}).read_audiences('a.md')` in `versions`.
- Checks that `(versions.adr_number, versions.engineers, version…` equals `(7, 'One.', 'Two.')`; if not, the test fails.
- Checks that `(versions.sibling_name, versions.sibling)` equals `('Billing team', 'Three. More.')`; if not, the test fails.

`tests/unit/infrastructure/test_markdown.py` lines 74 to 76:

```python
def test_missing_audience_sections_parse_to_empty_text():
    versions = reader({"a.md": "# nothing\n"}).read_audiences("a.md")
    assert (versions.adr_number, versions.engineers, versions.sibling, versions.sibling_name) == (None, "", "", "")
```

**Test `test_missing_audience_sections_parse_to_empty_text`** checks: missing audience sections parse to empty text.

Step by step:

- Stores the result of calling `reader({'a.md': '# nothing\n'}).read_audiences('a.md')` in `versions`.
- Checks that `(versions.adr_number, versions.engineers, version…` equals `(None, '', '', '')`; if not, the test fails.

`tests/unit/infrastructure/test_markdown.py` lines 79 to 88:

```python
def test_a_reaction_log_is_parsed():
    text = (
        "# Reaction log: ADR 0007\n\nReader: an engineer\nReader kind: real\nADR: 0007\n\n"
        "## Said back\n> They send it once.\n> Always.\n\n## Misunderstood\nThey missed repeats.\n\n"
        '## Fix\nBefore: "old words."\nAfter: "new words."\n'
    )
    reaction = reader({"a.md": text}).read_reaction("a.md")
    assert (reaction.reader, reaction.reader_kind, reaction.adr_number) == ("an engineer", "real", 7)
    assert reaction.said_back == "They send it once. Always."
    assert (reaction.before, reaction.after) == ("old words.", "new words.")
```

**Test `test_a_reaction_log_is_parsed`** checks: a reaction log is parsed.

Step by step:

- Stores the text `'# Reaction log: ADR 0007\n\nReader: an engineer\nReader ki…` in `text`.
- Stores the result of calling `reader({'a.md': text}).read_reaction('a.md')` in `reaction`.
- Checks that `(reaction.reader, reaction.reader_kind, reaction.…` equals `('an engineer', 'real', 7)`; if not, the test fails.
- Checks that `reaction.said_back` equals `'They send it once. Always.'`; if not, the test fails.
- Checks that `(reaction.before, reaction.after)` equals `('old words.', 'new words.')`; if not, the test fails.

## Try it yourself

```bash
.venv/bin/pytest -q tests/unit/infrastructure
```
Prints a row of dots, one per passing test, and a summary line such as `N passed in 0.5s` (skipped tests show as `s`).

```bash
.venv/bin/mypy
```
Checks the whole project (the `files` setting in `pyproject.toml`), these files included. Prints `Success: no issues found in 36 source files`.

```bash
.venv/bin/ruff check tests/unit/infrastructure/test_filesystem_and_settings.py tests/unit/infrastructure/test_markdown.py
```
Prints `All checks passed!`.

## Mistakes people make

- Tests that depend on each other's order. Each test here builds its own data.
- Asserting only the happy path. These tests also break the input on purpose and check the exact rule that fails.
- Forgetting `test_` in a name, so the test never runs.

## Check yourself

1. What does the test `test_the_store_lists_only_markdown_files_in_one_folder` check?
   **Answer:** it checks: the store lists only markdown files in one folder.
2. What does the test `test_the_store_writes_creates_folders_and_reads_back` check?
   **Answer:** it checks: the store writes creates folders and reads back.
3. What does the test `test_the_store_refuses_to_leave_its_root` check?
   **Answer:** it checks: the store refuses to leave its root.
4. What does the test `test_settings_have_defaults` check?
   **Answer:** it checks: settings have defaults.
5. What does the test `test_settings_read_the_environment` check?
   **Answer:** it checks: settings read the environment.

## Further reading

- pytest 9.1 documentation: <https://docs.pytest.org/en/stable/>
- How to use fixtures: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- `assert` rewriting: <https://docs.pytest.org/en/stable/how-to/assert.html>
