#!/usr/bin/env bash
# Populate a scratch clone's submodules from the review clone's checkouts (shared objects), at the tree's gitlinks.
# Usage: scratch_submodules.sh <review-clone> <scratch-clone>
set -euo pipefail
C=$1; T=$2
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  c=$(git -C "$T" rev-parse "HEAD:$sm")
  git clone -q --shared --no-checkout "$C/$sm" "$T/$sm"
  git -C "$T/$sm" -c advice.detachedHead=false checkout -q "$c"
  echo "$sm gitlink=$c checkout=$(git -C "$T/$sm" rev-parse HEAD)"
done
