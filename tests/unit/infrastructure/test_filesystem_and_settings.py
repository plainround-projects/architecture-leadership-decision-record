import pytest

from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.settings import SettingsError, load_settings


def test_the_store_lists_only_markdown_files_in_one_folder(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "b.md").write_text("b")
    (tmp_path / "docs" / "a.md").write_text("a")
    (tmp_path / "docs" / "c.txt").write_text("c")
    (tmp_path / "docs" / "sub").mkdir()
    store = FileSystemStore(tmp_path)
    assert store.list_paths("docs") == ["docs/a.md", "docs/b.md"]
    assert store.list_paths("missing") == []


def test_the_store_writes_creates_folders_and_reads_back(tmp_path):
    store = FileSystemStore(tmp_path)
    assert not store.exists("build/report.md")
    store.write_text("build/report.md", "hello")
    assert store.exists("build/report.md")
    assert store.read_text("build/report.md") == "hello"


def test_the_store_refuses_to_leave_its_root(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        FileSystemStore(tmp_path).read_text("../secret.md")


def test_settings_have_defaults():
    settings = load_settings({})
    assert (settings.report_dir, settings.check.limits.max_lines, settings.check.required_adrs) == ("build", 70, ())


def test_settings_read_the_environment():
    env = {"ADR_ROOT": "x", "ADR_MAX_LINES": "40", "ADR_MAX_WORDS": "300", "ADR_REQUIRED_COMMUNICATION": "7, 9"}
    settings = load_settings(env)
    assert (str(settings.root), settings.check.limits.max_words, settings.check.required_adrs) == ("x", 300, (7, 9))


@pytest.mark.parametrize(
    "env",
    [{"ADR_MAX_LINES": "many"}, {"ADR_MAX_WORDS": "0"}, {"ADR_REQUIRED_COMMUNICATION": "seven"}],
)
def test_bad_settings_are_rejected_with_the_name(env):
    with pytest.raises(SettingsError):
        load_settings(env)
