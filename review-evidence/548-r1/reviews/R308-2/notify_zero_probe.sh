#!/bin/sh
# Focused re-run of the milan_dp timed notification leg (obj_notify) at the
# checked-out head, plus a nonzero CTLR_DIAG mutant, without editing tracked
# files. The mutant is a scratch copy of milan_datapath.sv whose tie
# `assign aecp_ctlr_diag = 32'd0;` drives 32'h01001001 instead; the build
# command substitutes that copy's path for the tracked one.
#
# Usage: notify_zero_probe.sh <repo> <scratch-dir> <verilator>
# Exit 0 only if the head leg passes and the mutant fails exactly the
# "[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO" check.
set -u
REPO=$1; SCR=$2; VL=$3
DP=$REPO/tb/verilator/milan_dp
mkdir -p "$SCR"
cd "$DP" || exit 2

# Exact recipe from the Makefile's default dry run.
make -n VERILATOR="$VL" VERILATOR_JOBS=8 > "$SCR/dryrun.txt" 2>&1 || exit 2
grep -E '^python3 .*(gen_ltn_rom\.py -o ltn_rom\.hex|gen_ucode\.py -o ucode\.hex|gen_gptp_ucode\.py .*-o gptp_ucode\.hex)$' \
  "$SCR/dryrun.txt" > "$SCR/gen.sh"
[ "$(wc -l < "$SCR/gen.sh")" -eq 3 ] || { echo "hex generator recipes not found"; exit 2; }
# Join backslash-continued recipe lines before selecting the notify build.
awk '{ if (sub(/\\$/, "")) { buf = buf $0 } else { print buf $0; buf = "" } }' \
  "$SCR/dryrun.txt" | grep -- '--Mdir obj_notify ' > "$SCR/build_notify.sh"
[ "$(wc -l < "$SCR/build_notify.sh")" -eq 1 ] || { echo "notify recipe not unique"; exit 2; }
trap 'rm -f "$DP/ltn_rom.hex" "$DP/ucode.hex" "$DP/gptp_ucode.hex"' EXIT
sh -e "$SCR/gen.sh" || exit 2

# Head build and run.
sed "s#--Mdir obj_notify #--Mdir $SCR/obj_notify_head #" "$SCR/build_notify.sh" > "$SCR/build_head.sh"
sh -e "$SCR/build_head.sh" > "$SCR/build_head.log" 2>&1; echo "head_build_exit=$?"
"$SCR/obj_notify_head/Vmilan_dp_notify" > "$SCR/run_head.log" 2>&1; HE=$?
echo "head_run_exit=$HE"

# Mutant copy and build.
cp "$REPO/hdl/milan/milan_datapath.sv" "$SCR/milan_datapath_mut.sv"
sed -i "s/assign aecp_ctlr_diag = 32'd0;/assign aecp_ctlr_diag = 32'h01001001;/" "$SCR/milan_datapath_mut.sv"
N=$(grep -c "assign aecp_ctlr_diag = 32'h01001001;" "$SCR/milan_datapath_mut.sv")
echo "mutant_tie_count=$N"
[ "$N" -eq 1 ] || exit 2
grep -q ' \.\./\.\./\.\./hdl/milan/milan_datapath\.sv ' "$SCR/build_notify.sh" || { echo "datapath path not found in recipe"; exit 2; }
sed -e "s#--Mdir obj_notify #--Mdir $SCR/obj_notify_mut #" \
    -e "s# \.\./\.\./\.\./hdl/milan/milan_datapath\.sv # $SCR/milan_datapath_mut.sv #" \
    "$SCR/build_notify.sh" > "$SCR/build_mut.sh"
sh -e "$SCR/build_mut.sh" > "$SCR/build_mut.log" 2>&1; echo "mut_build_exit=$?"
"$SCR/obj_notify_mut/Vmilan_dp_notify" > "$SCR/run_mut.log" 2>&1; ME=$?
echo "mut_run_exit=$ME"

# Remove the generated hex files the recipe wrote into the tracked directory.
rm -f ltn_rom.hex ucode.hex gptp_ucode.hex

echo "--- head: CTLR_DIAG lines and summary"
grep -n "CTLR_DIAG" "$SCR/run_head.log"; tail -n 3 "$SCR/run_head.log"
echo "--- mutant: failing lines and summary"
grep -n -i -E "FAIL|CTLR_DIAG" "$SCR/run_mut.log" | head -n 20; tail -n 3 "$SCR/run_mut.log"
MF=$(grep -c -E "^ *(\[FAIL\]|FAIL)" "$SCR/run_mut.log")
echo "mutant_fail_lines=$MF"
[ "$HE" -eq 0 ] && [ "$ME" -ne 0 ] && grep -q "CTLR_DIAG (0x6F4) is STRUCTURAL ZERO" "$SCR/run_mut.log" \
  && { echo "RESULT PASS"; exit 0; }
echo "RESULT FAIL"; exit 1
