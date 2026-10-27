# Markdown (the document format)

## What it is

Markdown is a way to write formatted text in a plain text file. A line starting with `#` is a heading (more `#` means
a smaller heading), `- ` starts a bullet, `1. ` starts a numbered list, `|` draws a table, and three backticks around
lines mark a block of code. GitHub and most editors show it formatted; as plain text it is still easy to read.

## Why this repository uses it

The lesson's deliverables are documents. They are Markdown so they diff and review like code. The toolkit then reads
those same files, so the documents are not only written but **checked**: a rule fails when a required part is
missing.

## Where it appears

| File | What it does with this technology |
| --- | --- |
| `docs/adr/*.md` | Decision records: `# ADR 0007: title`, header lines, `## Context`, `## Options considered`, `## Decision`, `## Consequences`. |
| `docs/communication/0007-audiences.md` | The same decision for engineers, a manager and a sibling team. |
| `docs/review/0007-reaction.md` | What a reader said back and what changed. |
| `docs/talk/0007-three-minute-talk.md` | The spoken version. |
| `docs/decision-log.md` | Generated table of all records (do not edit by hand). |
| `templates/adr-template.md` | The empty record. |
| `build/report.md` | The generated report. |

## How it works underneath

Markdown has no schema. This repository adds a small convention on top: second-level headings (`## Name`) mark
sections, `Label: text` lines hold fields, and tables hold lists of items. The parser reads the file as lines, groups
the lines under each heading, and picks out fields and rows with the regular expressions in `re.md`. It does not turn
Markdown into HTML; it only extracts the parts the rules need.

## Walkthrough of this repository's use

### A real document

`docs/adr/0007-announce-paid-orders.md`:

```markdown
# ADR 0007: How the orders service announces paid orders

Status: Accepted
Date: 2026-10-22
Deciders: Orders tech lead, database owner, Warehouse team lead
Supersedes: ADR 0005

## Context
Orders are announced by a worker that scans the orders table every 10 seconds for paid rows. Volume grew from 2,000 to 40,000 orders a day. A scan now takes about 6 seconds, so confirmation emails arrive up to 25 seconds late, and the database owner has asked us to reduce the load. The Warehouse team needs the same event. The team has 6 engineers and no one has run a message broker. Black Friday is in 10 weeks and the tooling budget is small. Orders must never be announced twice to the stock system, and must never be lost.

## Options considered
### Option A: keep polling, make it cheap
Advantage: nothing new to run; it ships this week.
Main cost: the Warehouse team polls too, so load grows with every new reader, and latency stays at the poll interval.
```

- The first line is the document's title (`#`).
- The lines `Label: value` are **fields**. The parser reads them with a pattern for the known labels.
- Each `##` line starts a **section**. The checker knows which sections must exist.
- `### Option A: ...` is a third-level heading that starts one option.

### How the parser groups lines

`src/adr_toolkit/infrastructure/markdown.py`:

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

`_sections` walks the lines. A line matching `## ...` starts a new group; every other line is added to the current group. The first group, named empty, holds anything before the first heading.

Rule codes such as `ADR013` or `PLN002` come from the checks that read these files; the README lists them. The
integration test `tests/integration/test_done_when.py` damages a copy of a document on purpose and checks that
the matching code appears.

## Try it yourself

```bash
head -12 docs/adr/0007-announce-paid-orders.md
```
Shows the top of a real document in this repository.

```bash
make run
```
Reads every document and prints `OK: N documents checked, 0 errors, ...` (a warning line may appear).

An experiment on a copy, outside the repository:

```bash
rm -rf /tmp/doc-experiment && mkdir /tmp/doc-experiment && cp -r docs /tmp/doc-experiment/
sed -i.bak 's/^Bad:/Worse:/' /tmp/doc-experiment/docs/adr/0007-announce-paid-orders.md
ADR_ROOT=/tmp/doc-experiment ADR_REQUIRED_COMMUNICATION=7 .venv/bin/adr-toolkit check | tail -3; echo "exit: ${PIPESTATUS[0]}"
```
The checker prints a finding with the code `ADR013` (the record lost its `Bad:` consequence) and the exit status is 1.

```bash
grep -c '^## ' docs/adr/0007-announce-paid-orders.md
```
Counts the sections of a document.

## Mistakes people make

- **Trailing spaces in Markdown** can mean a hard line break; `.editorconfig` leaves them alone in `*.md` for that reason.
- **Renaming a section heading** in a document, which makes the checker report it missing.
- **Editing generated files** (`docs/decision-log.md`, `build/report.md`) by hand. The next run overwrites them.
- **Mixing tabs and spaces in a table**, which breaks the cell split.

## Check yourself

1. What marks a section in these documents?
   **Answer:** A second-level heading, `## Name`.
2. How are fields written?
   **Answer:** As `Label: text` lines.
3. What does the second row of a Markdown table do?
   **Answer:** It separates the header from the data rows (`| --- |`); the parser skips it.
4. Why does the checker read Markdown instead of rendering it?
   **Answer:** It needs the parts (sections, fields, rows) to apply rules, not the look.
5. Why is `docs/decision-log.md` not edited by hand?
   **Answer:** It is generated by `adr-toolkit log --write`; a stale copy fails the check.

## Further reading

- CommonMark specification: <https://spec.commonmark.org/0.31.2/>
- GitHub Flavored Markdown (tables): <https://github.github.com/gfm/>
