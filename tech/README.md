# Technology notes: Decision record toolkit

These notes teach every technology used by `architecture-leadership-decision-record`, from zero, through this repository's own files. Each note says what the technology is, why the repository uses it, where it appears, how it works underneath, walks through the repository's own lines, and ends with commands to try, common mistakes, five questions with answers, and links to the official documentation for the pinned version.

## Reading order

Read the language first, then the build tool, then the runtime pieces, then the tests and the checks.

1. [python.md](python.md): Python: the language the whole program is written in; read this first.
2. [python-standard-library.md](python-standard-library.md): Standard library: `enum`, `typing`, `collections`, `os`, `sys`, `shutil`, `datetime`, `itertools`.
3. [dataclasses.md](dataclasses.md): `dataclasses`: the small frozen value types (`Finding`, `Report`, settings, parsed documents).
4. [re.md](re.md): `re`: the patterns that find headings, labels, numbers and sentences in Markdown text.
5. [argparse.md](argparse.md): `argparse` and exit codes: how `adr-toolkit` reads its subcommands and reports success.
6. [pathlib.md](pathlib.md): `pathlib`: how the program reads and writes files, and refuses to leave the repository root.
7. [markdown.md](markdown.md): Markdown: the format of every deliverable document, and of the conventions the checker reads.
8. [toml.md](toml.md): TOML: the format of `pyproject.toml`.
9. [bash.md](bash.md): Shell: the small command-line programs (`grep`, `sed`, `sort`, `cp`, `rm`, `touch`, `command -v`) that the Makefile recipes run.
10. [make.md](make.md): Make: `Makefile`, the one place that names every command (`make run`, `make test`, `make lint`).
11. [venv-and-pip.md](venv-and-pip.md): venv and pip: the private `.venv/` folder and the installer that fills it from the lock file.
12. [setuptools.md](setuptools.md): setuptools and `pyproject.toml` packaging: how `src/adr_toolkit` becomes an installable project with a `adr-toolkit` command.
13. [hash-pinned-lock-files.md](hash-pinned-lock-files.md): Lock files: `requirements-dev.lock` and `requirements.lock`, the exact packages and file hashes pip installs.
14. [env-files.md](env-files.md): `.env` files: how settings reach the program (`.env.example` is committed, `.env` is local).
15. [pytest.md](pytest.md): pytest: runs the 90 tests under `tests/`; one integration test per "Done when" line.
16. [pytest-cov.md](pytest-cov.md): Coverage: measures which lines the tests ran; `make test` fails under 95 percent in `domain/` and `application/`.
17. [ruff.md](ruff.md): ruff: the linter and formatter (`ruff check`, `ruff format --check`) with rules chosen in `pyproject.toml`.
18. [mypy.md](mypy.md): mypy: the static type checker, in strict mode, over `src/` and `tests/`.
19. [import-linter.md](import-linter.md): import-linter: enforces the layer rule `interfaces -> infrastructure -> application -> domain` (`lint-imports`).
20. [pip-audit.md](pip-audit.md): pip-audit: checks the pinned packages against vulnerability databases (`make audit`).
21. [editorconfig.md](editorconfig.md): EditorConfig: `.editorconfig`, the editor settings (encoding, line endings, tabs or spaces) shared by everyone.
22. [git.md](git.md): Git: the history of the repository (the commits) and `.gitignore`, the list of files it should not track.
23. [github-actions.md](github-actions.md): GitHub Actions: `.github/workflows/ci.yml`, which runs the same `make` commands on every push.
24. [yaml.md](yaml.md): YAML: the file format of `.github/workflows/ci.yml`.

## If you have ten minutes

Read these three, in this order:

- [python.md](python.md): Python: the language the whole program is written in; read this first.
- [make.md](make.md): Make: `Makefile`, the one place that names every command (`make run`, `make test`, `make lint`).
- [markdown.md](markdown.md): Markdown: the format of every deliverable document, and of the conventions the checker reads.
