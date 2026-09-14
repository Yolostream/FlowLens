from abc import ABC, abstractmethod

from ..models import Finding, Workflow


class Rule(ABC):
    rule_id = ""
    title = ""
    severity = "warning"

    @abstractmethod
    def evaluate(self, workflow: Workflow) -> list[Finding]:
        raise NotImplementedError
