#!/usr/bin/env bash
# Replays, command for command, the rtl-fast step "Prove the OOC read sets come
# from run.sh and refuse a bad one" (.github/workflows/rtl-fast.yml:201-216 at
# 6904af6b) with a chosen python3 first on PATH. Each command gets its own log
# and rc; the script does not stop at the first failure.
# Usage: rtl_fast_ooc_step.sh <checkout> <dir-holding-python3> <log-dir> <tag>
set -u
checkout=$1; pybin=$2; logs=$3; tag=$4
export PATH="$pybin:$PATH" PYTHONDONTWRITEBYTECODE=1
cd "$checkout" || exit 2
python3 -c 'import sys; print(sys.executable, sys.version)' > "$logs/${tag}_interpreter.log"
n=0
step() {
  n=$((n + 1)); name=$(printf '%02d_%s' "$n" "$1"); shift
  "$@" > "$logs/${tag}_${name}.log" 2>&1
  rc=$?
  echo "$rc" > "$logs/${tag}_${name}.rc"
  printf '%s rc=%s : %s\n' "$name" "$rc" "$*"
}
step dp_srcs_selftest python3 syn/ooc/dp_srcs.py --selftest
step ooc_tcl_selftest python3 syn/ooc/ooc_tcl_selftest.py
step pp_baseline_selftest python3 syn/ooc/pp_baseline.py --selftest
step pp_baseline_mutants python3 syn/ooc/pp_baseline_mutants.py
step pp_baseline_reports_selftest python3 syn/ooc/pp_baseline_reports_selftest.py
step pp_resource_gate_selftest python3 syn/ooc/pp_resource_gate.py --selftest
step pp_resource_gate_mutants python3 syn/ooc/pp_resource_gate_mutants.py
step check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
step dp_srcs_top_datapath sh -c 'python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null'
step dp_srcs_top_shadow sh -c 'python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null'
