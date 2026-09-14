from pathlib import Path

from flowlens.analyzer import analyze


def test_all_initial_rules_are_detected():
    report = analyze(Path("examples/synthetic-solution"))
    ids = {finding.rule for finding in report.findings}
    assert ids == {"FL001", "FL002", "FL003", "FL004"}


def test_findings_are_serializable():
    report = analyze(Path("examples/synthetic-solution"))
    data = report.to_dict()
    assert data["summary"]["workflow_count"] == 1
    assert data["summary"]["finding_count"] >= 4
