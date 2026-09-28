#!/usr/bin/env bash
# Run a named subset of processor Verilator suites from an exported copy of
# an exact commit. Usage: run_suites_subset.sh SRC_CLONE SCRATCH VERILATOR OUT JOBS suite...
# Writes one log per suite plus a summary to OUT. Never touches SRC_CLONE.
set -uo pipefail
src=$1; scratch=$2; vl=$3; out=$4; jobs=$5; shift 5
mkdir -p "$scratch" "$out"
rm -rf "$scratch/tree"; mkdir -p "$scratch/tree"
git -C "$src" archive HEAD | tar -x -C "$scratch/tree"
echo "head $(git -C "$src" rev-parse HEAD)" > "$out/summary.txt"
echo "verilator $("$vl" --version)" >> "$out/summary.txt"
run_one() {
  s=$1; ( cd "$scratch/tree/tb/$s" && make VERILATOR="$vl" ) > "$out/$s.log" 2>&1
  rc=$?
  t=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/$s.log" | tail -1)
  echo "$s rc=$rc ${t:-NO-TALLY}"
}
export -f run_one; export scratch vl out
printf '%s\n' "$@" | xargs -P "$jobs" -I{} bash -c 'run_one {}' | sort >> "$out/summary.txt"
cat "$out/summary.txt"
