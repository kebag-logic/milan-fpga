#!/usr/bin/env bash
# Focused head gates for the review: RTL lint ratchet, the milan_dp sim-pool
# self-test and the docs wording gate, concurrently, one log + rc each.
# usage: run_gates.sh <repo> <out-dir> <pinned-verilator-dir>
set -u
repo=$1 out=$2 vdir=$3
mkdir -p "$out"
export PATH="$vdir:$PATH"
cd "$repo" || exit 2
run() { local name=$1; shift; "$@" > "$out/$name.log" 2>&1; echo "rc=$?" > "$out/$name.rc"; }
run lint_rtl_check timeout 900 python3 scripts/lint_rtl.py --check &
run test_sim_pool timeout 600 python3 tb/verilator/milan_dp/test_sim_pool.py &
run docs_check timeout 600 python3 scripts/docs_check.py &
wait
for f in lint_rtl_check test_sim_pool docs_check; do
  echo "== $f $(cat "$out/$f.rc")"; tail -n 3 "$out/$f.log" | cut -c1-250
done
