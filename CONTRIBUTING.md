# Contributing to FlowLens

Thank you for helping make Power Automate solution reviews easier.

## Development setup

```bash
git clone https://github.com/Yolostream/flowlens.git
cd flowlens
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux or macOS
source .venv/bin/activate
```

Install the project and test tools:

```bash
python -m pip install -e .
python -m pip install pytest ruff
pytest
ruff check .
```

## Contribution workflow

1. Search existing issues.
2. Create or comment on an issue before a large change.
3. Create a branch such as `feat/fl005-concurrency-rule`.
4. Add tests and synthetic fixtures.
5. Run `pytest` and `ruff check .`.
6. Open a focused pull request and explain test coverage.

## Adding a rule

1. Add a class in `src/flowlens/rules/builtin.py`.
2. Give it a stable identifier such as `FL005`.
3. Return a `Finding` with actionable wording.
4. Add positive and negative tests.
5. Update the rules table in `README.md`.

## Data safety

Never contribute real exported solutions unless you own the data and have verified that all identifiers and secrets were removed. Prefer synthetic fixtures. Review the anonymization guide before contributing samples.

## Definition of done

- Behavior is covered by tests.
- User-facing behavior is documented.
- Error messages are actionable.
- Existing command behavior remains backward-compatible or the change is clearly documented.
