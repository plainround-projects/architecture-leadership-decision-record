# architecture-leadership-decision-record

A decision record for one real choice (how an orders service announces paid orders), told three ways for three readers, plus a small toolkit that lints the record, its audience versions, its reaction log and its talk, and keeps a decision log of what superseded what.

| | |
| --- | --- |
| **Lesson** | `/prep/architecture-leadership/project-decision-record`, "A decision record and its communication" (`data-structure-explainer/src/content/tracks/architecture-leadership/13-project-decision-record.md` in the Plainround app) |
| **Planned hours** | 4 |
| **Level** | Beginner |
| **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md), the records: [docs/adr](docs/adr), the log: [docs/decision-log.md](docs/decision-log.md) |

The lesson says "nothing here is code; the deliverables are documents". Both halves are real here: the documents are the lesson's deliverables, and the toolkit is what turns each "Done when" line from a judgment into a check you can run, so the records cannot drift into advertising, straw men or one paragraph copied three times.

## Prerequisites

| Tool | Version | Used for |
| --- | --- | --- |
| Python | 3.12 or 3.13 (tested with 3.13.12; the CI uses 3.12) | the toolkit and its tests |
| GNU Make | 3.81 or newer | every command below |
| Python packages | none at run time (standard library only); pytest, pytest-cov, ruff, mypy, import-linter and pip-audit for development, pinned with hashes in `requirements-dev.lock`; `make` installs them into `.venv/` | development |

No Docker, no cloud account, no network after the install. All settings are environment variables with defaults, listed in `.env.example`; `make up` copies it to `.env` the first time.

## Setup, run, test, stop

```bash
make up          # create .venv from the hash-pinned lock file and copy .env.example to .env
make run         # run every document check, then write build/report.md
make test        # unit and integration tests with coverage (domain and application at 95% or more)
make lint        # ruff, ruff format, mypy --strict, import-linter, then the document checks
make audit       # pip-audit over the locked dependencies
make check       # lint and test, what the CI runs first
make down        # remove build/ (nothing is running, so there is nothing to stop)
```

Other commands: `.venv/bin/adr-toolkit log` prints the decision log, and `.venv/bin/adr-toolkit log --write` regenerates [docs/decision-log.md](docs/decision-log.md) after you add or change a record (`check` fails while the file is stale). `make help` lists every target.

`make run` on a fresh clone prints:

```text
.venv/bin/adr-toolkit check
WARNING REA004 docs/review/0007-reaction.md: reader kind is 'worked-example': this is a worked example; replace it with a real reading
OK: 6 documents checked, 0 errors, 1 warnings
.venv/bin/adr-toolkit report
wrote build/report.md
```

## The documents

| Path | What it is | Lesson step |
| --- | --- | --- |
| [docs/adr/0007-announce-paid-orders.md](docs/adr/0007-announce-paid-orders.md) | The lesson's record: three honest options, the decision, the consequences with a bad result and a trigger. | 1 to 4 |
| [docs/communication/0007-audiences.md](docs/communication/0007-audiences.md) | The same decision for engineers, a manager and the Warehouse team. | 5 |
| [docs/review/0007-reaction.md](docs/review/0007-reaction.md) | What a reader misunderstood, and the sentence that changed because of it. | 6 |
| [docs/talk/0007-three-minute-talk.md](docs/talk/0007-three-minute-talk.md) | The decision as a talk of about 360 words (stretch). | stretch |
| [docs/adr/0005-announce-paid-orders-by-polling.md](docs/adr/0005-announce-paid-orders-by-polling.md) | The record the old polling worker should have had; ADR 0007 supersedes it (stretch). | stretch |
| [docs/adr/0006-index-the-paid-orders.md](docs/adr/0006-index-the-paid-orders.md) | An interim decision taken while 0007 was open. | stretch |
| [docs/decision-log.md](docs/decision-log.md) | Generated: every record, and which one replaced which. | stretch |
| [templates/adr-template.md](templates/adr-template.md) | A blank record in the format the linter checks. | |

