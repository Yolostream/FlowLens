# Architecture

FlowLens deliberately separates input handling, parsing, rule evaluation and reporting.

```text
ZIP or directory
      |
      v
 extractor.py     safe temporary extraction
      |
      v
 parser.py        discover and normalize workflow JSON
      |
      v
 rules/           evaluate normalized workflows
      |
      v
 reporter.py      write Markdown and JSON
```

## Design principles

- Local-first and privacy-conscious
- Deterministic output
- Small core with testable rule classes
- Graceful handling of unknown JSON shapes
- No claim that a static finding proves a security issue

## Data model

A `Workflow` contains its display name, source path, trigger names, action records, connector hints and raw JSON. A `Finding` contains a rule ID, severity, workflow, optional action, message, path and preview.
