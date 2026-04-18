# Policies & Data Model Glossary

Derived from the current Paper glossary artboard export.

## Paper Source
- **Artboard ID:** OXZ-0
- **Artboard Name:** Glossary — Policies & Data Model
- **Dimensions:** 1440 × 1338

## Permissions & Policies

### Permission Tags
Labels assigned to peers that control allowed peer actions. Peer policy tags are SIGN, ECDH, PING, and ONBOARD. Requests not explicitly allowed by signer policies require a peer policy decision.

### SIGN
A permission tag that allows a peer to automatically trigger signing operations. When a peer has the SIGN tag, your node responds to their signature requests without manual approval.

### ECDH
A permission tag that allows a peer to trigger ECDH key exchange operations used by nip04/nip44 encryption flows. Requests not explicitly allowed by signer policies require a peer policy decision.

### ONBOARD
A permission tag that allows onboarding operations for this peer/device relationship, including onboarding package exchange and handshake steps.

### PING
A permission tag that allows peer health-check actions (ping/pong). Grants this peer permission to participate in connectivity and latency checks.

### Signer Policy Prompt
A prompt shown for external requests not explicitly allowed by signer policies. Displays method details and requester pubkey. Options: Reject, Allow once, Allow forever, or Allow forever for kind X. If timeout expires, the request is rejected.

### NIP-44
A Nostr encryption standard for private messages. Uses ECDH key exchange to derive a shared secret between two pubkeys. In Igloo, ECDH operations for NIP-44 require the ECDH permission tag or manual approval.

### Signer Policies
Rules that control how this signer responds to external requests using NIP-46 permission strings (get_public_key, sign_event, sign_event:

### , nip04_encrypt/decrypt, nip44_encrypt/decrypt, switch_relays). Decisions: Allow once, Allow forever, Allow forever for kind X, or Reject. Requests not explicitly allowed require a peer policy decision.


## Data Model

### Group Profile
Shared keyset configuration visible to all peers. Contains keyset name, keyset npub, threshold, total keys, and created/updated timestamps. Synced via Nostr automatically — cannot be edited from a single device.

### Device Profile
The local configuration for a single profile. Contains the share key, index, profile name, relay list, and peer policies. Each device configures its profiles independently — changes only affect this device.

### Device State
Ephemeral runtime data such as nonce pools and pending operations. Not persisted or shared between devices — regenerated each session.

### Profile
A saved local profile containing one share plus the configuration needed to use it on this device.
