# User Testing

Testing surface, required testing skills/tools, and resource cost classification.

---

## Validation Surface

This is a **static documentation repository** with no runtime surface. There is no browser UI, CLI app, or API to test.

**Testing surface:** File system only
- Directory structure correctness
- File existence (README.md, screenshot.png, reference.html/screen.html per artboard)
- JSON validity (tokens files, artboard-map.json)
- Content completeness (word counts, key counts, term coverage)

**Tool:** `bash` (shell commands: `test -f`, `find`, `wc`, `python3`)

**No agent-browser, tuistory, or curl needed.** All validation is file-based.

## Validation Approach

1. Run `python3 scripts/verify.py` — automated completeness check
2. Shell commands for specific assertions (file existence, JSON parsing, word counts)
3. Paper MCP spot-checks for accuracy (compare extracted tokens against canvas values)

## Validation Concurrency

**Surface: file system**
- Resource cost per validator: negligible (~10MB RAM, minimal CPU)
- Max concurrent validators: **5**
- Rationale: Shell commands and Python scripts are lightweight. 128GB RAM, 18 cores. No constraint on parallelism.
