#!/usr/bin/env bash
# Run the round-3 documentation gates and the baseline-helper self-test
# concurrently at the checked-out head; one log and one rc file per step.
# Usage: run_gates.sh <repo> <markdown-python> <em-dash-base> <out-dir>
set -u
REPO=$1 MDPY=$2 BASE=$3 OUT=$4
mkdir -p "$OUT"
cd "$REPO" || exit 2
step() {
  name=$1; shift
  ( "$@" > "$OUT/$name.log" 2>&1; echo $? > "$OUT/$name.rc" ) &
}
step gen_toc_selftest       "$MDPY" scripts/gen_toc.py --selftest
step gen_toc_verify_anchors "$MDPY" scripts/gen_toc.py --verify-anchors
step gen_toc_check          "$MDPY" scripts/gen_toc.py --check
step docs_check             "$MDPY" scripts/docs_check.py
step check_doc_style        "$MDPY" scripts/check_doc_style.py
step check_doc_style_selftest "$MDPY" scripts/check_doc_style.py --selftest
step check_em_dash          "$MDPY" scripts/check_em_dash.py --base "$BASE"
step pp_baseline_selftest   python3 syn/ooc/pp_baseline.py --selftest
step pp_resource_gate_check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
