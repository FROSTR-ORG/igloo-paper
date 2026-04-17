---
name: extractor
description: Extracts content from Paper canvas artboards and writes organized reference files
---

# Extractor

NOTE: Startup and cleanup are handled by `worker-base`. This skill defines the WORK PROCEDURE.

## When to Use This Skill

Features that require extracting content from Paper canvas artboards and writing organized files: HTML references, screenshots, token files, glossary markdown, and per-directory README documentation.

## Required Skills

None. This worker uses Paper MCP tools directly (Paper___get_jsx, Paper___get_screenshot, Paper___get_tree_summary, Paper___get_children, Paper___get_node_info).

## Work Procedure

### Step 1: Read Feature Description

Read the feature description carefully. It specifies:
- Which Paper artboard IDs to extract
- Which output directories to write to
- Any special extraction rules (tokens, glossary, icons)

Read `AGENTS.md` for the full artboard ID reference and coding conventions.

### Step 2: Verify Paper MCP Access

Call `Paper___get_node_info` on the first artboard ID in your feature to verify Paper MCP is accessible. If it fails, return to orchestrator immediately.

### Step 3: For Each Artboard — Extract Content

For each artboard ID in your feature:

**3a. Get the tree summary** for structural understanding:
```
Paper___get_tree_summary(nodeId=ARTBOARD_ID, depth=5)
```
Save the tree summary text — you'll use it to write the README.md.

**3b. Get the HTML/CSS reference:**
```
Paper___get_jsx(nodeId=ARTBOARD_ID, format="tailwind")
```
Save the output as `reference.html` (design system) or `screen.html` (web screens) in the target directory.

**3c. Get the screenshot:**
```
Paper___get_screenshot(nodeId=ARTBOARD_ID)
```
The tool returns base64 PNG data. Save it to a file using:
```bash
python3 -c "
import base64, sys
data = '''BASE64_DATA_HERE'''
with open('TARGET_DIR/screenshot.png', 'wb') as f:
    f.write(base64.b64decode(data))
"
```
If the base64 string is very large (>100KB), write it to a temp file first:
```bash
# Write base64 to temp file using Create tool, then decode
python3 -c "import base64; open('TARGET_DIR/screenshot.png','wb').write(base64.b64decode(open('/tmp/ss_temp.txt').read().strip()))"
rm /tmp/ss_temp.txt
```

### Step 4: Write README.md Per Directory

For each artboard's output directory, write a `README.md` with:

```markdown
# [Artboard Name]

## Description
[What this artboard contains and its purpose in the design system / app flow]

## Paper Source
- **Artboard ID:** [ID]
- **Artboard Name:** [Full name from Paper]
- **Dimensions:** [width × height]

## Contents
[List the key elements/components/screens visible in this artboard, derived from the tree summary]

## [Additional sections as relevant]
[Usage notes, variants, states, related artboards, flow context]
```

For web screen READMEs, also include:
- **Flow:** which user flow this screen belongs to
- **Previous/Next:** screen navigation context
- **State:** what user state or condition this screen represents

### Step 5: Special Extraction Rules

**For token extraction (Foundations artboard 8B-0):**
- Parse the tree summary to extract all color names and hex values
- Parse typography names, sizes, weights, and font families
- Write structured JSON files to `design-system/tokens/`:
  - `colors.json` — organized by category (background, blue-scale, semantic, status)
  - `typography.json` — organized by scale (display, heading, body, caption, mono)
- Write `tokens.css` with CSS custom properties for all tokens
- Also write the standard reference.html and screenshot.png

**For glossary artboards (ONB-0, OSN-0, OXZ-0):**
- Use `Paper___get_tree_summary(nodeId, depth=8)` to get all text content
- Extract term names and definitions from the text nodes
- Write as markdown files in `design-system/glossary/`:
  - `core-protocol.md` (from ONB-0)
  - `operations-setup.md` (from OSN-0)
  - `policies-data-model.md` (from OXZ-0)
- Also write screenshot.png for visual reference (in the glossary/ directory)

**For shared screen elements:**
- When extracting the first web screen, also extract shared elements (AppHeader, AppFooter)
- Use `Paper___get_children` on the screen artboard to identify shared components
- Extract their JSX separately and save to `screens/_shared/app-header.html` and `screens/_shared/app-footer.html`

### Step 6: Verify Output

After extracting all artboards in the feature:
1. List the output directories and verify all expected files exist
2. Check that HTML files are non-empty
3. Check that screenshot PNGs are valid (file size > 0)
4. Check that README.md files contain substantive content

If the verification script exists (`scripts/verify.py`), run it.

### Step 7: Commit

Commit all changes with a descriptive message referencing the artboards extracted.

## Example Handoff

```json
{
  "salientSummary": "Extracted Core Components (AX-0) and Interactive Controls (E1-0) artboards. Created reference.html, screenshot.png, and README.md for each in design-system/components/core/ and design-system/components/interactive-controls/. Verified all 6 files present and non-empty.",
  "whatWasImplemented": "Extracted 2 design system artboards via Paper MCP get_jsx (Tailwind format) and get_screenshot. Core Components README documents buttons (6 variants), inputs (3 states), badges (12 variants), content cards, and alerts (4 types). Interactive Controls README documents toggles, sliders, and dropdowns. Both directories have complete file sets.",
  "whatWasLeftUndone": "",
  "verification": {
    "commandsRun": [
      {
        "command": "ls -la design-system/components/core/",
        "exitCode": 0,
        "observation": "reference.html (45KB), screenshot.png (89KB), README.md (2.1KB) all present"
      },
      {
        "command": "ls -la design-system/components/interactive-controls/",
        "exitCode": 0,
        "observation": "reference.html (62KB), screenshot.png (112KB), README.md (1.8KB) all present"
      },
      {
        "command": "wc -l design-system/components/core/reference.html",
        "exitCode": 0,
        "observation": "423 lines of Tailwind HTML"
      }
    ],
    "interactiveChecks": [
      {
        "action": "Called Paper___get_node_info on AX-0 to verify Paper MCP access",
        "observed": "Successfully returned artboard info: Core Components, 1440x1226, 5 children"
      },
      {
        "action": "Called Paper___get_jsx(AX-0, format='tailwind') for Core Components",
        "observed": "Received ~420 lines of HTML with Tailwind classes covering all component sections"
      },
      {
        "action": "Called Paper___get_screenshot(AX-0) for Core Components",
        "observed": "Received base64 PNG data, decoded to 89KB PNG file showing all button variants, input states, badges, cards, and alerts"
      }
    ]
  },
  "tests": {
    "added": []
  },
  "discoveredIssues": []
}
```

## When to Return to Orchestrator

- Paper MCP is not responding or returns errors
- An artboard ID from the feature description doesn't exist in the canvas
- The canvas appears to have changed significantly (artboard names don't match expected)
- Screenshot base64 data is too large to save via the shell (>500KB base64)
- Feature scope is unclear or artboard assignment is ambiguous
