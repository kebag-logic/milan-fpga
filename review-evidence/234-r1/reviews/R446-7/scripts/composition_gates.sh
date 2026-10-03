#!/usr/bin/env bash
# Composition gates for issue #234 / PR #638 on the merge-train candidate.
# Usage: composition_gates.sh <candidate-clone> <nogit-extraction> <receipts-dir> <dev-tip-sha>
# Each gate runs in parallel (up to 16) with its own log and rc file.
set -u
TREE=$1; NOGIT=$2; OUT=$3; DEV=$4
mkdir -p "$OUT"
cat > "$OUT/gates.list" <<EOF
docs_check|$TREE|python3 scripts/docs_check.py
docs_check_nogit|$NOGIT|python3 scripts/docs_check.py
feature_status_nogit|$NOGIT|python3 scripts/check_feature_status.py
gen_toc_check|$TREE|python3 scripts/gen_toc.py --check
gen_toc_anchors|$TREE|python3 scripts/gen_toc.py --verify-anchors
gen_toc_selftest|$TREE|python3 scripts/gen_toc.py --selftest
check_doc_paths|$TREE|python3 scripts/check_doc_paths.py
check_em_dash_dev|$TREE|python3 scripts/check_em_dash.py --base $DEV
doc_map_check|$TREE|python3 docs/DOC_MAP.gen.py --check
doc_style|$TREE|python3 scripts/check_doc_style.py
check_archive|$TREE|python3 scripts/check_archive.py
ci_events_check|$TREE|python3 scripts/ci_events.py --check
ci_events_selftest|$TREE|python3 scripts/ci_events.py --selftest
ci_scope_selftest|$TREE|python3 scripts/ci_scope.py --selftest
gate_selftest|$TREE|python3 syn/ooc/pp_resource_gate.py --selftest
gate_mutants|$TREE|python3 syn/ooc/pp_resource_gate_mutants.py
gate_check_baseline|$TREE|python3 syn/ooc/pp_resource_gate.py check-baseline
dp_srcs_selftest|$TREE|python3 syn/ooc/dp_srcs.py --selftest
ooc_tcl_selftest|$TREE|python3 syn/ooc/ooc_tcl_selftest.py
pp_baseline_selftest|$TREE|python3 syn/ooc/pp_baseline.py --selftest
pp_baseline_mutants|$TREE|python3 syn/ooc/pp_baseline_mutants.py
pp_baseline_reports_selftest|$TREE|python3 syn/ooc/pp_baseline_reports_selftest.py
dp_srcs_milan_datapath|$TREE|python3 syn/ooc/dp_srcs.py --top milan_datapath
dp_srcs_pp_shadow|$TREE|python3 syn/ooc/dp_srcs.py --top KL_pp_shadow
EOF
run_one() {
  IFS='|' read -r name dir cmd <<<"$1"
  ( cd "$dir" && start=$(date +%s); bash -c "$cmd" > "$OUT/$name.log" 2>&1; rc=$?
    echo "$rc" > "$OUT/$name.rc"; echo "$name rc=$rc $(( $(date +%s) - start ))s" )
}
export -f run_one; export OUT
xargs -P 16 -I{} -d '\n' bash -c 'run_one "$@"' _ {} < "$OUT/gates.list" | sort > "$OUT/summary.txt"
cat "$OUT/summary.txt"
