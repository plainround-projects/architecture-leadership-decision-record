"""Settings from the environment, validated once at start-up (twelve-factor)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from adr_toolkit.application.check_documents import CheckSettings
from adr_toolkit.domain.adr import AdrLimits


class SettingsError(ValueError):
    """An environment variable holds a value the program cannot use."""


@dataclass(frozen=True)
class Settings:
    """Where the documents are, where the report goes, and the page limits."""

    root: Path
    report_dir: str
    check: CheckSettings


def _positive_int(env: Mapping[str, str], name: str, default: int) -> int:
    raw = env.get(name, str(default))
    try:
        value = int(raw)
    except ValueError:
        raise SettingsError(f"{name} must be a whole number, got {raw!r}") from None
    if value <= 0:
        raise SettingsError(f"{name} must be positive, got {value}")
    return value


def load_settings(env: Mapping[str, str]) -> Settings:
    """Read ADR_ROOT, REPORT_DIR, ADR_MAX_LINES, ADR_MAX_WORDS and ADR_REQUIRED_COMMUNICATION."""
    required_raw = env.get("ADR_REQUIRED_COMMUNICATION", "")
    try:
        required = tuple(int(part) for part in required_raw.split(",") if part.strip())
    except ValueError:
        raise SettingsError(
            f"ADR_REQUIRED_COMMUNICATION must be comma-separated numbers, got {required_raw!r}"
        ) from None
    limits = AdrLimits(
        max_lines=_positive_int(env, "ADR_MAX_LINES", 70),
        max_words=_positive_int(env, "ADR_MAX_WORDS", 600),
    )
    return Settings(
        root=Path(env.get("ADR_ROOT", ".")),
        report_dir=env.get("REPORT_DIR", "build"),
        check=CheckSettings(limits=limits, required_adrs=required),
    )
