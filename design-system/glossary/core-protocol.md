# Core & Protocol Glossary

Derived from the current Paper glossary artboard export.

## Paper Source
- **Artboard ID:** 1QH-0
- **Artboard Name:** Glossary — Core & Protocol
- **Dimensions:** 1440 × 2564

## Artifacts & Protocol

### Bifrost
The reference FROSTR node implementation. Each Bifrost node manages a Group Profile, Device Profile, and ephemeral Device State. Handles relay communication and threshold signing coordination between peers.

### Peer
Another signer node in your FROSTR threshold group. Peers coordinate over relays to co-sign requests.

### Onboarding Package
The transport format for delivering a share to a device. Used for first-time onboarding and runtime Replace Share. Contains the share secret plus group metadata needed to save or migrate a profile. Encoded as a bech32m string with the bfonboard prefix. Colloquially: "here's your bfonboard."

### bfonboard
The bech32m prefix for onboarding packages (bfonboard1...). Onboarding packages are produced outside runtime from an nsec or a threshold of source shares, then imported by Onboard or Replace Share.

### bfprofile
The bech32m prefix for profile backups (bfprofile1...). Used when importing a saved profile from text or file.

### Profile Backup
A full encrypted export of a saved profile, including its share and configuration. Import it on another device to save the same profile there.

### Export Share
Create a password-protected bfshare package for this device's share. Used as a source package during keyset rotation.

### bfshare
The bech32m prefix for password-protected share packages (bfshare1...). Used as a keyset-rotation source package and for share recovery flows.

### Package Password
Password used to decrypt bfonboard, bfprofile, or bfshare packages.

### Profile Password
The password used to encrypt and unlock a saved profile on this device.

### Package Producer
The outside-runtime process or operator that creates a bfonboard package from an nsec or threshold source shares. Runtime Replace Share only imports the finished package.

### Apply Package
The process of decrypting, validating, and saving share data from a bfonboard package. Used for first-time onboarding and runtime Replace Share.

### Profile Name
A human-readable name for a profile on this device, used to identify it in the peer list and profile selector.
