import argparse
from pathlib import Path
import sys

from . import __version__
from .analyzer import analyze
from .extractor import InputError
from .parser import ParseError
from .reporter import write_report
from .rules import BUILTIN_RULES

SEVERITY = {"none": 99, "warning": 1, "error": 2}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="flowlens", description="Analyze exported Power Automate solutions")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_cmd = sub.add_parser("analyze", help="Analyze a solution ZIP or extracted directory")
    analyze_cmd.add_argument("solution", type=Path)
    analyze_cmd.add_argument("--output", type=Path, default=Path("flowlens-report"))
    analyze_cmd.add_argument("--format", choices=("all", "markdown", "json"), default="all")
    analyze_cmd.add_argument("--fail-on", choices=("none", "warning", "error"), default="none")

    sub.add_parser("rules", help="List built-in rules")
    sub.add_parser("version", help="Print version")
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "version":
        print(__version__)
        return
    if args.command == "rules":
        for rule in BUILTIN_RULES:
            print(f"{rule.rule_id}\t{rule.severity}\t{rule.title}")
        return

    try:
        report = analyze(args.solution)
        written = write_report(report, args.output, args.format)
    except (InputError, ParseError, OSError) as exc:
        print(f"flowlens: error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    print(f"Analyzed {len(report.workflows)} workflow(s); found {len(report.findings)} finding(s).")
    for path in written:
        print(f"Wrote {path}")

    threshold = SEVERITY[args.fail_on]
    finding_levels = {"warning": 1, "error": 2}
    if any(finding_levels.get(item.severity, 0) >= threshold for item in report.findings):
        raise SystemExit(1)
