---
name: documenter
description: Writes cross-cutting documentation, READMEs, INSTRUCTIONS.md runbook, and verification scripts
---

# Documenter

NOTE: Startup and cleanup are handled by `worker-base`. This skill defines the WORK PROCEDURE.

## When to Use This Skill

Features that produce documentation, flow maps, verification scripts, and the extraction runbook. These features synthesize across the repository rather than extracting from specific artboards.

## Required Skills

None. This worker reads existing repository files and writes documentation. May use Paper MCP tools for reference if needed.

## Work Procedure

### Step 1: Read Feature Description and Survey Repository

Read the feature description carefully. Then survey the current state of the repository:
- List all directories under `design-system/` and `screens/`
- Check which files already exist (README.md, reference.html, screenshot.png, screen.html)
- Read `AGENTS.md` for the artboard ID reference
- Read `.factory/library/architecture.md` for the system overview

### Step 2: Write Documentation

Follow the feature description for exactly what to produce. General guidelines:

**For README.md files:**
- Start with a clear `# Title`
- Include a purpose/description section
- Include a directory map or content listing
- Cross-reference related sections with relative links
- For screens/README.md: include a flow map showing all user journeys

**For INSTRUCTIONS.md (extraction runbook):**
Must include ALL of these sections:
1. **Prerequisites** — Droid, Paper MCP connection, canvas file open
2. **How Paper MCP Works** — Brief explanation of the Paper___* tools
3. **Artboard Mapping Table** — Complete table mapping every Paper artboard ID to its name, category, and output path. Use the artboard reference from AGENTS.md.
4. **Step-by-Step Extraction Procedure** — Detailed instructions for re-running the extraction, including:
   - How to verify Paper MCP connectivity
   - How to extract each artboard type (standard, tokens, glossary)
   - How to save screenshots from base64
   - How to write README.md files
5. **Verification Checklist** — How to verify the extraction is complete
6. **Troubleshooting** — Common issues and solutions (Paper MCP down, artboard ID changed, etc.)

**For verification scripts:**
- Write `scripts/verify.py` that checks:
  - All expected directories exist
  - All expected files exist (README.md, screenshot.png, reference.html/screen.html)
  - JSON token files are valid JSON with expected keys
  - artboard-map.json is valid and complete
  - Outputs a clear pass/fail summary with counts

### Step 3: Cross-Reference and Consistency Check

After writing documentation:
- Verify all relative links work (referenced files exist)
- Verify directory listings match actual directory structure
- Verify artboard counts in documentation match actual files
- Verify flow descriptions in screens/README.md match actual screen directories

### Step 4: Verify Output

Run any verification scripts you created. Check that documentation files are non-empty and substantive (not placeholder content).

### Step 5: Commit

Commit all changes with a descriptive message.

## Example Handoff

```json
{
  "salientSummary": "Wrote INSTRUCTIONS.md extraction runbook with complete artboard mapping table (76 entries), step-by-step extraction procedure, and troubleshooting guide. Total 850 words. Verified all artboard IDs match AGENTS.md reference.",
  "whatWasImplemented": "Created INSTRUCTIONS.md with 6 sections: prerequisites, Paper MCP explanation, full artboard-to-path mapping table covering all 76 artboards (24 design system + 51 screens + 1 divider), detailed extraction procedure for standard/token/glossary artboards, verification checklist, and troubleshooting guide. All artboard IDs cross-referenced against AGENTS.md and verified present.",
  "whatWasLeftUndone": "",
  "verification": {
    "commandsRun": [
      {
        "command": "wc -w INSTRUCTIONS.md",
        "exitCode": 0,
        "observation": "850 words"
      },
      {
        "command": "grep -c '|' INSTRUCTIONS.md",
        "exitCode": 0,
        "observation": "78 table rows (76 artboards + header + separator)"
      },
      {
        "command": "python3 scripts/verify.py",
        "exitCode": 0,
        "observation": "All checks passed: 76/76 artboards mapped, 45/45 directories verified"
      }
    ],
    "interactiveChecks": [
      {
        "action": "Verified all artboard IDs in mapping table exist in AGENTS.md",
        "observed": "All 76 IDs match — no missing or extra entries"
      }
    ]
  },
  "tests": {
    "added": [
      {
        "file": "scripts/verify.py",
        "cases": [
          { "name": "check_directory_structure", "verifies": "All expected directories exist" },
          { "name": "check_file_completeness", "verifies": "Each directory has README.md + screenshot + HTML" },
          { "name": "check_json_validity", "verifies": "Token JSON files parse without errors" },
          { "name": "check_artboard_map", "verifies": "artboard-map.json has 76 entries" }
        ]
      }
    ]
  },
  "discoveredIssues": []
}
```

## When to Return to Orchestrator

- Required input files are missing (e.g., artboard-map.json not yet created)
- Repository structure is inconsistent with expected layout (directories missing or renamed)
- Feature scope requires Paper MCP extraction (should use extractor skill instead)