## The checks

`adr-toolkit check` applies these rules. A rule with a code fails the run; the two warnings are reported only.

| Codes | What they check |
| --- | --- |
| ADR001 to ADR005 | Title `# ADR NNNN: ...`, status (Proposed, Accepted, Superseded by ADR NNNN), ISO date, named deciders, the four sections in order. |
| ADR006 to ADR008 | At least two options; each with an advantage, a main cost and a "Pick it if" line of real length; no two options with the same name or advantage. |
| ADR009, ADR010 | The context holds a number, and argues for no answer ("we will", "so we need", "Option A"). |
| ADR011, ADR012, ADR017 | The decision reads "We will ..., because ...", gives one reason, and names one of the options considered. |
| ADR013 to ADR015 | A good and a bad consequence; a "Revisit when" trigger that holds a number and is not "if needed" or "if it stops working". |
| ADR016 | One page: at most 70 non-blank lines and 600 words (`ADR_MAX_LINES`, `ADR_MAX_WORDS`). |
| ADR018 (warning) | A record still Proposed. |
| ADR100 to ADR103 | Supersession points at a real record, and the replaced record and its successor both say so. |
| AUD001 to AUD008 | Three versions exist. Engineers: 3 to 8 sentences that describe the chosen mechanism. Manager: at most two sentences, a number in each, none of the engineers' words. Sibling team: a date in the first sentence, an action, none of the internal words. No sentence or paragraph repeated across versions. |
| REA001 to REA003 | The reaction log names the reader, what they said back and what they misunderstood, and the "After" sentence is in the record while the "Before" sentence is gone. |
| REA004 (warning) | The reaction is a worked example, not a real reading. |
| TLK001 | The talk is between 150 and 400 words. |
| DOC001, DOC002, LOG001 | A required record, its companions and an up-to-date decision log exist. |

## Done when: the lesson's checklist and the proof for each line

The lesson has one "Done when" per step. Four of them contain a judgment no program can make (a reasonable person would choose differently; the advocate feels fairly represented). For those, the toolkit enforces what can be checked and the review checklist in the lesson covers the rest; each row says which part is which.

| # | Done when (from the lesson) | Command | What proves it |
| --- | --- | --- | --- |
| 1 | You can name at least two options that each have a genuine advantage. | `make run`; `pytest tests/integration/test_done_when.py -k done_when_1` | ADR 0007 has options A, B and C, each with an "Advantage:" line of real length (ADR006, ADR007, ADR008 pass). The test blanks one advantage and the run fails with ADR007. That the advantages are genuine (each has a champion) is the lesson's checklist question; the record names the champions in the talk. |
| 2 | A reader who disagrees with your choice would still agree the context is accurate. | `make run`; `pytest ... -k done_when_2` | The context holds figures (2,000 to 40,000 orders a day, 6 seconds, 25 seconds, 6 engineers, 10 weeks) and no answer: ADR009 fails a context with no number, ADR010 fails one containing "so we need" or "Option C". Whether the facts are accurate to a skeptic is for the real reader of step 6. |
| 3 | Each option is described well enough that its advocate would feel fairly represented. | `make run`; `pytest ... -k done_when_3` | Every option uses the same three lines (advantage, main cost, pick it if), each of real length, in terms of the team. Removing a line fails ADR007. Fairness to the advocate is again the reader's call. |
| 4 | The record lists at least one negative consequence of the chosen option and a trigger that would make you revisit it. | `make run`; `pytest ... -k done_when_4` | ADR 0007 has `Bad:` (one more table and a relay, a stuck relay delays every consumer, the relay can publish twice) and `Revisit when:` "the relay's backlog is over 1,000 events for more than 5 minutes, or a third consumer needs ordering guarantees". Deleting the Bad line fails ADR013; replacing the trigger with "it stops working well" fails ADR015. |
| 5 | None of the three versions repeats jargon the audience would not use, and each answers that audience's first question. | `make run`; `pytest ... -k done_when_5` | [0007-audiences.md](docs/communication/0007-audiences.md): the manager version is two sentences with a number each and no engineer's word (AUD004 to AUD006); the Warehouse note opens with a date, "From 3 November", and an action (AUD007); copying one paragraph into two versions fails AUD008. |
| 6 | The record is updated for the one thing a reader got wrong, and you record what it was. | `make run`; `pytest ... -k done_when_6` | [0007-reaction.md](docs/review/0007-reaction.md) quotes the sentence before and after; REA002 and REA003 prove the "After" sentence is in ADR 0007 and the "Before" sentence is not. **Not built as a real reading:** the file is marked `Reader kind: worked-example` and the run prints warning REA004 until you replace it with a real session (see below). |

