from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Action:
    name: str
    action_type: str
    path: str
    connector: str | None = None


@dataclass
class Workflow:
    name: str
    source: str
    triggers: list[str] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    connectors: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class Finding:
    rule: str
    severity: str
    workflow: str
    message: str
    path: str
    action: str | None = None
    preview: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Report:
    solution: str
    workflows: list[Workflow]
    findings: list[Finding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "solution": self.solution,
            "summary": {
                "workflow_count": len(self.workflows),
                "finding_count": len(self.findings),
            },
            "workflows": [
                {
                    "name": w.name,
                    "source": w.source,
                    "triggers": w.triggers,
                    "actions": [asdict(a) for a in w.actions],
                    "connectors": w.connectors,
                }
                for w in self.workflows
            ],
            "findings": [f.to_dict() for f in self.findings],
        }
