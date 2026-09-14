# FlowLens

FlowLens is a small, privacy-friendly static analyzer and documentation generator for exported Microsoft Power Automate solutions.

It inventories cloud flows, triggers, actions and connectors and reports maintainability findings such as hardcoded URLs, email addresses, GUIDs and HTTP actions. Analysis is local. Nothing is uploaded.

> Project status: early development. FlowLens provides static findings, not proof that a flow is secure or insecure.

## Features

- Analyze a Power Platform solution `.zip` or extracted directory
- Inventory flows, triggers, actions and connector hints
- Produce Markdown and JSON reports
- Built-in rules: hardcoded URL, email address, GUID and HTTP action
- CI-friendly exit codes
- No runtime dependencies beyond Python 3.10+

## Quick start

### Run without installing

```bash
python -m flowlens analyze path/to/Solution.zip --output flowlens-report
```

When running from a cloned repository, set the source directory first:

```bash
# PowerShell
$env:PYTHONPATH = "src"
python -m flowlens analyze examples/synthetic-solution --output flowlens-report

# Bash
PYTHONPATH=src python -m flowlens analyze examples/synthetic-solution --output flowlens-report
```

### Install locally

```bash
python -m pip install -e .
flowlens analyze examples/synthetic-solution --output flowlens-report
```

Generated files:

```text
flowlens-report/
├── summary.md
└── findings.json
```

## Commands

```bash
flowlens analyze SOLUTION [--output DIR] [--format all|markdown|json] [--fail-on none|warning|error]
flowlens rules
flowlens version
```

Examples:

```bash
flowlens analyze MySolution.zip
flowlens analyze MySolution.zip --output report --format all
flowlens analyze MySolution.zip --fail-on warning
flowlens rules
```

Exit codes:

- `0`: analysis completed and fail threshold was not reached
- `1`: configured finding threshold was reached
- `2`: invalid input or analysis failure

## Findings

| Rule | Default severity | Description |
|---|---:|---|
| FL001 | warning | Hardcoded HTTP or HTTPS URL |
| FL002 | warning | Hardcoded email address |
| FL003 | warning | Hardcoded GUID |
| FL004 | warning | HTTP action detected |

False positives are possible. Findings include a value preview, but likely secrets are redacted.

## Supported input

FlowLens searches recursively for JSON files that resemble Power Automate workflow definitions. Power Platform export formats can vary. Please open an issue with a sanitized fixture when a valid workflow is not detected.

## Privacy

Do not commit real corporate solution exports. They can contain tenant URLs, account names, email addresses, IDs and connection metadata. Use synthetic or carefully anonymized fixtures. See [the anonymization guide](docs/anonymizing-solutions.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New rules and sanitized parser fixtures are especially welcome.

## Security

See [SECURITY.md](SECURITY.md). Please do not open public issues for suspected vulnerabilities.

## License

MIT. See [LICENSE](LICENSE).
