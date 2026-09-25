#!/usr/bin/env bash
# Two focused milan_dp legs over the COMPOSED milan_datapath of the issue 546
# merge-train candidate: the #548 CTLR_DIAG structural-zero check (timed
# notification leg, recipe copied from the `run` target) and the #387 gmstep
# leg (CRF selection, exercises the #546 crf_rate_valid wiring).
# Usage: run_composed_legs.sh <candidate-clone> <out-dir> <build-dir> <verilator> [notify|gmstep]...
# Builds go to <build-dir>; the clone's tracked bytes are not modified
# (generated hex files are gitignored).
set -u
clone=$1 out=$2 bdir=$3 vl=$4
shift 4
legs=${*:-notify gmstep}
mkdir -p "$out" "$bdir"
here=$(cd "$(dirname "$0")" && pwd)
cd "$clone/tb/verilator/milan_dp" || exit 2
"$vl" --version > "$out/verilator_version.txt" 2>&1
touch "$out/legs.tsv"
leg() {
  local name=$1; shift
  local t0=$SECONDS
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%ss\n' "$name" "$rc" "$((SECONDS - t0))" >> "$out/legs.tsv"
}
case " $legs " in *" notify "*)
leg notify_build make -f "$here/r303_notify.mk" VERILATOR="$vl" VERILATOR_JOBS=4 \
  R303_MDIR="$bdir/obj_notify" r303-notify
leg notify_run "$bdir/obj_notify/Vmilan_dp_notify" ;; esac
case " $legs " in *" gmstep "*)
leg gmstep make VERILATOR="$vl" VERILATOR_JOBS=4 GMSTEP_MDIR="$(python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1]))' "$bdir/obj_gmstep")" gmstep ;; esac
cat "$out/legs.tsv"
