#!/usr/bin/env bash
# Reviewer gate runner: the focused gates this round ran at the head under
# review, concurrently, one log and one rc file per gate.
# Usage: run_gates.sh <clone-at-head> <base-rev> <log-dir> <python>
# <python> must import the Markdown renderer pinned in
# tools/markdown/requirements.txt, and behave.
# Not run here, by the round's rules: scripts/act_ci.py and its self-test.
set -u
CLONE=$1
BASE=$2
L=$3
PY=$4
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$L"
cd "$CLONE" || exit 97

run() { # name, command...
    local name=$1
    shift
    (
        "$@" > "$L/$name.log" 2>&1
        echo $? > "$L/$name.rc"
    ) &
}

run docs_check "$PY" scripts/docs_check.py
run doc_style "$PY" scripts/check_doc_style.py
run em_dash "$PY" scripts/check_em_dash.py --base "$BASE"
run toc_check "$PY" scripts/gen_toc.py --check
run toc_anchors "$PY" scripts/gen_toc.py --verify-anchors
run doc_paths "$PY" scripts/check_doc_paths.py
run docs_inventory "$PY" scripts/docs_inventory.py --check
run gen_register_reference "$PY" scripts/gen_register_reference.py --check
run DOC_MAP.gen "$PY" docs/DOC_MAP.gen.py --check
run check_feature_status "$PY" scripts/check_feature_status.py
run check_todo_ownership "$PY" scripts/check_todo_ownership.py
run hygiene "$PY" scripts/check_hygiene.py --check
run py_idiom "$PY" scripts/check_py_idiom.py
run sh_idiom "$PY" scripts/check_sh_idiom.py
run naming "$PY" scripts/measure_naming.py --check
run test_evidence "$PY" scripts/measure_test_evidence.py --check
run sh_syntax bash -n tb/tools/check_tu_on_wire.sh
run avtp_wire_truth "$PY" tb/tools/avtp_wire_truth.py --self-test
run torture_campaign "$PY" tb/tools/torture_campaign.py --self-test
run baremetal_check "$PY" scripts/check_baremetal_only.py --check
run baremetal_selftest "$PY" scripts/check_baremetal_only.py --selftest
(
    cd tests || exit 97
    "$PY" -m behave --no-capture -f plain \
        features/milan_streaming_licence.feature \
        features/torture_campaign_plan.feature \
        features/wire_truth_avtp.feature > "$L/behave_touched.log" 2>&1
    echo $? > "$L/behave_touched.rc"
) &
(
    cd tests || exit 97
    "$PY" -m behave --no-capture -f plain > "$L/behave_full.log" 2>&1
    echo $? > "$L/behave_full.rc"
) &
wait

for f in "$L"/*.rc; do
    n=$(basename "$f" .rc)
    printf '%s\trc=%s\t%s\n' "$n" "$(cat "$f")" "$(tail -n 1 "$L/$n.log" | cut -c1-200)"
done
