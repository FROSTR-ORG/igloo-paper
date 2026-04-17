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

## Flow Validator Guidance: file system

- Stay within repository and mission paths only:
  - Repo: `/Users/plebdev/Desktop/code/igloo/igloo-paper`
  - Mission: `/Users/plebdev/.factory/missions/ff6023b0-52c0-460f-b23e-e9cc73c3dd47`
- Do not use network tools or browser automation; assertions for this milestone are file-based.
- Do not mutate implementation files while validating; read/inspect files and run verification commands only.
- Write exactly one flow report JSON at the assigned output path and save any command outputs/screenshots only under the assigned evidence directory.
- If an assertion cannot be tested due to missing prerequisite artifacts, mark it `blocked` with a concrete reason and command evidence.
