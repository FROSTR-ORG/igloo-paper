# Architecture — Igloo Paper Reference Repository

## Purpose

This repository is a **static reference codebase** — not a functional application. It captures the complete Igloo design system and web app prototype from a Paper canvas as organized, structured files optimized for human and AI agent consumption.

## Two Distinct Sections

### 1. Design System (`design-system/`)

The authoritative reference for Igloo's visual language. Contains:

- **Tokens** (`tokens/`) — Structured design tokens as JSON + CSS custom properties
  - `colors.json` — Background, primary (blue scale), semantic, status colors
  - `typography.json` — Font families, size scale, weights
  - `tokens.css` — CSS custom properties for all tokens
- **Foundations** (`foundations/`) — The base visual layer: color palettes, type scale, status indicators
- **Components** (`components/`) — Reusable UI elements organized by category:
  - Core (buttons, inputs, badges, cards, alerts)
  - Interactive Controls
  - Form Controls
  - Data Display (3 sub-categories: tables/lists, progress/cards, review/summary)
  - Overlays & Feedback
  - Navigation & Layout
  - Settings Sidebar
- **Patterns** (`patterns/`) — Domain-specific UI patterns:
  - Signer states (3 categories)
  - Flows & QR codes (2 categories)
  - Pool & signing readiness
  - Rotate keyset + shared distribution sections
  - Key lifecycle progress
- **Icons & Logos** (`icons-logos/`)
- **Glossary** (`glossary/`) — Term definitions in markdown (3 docs)
- **Tooltips & Help** (`tooltips-help/`) — Help text patterns (2 categories)

### 2. Web App Screens (`screens/`)

The full Igloo Web prototype organized by user flow. Shows the design system in action across real screens.

**Flows:**
- `welcome/` — Entry point, returning user states, profile unlock modals (9 screens)
- `import/` — Backup import flow (4 screens)
- `onboard/` — Device onboarding flow (4 screens)
- `create/` — Keyset creation flow (3 screens)
- `shared/` — Screens reused across multiple flows: profile creation, share distribution (3 screens)
- `dashboard/` — Main signer dashboard with all states (16 screens)
- `rotate-keyset/` — Full keyset rotation flow (6 screens)
- `rotate-share/` — Individual share rotation flow (4 screens)
- `recover/` — Key recovery flow (2 screens)
- `_shared/` — Shared HTML elements: AppHeader, AppFooter

## File Pattern Per Directory

Every extracted artboard produces a directory with:
- `README.md` — Description, purpose, contained elements, usage notes
- `screenshot.png` — Visual reference (PNG from Paper canvas)
- `reference.html` or `screen.html` — Full HTML/CSS with Tailwind classes (from Paper get_jsx)

Exceptions: Glossary artboards produce markdown files instead of HTML. The `_shared/` directory contains individual HTML component files.

## Data Flow

```
Paper Canvas (igloo-ui, page: core)
  ↓ get_jsx (Tailwind format)
  ↓ get_screenshot (PNG)
  ↓ get_tree_summary (for text extraction)
  ↓
Organized Repository Files
  ├── Structured tokens (JSON + CSS)
  ├── Reference HTML per artboard
  ├── Screenshots per artboard
  ├── Markdown documentation per directory
  └── Glossary as markdown
```

## Source of Truth

The Paper canvas is the source of truth. This repository is a derived artifact. When the canvas is updated, this repository should be re-extracted following `INSTRUCTIONS.md`.

## Fonts

The design system uses these font families:
- **Inter** — Primary UI font
- **Share Tech Mono** — Monospace display
- **IBM Plex Mono** — Code/technical content
- **Roboto Mono** — Alternative mono
- **System Sans-Serif** — System fallback
