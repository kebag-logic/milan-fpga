#!/usr/bin/env bash
# Composition static gates for the issue 501 merge-train candidate.
# Usage: run_static_gates.sh <repo-checkout> <receipt-dir> <em-dash-base>
# Runs each command from the candidate checkout, at most 8 at a time, and
# writes <receipt-dir>/<n>.log plus a summary table (index, rc, command).
set -u
REPO=$(cd "$1" && pwd); OUT=$(mkdir -p "$2" && cd "$2" && pwd); BASE=$3
cmds=(
  "python3 scripts/docs_check.py"
  "python3 scripts/check_em_dash.py --base $BASE"
  "python3 scripts/check_doc_style.py"
  "python3 scripts/check_doc_style.py --selftest"
  "python3 docs/DOC_MAP.gen.py --check"
  "python3 scripts/gen_toc.py --selftest"
  "python3 scripts/gen_toc.py --verify-anchors"
  "python3 scripts/gen_toc.py --check"
  "python3 scripts/check_doc_paths.py"
  "python3 docs/traceability/gen_module_matrix.py --check"
  "python3 scripts/check_feature_status.py"
  "python3 scripts/check_feature_status.py --self-test"
  "python3 scripts/check_nvm_record_space.py"
  "python3 scripts/check_nvm_record_space.py --self-test"
  "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py"
  "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test"
  "python3 scripts/check_baremetal_only.py --check"
  "python3 scripts/check_baremetal_only.py --selftest"
  "python3 scripts/measure_test_evidence.py --check"
  "python3 scripts/measure_test_evidence.py --selftest"
  "python3 scripts/ci_events.py --check"
  "python3 scripts/ci_events.py --selftest"
  "python3 scripts/check_cpp_idiom.py"
  "python3 scripts/check_py_idiom.py"
  "python3 scripts/check_hygiene.py --check"
  "python3 scripts/check_todo_ownership.py"
  "python3 scripts/measure_naming.py --check"
  "python3 scripts/measure_fail_fast.py --check"
  "python3 scripts/check_rtl_source_lists.py"
  "python3 scripts/check_archive.py"
  "git diff --check 0b81fdc969131b82c535c4a183a78065fd1cd2d8 2ab66c9de3a63942c4d3251e1354e8ad3a50d88c"
)
: > "$OUT/cmds.txt"
for i in "${!cmds[@]}"; do printf '%02d\t%s\n' "$i" "${cmds[$i]}" >> "$OUT/cmds.txt"; done
cd "$REPO" || exit 2
export OUT
cut -f1 "$OUT/cmds.txt" | xargs -P 8 -I{} bash -c '
  n={}; c=$(awk -F"\t" -v n="$n" "\$1==n{print \$2}" "$OUT/cmds.txt")
  s=$(date +%s); timeout 3600 bash -c "$c" > "$OUT/$n.log" 2>&1; rc=$?
  printf "%s\t%s\t%ss\t%s\n" "$n" "$rc" "$(( $(date +%s) - s ))" "$c" > "$OUT/$n.rc"'
sort -n "$OUT"/*.rc > "$OUT/SUMMARY.tsv"; rm -f "$OUT"/*.rc
cat "$OUT/SUMMARY.tsv"
awk -F'\t' '$2!=0{bad=1} END{exit bad}' "$OUT/SUMMARY.tsv"
