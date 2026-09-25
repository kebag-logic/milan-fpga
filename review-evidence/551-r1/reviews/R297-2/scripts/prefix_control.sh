#!/bin/sh
# Pre-fix processor control: build the UNCHANGED head leg against the
# processor hdl/ tree at 7a47f578 (the merge parent of a8f8ce81 before the
# #112 fix), extracted with git archive into scratch. The clone's submodule
# checkout and gitlink are not touched. usage: prefix_control.sh <clone>
set -u
CLONE=$1
PACKET=${PACKET:-$REVIEWS/551-r297-2-packet}
OLD=7a47f5788ff504f099a47ad4407c340771bb6bdb
X=$PACKET/scratch/pp_$OLD
R=$PACKET/receipts
JOBS=${JOBS:-8}
MDIR=$PACKET/scratch/obj_prefix_control
mkdir -p "$R"
rm -rf "$X" "$MDIR"; mkdir -p "$X"
git -C "$CLONE/protocol-processor" archive "$OLD" hdl | tar -x -C "$X" || exit 2
# identity of the extracted control tree
git -C "$CLONE/protocol-processor" rev-parse "$OLD^{tree}:hdl" > "$R/prefix_control.pp_hdl_tree"
git -C "$CLONE/protocol-processor" rev-parse "990f96526bb89356c963a260ebbdcf2a77e6623a^{tree}:hdl" >> "$R/prefix_control.pp_hdl_tree"
cd "$CLONE/tb/verilator/milan_dp" || exit 2
make -s crflic-build VERILATOR="$VERILATOR" VERILATOR_JOBS="$JOBS" CRFLIC_MDIR="$MDIR" PP_DIR="$X/hdl" \
  > "$R/prefix_control.build.log" 2>&1
brc=$?
echo "build_rc=$brc" > "$R/prefix_control.rc"
# prove the control compiled the old admission engine, not the pinned one
grep -c 'pend_acc_r' "$X/hdl/srp/KL_srp_admission.sv" >> "$R/prefix_control.rc"
grep -l "$X/hdl/srp/KL_srp_admission.sv" "$MDIR"/*.d 2>/dev/null | head -1 >> "$R/prefix_control.rc"
[ $brc -eq 0 ] && [ -x "$MDIR/Vmilan_dp_crflic" ] || { tail -40 "$R/prefix_control.build.log"; exit 3; }
"$MDIR/Vmilan_dp_crflic" > "$R/prefix_control.run.log" 2>&1
echo "run_rc=$?" >> "$R/prefix_control.rc"
tail -3 "$R/prefix_control.run.log" >> "$R/prefix_control.rc"
cat "$R/prefix_control.rc"
