#!/usr/bin/env bash
# Run the documentation gates relevant to a docs-only change, concurrently,
# each with its own log and rc file. Usage:
#   run_docs_gates.sh <repo> <python> <base-sha> <outdir>
set -u
repo=$1; py=$2; base=$3; out=$4
mkdir -p "$out"
cd "$repo" || exit 2
declare -A G=(
  [docs_check]="$py scripts/docs_check.py"
  [docs_self]="$py scripts/docs_check.py --selftest"
  [docs_nogit]="env GIT_DIR=/dev/null $py scripts/docs_check.py"
  [feature_status]="$py scripts/check_feature_status.py"
  [feature_self]="$py scripts/check_feature_status.py --self-test"
  [em_dash]="$py scripts/check_em_dash.py --base $base"
  [em_dash_self]="$py scripts/check_em_dash.py --selftest"
  [doc_style]="$py scripts/check_doc_style.py"
  [doc_style_self]="$py scripts/check_doc_style.py --selftest"
  [gptp_docs]="$py scripts/check_gptp_docs.py"
  [doc_map]="$py docs/DOC_MAP.gen.py --check"
  [solution]="$py scripts/check_solution_docs.py"
  [submodule_docs]="$py scripts/check_submodule_docs.py"
  [module_matrix]="$py docs/traceability/gen_module_matrix.py --check"
  [doc_paths]="$py scripts/check_doc_paths.py"
  [archive]="$py scripts/check_archive.py"
  [toc_self]="$py scripts/gen_toc.py --selftest"
  [toc_anchors]="$py scripts/gen_toc.py --verify-anchors"
  [toc_check]="$py scripts/gen_toc.py --check"
  [todo]="$py scripts/check_todo_ownership.py"
  [hygiene]="$py scripts/check_hygiene.py --check"
  [resource_baseline]="$py syn/ooc/pp_resource_gate.py check-baseline"
  [diff_check_base]="git diff --check $base HEAD"
)
for k in "${!G[@]}"; do
  ( bash -c "${G[$k]}" > "$out/$k.log" 2>&1; echo $? > "$out/$k.rc" ) &
done
wait
fail=0
for k in $(printf '%s\n' "${!G[@]}" | sort); do
  rc=$(cat "$out/$k.rc"); printf '%-20s rc=%s  %s\n' "$k" "$rc" "${G[$k]}"
  [ "$rc" = 0 ] || fail=1
done
exit $fail
