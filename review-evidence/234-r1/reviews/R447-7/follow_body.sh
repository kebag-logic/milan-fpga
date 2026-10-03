#!/usr/bin/env bash
# Follow PR #638's "How to get into the same state" and "How to validate" verbatim in a fresh clone.
# usage: follow_body.sh <object-source clone> <work dir> <receipt dir>
set -u
SRC=$1 WORK=$2 OUT=$3
mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
rm -rf "$WORK"
git clone -q --no-checkout --shared "$SRC" "$WORK" || exit 9
cd "$WORK" || exit 9
git remote set-url origin https://github.com/kebag-logic/milan-fpga
{
  echo '$ git fetch origin 234-area-baseline'; git fetch origin 234-area-baseline 2>&1; echo "rc=$?"
  echo '$ git switch --detach d5f56313dc5a5c2716211356f99796664dc843dd'; git switch --detach d5f56313dc5a5c2716211356f99796664dc843dd 2>&1; echo "rc=$?"
  echo '$ git submodule update --init third_party/verilog-axis protocol-processor gptp-processor'
  git submodule update --init third_party/verilog-axis protocol-processor gptp-processor 2>&1 | grep -v '^remote:' ; echo "rc=${PIPESTATUS[0]}"
  echo "FETCH_HEAD $(git rev-parse FETCH_HEAD)"; echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
  git submodule status
  git status --porcelain --ignored
} > "$OUT/state.log" 2>&1
run() { local n=$1; shift; ( "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc" ) & }
run v1_gate_selftest python3 syn/ooc/pp_resource_gate.py --selftest
run v2_gate_mutants python3 syn/ooc/pp_resource_gate_mutants.py
run v3_check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run v4_fuzz20000 python3 syn/ooc/pp_resource_gate.py --fuzz 20000
run v5_pp_baseline_selftest python3 syn/ooc/pp_baseline.py --selftest
run v6_pp_baseline_mutants python3 syn/ooc/pp_baseline_mutants.py
run v7_ci_scope_selftest python3 scripts/ci_scope.py --selftest
run v8_ci_events_check python3 scripts/ci_events.py --check
wait
for f in "$OUT"/v*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done > "$OUT/SUMMARY.log"
sed -i "s#$WORK#\$FOLLOW#g; s#$SRC#\$CHECKOUT#g" "$OUT"/*.log
