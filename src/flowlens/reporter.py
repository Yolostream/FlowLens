import json
from pathlib import Path

from .models import Report


def markdown(report: Report) -> str:
    lines = [
        f"# FlowLens report: {report.solution}",
        "",
        f"- Workflows: **{len(report.workflows)}**",
        f"- Findings: **{len(report.findings)}**",
        "",
        "> Static findings require human review. They are not proof of a security defect.",
        "",
        "## Workflows",
        "",
    ]
    for workflow in report.workflows:
        lines.extend([
            f"### {workflow.name}",
            "",
            f"Source: `{workflow.source}`",
            "",
            "**Triggers:** " + (", ".join(f"`{x}`" for x in workflow.triggers) or "None detected"),
            "",
            "**Connectors:** " + (", ".join(f"`{x}`" for x in workflow.connectors) or "None detected"),
            "",
            "| Action | Type | Path |",
            "|---|---|---|",
        ])
        if workflow.actions:
            for action in workflow.actions:
                lines.append(f"| {action.name} | {action.action_type} | `{action.path}` |")
        else:
            lines.append("| None detected |  |  |")
        lines.append("")

    lines.extend(["## Findings", ""])
    if not report.findings:
        lines.append("No findings detected by the enabled rules.")
    else:
        lines.extend(["| Rule | Severity | Workflow | Action | Message | Path | Preview |", "|---|---|---|---|---|---|---|"])
        for finding in report.findings:
            values = [
                finding.rule, finding.severity, finding.workflow,
                finding.action or "", finding.message, f"`{finding.path}`", finding.preview or "",
            ]
            values = [str(v).replace("|", "\\|").replace("\n", " ") for v in values]
            lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    return "\n".join(lines)


def write_report(report: Report, output: Path, output_format: str = "all") -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    written = []
    if output_format in {"all", "markdown"}:
        path = output / "summary.md"
        path.write_text(markdown(report), encoding="utf-8")
        written.append(path)
    if output_format in {"all", "json"}:
        path = output / "findings.json"
        path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(path)
    return written
