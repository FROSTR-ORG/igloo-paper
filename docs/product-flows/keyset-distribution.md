# Keyset Distribution Notes

This document preserves product-flow details that were previously mixed into Paper design reference boards. The design exports should show canonical UI surfaces only; protocol notes, implementation warnings, and standalone state diagrams belong here.

## Outside-Runtime Rotation

Keyset rotation is an outside-runtime flow. It reconstructs the existing signing key from threshold source packages, creates fresh shares for the same group public key, replaces the current local source profile, and prepares remote bfonboard packages for the other devices to adopt.

Shared Create Profile and Distribute Shares screens are reused by both new key creation and keyset rotation. Runtime Replace Share remains a separate Settings-launched maintenance flow.

## Shared Create Profile

The operator chooses which generated share stays on this device on the shared Create Profile screen. Exactly one share is marked for local save; the remaining shares are distributed remotely on the next step.

The profile setup surface combines that local-share picker with profile name, profile password, relay list editing, and peer permission editing. For keyset rotation, the local share is predetermined (Local Replace for the rotating device) and the picker is read-only.

Rotate Keyset reuses this screen but does not reopen share selection — the rotating device's replacement share is already assigned before profile setup begins.

## Distribution Workspace

Distribution is completed per remote share (every index except the one saved locally on Create Profile):

- Set a package password for the remote device.
- Saving the password creates the bfonboard package for that device.
- Copy the package and password, or show the QR code, once the package exists.
- Echo confirmation or manual marking completes the handoff.

Package actions stay disabled until a saved password creates the package.

## Remote Share State Sequence

- Package not created: password field is editable; copy, QR, and manual mark stay disabled.
- Ready to distribute: package and masked password exist; transfer actions unlock.
- Waiting for echo: after copy or QR handoff, amber status keeps manual mark available.
- Echo received: green completed state from device confirmation.
- Manually marked: green completed state from operator confirmation.

Echo confirmation and manual marking both count as completed package handoff.
