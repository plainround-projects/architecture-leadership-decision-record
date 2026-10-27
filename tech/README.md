# Technology notes: Decision record toolkit

These notes teach every technology used by `architecture-leadership-decision-record`, from zero, through this repository's own files. Each note says what the technology is, why the repository uses it, where it appears, how it works underneath, walks through the repository's own lines, and ends with commands to try, common mistakes, five questions with answers, and links to the official documentation for the pinned version.

## Reading order

Read the language first, then the build tool, then the runtime pieces, then the tests and the checks.

1. [python.md](python.md): Python: the language the whole program is written in; read this first.
2. [python-standard-library.md](python-standard-library.md): Standard library: `enum`, `typing`, `collections`, `os`, `sys`, `shutil`, `datetime`, `itertools`.
3. [python-code-application.md](python-code-application.md): Application layer: 140 lines of Python, every file quoted and explained.
4. [python-code-domain.md](python-code-domain.md): Domain layer: 495 lines of Python, every file quoted and explained.
5. [python-code-infrastructure.md](python-code-infrastructure.md): Infrastructure layer: 218 lines of Python, every file quoted and explained.
6. [python-code-interfaces.md](python-code-interfaces.md): Interfaces layer: 49 lines of Python, every file quoted and explained.
7. [python-tests-application.md](python-tests-application.md): Tests: `application` (58 lines), explained line by line.
8. [python-tests-domain.md](python-tests-domain.md): Tests: `domain` (193 lines), explained line by line.
9. [python-tests-infrastructure.md](python-tests-infrastructure.md): Tests: `infrastructure` (96 lines), explained line by line.
10. [python-tests-integration.md](python-tests-integration.md): Tests: `integration` (84 lines), explained line by line.
11. [python-tests-interfaces.md](python-tests-interfaces.md): Tests: `interfaces` (33 lines), explained line by line.
12. [python-tests-shared.md](python-tests-shared.md): Tests: `shared` (62 lines), explained line by line.
13. [dataclasses.md](dataclasses.md): `dataclasses`: the small frozen value types (`Finding`, `Report`, settings, parsed documents).
14. [re.md](re.md): `re`: the patterns that find headings, labels, numbers and sentences in Markdown text.
15. [argparse.md](argparse.md): `argparse` and exit codes: how `adr-toolkit` reads its subcommands and reports success.
16. [pathlib.md](pathlib.md): `pathlib`: how the program reads and writes files, and refuses to leave the repository root.
17. [markdown.md](markdown.md): Markdown: the format of every deliverable document, and of the conventions the checker reads.
18. [toml.md](toml.md): TOML: the format of `pyproject.toml`.
19. [bash.md](bash.md): Shell: the small command-line programs (`grep`, `sed`, `sort`, `cp`, `rm`, `touch`, `command -v`) that the Makefile recipes run.
20. [make.md](make.md): Make: `Makefile`, the one place that names every command (`make run`, `make test`, `make lint`).
21. [venv-and-pip.md](venv-and-pip.md): venv and pip: the private `.venv/` folder and the installer that fills it from the lock file.
22. [setuptools.md](setuptools.md): setuptools and `pyproject.toml` packaging: how `src/adr_toolkit` becomes an installable project with a `adr-toolkit` command.
23. [hash-pinned-lock-files.md](hash-pinned-lock-files.md): Lock files: `requirements-dev.lock` and `requirements.lock`, the exact packages and file hashes pip installs.
24. [env-files.md](env-files.md): `.env` files: how settings reach the program (`.env.example` is committed, `.env` is local).
25. [pytest.md](pytest.md): pytest: runs the 90 tests under `tests/`; one integration test per "Done when" line.
26. [pytest-cov.md](pytest-cov.md): Coverage: measures which lines the tests ran; `make test` fails under 95 percent in `domain/` and `application/`.
27. [ruff.md](ruff.md): ruff: the linter and formatter (`ruff check`, `ruff format --check`) with rules chosen in `pyproject.toml`.
28. [mypy.md](mypy.md): mypy: the static type checker, in strict mode, over `src/` and `tests/`.
29. [import-linter.md](import-linter.md): import-linter: enforces the layer rule `interfaces -> infrastructure -> application -> domain` (`lint-imports`).
30. [pip-audit.md](pip-audit.md): pip-audit: checks the pinned packages against vulnerability databases (`make audit`).
31. [editorconfig.md](editorconfig.md): EditorConfig: `.editorconfig`, the editor settings (encoding, line endings, tabs or spaces) shared by everyone.
32. [git.md](git.md): Git: the history of the repository (the commits) and `.gitignore`, the list of files it should not track.
33. [github-actions.md](github-actions.md): GitHub Actions: `.github/workflows/ci.yml`, which runs the same `make` commands on every push.
34. [yaml.md](yaml.md): YAML: the file format of `.github/workflows/ci.yml`.

## If you have ten minutes

Read these three, in this order:

- [python.md](python.md): Python: the language the whole program is written in; read this first.
- [make.md](make.md): Make: `Makefile`, the one place that names every command (`make run`, `make test`, `make lint`).
- [markdown.md](markdown.md): Markdown: the format of every deliverable document, and of the conventions the checker reads.
