#!/usr/bin/env bash
# Run the processor documentation gates (CI docs job + make check targets)
# against a checkout. Usage: run_gates.sh <checkout> <receipt-dir>
# Each gate's output goes to <receipt-dir>/gate-<name>.log; a summary with
# exit codes goes to <receipt-dir>/gates-summary.txt.
set -u
repo=${1:?checkout}
out=${2:?receipt dir}
mkdir -p "$out"
summary="$out/gates-summary.txt"
: > "$summary"
cd "$repo" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')" >> "$summary"
run() {
  local name=$1; shift
  "$@" > "$out/gate-$name.log" 2>&1
  local rc=$?
  printf '%-22s rc=%d  %s\n' "$name" "$rc" "$*" >> "$summary"
}
run check-links      python3 scripts/check-links.py
run check-matrix     python3 scripts/check-matrix.py
run integrator-params python3 scripts/check-integrator-params.py
run wavedrom-check   python3 scripts/render-wavedrom.py --check
run stale            make stale
run lint-diagrams    make lint
run gen-matrix       python3 scripts/gen_matrix.py --check
run diff-check       git diff --check 493e5e4bf58a6146bf9310194d71c72e18610704 HEAD
run make-check       make check
cat "$summary"
