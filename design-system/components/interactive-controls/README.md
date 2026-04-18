# Interactive Controls

## Description

The Interactive Controls artboard contains complex, interactive UI components used throughout the Igloo application. These go beyond basic buttons and inputs to include tabbed navigation, list editors, collapsible sections, credential displays, validated inputs, full-width action buttons, profile switcher dropdowns, and peer permission editors.

## Paper Source

- **Artboard ID:** E1-0
- **Artboard Name:** Interactive Controls
- **Dimensions:** 1440 × 2351

## Contents

### Tabs

A segmented tab bar with pill-style active indicator:
- **Container:** `rounded-lg`, `bg-gray-800/50`, `p-1`
- **Active tab:** `rounded-md`, `bg-blue-900/60`, blue-200 text
- **Inactive tab:** `rounded-md`, blue-400 text
- Example tabs: Overview, Keys, Relays, Event Log

### Relay List Editor

An editable list component for managing WebSocket relay URLs:
- **Container:** `rounded-xl`, `bg-slate-900/60`, `border-blue-900/30`
- **Rows:** Each relay URL displayed in Share Tech Mono (blue-400) with a red X delete button
- **Add row:** Input field with `wss://` placeholder and green "Add" button (`bg-green-600`)
- **Variant note:** Full-form screens may include per-row helper text (connection status, latency)

### Collapsible Section

Expandable/collapsible panels with status indicators:
- **Expanded state:** Chevron-down icon, content visible, green dot (running), border-bottom divider
- **Collapsed state:** Chevron-right icon, content hidden, red dot (stopped), no divider
- **Header:** Title (semibold), count badge (`rounded-full`, blue-500/15), status dot
- Example: "Event Log (24)" expanded, "Peers (3)" collapsed

### Credential Display

A card showing FROST key share credentials:
- **Header:** Key name ("My Signing Key"), share info ("Share 1 of 3", "Threshold: 2 of 3"), Active badge
- **Public Key row:** Label (uppercase, muted), npub value (blue-400, mono), copy button
- **Local Share row:** Label, masked value (dots), eye toggle + copy buttons
- **Group Key row:** Label, hex value (purple-400, mono), eye-off toggle + copy buttons
- **Container:** `rounded-xl`, `bg-slate-900/60`, `border-blue-900/30`

### Input With Validation

Input fields with inline validation feedback:
- **Valid state:** Green border (`border-green-600/40`), green checkmark icon, green helper text ("Valid relay URL")
- **Invalid state:** Red border (`border-red-600/40`), red X icon, red helper text ("Must start with wss:// or ws://")
- Both use Share Tech Mono for the input value

### Full-Width Action Button

Wide, centered action buttons used for important single actions:
- **Active state:** `bg-blue-600/25`, white/66 text, `rounded-lg`, full width
- **Disabled state:** `opacity-50`, `bg-blue-600/10`, white/27 text, helper text below ("1 more share needed to meet the 3-of-5 threshold")
- Example: "Recover NSEC" button

### Profile Switcher Dropdown

A dropdown menu for switching between key profiles:
- **Container:** `rounded-[10px]`, `bg-slate-900/93`, heavy shadow, `border-blue-900/30`
- **Active profile:** Blue background tint (`bg-blue-900/20`), blue checkmark, blue-300 name
- **Inactive profiles:** No background, muted text
- **Each row:** Lock icon, profile name (mono), share info (e.g., "2/3 · #0 · npub1qe3...7k4m")
- **Add Profile:** Ghost variant with plus icon, blue-400/70 text, separated by divider

### Peer Permission Editor

Editable peer rows with permission chips:
- **Container:** Stacked rows, each `h-12`, `rounded-lg`, `bg-slate-900/60`, `border-blue-900/30`
- **Peer info:** Peer name ("Peer #0", "Peer #1") with optional truncated public key
- **Permission chips:** Inline colored chips in Share Tech Mono uppercase:
  - **SIGN** — Green (`#22C55E`)
  - **ECDH** — Cyan (`#22D3EE`)
  - **PING** — Purple (`#A855F7`)
  - **ONBOARD** — Amber (`#FBBF24`)
- Chips can be active (full opacity) or inactive (reduced opacity)
- Used for defaults and local profile setup (not read-only policy review)

## Usage Notes

- All components follow the dark theme with semi-transparent backgrounds
- Interactive states (hover, focus) are implied but not shown — use consistent patterns from Core Components
- Relay List Editor and Peer Permission Editor are designed for both full-screen and sidebar contexts
- The Profile Switcher Dropdown is used in the app header for quick profile switching
