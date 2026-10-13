#!/usr/bin/env bash
# Run the focused merge-delta gates concurrently against one checkout.
# Usage: run_gates.sh <checkout> <python> <out_dir>
# Each gate writes <out_dir>/<name>.log and <out_dir>/<name>.rc; a summary goes to <out_dir>/SUMMARY.tsv.
set -u
repo=$1 py=$2 out=$3
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
gates=(
  "ci-scope-selftest|scripts/ci_scope.py --selftest"
  "ci-events-check|scripts/ci_events.py --check"
  "ci-events-selftest|scripts/ci_events.py --selftest"
  "docs-check|scripts/docs_check.py"
  "docs-check-selftest|scripts/docs_check.py --selftest"
  "doc-paths|scripts/check_doc_paths.py"
  "doc-style|scripts/check_doc_style.py"
  "toc-check|scripts/gen_toc.py --check"
  "toc-anchors|scripts/gen_toc.py --verify-anchors"
  "em-dash-base-0136de16|scripts/check_em_dash.py --base 0136de16291a127e0a34627c77ac09cd41efc08b"
  "py-idiom|scripts/check_py_idiom.py"
  "sh-idiom|scripts/check_sh_idiom.py"
  "pp-srcs|scripts/pp_srcs.py --check"
  "test-evidence|scripts/measure_test_evidence.py --check"
)
cd "$repo" || exit 2
for g in "${gates[@]}"; do
  name=${g%%|*} cmd=${g#*|}
  ( start=$(date +%s.%N)
    # shellcheck disable=SC2086
    "$py" $cmd >"$out/$name.log" 2>&1
    rc=$?
    end=$(date +%s.%N)
    printf '%s\n' "$rc" >"$out/$name.rc"
    printf '%s\t%s\t%.1f\t%s\n' "$name" "$rc" "$(echo "$end - $start" | bc)" "$cmd" >"$out/$name.row" ) &
done
wait
{ printf 'gate\trc\tseconds\tcommand\n'; cat "$out"/*.row; } >"$out/SUMMARY.tsv"
rm -f "$out"/*.row
cat "$out/SUMMARY.tsv"
