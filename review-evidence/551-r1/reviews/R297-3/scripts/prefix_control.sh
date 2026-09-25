#!/bin/sh
# R297-3: rerun the README's pre-#112 processor control and the head leg.
# Builds the UNCHANGED head obj_crflic leg (a) against the pinned processor
# (990f9652, clean head control) and (b) against the processor hdl/ tree at
# 7a47f578 (before the #112 fix a8f8ce81), extracted with git archive into
# scratch. The clone's submodule checkout and gitlink are never touched.
# usage: prefix_control.sh <clone> ; env VERILATOR, JOBS, PACKET
set -u
CLONE=$1
PACKET=${PACKET:-$REVIEWS/551-r297-3-packet}
OLD=7a47f5788ff504f099a47ad4407c340771bb6bdb
PIN=990f96526bb89356c963a260ebbdcf2a77e6623a
X=$PACKET/scratch/pp_$OLD
R=$PACKET/receipts/crflic
JOBS=${JOBS:-8}
mkdir -p "$R"
rm -rf "$X"; mkdir -p "$X"
git -C "$CLONE/protocol-processor" archive "$OLD" hdl | tar -x -C "$X" || exit 2
{ echo "old_hdl_tree $(git -C "$CLONE/protocol-processor" rev-parse "$OLD^{tree}:hdl")"
  echo "pin_hdl_tree $(git -C "$CLONE/protocol-processor" rev-parse "$PIN^{tree}:hdl")"
  echo "is_ancestor(OLD,a8f8ce81)=$(git -C "$CLONE/protocol-processor" merge-base --is-ancestor $OLD a8f8ce81 && echo yes || echo no)"
  echo "is_ancestor(a8f8ce81,PIN)=$(git -C "$CLONE/protocol-processor" merge-base --is-ancestor a8f8ce81 $PIN && echo yes || echo no)"
} > "$R/control_identity.txt"

leg() { label=$1; shift
  M=$PACKET/scratch/obj_$label; rm -rf "$M"
  ( cd "$CLONE/tb/verilator/milan_dp" && make -s crflic-build VERILATOR="$VERILATOR" \
      VERILATOR_JOBS="$JOBS" CRFLIC_MDIR="$M" "$@" ) > "$R/$label.build.log" 2>&1
  brc=$?
  echo "build_rc=$brc" > "$R/$label.rc"
  [ $brc -eq 0 ] && [ -x "$M/Vmilan_dp_crflic" ] || { tail -40 "$R/$label.build.log"; return 3; }
  "$M/Vmilan_dp_crflic" > "$R/$label.run.log" 2>&1
  echo "run_rc=$?" >> "$R/$label.rc"
  # which admission-engine source the build depended on
  grep -ho '[^ ]*/srp/KL_srp_admission.sv' "$M"/*.d 2>/dev/null | sort -u >> "$R/$label.rc"
  # failures per section header ([A]..[J])
  awk '/^\[[A-Z]\] /{s=substr($0,2,1)} /^[ \t]*\[FAIL\]/{n[s]++; t++}
       END{for(k in n) printf "fail_section_%s=%d\n", k, n[k]; printf "fail_total=%d\n", t+0}' \
      "$R/$label.run.log" | sort >> "$R/$label.rc"
  tail -n 2 "$R/$label.run.log" >> "$R/$label.rc"
  cat "$R/$label.rc"
}
leg head_pin
leg prefix_control PP_DIR="$X/hdl"
