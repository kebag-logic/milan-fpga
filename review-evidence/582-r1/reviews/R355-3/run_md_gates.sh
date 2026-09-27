#!/usr/bin/env bash
# Re-run the renderer-dependent documentation gates with the pinned Markdown
# renderer environment (tools/markdown/requirements.txt).
# Usage: run_md_gates.sh <candidate-clone> <receipt-dir> <python-with-pinned-renderer>
set -u
repo=$1
out=$2
py=$3
parent=b468a56d9e3ed9c10e4e41503c446dd6b242b9f8
mkdir -p "$out/logs"
export PYTHONDONTWRITEBYTECODE=1
summary="$out/md-gates-summary.tsv"
printf 'n\trc\tcommand\n' > "$summary"
n=0
run() {
    n=$((n + 1))
    local log
    log=$(printf '%s/logs/md%02d.log' "$out" "$n")
    (cd "$repo" && printf '$ %s\n' "$*" && "$@") > "$log" 2>&1
    local rc=$?
    printf 'md%02d\t%d\t%s\n' "$n" "$rc" "$*" >> "$summary"
}
run "$py" -c 'from importlib.metadata import version as v; print(v("cmarkgfm"), v("html5lib"))'
run "$py" scripts/check_em_dash.py --base "$parent"
run "$py" scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5
run "$py" scripts/check_em_dash.py --selftest
run "$py" scripts/gen_toc.py --selftest
run "$py" scripts/gen_toc.py --verify-anchors
run "$py" scripts/gen_toc.py --check
run "$py" scripts/docs_check.py
run git status --porcelain --ignored=matching
