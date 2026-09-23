#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Leg sizes and bases at base, reviewed and head (scripts/leg_sizes.py).
set -eu
. "$(dirname "$0")/env.sh"
python3 "$PACKET/scripts/leg_sizes.py" "$CLONE" "$BASE_SHA" "$REVIEWED_SHA" "$HEAD_SHA"
