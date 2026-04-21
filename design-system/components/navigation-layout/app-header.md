# AppHeader Component

The AppHeader is the primary navigation bar used across all Igloo Web screens. It adapts its content based on the user's authentication state.

## Variants

### Welcome Flow (Entry Point)

First-time or returning user entry. Designed for exploration/discovery.

**Visual Pattern:**
- Left: Snowflake icon + "Igloo" wordmark + "Threshold Signing for Nostr" subtitle
- Right: Website · Docs · GitHub navigation links

**Applied to 6 screens:**
- `34C-0` Welcome — 1. Welcome
- `6MP-0` Welcome — 1b. Returning
- `H4X-0` Welcome — 1c. Returning (Multi)
- `IMQ-0` Welcome — 1d. Returning (Many)
- `QI3-0` Unlock Profile (Modal)
- `QKO-0` Unlock Error (Modal)

### Task Flows / PublicFocus (Create / Import / Onboard)

Focused task execution. The header stays reserved for brand presence; back/exit navigation is handled by the screen-level `PageBackLink`.

**Visual Pattern:**
- Left: Snowflake icon + "Igloo" wordmark + "Threshold Signing for Nostr" subtitle
- Right: Passive flow tag (`Create`, `Import`, or `Onboard`)

**Applied to 11 screens:**

**Create (3 screens):**
- `35L-0` Create — 1. Create Keyset
- `RNX-0` Create — 1c. Generation Progress
- `4FB-0` Create — 1b. Validation Error

**Import (4 screens):**
- `3B1-0` Import — 1. Load Backup
- `6VS-0` Import — 2. Decrypt Backup
- `6XP-0` Import — 3. Review & Save Profile
- `6ZH-0` Import — Error

**Onboard (4 screens):**
- `GW5-0` Onboard — 1. Enter Package
- `70L-0` Onboard — 2. Handshake
- `726-0` Onboard — 3. Onboarding Complete
- `73U-0` Onboard — 2b. Onboarding Failed

### Post-Auth with Profile Context

Used when a profile is selected but not fully unlocked (intermediate states).

**Visual Pattern:**
- Left: Snowflake icon + "Igloo" wordmark
- Right: Active profile name (e.g., "My Signing Key")

**Applied to 15 screens:**
- `60R-0` Create Profile
- `83Q-0` Rotate Keyset
- `8GU-0` Distribute Shares
- `IS8-0` Enter Rotate Package
- `JIJ-0` Local Share Updated
- `J3O-0` Share Update Failed
- `LPE-0` Error: Wrong Password
- `LRH-0` Error: Group Mismatch
- `LTC-0` Error: Generation Failed
- `LN7-0` Distribution Completion
- `LF2-0` Review & Generate
- `LHT-0` Generation Progress
- `IV8-0` Applying Share Update
- `59J-0` Collect Shares
- `3HJ-0` Recover Success

### Dashboard (Fully Unlocked)

Used when signer is fully operational.

**Visual Pattern:**
- Left: Snowflake icon + "Igloo" wordmark
- Right: Action buttons (Recover · Export · Policies · Settings)

**Applied to dashboard screens:**
- `3QW-0` Signer Dashboard
- `DCI-0` Policies
- `518-0` Settings & Lock Profile
- And all other dashboard variants

## Structure

```
AppHeader (1440×120)
└── Pill (1000×74, flex, space-between, align-center)
    ├── Left Cluster (flex, align-center, gap: 14px)
    │   ├── Snowflake Icon (44×44)
    │   └── Wordmark (flex-col, gap: 2px, width: 180px)
    │       ├── "Igloo" (Inter, 28/32, #60A5FA, weight 700)
    │       └── "Threshold Signing for Nostr" (Inter, 12/16, #64748B)
    └── Right Cluster
        ├── Welcome Flow: "Website" · "Docs" · "GitHub" (Paper Mono, 13/16, #8494A7)
        ├── Task Flows: passive flow tag (Paper Mono, 13/16, #8494A7)
        ├── Post-Auth: Profile Name (Inter, 16px, #8494A7)
        └── Dashboard: [Buttons]
```

## Styling Specification

### Container
- Width: 100% (1440px in artboards)
- Height: 120px
- Padding: 20px vertical, 80px horizontal
- Display: flex
- Justify: center
- Align: center

### Pill
- Width: 1000px
- Height: 74px
- Background: `#0F172A99` (semi-transparent dark)
- Border: 1px solid `#1E3A8A4D`
- Border-radius: 12px
- Padding: 14px 20px
- Display: flex
- Justify: space-between
- Align: center

### Left Cluster
- Display: flex
- Align: center
- Gap: 14px

#### Snowflake Icon
- Width: 44px
- Height: 44px
- Border-radius: 10px

#### Wordmark
- Display: flex
- Direction: column
- Gap: 2px
- Width: 180px
- Height: 50px

##### "Igloo" (Primary)
- Font: Inter, system-ui, sans-serif
- Size: 28px
- Line-height: 32px
- Letter-spacing: -0.01em
- Weight: 700
- Color: `#60A5FA`
- White-space: nowrap

##### "Threshold Signing for Nostr" (Subtitle)
- Font: Inter, system-ui, sans-serif
- Size: 12px
- Line-height: 16px
- Letter-spacing: 0.01em
- Weight: 400
- Color: `#64748B`
- White-space: nowrap

### Right Cluster (Welcome Links)
- Display: flex
- Align: center
- Gap: 20px

#### Nav Links
- Font: Paper Mono (Preview), monospace
- Size: 13px
- Line-height: 16px
- Weight: 400
- Color: `#8494A7`
- White-space: nowrap

### Right Cluster (PublicFocus)
- Display-only flow tag when no other right-side header content exists.
- Do not render back or exit copy in the app header.
- Do not replace `PublicLinks`, `FlowContext`, or `AuthActions` content.

#### HeaderFlowTag
- Text only, no icon.
- Font: Paper Mono (Preview), monospace fallback.
- Size: 13px.
- Line-height: 16px.
- Weight: 400.
- Color: `#8494A7`.
- White-space: nowrap.
- Labels: `Create`, `Import`, `Onboard`; reserve `Rotate` for rotate headers that do not already show profile context.

### Right Cluster (Post-Auth Profile)
- Font: Inter, system-ui, sans-serif
- Size: 16px
- Weight: 400
- Color: `#8494A7`

## PageBackLink

Use one screen-level `PageBackLink` when the screen needs backward navigation.

- Placement: first item in the content column, before stepper/title/body content.
- Icon: 14px chevron-left.
- Label: Inter 13/18, destination-aware (`Back`, `Back to Welcome`, `Back to Settings`, `Back to Signer`).
- Hit target: minimum 32px height.
- Gap: 6px between icon and label.
- Default color: `#8494A7`.
- Hover/focus color: `#93C5FD`.
- Error screens with contextual recovery buttons should not also render a top `PageBackLink`.

## State Logic

| Flow Type | Condition | Right Cluster |
|-----------|-----------|---------------|
| Welcome | Entry screen | Website · Docs · GitHub |
| Create / Import / Onboard | Task in progress | Passive flow tag |
| Profile context | `profile && !unlocked` | Profile name |
| Dashboard | `profile && unlocked` | Action buttons |

## Paper References

- **Navigation & Layout artboard:** `LW-0` (component reference)
- **Foundations artboard:** `8B-0` (color tokens)
- **Typography tokens:** See `design-system/tokens/typography.json`
