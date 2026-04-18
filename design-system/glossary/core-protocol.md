# Core & Protocol Glossary

Derived from the current Paper glossary artboard export.

## Paper Source
- **Artboard ID:** ONB-0
- **Artboard Name:** Glossary — Core & Protocol
- **Dimensions:** 1440 × 2564

## Core Concepts

### FROSTR
Flexible Round-Optimized Schnorr Threshold signatures. Splits an nsec into k-of-n shares and coordinates signing over Nostr relays via bifrost nodes.

### Share
An individual secret key piece within a FROSTR keyset's group. A single share cannot sign or reveal the private key — only a threshold of shares working together can produce a signature. Each device holds exactly one share. For transport, a share is wrapped with group metadata into an onboarding package (bfonboard).

### Keyset
The complete FROSTR threshold signing unit: a group of related shares plus the shared group configuration (Group Profile). A keyset is identified by its keyset npub and name. Shares from different keysets cannot be combined.

### nsec
Your Nostr private key. In Igloo it is split into shares — the full key is never reconstructed during signing.

### Threshold
The minimum number of shares required to produce a valid signature (e.g., 2-of-3 means any 2 of 3 shares can sign).

### Relay
A Nostr relay server that facilitates communication between signer nodes. All signers in a group need at least one common relay.

### Index
The numeric identifier of a share within a keyset (e.g. #0, #1, #2). Each device holds one share at a specific index. Index 0 is assigned to the creator by default.

### Remote Signing Service
The app category label shown in the header. Refers to any igloo application that signs Nostr events on behalf of a user from a remote device or browser, using FROST threshold signatures.

### Keyset npub
The group public key of a FROSTR keyset, displayed in npub format. Visible to all peers via the group profile. Derived from the signing key that was split into shares.

### Group
The collective signing unit within a keyset. Consists of all shares, the shared group configuration, and the group's public key. When we say "the group" we mean the set of participants and their shared parameters — distinct from any individual share.

## Artifacts & Protocol

### Bifrost
The reference FROSTR node implementation. Each Bifrost node manages a Group Profile, Device Profile, and ephemeral Device State. Handles relay communication and threshold signing coordination between peers.

### Peer
Another signer node in your FROSTR threshold group. Peers coordinate over relays to co-sign requests.

### Onboarding Package
The transport format for delivering a share to a device. Used for both first-time onboarding and rotated-share adoption. Contains the share secret plus group metadata needed to connect to an onboarding peer. Encoded as a bech32m string with the bfonboard prefix. Colloquially: "here's your bfonboard."

### bfonboard
The bech32m prefix for onboarding packages (bfonboard1...). Used for standard onboarding, including first-time onboarding and rotated-share adoption.

### bfprofile
The bech32m prefix for profile backups (bfprofile1...). Used when importing a saved profile from text or file.

### Profile Backup
A full encrypted export of a saved profile, including its share and configuration. Import it on another device to save the same profile there.

### Export Share
Copy the raw share key in hex format. This export is unencrypted, so handle it with care. Available in Settings under Export & Backup.

### bfshare
The bech32m prefix for shares (bfshare1...). Used when recovering a profile from a relay.

### Package Password
The password that decrypts an onboarding package (bfonboard1...) during onboarding.

### Profile Password
The password used to encrypt and unlock a saved profile on this device.

### Onboarding Peer
The device already online that sponsors onboarding for another device. During onboarding, the onboarding peer transmits group configuration and share data over relays. Must be online for onboarding to complete.

### Handshake
The process of connecting to relays, finding an onboarding peer, and receiving group/share data from a bfonboard package. Used for both first-time onboarding and rotated-share adoption.

### Profile Name
A human-readable name for a profile on this device, used to identify it in the peer list and profile selector.
