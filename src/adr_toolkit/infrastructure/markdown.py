"""Parse the Markdown of each document type into the domain's values."""

from __future__ import annotations

import re

from adr_toolkit.application.ports import DocumentStore
from adr_toolkit.domain.adr import Adr, Option
from adr_toolkit.domain.audiences import AudienceVersions
from adr_toolkit.domain.reaction import Reaction

_TITLE = re.compile(r"^# ADR (\d+): (.+?)\s*$")
_META = re.compile(r"^(Status|Date|Deciders|Supersedes):\s*(.*?)\s*$")
_SUPERSEDED_BY = re.compile(r"^Superseded by ADR (\d+)$")
_ADR_REF = re.compile(r"^ADR (\d+)$")
_HEADING2 = re.compile(r"^## (.+?)\s*$")
_HEADING3 = re.compile(r"^### (.+?)\s*$")
_OPTION_NAME = re.compile(r"^Option [A-Z]: (.+)$")


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


def _fields(lines: list[str], labels: tuple[str, ...]) -> dict[str, str]:
    """`Label: text` fields whose text may continue on the following lines until the next label."""
    pattern = re.compile(rf"^({'|'.join(re.escape(label) for label in labels)}):\s*(.*)$")
    values: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            current = match.group(1)
            values[current] = [match.group(2)]
        elif current is not None and line.strip():
            values[current].append(line.strip())
    return {label: " ".join(parts).strip() for label, parts in values.items()}


def _paragraph(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip())


class MarkdownRecordReader:
    """Reads the repository's three document types from a store."""

    def __init__(self, store: DocumentStore) -> None:
        self._store = store

    def read_adr(self, path: str) -> Adr:
        """Parse a decision record; whatever is missing stays empty for the rules to report."""
        text = self._store.read_text(path)
        lines = text.splitlines()
        title_match = _TITLE.match(lines[0]) if lines else None
        meta = {m.group(1): m.group(2) for line in lines if (m := _META.match(line))}
        sections = _sections(lines)
        status, superseded_by = _status(meta.get("Status", ""))
        supersedes = _adr_number(meta.get("Supersedes", ""))
        consequences = _fields(sections.get("Consequences", []), ("Good", "Bad", "Revisit when"))
        return Adr(
            path=path,
            number=int(title_match.group(1)) if title_match else None,
            title=title_match.group(2) if title_match else "",
            status=status,
            superseded_by=superseded_by,
            supersedes=supersedes,
            date_text=meta.get("Date", ""),
            deciders=meta.get("Deciders", ""),
            sections=tuple(name for name in sections if name),
            context=_paragraph(sections.get("Context", [])),
            options=_options(sections.get("Options considered", [])),
            decision=_paragraph(sections.get("Decision", [])),
            good=consequences.get("Good", ""),
            bad=consequences.get("Bad", ""),
            revisit_when=consequences.get("Revisit when", ""),
            line_count=len([line for line in lines if line.strip()]),
            word_count=len(text.split()),
        )

    def read_audiences(self, path: str) -> AudienceVersions:
        """Parse the audience file: the first two headings are Engineers and Manager, any other is the sibling team."""
        text = self._store.read_text(path)
        lines = text.splitlines()
        sections = _sections(lines)
        first = lines[0] if lines else ""
        number = re.search(r"ADR (\d+)", first)
        engineers = _paragraph(sections.get("Engineers", []))
        manager = _paragraph(sections.get("Manager", []))
        others = [name for name in sections if name and name not in ("Engineers", "Manager")]
        sibling_name = others[0] if others else ""
        return AudienceVersions(
            path=path,
            adr_number=int(number.group(1)) if number else None,
            engineers=engineers,
            manager=manager,
            sibling=_paragraph(sections.get(sibling_name, [])) if sibling_name else "",
            sibling_name=sibling_name,
        )

    def read_reaction(self, path: str) -> Reaction:
        """Parse a reaction log."""
        lines = self._store.read_text(path).splitlines()
        sections = _sections(lines)
        header = _fields(sections[""], ("Reader", "Reader kind", "ADR"))
        fix = _fields(sections.get("Fix", []), ("Before", "After"))
        number = re.search(r"\d+", header.get("ADR", ""))
        return Reaction(
            path=path,
            adr_number=int(number.group(0)) if number else None,
            reader=header.get("Reader", ""),
            reader_kind=header.get("Reader kind", ""),
            said_back=_paragraph([line.lstrip("> ") for line in sections.get("Said back", [])]),
            misunderstood=_paragraph(sections.get("Misunderstood", [])),
            before=fix.get("Before", "").strip('"'),
            after=fix.get("After", "").strip('"'),
        )


def _status(raw: str) -> tuple[str, int | None]:
    match = _SUPERSEDED_BY.match(raw)
    if match:
        return "Superseded", int(match.group(1))
    return raw, None


def _adr_number(raw: str) -> int | None:
    match = _ADR_REF.match(raw)
    return int(match.group(1)) if match else None


def _options(lines: list[str]) -> tuple[Option, ...]:
    options: list[Option] = []
    block_name: str | None = None
    block: list[str] = []

    def flush() -> None:
        if block_name is None:
            return
        fields = _fields(block, ("Advantage", "Main cost", "Pick it if"))
        name_match = _OPTION_NAME.match(block_name)
        options.append(
            Option(
                name=name_match.group(1) if name_match else block_name,
                advantage=fields.get("Advantage", ""),
                main_cost=fields.get("Main cost", ""),
                pick_if=fields.get("Pick it if", ""),
            )
        )

    for line in lines:
        heading = _HEADING3.match(line)
        if heading:
            flush()
            block_name, block = heading.group(1), []
        elif block_name is not None:
            block.append(line)
    flush()
    return tuple(options)
