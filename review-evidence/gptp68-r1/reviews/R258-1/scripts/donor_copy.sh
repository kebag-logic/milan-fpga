#!/bin/bash
# Export the donor tree at REV into a disposable scratch directory and run
# one make target there with the pinned Verilator first on PATH, so no build
# product is ever written into the review clone.
# Usage: donor_copy.sh <label> <rev> <make args...>
set -euo pipefail
. "$(dirname "$0")/env.sh"
label=$1; rev=$2; shift 2
dst=$PACKET/scratch/donor-$label
rm -rf "$dst"; mkdir -p "$dst"
git -C "$CLONE" archive "$rev" | tar -x -C "$dst"
echo "verilator: $(command -v verilator) $(verilator --version)"
echo "donor $(git -C "$CLONE" rev-parse "$rev") label $label: make $*"
make -C "$dst" "$@"
