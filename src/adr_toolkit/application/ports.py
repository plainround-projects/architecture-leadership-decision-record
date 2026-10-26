"""What the use cases need from the outside world."""

from __future__ import annotations

from typing import Protocol

from adr_toolkit.domain.adr import Adr
from adr_toolkit.domain.audiences import AudienceVersions
from adr_toolkit.domain.reaction import Reaction


class DocumentStore(Protocol):
    """Reads and writes the repository's documents by path relative to its root."""

    def list_paths(self, folder: str) -> list[str]:
        """Markdown files directly inside the folder, sorted; empty when the folder is missing."""
        ...

    def read_text(self, path: str) -> str:
        """The text of a file."""
        ...

    def exists(self, path: str) -> bool:
        """True when the file exists."""
        ...

    def write_text(self, path: str, text: str) -> None:
        """Replace a file, creating its folder."""
        ...


class RecordReader(Protocol):
    """Turns the Markdown of each document type into the domain's values."""

    def read_adr(self, path: str) -> Adr:
        """Parse a decision record."""
        ...

    def read_audiences(self, path: str) -> AudienceVersions:
        """Parse the three audience versions."""
        ...

    def read_reaction(self, path: str) -> Reaction:
        """Parse a reaction log."""
        ...
