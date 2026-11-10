#!/bin/bash
# extra2.sh <clone> <gate>...: the named gates chain D did not reach before the 17:00 host reset, each as extra.sh runs it
# (same command, env, log and rc layout), in turn, on a fresh clone of the gate head; two chains run side by side on two clones
: "${CPUS:?CPUS unset}"
set -u
G=$VALIDATION_STORAGE/665s8-a758b/gates; H=$(cat $G/HEAD); W=$1; shift; L=$G/extra/logs; mkdir -p $L
[ -d $W ] || bash $VALIDATION_STORAGE/665s8-a758b/clone_at.sh $H $W > $L/clone-$(basename $W).log 2>&1
cd $W || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$G/home VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$G/extra/tmp-$(basename $W) PYTHONHASHSEED=0 \
  COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p $TMPDIR
BASE=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
LITEX=$WORKSPACE_HOME/litex-milan/venv/bin
run() { id=$1; p=$2; shift 2; { echo "# head $H gate $id: $*"; PATH=$p:$BASE taskset -c "$CPUS" bash -c "$*"; } > "$L/$id.log" 2>&1; rc=$?; echo $rc > "$L/$id.rc"; echo "$id rc=$rc" >> $G/extra/jobs.txt; }
for id in "$@"; do
  case $id in
    budget-1x1) run budget-1x1 $LITEX "python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $G/extra/budget-1x1 --record-budget-findings" ;;
    budget-8x8) run budget-8x8 $LITEX "python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $G/extra/budget-8x8 --record-budget-findings" ;;
    wire-8x8-none) run wire-8x8-none $LITEX "python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir $G/extra/wire-8x8 --draws 16 --load none --out $G/extra/wire-8x8-none" ;;
    wire-8x8-composed) run wire-8x8-composed $LITEX "python3 -B tb/verilator/ctrl_wire_timing/run.py --reuse-build --build-dir $G/extra/wire-8x8 --draws 16 --load composed --out $G/extra/wire-8x8-composed" ;;
    *) echo "unknown gate $id" >&2; exit 5 ;;
  esac
done
git status --short > $L/tree-after-$(basename $W).txt
echo "done $(basename $W)" >> $G/extra/jobs.txt
