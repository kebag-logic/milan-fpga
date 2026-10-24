#!/usr/bin/env bash
# Round-2 gate campaign for PR #782 at an exact head. Each gate runs in the
# background with its own log and rc file under $OUT; wait_gates.sh polls them.
# Usage: run_gates.sh <clone> <base-sha> <out-dir> <verilator>
set -u
CLONE=$1 BASE=$2 OUT=$3 VLT=$4
mkdir -p "$OUT"
cd "$CLONE" || exit 2

gate() {  # gate <name> <dir> <cmd...>
  local name=$1 dir=$2; shift 2
  ( cd "$dir" && "$@" ) > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
}

listings() {  # listings <tree> <prefix>
  local tree=$1 p=$2 k
  ( cd "$tree" || exit 2
    scripts/run_all_suites.sh --list > "$OUT/$p-list.txt" 2>&1 || exit 1
    scripts/run_all_suites.sh --ci-pieces --list > "$OUT/$p-cipieces-list.txt" 2>&1 || exit 1
    for k in $(seq 0 16); do
      scripts/run_all_suites.sh --ci-pieces --shard "$k/17" --list > "$OUT/$p-shard-$k-17.txt" 2>&1 || exit 1
    done )
}

BASETREE=$OUT/../../scratch/base-$BASE
rm -rf "$BASETREE"; mkdir -p "$BASETREE"
git archive "$BASE" | tar -x -C "$BASETREE"

gate selftest "$CLONE" python3 -E -s scripts/suite_shards.py --selftest &
gate ci_gate_workflows "$CLONE" python3 -E -s scripts/ci_gate_workflows.py --check &
gate ci_events "$CLONE" python3 -E -s scripts/ci_events.py --check &
gate docs_check "$CLONE" python3 -E -s scripts/docs_check.py &
gate feature_status "$CLONE" python3 -E -s scripts/check_feature_status.py &
gate lint "$CLONE" env VERILATOR="$VLT" python3 -E -s scripts/lint_rtl.py --check &
gate behave "$CLONE/tests" behave --no-capture -f plain &
( listings "$CLONE" head; echo $? > "$OUT/listings-head.rc" ) &
( listings "$BASETREE" base; echo $? > "$OUT/listings-base.rc" ) &
wait
echo done > "$OUT/ALL.done"
