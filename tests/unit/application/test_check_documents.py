from pathlib import Path

from adr_toolkit.application.check_documents import CheckSettings, check_documents, current_log, write_log
from adr_toolkit.application.reporting import render_markdown, render_text
from adr_toolkit.domain.findings import Report
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from tests.conftest import REPOSITORY_ROOT, MemoryStore


def repo_files() -> dict[str, str]:
    files: dict[str, str] = {}
    for path in REPOSITORY_ROOT.glob("docs/**/*.md"):
        files[path.relative_to(REPOSITORY_ROOT).as_posix()] = Path(path).read_text()
    return files


def run(files: dict[str, str], required=(7,)):
    store = MemoryStore(files)
    return check_documents(store, MarkdownRecordReader(store), CheckSettings(required_adrs=required))


def codes(report) -> set[str]:
    return {finding.code for finding in report.findings}


def test_the_repository_documents_pass():
    report = run(repo_files())
    assert report.ok
    assert {f.code for f in report.warnings} == {"REA004"}
    assert len(report.subjects) == 6


def test_a_required_record_that_does_not_exist_is_reported():
    assert "DOC001" in codes(run(repo_files(), required=(9,)))


def test_missing_companions_are_reported():
    files = repo_files()
    del files["docs/communication/0007-audiences.md"]
    del files["docs/review/0007-reaction.md"]
    assert codes(run(files)) == {"DOC002"}


def test_a_missing_log_is_reported():
    files = repo_files()
    del files["docs/decision-log.md"]
    assert codes(run(files)) == {"LOG001", "REA004"}


def test_a_stale_log_is_reported_and_write_log_repairs_it():
    files = repo_files()
    files["docs/decision-log.md"] = "old\n"
    store = MemoryStore(files)
    reader = MarkdownRecordReader(store)
    assert "LOG001" in codes(check_documents(store, reader, CheckSettings(required_adrs=(7,))))
    write_log(store, reader)
    assert store.files["docs/decision-log.md"] == current_log(store, reader)
    assert "LOG001" not in codes(check_documents(store, reader, CheckSettings(required_adrs=(7,))))


def test_a_fix_logged_but_not_made_is_reported():
    files = repo_files()
    files["docs/adr/0007-announce-paid-orders.md"] = files["docs/adr/0007-announce-paid-orders.md"].replace(
        "a stuck relay delays every consumer, and the relay can publish an event twice, "
        "so consumers must ignore repeats by order id.",
        "and a stuck relay delays every consumer.",
    )
    assert {"REA002", "REA003"} <= codes(run(files))


def test_text_and_markdown_reports_carry_the_verdict():
    report = run(repo_files())
    assert render_text(report).splitlines()[-1] == "OK: 6 documents checked, 0 errors, 1 warnings"
    markdown = render_markdown(report)
    assert "**Verdict:** OK" in markdown
    assert "REA004" in markdown
    broken = run({})
    assert "FAILED" in render_text(broken)
    assert "None." in render_markdown(Report(subjects=(), findings=()))
