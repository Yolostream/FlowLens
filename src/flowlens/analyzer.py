from pathlib import Path

from .extractor import solution_directory
from .models import Report
from .parser import parse_solution
from .rules import BUILTIN_RULES


def analyze(source: Path) -> Report:
    with solution_directory(source) as root:
        workflows = parse_solution(root)
        findings = []
        for workflow in workflows:
            for rule in BUILTIN_RULES:
                findings.extend(rule.evaluate(workflow))
        findings.sort(key=lambda f: (f.workflow.lower(), f.rule, f.path))
        return Report(solution=source.stem, workflows=workflows, findings=findings)
