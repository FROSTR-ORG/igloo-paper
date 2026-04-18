# Core Components

## Description

The Core Components artboard contains the fundamental UI building blocks of the Igloo design system. These are the most commonly reused elements across the application, including buttons, text inputs, status badges, content cards, and alert banners. Each component is shown with its variant label and styling notes.

## Paper Source

- **Artboard ID:** AX-0
- **Artboard Name:** Core Components
- **Dimensions:** 1440 × 1254

## Contents

### Buttons (7 variants)

| Variant | Style | Color |
|---------|-------|-------|
| **Primary** | Solid fill | `bg-blue-600` (#2563EB), white text |
| **Ghost** | Transparent with border | `border-blue-500/30`, blue-300 text |
| **Destructive** | Solid fill | `bg-red-600` (#DC2626), white text |
| **Success** | Solid fill | `bg-green-600` (#16A34A), white text |
| **Secondary** | Semi-transparent fill + border | `bg-gray-800/50`, `border-blue-900/50`, blue-300 text |
| **Outline** | Border only | `border-slate-400/30`, slate-400 text |
| **Ghost Blue** | Transparent with blue border | `border-blue-900/45`, blue-300 text |

#### Icon Buttons (3 variants)
- **Ghost** — Copy icon, no background, slate stroke
- **Destructive** — Trash icon, `bg-red-600/10`, red stroke
- **Default** — Settings icon, `bg-blue-900/30`, blue stroke

All buttons use `rounded-lg`, `py-2.5 px-5`, Inter font medium at 14px.

### Inputs (3 states)

| State | Border | Notes |
|-------|--------|-------|
| **Default** | `border-blue-900/30` | Placeholder text, helper text below |
| **Focused** | `border-2 border-blue-500/50` | Monospace value, ring highlight |
| **Error** | `border-red-600/50` | Red error message, eye icon for password |

All inputs use `rounded-lg`, `bg-slate-900/60`, `py-2.5 px-3`, 14px text.

### Badges (11 variants)

All badges use `rounded-full`, `py-1 px-2.5`, 12px medium text with semi-transparent background and border:

| Badge | Text Color | Background |
|-------|-----------|------------|
| **Connected** | `#4ADE80` (green-400) | green-600/15 |
| **Error** | `#F87171` (red-400) | red-600/15 |
| **Slow** | `#FACC15` (yellow-300) | yellow-500/15 |
| **Info** | `#60A5FA` (blue-400) | blue-500/15 |
| **Onboarding** | `#FBBF24` (amber-400) | amber-400/15, Share Tech Mono uppercase |
| **Recovery** | `#C084FC` (purple-400) | purple-600/15 |
| **Signing** | `#FB923C` (orange-400) | orange-500/15 |
| **PEER POLICY** | `#60A5FA` (blue-400) | blue-400/15 |
| **Local Replace** | `#60A5FA` (blue-400) | blue-600/15 |
| **Rotate Existing** | `#FBBF24` (amber-400) | amber-500/15 |
| **New Device** | `#4ADE80` (green-400) | green-600/15 |

### Content Card

A dark card component (`bg-[#11182766]`, `border-blue-900/30`, shadow) containing:
- Title in Share Tech Mono (blue-300)
- Subtitle in Inter (gray-400)
- Divider line
- Key-value rows (Status with Connected badge, Active Keys, Connected Relays)
- Action buttons row (ghost "Settings", primary "Manage Keys")

### Alerts (4 types)

| Type | Icon | Colors |
|------|------|--------|
| **Info** | `i` circle | Blue tones — `bg-blue-500/10`, `border-blue-500/25` |
| **Success** | `✓` circle | Green tones — `bg-green-500/10`, `border-green-500/25` |
| **Error** | `!` circle | Red tones — `bg-red-400/10`, `border-red-400/25` |
| **Warning** | `!` circle | Amber tones — `bg-amber-500/10`, `border-amber-500/25` |

Each alert has a title (semibold) and description text, with colors matching the alert severity.

## Usage Notes

- All components use the dark theme color palette with semi-transparent backgrounds
- Font stack: Inter for UI text, Share Tech Mono for labels and monospace values
- Consistent border-radius: `rounded-lg` (8px) for buttons/inputs/cards, `rounded-full` for badges
- Backgrounds use oklch/oklab gradients for the artboard canvas
