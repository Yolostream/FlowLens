import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .models import Action, Workflow


class ParseError(ValueError):
    pass


def _is_workflow(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    definition = data.get("definition", data)
    return isinstance(definition, dict) and (
        isinstance(definition.get("triggers"), dict)
        or isinstance(definition.get("actions"), dict)
    )


def _connector_hint(node: Any) -> str | None:
    if not isinstance(node, dict):
        return None
    inputs = node.get("inputs")
    if not isinstance(inputs, dict):
        return None
    host = inputs.get("host")
    if isinstance(host, dict):
        for key in ("connectionName", "apiId", "operationId"):
            value = host.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def _walk_actions(actions: dict[str, Any], prefix: str = "actions") -> Iterator[Action]:
    for name, node in actions.items():
        if not isinstance(node, dict):
            continue
        path = f"{prefix}.{name}"
        action_type = str(node.get("type", "Unknown"))
        yield Action(name=name, action_type=action_type, path=path, connector=_connector_hint(node))
        nested = node.get("actions")
        if isinstance(nested, dict):
            yield from _walk_actions(nested, path + ".actions")
        for branch_key in ("else", "cases"):
            branch = node.get(branch_key)
            if isinstance(branch, dict):
                branch_actions = branch.get("actions", branch)
                if isinstance(branch_actions, dict):
                    yield from _walk_actions(branch_actions, path + f".{branch_key}")


def _display_name(data: dict[str, Any], path: Path) -> str:
    for key in ("displayName", "name"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    properties = data.get("properties")
    if isinstance(properties, dict):
        value = properties.get("displayName")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return path.stem


def parse_solution(root: Path) -> list[Workflow]:
    workflows: list[Workflow] = []
    for path in sorted(root.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError, OSError):
            continue
        if not _is_workflow(data):
            continue
        definition = data.get("definition", data)
        triggers = list((definition.get("triggers") or {}).keys())
        actions = list(_walk_actions(definition.get("actions") or {}))
        connectors = sorted({a.connector for a in actions if a.connector})
        workflows.append(
            Workflow(
                name=_display_name(data, path),
                source=str(path.relative_to(root)),
                triggers=triggers,
                actions=actions,
                connectors=connectors,
                raw=data,
            )
        )
    if not workflows:
        raise ParseError("No workflow JSON definitions were detected")
    return workflows
