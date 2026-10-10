#!/usr/bin/env bash
# Launch the focused MAAP gates concurrently, each with its own log and rc file.
# Usage: launch_focus.sh <tree> <outdir>
# <tree> is a disposable copy of the exact head; <outdir> receives logs/rc files.
set -u
TREE=$1
OUT=$2
SCR=$(cd "$(dirname "$0")/.." && pwd)/scratch
mkdir -p "$OUT" "$SCR/tmp" "$SCR/build"
export PATH="$SCR/bin:$PATH"
export VERILATOR="$SCR/bin/verilator"
export TMPDIR="$SCR/tmp"

job() {  # job <name> <command...>
  local name=$1; shift
  ( cd "$TREE" && "$@" ) > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
}

B="$SCR/build"
job unit make -j4 -C tb/verilator/maap run MDIR="$B/unit" VERILATOR_JOBS=4 &
job integration bash -c "make -j8 -C tb/verilator/maap integration-build DP_MDIR='$B/integration' VERILATOR_JOBS=4 && cd '$B/integration' && ./maap_integration" &
job coverage make -j4 -C tb/verilator/maap coverage COV_MDIR="$B/coverage" VERILATOR_JOBS=4 &
job campaign bash -c "cd tb/verilator/maap && VERILATOR_JOBS=4 python3 mutants.py" &
job differential python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$B/differential" &
wait
echo all-done > "$OUT/ALL.done"
