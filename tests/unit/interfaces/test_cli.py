import shutil
from pathlib import Path

import pytest

from adr_toolkit.interfaces.cli import main
from tests.conftest import REPOSITORY_ROOT


@pytest.fixture
def copy_of_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    shutil.copytree(REPOSITORY_ROOT / "docs", tmp_path / "docs")
    monkeypatch.setenv("ADR_ROOT", str(tmp_path))
    monkeypatch.setenv("ADR_REQUIRED_COMMUNICATION", "7")
    monkeypatch.setenv("REPORT_DIR", "build")
    return tmp_path


def test_check_passes_on_the_repository_documents(copy_of_repo, capsys):
    assert main(["check"]) == 0
    assert capsys.readouterr().out.splitlines()[-1].startswith("OK: 6 documents")


def test_check_fails_when_the_bad_consequence_is_removed(copy_of_repo, capsys):
    adr = copy_of_repo / "docs/adr/0007-announce-paid-orders.md"
    adr.write_text("\n".join(line for line in adr.read_text().splitlines() if not line.startswith("Bad:")) + "\n")
    assert main(["check"]) == 1
    assert "ADR013" in capsys.readouterr().out


def test_report_writes_markdown(copy_of_repo, capsys):
    assert main(["report"]) == 0
    assert (copy_of_repo / "build/report.md").read_text().startswith("# Decision record report")


def test_log_prints_and_writes(copy_of_repo, capsys):
    assert main(["log"]) == 0
    assert "# Decision log" in capsys.readouterr().out
    (copy_of_repo / "docs/decision-log.md").write_text("stale\n")
    assert main(["log", "--write"]) == 0
    assert "stale" not in (copy_of_repo / "docs/decision-log.md").read_text()


def test_a_bad_setting_exits_with_2(monkeypatch, capsys):
    monkeypatch.setenv("ADR_MAX_LINES", "lots")
    assert main(["check"]) == 2
    assert "ADR_MAX_LINES" in capsys.readouterr().err
