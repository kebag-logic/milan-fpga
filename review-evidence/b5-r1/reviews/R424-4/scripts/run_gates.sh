#!/usr/bin/env bash
# Run the documentation gates of the B5 lane at the checked-out head.
# usage: run_gates.sh <repo> <python with the tools/markdown lock> <out-file>
set -uo pipefail
repo=$1 py=$2 out=$3
cd "$repo" || exit 2
: > "$out"
fail=0
run() {
    local rc
    {
        echo "== \$ $*"
        "$@" 2>&1 | tail -n 15
        rc=${PIPESTATUS[0]}
        echo "rc=$rc"
        echo
    } >> "$out"
    rc=$(tail -n 2 "$out" | head -n 1 | sed 's/rc=//')
    [[ $rc == 0 ]] || fail=1
}
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')" >> "$out"
echo "python $("$py" --version 2>&1); $("$py" -m pip freeze 2>/dev/null | tr '\n' ' ')" >> "$out"
echo >> "$out"
run "$py" scripts/docs_check.py
run "$py" scripts/check_doc_style.py
run "$py" scripts/gen_toc.py --check
run "$py" scripts/gen_toc.py --verify-anchors
run "$py" scripts/check_em_dash.py --base e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b
run "$py" scripts/check_em_dash.py --selftest
run "$py" scripts/check_doc_paths.py
run "$py" scripts/ci_scope.py --selftest
run python3 scripts/check_baremetal_only.py --check  # needs pyyaml, outside the Markdown lock
run "$py" scripts/check_feature_status.py --self-test
run git diff --check
run git diff --check e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b HEAD
run git diff --check cf38633ad9a5bdb05517bedba73ce50965af967b HEAD
run git diff --check c5804007630b4ef39b93f725807019f46e700ecd HEAD
echo "overall: $([[ $fail == 0 ]] && echo 'all rc 0' || echo 'FAILURE')" >> "$out"
exit $fail
