"""Format a report as text for the terminal and as Markdown for the build artifact."""

from __future__ import annotations

from adr_toolkit.domain.findings import Report


def render_text(report: Report) -> str:
    """One line per finding, then the verdict."""
    lines = [
        f"{finding.severity.value.upper():7} {finding.code} {finding.subject}: {finding.message}"
        for finding in report.findings
    ]
    verdict = "OK" if report.ok else "FAILED"
    counts = f"{len(report.subjects)} documents checked, {len(report.errors)} errors, {len(report.warnings)} warnings"
    lines.append(f"{verdict}: {counts}")
    return "\n".join(lines)


def render_markdown(report: Report) -> str:
    """The report the CI run uploads: verdict, documents checked, findings."""
    verdict = "OK" if report.ok else "FAILED"
    lines = [
        "# Decision record report",
        "",
        f"**Verdict:** {verdict} ({len(report.errors)} errors, {len(report.warnings)} warnings)",
        "",
        "## Documents checked",
        "",
        *[f"- `{subject}`" for subject in report.subjects],
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        lines += ["| Severity | Code | Document | Message |", "| --- | --- | --- | --- |"]
        lines += [f"| {f.severity.value} | {f.code} | `{f.subject}` | {f.message} |" for f in report.findings]
    else:
        lines.append("None.")
    return "\n".join(lines) + "\n"
