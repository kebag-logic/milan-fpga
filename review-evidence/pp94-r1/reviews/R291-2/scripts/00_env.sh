#!/usr/bin/env bash
# Shared environment for the R291-2 probes. Override PKT / VBIN / SRC as needed.
set -euo pipefail
PKT=${PKT:-$REVIEWS/pp94-r291-2-packet}
SRC=${SRC:-$REVIEWS/r291-2-pp94}           # exact-head clone (read only)
HEAD_SHA=cc077a6ffe20585d20b116f008e07189ba1bb7f8
VBIN=${VBIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}
TREE=$PKT/scratch/tree                                 # git-archive export of HEAD_SHA
RCPT=$PKT/receipts
export PATH="$VBIN:$PATH"
