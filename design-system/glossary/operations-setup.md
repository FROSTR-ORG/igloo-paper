# Operations, Setup & Infrastructure Glossary

Derived from the current Paper glossary artboard export.

## Paper Source
- **Artboard ID:** OSN-0
- **Artboard Name:** Glossary — Operations, Setup & Infrastructure
- **Dimensions:** 1440 × 2086

## Operations

### Import
Bringing a profile onto this device from an external source.

### Recover
Recovering a profile from a relay using a share.

### Load
Selecting a saved profile that already exists on this device.

### Recover NSEC
Combining a threshold of shares to recover the original nsec.

### Unlock
Decrypting a saved local profile that is encrypted at rest.

### Lock Profile
Encrypting and unloading the active profile, returning to the profile list. The profile remains saved on this device.

### Clear Credentials
Deleting this device's saved profile, share, password, and relay configuration. Shared group data and other peers are not changed.

### Switch Profile
Locking the current active profile and unlocking a different saved profile. Requires the target profile's password.

### Profile List
The selection screen showing all saved profiles on this device, allowing the user to choose which to unlock.

## Device Setup

### Create Keyset
The outside-runtime flow for generating a new FROSTR threshold keyset from scratch. Generates a new signing key and initial share set, then converges into shared Create Profile and Distribute Shares.

### Import Device Profile
A device setup path for bringing an existing profile onto this device from a backup or by recovering it from a relay.

### Onboard Device
A device setup path for applying an onboarding package (bfonboard) that was produced outside runtime. Used for first-time device onboarding and for replacing a loaded profile's local share in runtime.

### Rotate Keyset
Outside-runtime full-keyset rotation launched from a saved profile card on returning before a profile is loaded into the signer. The selected saved profile automatically provides the local source share as Source Share #1, and the operator adds the remaining threshold source packages externally. Each source package may be a bfprofile or bfshare. Fresh device shares are generated for the same group public key, then the flow converges into shared Create Profile and Distribute Shares.

### Replace Share
Inside-runtime single-share replacement launched from Settings for the currently loaded profile. The operator imports a valid onboarding package and password, applies the replacement, and returns to the signer with the same group public key and a new local share.

## Signing Infrastructure

### Signing Capacity
The number of signatures your node can produce with a given peer before needing to replenish. Each unit of capacity corresponds to a pre-exchanged nonce. Displayed as a visual bar and count in the peer list. When capacity runs low, it is automatically refilled during health checks.

### Nonce Pool
A reserve of pre-computed cryptographic nonces exchanged between peers. Each peer maintains two pools per counterpart: an outgoing pool (nonces you sent) and an incoming pool (nonces you received). One nonce is consumed per signature. Surfaced in the UI as "signing capacity" — users see the pool level without needing to understand the cryptographic mechanism. Default pool size: 100, low threshold: 20, critical threshold: 5.

### Nonce
A one-time random value used in threshold signature generation. In FROSTR, peers pre-exchange nonces so that signatures can be produced instantly without an extra round trip. Each nonce can only be used once — reusing a nonce would compromise the private key. The term "nonce" is never shown in the user interface; it is abstracted as "signing capacity."

### Health Check (Ping/Pong)
A periodic ping/pong exchange between signer nodes. Confirms peer liveness, measures latency, and — critically — replenishes nonce pools when they fall below the minimum threshold. Health checks are the mechanism that keeps signing capacity topped up. Shown in the event log as PING events and, when nonces are exchanged, as SYNC events.

### Sync Event
A log event indicating that nonce pools have been exchanged with a peer. Triggered during health checks when a peer’s pool drops below the minimum threshold. The event reports how many nonces were exchanged in each direction (e.g., "Pool sync with peer #0 — 50 received · 50 sent"). Asymmetric exchanges are flagged. Displayed with a teal SYNC badge in the event log.
