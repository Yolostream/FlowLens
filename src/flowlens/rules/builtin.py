import re
from collections.abc import Iterator
from typing import Any

from ..models import Finding, Workflow
from .base import Rule

URL = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
EMAIL = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.IGNORECASE)
GUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE)


def walk_strings(value: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{path}[{index}]")


def preview(value: str, match: str) -> str:
    lowered = value.lower()
    if any(token in lowered for token in ("password", "secret", "token", "apikey", "api_key")):
        return "[redacted: potentially sensitive value]"
    return match[:117] + ("..." if len(match) > 117 else "")


class PatternRule(Rule):
    pattern = re.compile(r"$^")
    message = "Pattern detected"

    def evaluate(self, workflow: Workflow) -> list[Finding]:
        findings = []
        seen = set()
        for path, value in walk_strings(workflow.raw):
            for match in self.pattern.finditer(value):
                key = (path, match.group(0))
                if key in seen:
                    continue
                seen.add(key)
                findings.append(Finding(
                    rule=self.rule_id,
                    severity=self.severity,
                    workflow=workflow.name,
                    message=self.message,
                    path=path,
                    preview=preview(value, match.group(0)),
                ))
        return findings


class HardcodedUrlRule(PatternRule):
    rule_id = "FL001"
    title = "Hardcoded URL"
    pattern = URL
    message = "A hardcoded HTTP or HTTPS URL was detected. Consider an environment variable."


class HardcodedEmailRule(PatternRule):
    rule_id = "FL002"
    title = "Hardcoded email address"
    pattern = EMAIL
    message = "A hardcoded email address was detected. Confirm that it is intentional."


class HardcodedGuidRule(PatternRule):
    rule_id = "FL003"
    title = "Hardcoded GUID"
    pattern = GUID
    message = "A hardcoded GUID was detected. Confirm that it is portable between environments."


class HttpActionRule(Rule):
    rule_id = "FL004"
    title = "HTTP action"
    severity = "warning"

    def evaluate(self, workflow: Workflow) -> list[Finding]:
        results = []
        for action in workflow.actions:
            normalized = action.action_type.lower().replace("_", "")
            if normalized in {"http", "httprequest", "apiconnectionwebhook"}:
                results.append(Finding(
                    rule=self.rule_id,
                    severity=self.severity,
                    workflow=workflow.name,
                    action=action.name,
                    path=action.path,
                    message="An HTTP-style action was detected. Review authentication, endpoint and data handling.",
                ))
        return results


BUILTIN_RULES = [HardcodedUrlRule(), HardcodedEmailRule(), HardcodedGuidRule(), HttpActionRule()]
