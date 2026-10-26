"""`adr-toolkit check | log | report`. Wires the adapters into the use cases and owns the exit codes."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

from adr_toolkit.application.check_documents import check_documents, current_log, write_log
from adr_toolkit.application.reporting import render_markdown, render_text
from adr_toolkit.infrastructure.filesystem import FileSystemStore
from adr_toolkit.infrastructure.markdown import MarkdownRecordReader
from adr_toolkit.infrastructure.settings import SettingsError, load_settings


def build_parser() -> argparse.ArgumentParser:
    """The command line: three subcommands, no options of their own."""
    parser = argparse.ArgumentParser(
        prog="adr-toolkit", description="Check decision records and the documents that carry them."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="run every rule; exit 1 on any error")
    log = commands.add_parser("log", help="print the decision log")
    log.add_argument("--write", action="store_true", help="write docs/decision-log.md instead of printing")
    commands.add_parser("report", help="write the Markdown report under REPORT_DIR")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run one command and return the exit code: 0 ok, 1 findings, 2 bad configuration."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(os.environ)
    except SettingsError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2
    store = FileSystemStore(settings.root)
    reader = MarkdownRecordReader(store)
    if args.command == "log":
        if args.write:
            write_log(store, reader)
            print("wrote docs/decision-log.md")
        else:
            print(current_log(store, reader), end="")
        return 0
    report = check_documents(store, reader, settings.check)
    if args.command == "report":
        store.write_text(f"{settings.report_dir}/report.md", render_markdown(report))
        print(f"wrote {settings.report_dir}/report.md")
        return 0 if report.ok else 1
    print(render_text(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
