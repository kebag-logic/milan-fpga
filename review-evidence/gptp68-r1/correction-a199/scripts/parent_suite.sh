#!/bin/bash
# Run one parent suite's default target on a disposable copy of the private
# parent clone with the gptp-processor gitlink staged at REV.
# Usage: parent_suite.sh <label> <rev> <suite dir under tb/verilator>
set -euo pipefail
. $REVIEWS/gptp68-a199-packet/scripts/env.sh
label=$1; rev=$2; suite=$3
src=$A199_PACKET/scratch/parent
dst=$A199_PACKET/scratch/parent-$label
rm -rf "$dst"; cp -a "$src" "$dst"
rm -rf "$dst/tb/verilator/$suite/obj_dir" "$dst/tb/verilator/$suite/gptp_ucode.hex"
git -C "$dst/gptp-processor" checkout -q "$rev"
git -C "$dst" add gptp-processor
echo "# date: $(date -Is)"
echo "# verilator: $(command -v verilator) $(verilator --version)"
echo "# parent $(git -C "$dst" rev-parse HEAD) staged gitlink: $(git -C "$dst" ls-files -s gptp-processor)"
echo "# donor tree $(git -C "$dst/gptp-processor" rev-parse 'HEAD^{tree}') suite $suite"
make -C "$dst/tb/verilator/$suite"
