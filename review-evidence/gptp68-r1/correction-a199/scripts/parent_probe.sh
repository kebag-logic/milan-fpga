#!/bin/bash
# Run the parent's tb/verilator/gptp_shadow `run` target on a disposable copy
# of the private parent clone (scratch/parent, parent 574c29fa with
# verilog-axis at its pin), with the gptp-processor gitlink staged at REV
# and an optional probe patch applied to the copy (prints only; the wedge
# probes exit after their loop). Usage: parent_probe.sh <label> <rev> [patch]
set -euo pipefail
. $REVIEWS/gptp68-a199-packet/scripts/env.sh
label=$1; rev=$2; patch=${3:-}
src=$A199_PACKET/scratch/parent
dst=$A199_PACKET/scratch/parent-$label
rm -rf "$dst"; cp -a "$src" "$dst"
rm -rf "$dst/tb/verilator/gptp_shadow/obj_dir" "$dst/tb/verilator/gptp_shadow/gptp_ucode.hex"
git -C "$dst/gptp-processor" checkout -q "$rev"
git -C "$dst" add gptp-processor
[ -n "$patch" ] && patch -d "$dst" -p1 < "$patch"
echo "# date: $(date -Is)"
echo "# verilator: $(command -v verilator) $(verilator --version)"
echo "# parent $(git -C "$dst" rev-parse HEAD) staged gitlink: $(git -C "$dst" ls-files -s gptp-processor)"
echo "# donor tree $(git -C "$dst/gptp-processor" rev-parse 'HEAD^{tree}') label $label patch ${patch:-none}"
make -C "$dst/tb/verilator/gptp_shadow" run
