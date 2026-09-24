#!/usr/bin/env bash
# Run a suite Makefile target's own recipe, taken from `make -n <target>`,
# with the verilator build parallelism capped (`--build -j 0` -> `-j <J>`)
# so the job bound holds. The pinned simulator directory goes first on PATH.
# Usage: run_recipe.sh <suite-dir> <target> <jobs> <pinned-bin-dir> <log> [make VAR=... ...]
set -uo pipefail
suite=$1 target=$2 jobs=$3 pin=$4 log=$5; shift 5
export PATH="$pin:$PATH"
cd "$suite" || exit 2
script=$(mktemp)
{
  echo "set -e"
  make -n "$target" VERILATOR_JOBS="$jobs" "$@" | sed -e "s/--build -j 0 /--build -j $jobs /g"
} > "$script"
{
  echo "# suite $(pwd) target $target jobs $jobs"
  echo "# head $(git rev-parse HEAD)"
  echo "# verilator $(verilator --version)"
  echo "# milan_datapath.sv sha256 $(sha256sum ../../../hdl/milan/milan_datapath.sv | cut -d' ' -f1)"
  echo "# recipe:"; sed 's/^/#   /' "$script" | cut -c1-400
} > "$log"
start=$(date +%s)
bash "$script" >> "$log" 2>&1
rc=$?
echo "exit=$rc wall_s=$(( $(date +%s) - start ))" >> "$log"
rm -f "$script"
exit $rc
