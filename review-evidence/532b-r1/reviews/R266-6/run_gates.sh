#!/usr/bin/env bash
# Offline gates for PR #570 at the exact head, run from the candidate clone.
# Usage: run_gates.sh <clone> <receipts-dir> <base-sha>
set -u
clone=$1
out=$2
base=$3
mkdir -p "$out"
cd "$clone" || exit 2
summary="$out/gates-summary.txt"
: > "$summary"
run() {
    local tag=$1
    shift
    local start end rc
    start=$(date +%s)
    "$@" > "$out/$tag.log" 2>&1
    rc=$?
    end=$(date +%s)
    printf '%s rc=%s secs=%s cmd=%s\n' "$tag" "$rc" "$((end - start))" "$*" >> "$summary"
}
run act-ci-selftest-isolated python3 -I scripts/act_ci.py --selftest
run act-ci-selftest-contract python3 scripts/act_ci.py --selftest
run slot-proof-selftest bash scripts/act_slot_proof.sh --selftest
run ci-events-check python3 scripts/ci_events.py --check
run ci-events-selftest python3 scripts/ci_events.py --selftest
run baremetal-check python3 scripts/check_baremetal_only.py --check
run baremetal-selftest python3 scripts/check_baremetal_only.py --selftest
run py-idiom python3 scripts/check_py_idiom.py
run sh-idiom python3 scripts/check_sh_idiom.py
run naming-check python3 scripts/measure_naming.py --check
run fail-fast-check python3 scripts/measure_fail_fast.py --check
run test-evidence-check python3 scripts/measure_test_evidence.py --check
run hygiene-check python3 scripts/check_hygiene.py --check
run todo-ownership python3 scripts/check_todo_ownership.py
run docs-check python3 -B scripts/docs_check.py
run doc-style python3 scripts/check_doc_style.py
run doc-paths python3 scripts/check_doc_paths.py
run toc-check python3 scripts/gen_toc.py --check
run toc-anchors python3 scripts/gen_toc.py --verify-anchors
run em-dash python3 scripts/check_em_dash.py --base "$base"
run diff-check git diff --check "$base" HEAD
cat "$summary"
