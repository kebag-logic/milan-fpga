#!/usr/bin/env bash
# Run the composition-relevant gates on the merge-train candidate.
# Usage: run_gates.sh <candidate-checkout> <receipt-dir> [scoped-tool-bin]
# Each command's combined output lands in <receipt-dir>/NN-<slug>.log and one
# line "NN<TAB>exit<TAB>seconds<TAB>command" is appended to <receipt-dir>/summary.tsv.
set -uo pipefail
repo=${1:?candidate checkout}
out=${2:?receipt dir}
toolbin=${3:-}
mkdir -p "$out"
out=$(cd "$out" && pwd)
: > "$out/summary.tsv"
export PYTHONDONTWRITEBYTECODE=1
if [ -n "$toolbin" ]; then export PATH="$toolbin:$PATH"; fi
cd "$repo" || exit 2

# Bases: parent 1 of the candidate (the train before this PR), the PR source
# base, and live dev.
P1=9912748d9c30f33a85056fcd1d836d3a4449cc69
SRC_BASE=483a133ed08867ea0d300d2b4a027b5b48a4282f
LIVE_DEV=776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d

cmds=(
  "git rev-parse HEAD HEAD^{tree}"
  "verilator --version"
  "python3 scripts/docs_check.py"
  "python3 scripts/docs_check.py --selftest"
  "python3 scripts/gen_toc.py --selftest"
  "python3 scripts/gen_toc.py --verify-anchors"
  "python3 scripts/gen_toc.py --check"
  "python3 scripts/check_em_dash.py --base $P1"
  "python3 scripts/check_em_dash.py --base $SRC_BASE"
  "python3 scripts/check_em_dash.py --base $LIVE_DEV"
  "python3 scripts/check_em_dash.py --selftest"
  "python3 scripts/check_doc_style.py"
  "python3 scripts/check_doc_style.py --selftest"
  "python3 scripts/ci_events.py --check"
  "python3 scripts/ci_events.py --selftest"
  "python3 scripts/ci_scope.py --selftest"
  "python3 scripts/measure_fail_fast.py --check"
  "python3 scripts/measure_fail_fast.py --selftest"
  "python3 scripts/check_hygiene.py --check"
  "python3 scripts/check_hygiene.py --selftest"
  "python3 scripts/check_py_idiom.py"
  "python3 scripts/check_py_idiom.py --selftest"
  "python3 scripts/check_sh_idiom.py"
  "python3 scripts/check_sh_idiom.py --selftest"
  "python3 scripts/check_todo_ownership.py"
  "python3 scripts/check_todo_ownership.py --selftest"
  "python3 scripts/measure_test_evidence.py --check"
  "python3 scripts/measure_test_evidence.py --selftest"
  "python3 scripts/check_doc_paths.py"
  "python3 scripts/check_baremetal_only.py --check"
  "python3 scripts/check_baremetal_only.py --selftest"
  "python3 docs/DOC_MAP.gen.py --check"
  "python3 scripts/check_archive.py"
  "python3 scripts/check_feature_status.py"
  "python3 scripts/check_feature_status.py --self-test"
  "python3 scripts/pp_srcs.py --check"
  "python3 scripts/pp_srcs.py --selftest"
  "python3 scripts/measure_control_flow.py --selftest"
  "python3 scripts/measure_cohesion.py --selftest"
  "python3 syn/yosys/result_cache.py --selftest"
  "python3 syn/yosys/rom_cache_selftest.py"
  "python3 syn/yosys/cache_selftest.py"
  "git diff --check $P1 HEAD"
  "git diff --check $SRC_BASE HEAD"
)

n=0
for c in "${cmds[@]}"; do
  n=$((n + 1))
  id=$(printf '%02d' "$n")
  slug=$(printf '%s' "$c" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-70)
  log="$out/$id-$slug.log"
  start=$(date +%s.%N)
  printf '$ %s\n' "$c" > "$log"
  bash -c "$c" >> "$log" 2>&1 < /dev/null
  rc=$?
  printf '[exit %s]\n' "$rc" >> "$log"
  end=$(date +%s.%N)
  printf '%s\t%s\t%.1f\t%s\n' "$id" "$rc" "$(echo "$end - $start" | bc)" "$c" >> "$out/summary.tsv"
done
cat "$out/summary.tsv"