### What could not be built

Step 6 needs a real person who was not in the room. A program cannot be that reader and inventing one would be a false record, so the repository ships a worked example, labeled as one, whose misunderstanding is plausible and whose fix is real (the relay can publish twice, which the first draft never said). To finish step 6: show ADR 0007 to someone, ask them to say it back, write what they said under "Said back" and "Misunderstood", fix the record, quote the sentence before and after under "Fix", set `Reader kind: real`, and run `make run`. The warning disappears.

## Stretch goals

| Stretch (from the lesson) | Built? |
| --- | --- |
| Add a small decision log that links several ADRs and shows how one superseded another. | Yes. ADR 0005 is superseded by ADR 0007; [docs/decision-log.md](docs/decision-log.md) is generated from the records and `check` fails when it is stale (ADR100 to ADR103, LOG001). |
| Record the decision as a short talk and keep it to three minutes. | Yes. [The talk](docs/talk/0007-three-minute-talk.md) is 361 words; TLK001 fails above 400. |
| Revisit an old decision of yours and write the ADR it should have had. | Yes, with a made-up history: ADR 0005 is written late, in the voice of the March 2025 team, and its own trigger ("a scan takes longer than 5 seconds, or orders pass 20,000 a day") is the one that fired. |

## What is simplified for teaching

- One scenario, the lesson's sample; the dates and numbers are the lesson's. The deciders are roles, not people.
- The reaction log is a worked example, not a real reading (above).
- The toolkit checks form, not truth: it cannot tell whether an advantage is genuine or an advocate would agree. Its limits are listed in [ARCHITECTURE.md](ARCHITECTURE.md).
- No Docker image and no service: nothing here serves traffic.

## Project structure

```text
src/adr_toolkit/
  domain/            records, findings, and the rules (adr, audiences, reaction, decision_log, text).
                     Depends on the standard library only.
  application/       the check and log use cases, the report formatting, and the ports
                     (DocumentStore, RecordReader). Depends on domain only.
  infrastructure/    the file-system store, the Markdown parsers, settings from the environment.
                     Depends on application and domain.
  interfaces/        the adr-toolkit command line. Wires adapters into use cases; owns exit codes.
                     Nothing depends on it.
docs/
  adr/               the decision records (0005 superseded, 0006, 0007).
  communication/     the three audience versions of ADR 0007.
  review/            the reaction log.
  talk/              the three-minute talk.
  decision-log.md    generated.
templates/           the blank record.
tests/
  unit/              domain, application (in-memory store), infrastructure, command line.
  integration/       one test per "Done when" line, over copies of the real documents.
pyproject.toml       metadata and every tool's configuration.   requirements*.lock  hash-pinned dependencies.
Makefile             the only commands a reader needs.          .github/workflows/ci.yml  the same checks on push.
```

The dependency rule (domain depends on nothing; application on domain; infrastructure and interfaces on both; nothing on interfaces) is enforced by `make lint` through import-linter.

## Author and license

Written by Sumit Srivastava. Released under the MIT License, see [LICENSE](LICENSE). Changes are in [CHANGELOG.md](CHANGELOG.md).
