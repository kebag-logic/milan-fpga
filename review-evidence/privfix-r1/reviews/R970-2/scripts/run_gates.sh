#!/usr/bin/env bash
# Reviewer gate runner. usage: run_gates.sh <tree> <outdir> <base-rev> <python-with-pinned-markdown-renderer>
# Runs each gate concurrently with its own log and rc file; prints a summary table.
set -u
TREE=$1; OUT=$2; BASE=$3; PY=$4
mkdir -p "$OUT"; cd "$TREE" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() { n=$1; shift; ( "$@" >"$OUT/$n.log" 2>&1; echo $? >"$OUT/$n.rc" ) & }
run docs_check            "$PY" scripts/docs_check.py
run doc_style             "$PY" scripts/check_doc_style.py
run doc_style_selftest    "$PY" scripts/check_doc_style.py --selftest
run em_dash               "$PY" scripts/check_em_dash.py --base "$BASE"
run em_dash_selftest      "$PY" scripts/check_em_dash.py --selftest
run doc_paths             "$PY" scripts/check_doc_paths.py
run toc_check             "$PY" scripts/gen_toc.py --check
run toc_anchors           "$PY" scripts/gen_toc.py --verify-anchors
run docs_inventory        "$PY" scripts/docs_inventory.py --check
run feature_status        "$PY" scripts/check_feature_status.py
run doc_map               "$PY" docs/DOC_MAP.gen.py --check
run hygiene               "$PY" scripts/check_hygiene.py --check
run py_idiom              "$PY" scripts/check_py_idiom.py
run sh_idiom              "$PY" scripts/check_sh_idiom.py
run todo_ownership        "$PY" scripts/check_todo_ownership.py
run naming                "$PY" scripts/measure_naming.py --check
wait
run test_evidence         "$PY" scripts/measure_test_evidence.py --check
run fail_fast             "$PY" scripts/measure_fail_fast.py --check
run sh_syntax_tu_on_wire  bash -n tb/tools/check_tu_on_wire.sh
run avtp_wire_truth       "$PY" tb/tools/avtp_wire_truth.py --self-test
run torture_campaign      "$PY" tb/tools/torture_campaign.py --self-test
run baremetal_check       "$PY" scripts/check_baremetal_only.py --check
run baremetal_selftest    "$PY" scripts/check_baremetal_only.py --selftest
( cd tests && "$PY" -m behave --no-capture -f plain features/milan_streaming_licence.feature features/torture_campaign_plan.feature features/wire_truth_avtp.feature >"$OUT/behave_touched.log" 2>&1; echo $? >"$OUT/behave_touched.rc" ) &
wait
for f in "$OUT"/*.rc; do n=$(basename "$f" .rc); printf '%s\t%s\t%s\t%s\n' "$n" "$(cat "$f")" "$(wc -l <"$OUT/$n.log")" "$(tail -n 1 "$OUT/$n.log" | cut -c1-160)"; done | tee "$OUT/summary.tsv"
