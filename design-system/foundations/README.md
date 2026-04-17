# Foundations

The Foundations artboard defines the complete design token system for the Igloo UI. Every color, font, and typographic scale used across components and screens originates here. This is the single source of truth that all other artboards reference.

## Description

The Foundations artboard establishes the visual language of Igloo — a dark-themed, security-focused application with a technical, crypto-native aesthetic. The palette is built on deep blue-grays for backgrounds, a blue primary scale for interactive elements, and carefully chosen semantic and status colors for system feedback.

## Paper Source

- **Artboard ID:** 8B-0
- **Artboard Name:** Foundations
- **Dimensions:** 1440 × 1080

## Token Categories

### Background Colors

Four background tokens define the depth layers of the interface:

| Token | Value | Usage |
|-------|-------|-------|
| `gray-950` | `#030712` | Primary app background — the darkest surface |
| `gray-900` | `#111827` | Secondary background for elevated containers |
| `gray-800/50` | `rgba(31,41,55,0.5)` | Semi-transparent overlay for modals and dimmed surfaces |
| `gray-900/40` | `rgba(17,24,39,0.4)` | Card surface — translucent background for card components |

### Blue Scale — Primary

The blue scale provides the primary accent palette used for interactive elements, headings, and brand expression:

| Token | Value | Usage |
|-------|-------|-------|
| `blue-100` | `#DBEAFE` | Lightest — subtle highlights and backgrounds |
| `blue-200` | `#BFDBFE` | Light — hover states, secondary highlights |
| `blue-300` | `#93C5FD` | Medium-light — heading text, active indicators |
| `blue-400` | `#60A5FA` | Medium — links, interactive text, info accents |
| `blue-600` | `#2563EB` | Primary — buttons, strong interactive elements |
| `blue-700` | `#1D4ED8` | Dark — pressed/active button states |
| `blue-900` | `#1E3A8A` | Deepest — borders, subtle dividers, container outlines |

### Semantic Colors

Semantic colors convey meaning — success, error, warning — through both solid foregrounds and translucent backgrounds:

| Token | Value | Usage |
|-------|-------|-------|
| `green-500` | `#22C55E` | Success — positive actions, confirmations |
| `red-500` | `#EF4444` | Destructive — errors, danger states |
| `yellow-500` | `#EAB308` | Warning — caution indicators |
| `amber-900` | `#78350FE6` | Caution background — muted amber surface |
| `green-900/30` | `#15803D4D` | Success background — translucent green for alerts |
| `red-900/30` | `#7F1D1D4D` | Error background — translucent red for alerts |
| `yellow-900/30` | `#713F124D` | Warning background — translucent yellow for alerts |

### Status Colors

Status indicators use colored dot badges with matching tinted backgrounds and ring borders:

| Status | Dot Color | Label Color | Background | Ring |
|--------|-----------|-------------|------------|------|
| Default (Offline) | `#6B7280` | `#9CA3AF` | `#6B728033` | `#6B72804D` |
| Success (Connected) | `#22C55E` | `#4ADE80` | `#22C55E33` | `#22C55E4D` |
| Error | `#EF4444` | `#F87171` | `#EF444433` | `#EF44444D` |
| Warning | `#EAB308` | `#FACC15` | `#EAB30833` | `#EAB3084D` |
| Info | `#3B82F6` | `#60A5FA` | `#3B82F633` | `#3B82F64D` |

### Typography

The type system uses two primary fonts with a monospace-forward aesthetic:

**Font Families:**
- **Share Tech Mono** — Primary display/heading font. Used for H1–H3 headings, section labels, and branded text. Gives the UI a technical, crypto-native feel.
- **Inter** — Primary body font. Used for all general UI text, labels, descriptions, and button labels.
- **IBM Plex Mono** — Code and data display (hex values, cryptographic keys).
- **Roboto Mono** — Alternative monospace for numeric displays and tabular data.
- **System Sans-Serif** — Fallback for OS-native UI elements.

**Type Scale:**

| Level | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| H1 | Share Tech Mono | 36px / bold | 700 | Page titles, hero sections |
| H2 | Share Tech Mono | 24px / semibold | 600 | Section headings, card group titles |
| H3 | Share Tech Mono | 20px / semibold | 600 | Card headings, dialog titles |
| Body | Inter | 14px / regular | 400 | Standard paragraph and UI text |
| Small | Inter | 12px / regular | 400 | Labels, metadata, secondary info |
| Section Label | Share Tech Mono | 13px / uppercase | 400 | Category headers (0.08em tracking) |
| Overline | Share Tech Mono | 11px / uppercase | 400 | Small branded text (0.12em tracking) |

## Contents

- `reference.html` — Tailwind CSS HTML extracted directly from the Paper artboard
- `screenshot.png` — Visual screenshot of the complete Foundations artboard

## Related Files

- `../tokens/colors.json` — Structured JSON of all color tokens by category
- `../tokens/typography.json` — Structured JSON of font families and type scale
- `../tokens/tokens.css` — CSS custom properties for all tokens
