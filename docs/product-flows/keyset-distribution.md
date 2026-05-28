# Keyset Distribution Notes

This document preserves product-flow details that were previously mixed into Paper design reference boards. The design exports should show canonical UI surfaces only; protocol notes, implementation warnings, and standalone state diagrams belong here.

## Outside-Runtime Rotation

Keyset rotation is an outside-runtime flow. It reconstructs the existing signing key from threshold source packages, creates fresh shares for the same group public key, replaces the current local source profile, and prepares remote onboarding packages for the other devices to adopt.

Shared Select Share, Save Profile, and Distribute Shares screens are reused by both new key creation and keyset rotation. Runtime Replace Share remains a separate Settings-launched maintenance flow.

## Shared Select Share

The operator chooses which generated share stays on this device on the Select Share screen. Exactly one share is marked for local save; the remaining shares are distributed remotely after the profile is saved.

Select Share also surfaces the group public key with a copy action so the operator can verify or retain the group identity before saving the local profile.

For keyset rotation, the local share is predetermined (Local Replace for the rotating device) and the picker is read-only.

## Shared Save Profile

Save Profile collects the local profile name, profile password, and relay list. Peer permission defaults are configured per remote share in the distribution workspace instead of on the profile-save step.

## Distribution Workspace

Distribution is completed per remote share:

- Set a package password for the remote device.
- Saving the password creates the remote onboarding package for that device.
- Once the package exists, Copy, Save, QR code, and Done actions are available for that share.
- The Done action manually marks handoff complete when the operator has finished distribution.

Package actions stay hidden until a saved password creates the package.

## Remote Share State Sequence

- Package not created: password field is editable; distribution actions are hidden.
- Package created: package content exists and Copy, Save, QR code, and Done actions are available.
- Done: the remote share handoff is marked complete and distribution actions are hidden.
