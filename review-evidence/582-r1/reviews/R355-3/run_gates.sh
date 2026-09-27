#!/usr/bin/env bash
# Run the composition-relevant gates on the merge-train candidate.
# Usage: run_gates.sh <candidate-clone> <receipt-dir>
# Each command runs in the foreground; its rc and output are recorded.
set -u
repo=$1
out=$2
parent=b468a56d9e3ed9c10e4e41503c446dd6b242b9f8
mkdir -p "$out/logs"
export PYTHONDONTWRITEBYTECODE=1
summary="$out/gates-summary.tsv"
printf 'n\trc\tcommand\n' > "$summary"
n=0
run() {
    n=$((n + 1))
    local log
    log=$(printf '%s/logs/%02d.log' "$out" "$n")
    (cd "$repo" && printf '$ %s\n' "$*" && "$@") > "$log" 2>&1
    local rc=$?
    printf '%02d\t%d\t%s\n' "$n" "$rc" "$*" >> "$summary"
}
run git rev-parse HEAD 'HEAD^{tree}'
run git diff --check "$parent" HEAD
run python3 scripts/docs_check.py
run python3 scripts/docs_check.py --selftest
run python3 scripts/check_em_dash.py --base "$parent"
run python3 scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 scripts/check_doc_paths.py
run python3 scripts/check_solution_docs.py
run python3 scripts/check_solution_docs.py --selftest
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/ci_scope.py --selftest
run python3 scripts/ci_events.py --check
run python3 scripts/ci_events.py --selftest
run python3 scripts/check_nvm_capture.py
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_entity_shape.py
run python3 scripts/check_entity_shape.py --self-test
run python3 scripts/check_sweep_shape.py --self-test
run python3 scripts/check_deploy_shape.py --self-test
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_feature_status.py
run python3 sw/builder/test_clock_contract.py
run python3 sw/builder/test_declarations.py
run git status --porcelain --ignored=matching
