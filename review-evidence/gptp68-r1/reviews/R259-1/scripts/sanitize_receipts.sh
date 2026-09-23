#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Replace workspace-specific absolute paths in text receipts with the same
# neutral placeholders the manager's receipts use. The paths are derived
# from the environment (env.sh), never spelled here.
# Usage: sanitize_receipts.sh <receipts dir>
set -euo pipefail
. "$(dirname "$0")/env.sh"
reviews="$(dirname "$PKT")"
storage="$(dirname "$(dirname "$PINNED_BIN")")"
find "$1" -type f -print0 | xargs -0 sed -i \
  -e "s#${PKT}#\$PACKET#g" \
  -e "s#${REVIEW_CLONE}#\$REVIEW_CLONE#g" \
  -e "s#${storage}#\$VALIDATION_STORAGE#g" \
  -e "s#${reviews}#\$REVIEWS#g" \
  -e "s#${HOME}#\$WORKSPACE_HOME#g"
