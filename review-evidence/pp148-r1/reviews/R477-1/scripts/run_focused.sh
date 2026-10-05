#!/bin/sh
# Focused #148 probes: tb/aecp_notify (section TW) and tb/pp_top --spacing-only
# (section CS) in one prepared source tree. Usage:
#   run_focused.sh TREE LABEL OUTDIR [pp_top-section-flag]
# TREE is a `git archive` extraction; LABEL names the receipts; OUTDIR holds
# LABEL-aecp_notify.{log,rc} and LABEL-pp_top.{log,rc}. VERILATOR must name the
# pinned 5.050 wrapper. The two suites run concurrently; each writes its own rc.
set -u
TREE=$1; LABEL=$2; OUT=$3; FLAG=${4:---spacing-only}
: "${VERILATOR:?set VERILATOR to the pinned wrapper}"
mkdir -p "$OUT"
(
  cd "$TREE/tb/aecp_notify" && make run VERILATOR="$VERILATOR" > "$OUT/$LABEL-aecp_notify.log" 2>&1
  echo $? > "$OUT/$LABEL-aecp_notify.rc"
) &
(
  cd "$TREE/tb/pp_top" && make gsi-build VERILATOR="$VERILATOR" > "$OUT/$LABEL-pp_top-build.log" 2>&1
  b=$?
  echo $b > "$OUT/$LABEL-pp_top-build.rc"
  if [ $b -eq 0 ]; then
    ./obj_dir/Vpp_top_sim "$FLAG" > "$OUT/$LABEL-pp_top.log" 2>&1
    echo $? > "$OUT/$LABEL-pp_top.rc"
  fi
) &
wait
