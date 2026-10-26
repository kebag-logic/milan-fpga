#!/usr/bin/env bash
# Run the lane's gates at the checked-out head; each writes <name>.log and <name>.rc.
# Usage: bash run_head_gates.sh <repo root> <pinned markdown python> <receipts dir>
set -u
repo=$1 md=$2 out=$3
cd "$repo" || exit 1
gate() {
    local name=$1
    shift
    "$@" > "$out/$name.log" 2>&1
    echo $? > "$out/$name.rc"
    echo "$name rc=$(cat "$out/$name.rc")"
}
gate selftest python3 -B tb/tools/torture_campaign.py --self-test
gate behave_plan python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain
(cd tests && behave --no-capture -f plain) > "$out/behave_all.full.log" 2>&1
echo $? > "$out/bdd_conformance.rc"
echo "bdd_conformance rc=$(cat "$out/bdd_conformance.rc")"
tail -5 "$out/behave_all.full.log" > "$out/bdd_conformance.summary.txt"
gate docs_check "$md" -B scripts/docs_check.py
gate gen_toc_check "$md" -B scripts/gen_toc.py --check
gate gen_toc_anchors "$md" -B scripts/gen_toc.py --verify-anchors
gate em_dash "$md" -B scripts/check_em_dash.py --base origin/dev
gate doc_style "$md" -B scripts/check_doc_style.py
gate doc_paths "$md" -B scripts/check_doc_paths.py
gate py_idiom python3 -B scripts/check_py_idiom.py
gate feature_status python3 -B scripts/check_feature_status.py
gate feature_status_selftest python3 -B scripts/check_feature_status.py --self-test
gate coverage_release python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,audio,power
python3 -B tb/tools/torture_campaign.py --plan --areas soak,audio,power --json > "$out/plan.json" 2> "$out/plan_json.stderr.log"
echo $? > "$out/plan_json.rc"
echo "plan_json rc=$(cat "$out/plan_json.rc")"
gate diff_check_range git diff --check origin/dev HEAD
gate diff_check_tree git diff --check
gate porcelain git status --porcelain
