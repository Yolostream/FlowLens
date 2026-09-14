from pathlib import Path

from flowlens.cli import main


def test_cli_writes_both_reports(tmp_path: Path, capsys):
    output = tmp_path / "report"
    main(["analyze", "examples/synthetic-solution", "--output", str(output)])
    assert (output / "summary.md").exists()
    assert (output / "findings.json").exists()
    assert "Analyzed 1 workflow" in capsys.readouterr().out
