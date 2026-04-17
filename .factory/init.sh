#!/bin/bash
# Environment setup for igloo-paper extraction mission
# Idempotent — safe to run multiple times

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Create directory structure skeleton (idempotent via -p)
mkdir -p design-system/tokens
mkdir -p design-system/foundations
mkdir -p design-system/components/core
mkdir -p design-system/components/interactive-controls
mkdir -p design-system/components/form-controls
mkdir -p design-system/components/data-display-tables-lists
mkdir -p design-system/components/data-display-progress-cards
mkdir -p design-system/components/data-display-review-summary
mkdir -p design-system/components/overlays-feedback
mkdir -p design-system/components/navigation-layout
mkdir -p design-system/components/settings-sidebar
mkdir -p design-system/patterns/signer-states-status-empty
mkdir -p design-system/patterns/signer-states-recovery
mkdir -p design-system/patterns/signer-states-tags-rotation
mkdir -p design-system/patterns/flows-qr-transfer
mkdir -p design-system/patterns/flows-qr-steppers
mkdir -p design-system/patterns/pool-signing-readiness
mkdir -p design-system/patterns/rotate-keyset-distribution
mkdir -p design-system/patterns/key-lifecycle-progress
mkdir -p design-system/icons-logos
mkdir -p design-system/glossary
mkdir -p design-system/tooltips-help/tooltip-patterns
mkdir -p design-system/tooltips-help/contextual-help
mkdir -p screens/_shared
mkdir -p screens/welcome/1-welcome
mkdir -p screens/welcome/1b-returning
mkdir -p screens/welcome/1c-returning-multi
mkdir -p screens/welcome/1c-returning-multi-alt
mkdir -p screens/welcome/1d-returning-many
mkdir -p screens/welcome/1c-1-unlock-modal
mkdir -p screens/welcome/1c-2-unlock-error-modal
mkdir -p screens/welcome/1c-3-rotate-keyset-modal
mkdir -p screens/welcome/1c-4-rotate-keyset-error-modal
mkdir -p screens/import/1-load-backup
mkdir -p screens/import/2-decrypt-backup
mkdir -p screens/import/3-review-save
mkdir -p screens/import/error
mkdir -p screens/onboard/1-enter-package
mkdir -p screens/onboard/2-handshake
mkdir -p screens/onboard/2b-failed
mkdir -p screens/onboard/3-complete
mkdir -p screens/create/1-create-keyset
mkdir -p screens/create/1b-validation-error
mkdir -p screens/create/1c-generation-progress
mkdir -p screens/shared/2-create-profile
mkdir -p screens/shared/3-distribute-shares
mkdir -p screens/shared/3b-distribution-completion
mkdir -p screens/dashboard/1-signer-dashboard
mkdir -p screens/dashboard/1b-connecting
mkdir -p screens/dashboard/1b-policies
mkdir -p screens/dashboard/1c-profile-switcher
mkdir -p screens/dashboard/1d-with-rotate-share
mkdir -p screens/dashboard/2-stopped
mkdir -p screens/dashboard/2b-all-relays-offline
mkdir -p screens/dashboard/2c-quorum-not-met
mkdir -p screens/dashboard/2d-signing-blocked
mkdir -p screens/dashboard/3-settings
mkdir -p screens/dashboard/4-export-profile
mkdir -p screens/dashboard/4b-export-complete
mkdir -p screens/dashboard/5-signer-policy-prompt
mkdir -p screens/dashboard/6-signing-failed
mkdir -p screens/dashboard/7-pending-approvals
mkdir -p screens/dashboard/8-switch-profile
mkdir -p screens/rotate-keyset/1-rotate-keyset
mkdir -p screens/rotate-keyset/1d-review-generate
mkdir -p screens/rotate-keyset/1e-generation-progress
mkdir -p screens/rotate-keyset/error-wrong-password
mkdir -p screens/rotate-keyset/error-group-mismatch
mkdir -p screens/rotate-keyset/error-generation-failed
mkdir -p screens/rotate-share/1-enter-rotate-package
mkdir -p screens/rotate-share/2-applying-share-update
mkdir -p screens/rotate-share/2b-share-update-failed
mkdir -p screens/rotate-share/3-local-share-updated
mkdir -p screens/recover/1-collect-shares
mkdir -p screens/recover/1b-recover-success
mkdir -p scripts
mkdir -p assets/icons

echo "Directory structure created successfully."
echo "Artboard count expected: 76 (24 DS + 51 screens + 1 divider)"
