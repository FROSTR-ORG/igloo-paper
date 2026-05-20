# Canvas + Repo Sync (igloo-ui-shared)

Paper file: **igloo-ui-shared** (`01KS0ZAKQ6KF98SHDJHB6STG1K`), page **core**.

## Paper changes (done)

1. Divider flow map split: Import / Onboard · Recipient / Onboard · Sponsor
2. **Recover Flow Sections** artboard (`BI4-0`) at `left: 12080`, `top: -11749`
3. Row label **Import Backup** (`BR8-0`) above import row
4. AIH sponsor subtitle corrected to runtime path

## Repo sync (run after restoring full igloo-paper tree)

```bash
# 1. Remap all paperNodeId values from snapshot (name-based)
python3 scripts/remap_artboard_ids.py

# 2. Patch export-metadata (Recover Flow + paper file id)
python3 scripts/apply_export_metadata_patch.py

# 3. Update verify.py expected counts (31 / 55 / 1 / 87 total)
python3 scripts/patch_verify_counts.py

# 4. Point export script at igloo-ui-shared (if hardcoded — check scripts/export_from_paper.py)

# 5. Export + verify
python3 scripts/export_from_paper.py
python3 scripts/verify.py
python3 scripts/verify.py --strict-drift
```

Refresh snapshot after future Paper changes:

```bash
# Paste get_basic_info artboards array into scripts/paper_artboards.shared.json, then:
python3 scripts/remap_artboard_ids.py
```

## Key ID changes (old igloo-ui → igloo-ui-shared)

| Role | Old | New |
|------|-----|-----|
| Divider | `347-0` | `3QR-0` |
| Settings screen | `518-0` | `502-0` |
| Sponsor Configure | `1B3Q-0` | `8V1-0` |
| Recipient Enter Package | `GW5-0` | `8SU-0` |
| DS Sponsor Sections | `1BUV-0` | `AIH-0` |
| DS Recipient Sections | `1CTF-0` | `AYG-0` |
| Recover Flow Sections | `N4P-0`* | `BI4-0` |

\*Old `N4P-0` was extended Signer Recovery DS; new `BI4-0` is the dedicated outside-runtime recover flow-sections board.
