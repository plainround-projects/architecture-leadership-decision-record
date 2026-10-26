"""The use case behind `adr-toolkit check`: every rule over every document."""

from __future__ import annotations

from dataclasses import dataclass, field

from adr_toolkit.application.ports import DocumentStore, RecordReader
from adr_toolkit.domain.adr import Adr, AdrLimits, check_adr
from adr_toolkit.domain.audiences import check_audiences
from adr_toolkit.domain.decision_log import check_links, render_log
from adr_toolkit.domain.findings import Finding, Report, error
from adr_toolkit.domain.reaction import check_reaction, check_talk

ADR_FOLDER = "docs/adr"
COMMUNICATION_FOLDER = "docs/communication"
REVIEW_FOLDER = "docs/review"
TALK_FOLDER = "docs/talk"
LOG_PATH = "docs/decision-log.md"


@dataclass(frozen=True)
class CheckSettings:
    """Which records must come with audience versions, a reaction log and a talk."""

    limits: AdrLimits = field(default_factory=AdrLimits)
    required_adrs: tuple[int, ...] = ()


def load_records(store: DocumentStore, reader: RecordReader) -> list[Adr]:
    """Every decision record in `docs/adr`, parsed."""
    return [reader.read_adr(path) for path in store.list_paths(ADR_FOLDER)]


def check_documents(store: DocumentStore, reader: RecordReader, settings: CheckSettings) -> Report:
    """Check the records, the links between them, the audience versions, the reaction logs, the talks and the log."""
    records = load_records(store, reader)
    findings: list[Finding] = []
    subjects = [record.path for record in records]
    for record in records:
        findings.extend(check_adr(record, settings.limits))
    findings.extend(check_links(records))
    by_number = {record.number: record for record in records if record.number is not None}
    for number in settings.required_adrs:
        required = by_number.get(number)
        if required is None:
            findings.append(error("DOC001", f"ADR {number:04d}", "a required record does not exist"))
            continue
        findings.extend(_companions(store, reader, required, subjects))
    findings.extend(_log_is_current(store, records))
    return Report(tuple(subjects), tuple(findings))


def _companions(store: DocumentStore, reader: RecordReader, record: Adr, subjects: list[str]) -> list[Finding]:
    assert record.number is not None
    prefix = f"{record.number:04d}"
    record_text = store.read_text(record.path)
    found: list[Finding] = []
    audiences = f"{COMMUNICATION_FOLDER}/{prefix}-audiences.md"
    reaction = f"{REVIEW_FOLDER}/{prefix}-reaction.md"
    talk = f"{TALK_FOLDER}/{prefix}-three-minute-talk.md"
    for path in (audiences, reaction):
        if not store.exists(path):
            found.append(error("DOC002", record.path, f"ADR {prefix} has no {path}"))
    if store.exists(audiences):
        subjects.append(audiences)
        found.extend(check_audiences(reader.read_audiences(audiences), record.decision))
    if store.exists(reaction):
        subjects.append(reaction)
        found.extend(check_reaction(reader.read_reaction(reaction), record_text))
    if store.exists(talk):
        subjects.append(talk)
        found.extend(check_talk(talk, store.read_text(talk)))
    return found


def _log_is_current(store: DocumentStore, records: list[Adr]) -> list[Finding]:
    if not store.exists(LOG_PATH):
        return [error("LOG001", LOG_PATH, "the decision log does not exist; run `adr-toolkit log --write`")]
    if store.read_text(LOG_PATH) != render_log(records):
        return [error("LOG001", LOG_PATH, "the decision log is out of date; run `adr-toolkit log --write`")]
    return []


def current_log(store: DocumentStore, reader: RecordReader) -> str:
    """The decision log as the records say it should read today."""
    return render_log(load_records(store, reader))


def write_log(store: DocumentStore, reader: RecordReader) -> str:
    """Regenerate `docs/decision-log.md` and return its text."""
    text = current_log(store, reader)
    store.write_text(LOG_PATH, text)
    return text
