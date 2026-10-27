# Regular expressions (the re module)

## What it is

A **regular expression** (regex) is a short pattern that describes a set of strings, like `^## (.+)$` for "a line
that starts with `## `". Python's standard `re` module compiles a pattern into an object you can use to **match** a
string, **search** inside it, **find all** matches or **split** it. Parentheses in a pattern make **groups** whose text
you can read back.

## Why this repository uses it

The documents are Markdown text with simple conventions (`## Heading`, `Label: text`, `Phase 3: name`). The
program recognizes them with a handful of regexes and turns them into typed values. The patterns are compiled once, as
module-level constants with a leading underscore.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `src/adr_toolkit/infrastructure/markdown.py` | Recognizes the title, the `Label: text` lines and the headings. |
| `src/adr_toolkit/domain/text.py` | Splits sentences and finds words. |
| `src/adr_toolkit/domain/*.py` | The rules use word lists and these helpers. |

## How it works underneath

`re.compile(pattern)` turns the pattern into a small program for matching. `pattern.match(line)` tries to match from
the **start** of the string and returns a match object or `None`. `pattern.search(text)` looks anywhere. A match
object's `.group(1)` is the text of the first parenthesized part. The symbols used here:

| Symbol | Meaning |
| --- | --- |
| `^` and `$` | start and end of the text |
| `.` | any one character |
| `+`, `*`, `?` | one or more, zero or more, optional |
| `+?`, `.*?` | the same but **lazy**: as few characters as possible |
| `\d`, `\s` | a digit, a whitespace character |
| `[A-Z0-9]` | one character from a set |
| `( ... )` | a group to capture |
| `a|b` | a or b |
| `(?<=x)`, `(?=x)` | look-behind and look-ahead: x must come before or after, but is not part of the match |
| `\.` | a literal dot (a backslash cancels a symbol's meaning) |

A string written `r"..."` is a **raw string**: backslashes are kept as they are, which is what patterns need.

## Walkthrough of this repository's use

`src/adr_toolkit/infrastructure/markdown.py`:

```python
_TITLE = re.compile(r"^# ADR (\d+): (.+?)\s*$")
_META = re.compile(r"^(Status|Date|Deciders|Supersedes):\s*(.*?)\s*$")
_SUPERSEDED_BY = re.compile(r"^Superseded by ADR (\d+)$")
_ADR_REF = re.compile(r"^ADR (\d+)$")
_HEADING2 = re.compile(r"^## (.+?)\s*$")
_HEADING3 = re.compile(r"^### (.+?)\s*$")
_OPTION_NAME = re.compile(r"^Option [A-Z]: (.+)$")
```

- `_TITLE = r"^# ADR (\d+): (.+?)\s*$"` matches the first line of a record, like `# ADR 0007: How the orders service
  announces paid orders`. `^# ADR ` is the fixed start. `(\d+)` is group 1: one or more digits (`0007`).
  `: ` is fixed. `(.+?)` is group 2: the title, as few characters as possible (lazy). `\s*$` allows trailing spaces
  before the end.
- `_META` matches `Status: Accepted`, `Date: ...`, `Deciders: ...`, `Supersedes: ...`: one of four labels (the
  `|` means "or"), a colon, optional spaces, then the rest of the line lazily.
- `_SUPERSEDED_BY` matches `Superseded by ADR 0007`; `_ADR_REF` matches `ADR 0005`. Both capture the number.
- `_HEADING2` and `_HEADING3` match `## Context` and `### Option A: ...` and capture the heading text.
- `_OPTION_NAME` matches `Option A: keep polling`: the word Option, one capital letter, a colon, then the name.

`src/adr_toolkit/infrastructure/markdown.py`:

```python
    pattern = re.compile(rf"^({'|'.join(re.escape(label) for label in labels)}):\s*(.*)$")
```

This builds a pattern **while the program runs**. `rf"..."` is a raw f-string: raw for the backslashes, f for the
braces. `'|'.join(re.escape(label) for label in labels)` joins the label names with `|` after `re.escape` has made
any special character in a name harmless. For the labels `Good`, `Bad`, `Revisit when` the result is
`^(Good|Bad|Revisit\ when):\s*(.*)$`.

`src/adr_toolkit/domain/text.py`:

```python
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
```

- `_SENTENCE_BREAK = (?<=[.!?])\s+(?=[A-Z0-9\"'(])` finds the whitespace **between** sentences: whitespace that comes
  right after a `.`, `!` or `?` (look-behind) and right before a capital letter, digit, quote or bracket
  (look-ahead). Look-around parts are checked but not consumed, so splitting on it removes only the spaces and keeps
  the full stops.
- `_WORD = [A-Za-z0-9][A-Za-z0-9'-]*` is a word: a letter or digit, then any number of letters, digits, apostrophes
  or hyphens (so `relay's` is one word).

`src/adr_toolkit/domain/text.py`:

```python
def sentences(text: str) -> list[str]:
    """Split prose into sentences. Lists and labels in the documents end with a full stop on purpose."""
    flat = squash(text)
    return [part for part in _SENTENCE_BREAK.split(flat) if part] if flat else []
```

`.split(flat)` cuts the text at each match; `if part` drops empty pieces.

## Try it yourself

```bash
.venv/bin/python -c "from adr_toolkit.infrastructure.markdown import _TITLE; m = _TITLE.match('# ADR 0007: How we announce'); print(m.group(1), '|', m.group(2))"
```
Prints `0007 | How we announce`.

```bash
.venv/bin/python -c "from adr_toolkit.domain.text import sentences; print(sentences('One. Two! Three? four'))"
```
Prints `['One.', 'Two!', 'Three? four']`: the split happens before `Two` and `Three` (capitals) but not before `four`.

```bash
.venv/bin/python -c "import re; print(re.findall(r\"[A-Za-z0-9][A-Za-z0-9'-]*\", \"The relay's backlog, 1,000\"))"
```
Prints `['The', "relay's", 'backlog', '1', '000']`.

```bash
.venv/bin/python -c "import re; print(re.match(r'^(.+?)\\s*$', 'abc   ').group(1) + '|')"
```
Prints `abc|`: the lazy group stops before the trailing spaces.

## Mistakes people make

- **Forgetting `r` before the string**, so `\d` is read as a plain `d` with a warning.
- **Greedy matching** that grabs too much: `.+` versus `.+?`.
- **Using `match` when `search` is needed** (`match` only matches at the start).
- **Parsing nested structure with a regex.** Here the patterns recognize single lines, and the code groups lines itself.
- **Not escaping user text** when it is placed inside a pattern. `re.escape` does that (used in the field parser).

## Check yourself

1. What do the two `^` and `$` in `_TITLE` anchor?
   **Answer:** The start and the end of the line, so the whole line must fit the pattern.
2. What does `(.+?)` capture?
   **Answer:** One or more characters, as few as possible, up to whatever the pattern needs next.
3. What is a look-behind such as `(?<=[.!?])`?
   **Answer:** A check that certain text comes right before, without including it in the match.
4. Why is the field pattern built with `re.escape`?
   **Answer:** So a label with special characters is matched literally.
5. What does `pattern.match(line)` return when nothing matches?
   **Answer:** `None`.

## Further reading

- `re` (Python 3.12): <https://docs.python.org/3.12/library/re.html>
- Regular Expression HOWTO: <https://docs.python.org/3.12/howto/regex.html>
