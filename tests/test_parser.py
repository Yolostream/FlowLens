from pathlib import Path

from flowlens.parser import parse_solution


def test_parse_synthetic_solution():
    root = Path("examples/synthetic-solution")
    workflows = parse_solution(root)
    assert len(workflows) == 1
    flow = workflows[0]
    assert flow.name == "Synthetic SharePoint notification"
    assert flow.triggers == ["Recurrence"]
    assert {a.name for a in flow.actions} == {"Get_items", "Notify_owner", "Call_example_API"}
    assert "shared_sharepointonline" in flow.connectors
