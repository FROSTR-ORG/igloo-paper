# Environment

Environment variables, external dependencies, and setup notes.

**What belongs here:** Required env vars, external dependencies, platform-specific notes.
**What does NOT belong here:** Service ports/commands (use `.factory/services.yaml`).

---

## Dependencies

- **Paper MCP** — Must be running and connected. Configured globally at `~/.factory/mcp.json` pointing to `http://127.0.0.1:29979/mcp`. Paper desktop app must be open with the `igloo-ui` file on the `core` page.
- **Python 3.9+** — Used for the verification script (`scripts/verify.py`)
- **No package managers or build tools** — This is a static reference repo

## Paper Canvas Details

- **File:** igloo-ui
- **Page:** core
- **Artboard count:** 76 (24 design system + 51 web screens + 1 divider)
- **Node count:** ~12,400
- **Font families:** Inter, Share Tech Mono, IBM Plex Mono, Roboto Mono, System Sans-Serif

## No Environment Variables Required

This project has no runtime dependencies, APIs, or secrets.
