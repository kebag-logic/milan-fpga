#!/usr/bin/env bash
# the scheduled physical gPTP suite at <sha> on a fresh clean clone
set -u
H=$1; S=<scratch>; W=$S/clone-phys; O=$S/physical
mkdir -p "$O" "$S/tmp-phys"
[ -d "$W" ] || bash $S/scripts/make_clone.sh "$W" "$H" > "$O/clone.log" 2>&1 || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=<home> VERILATOR=<data>/tools/pinned-verilator-5.050/verilator TMPDIR=$S/tmp-phys MAKEFLAGS="-j4 --no-print-directory" VERILATOR_JOBS=4 PYTHONHASHSEED=0
export PATH=<data>/scratch/a662/make43/bin:<data>/tools/sv2v-v0.0.12:<data>/tools/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
s=$(date +%s)
{ echo "# head $H gate milan_dp_gptp: make -C tb/verilator/milan_dp_gptp"; make -C tb/verilator/milan_dp_gptp; } > "$O/milan_dp_gptp.log" 2>&1
echo "$? $(( $(date +%s) - s ))" > "$O/milan_dp_gptp.rc"
git status --porcelain > "$O/tree-after.txt"
echo done > "$O/DONE"
