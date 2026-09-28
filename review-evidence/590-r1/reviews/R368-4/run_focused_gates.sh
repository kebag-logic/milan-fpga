#!/usr/bin/env bash
# Focused head gates for R368-4, at most 6 in parallel, foreground.
# Usage: run_focused_gates.sh <repo at exact head> <receipt dir>
set -u
repo=$1 out=$2 md=${MD_PY:?set MD_PY to the pinned Markdown environment interpreter}
mkdir -p "$out"
cd "$repo" || exit 2
cat > "$out/gates.list" <<LIST
host-selftest|timeout 3600 python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
service-selftest|timeout 3600 python3 -B tb/verilator/fw_service_budget/run.py --self-test
ci-scope-selftest|timeout 1800 python3 -B scripts/ci_scope.py --selftest
clock-contract|timeout 1800 python3 -B sw/builder/test_clock_contract.py
em-dash|timeout 1800 $md -B scripts/check_em_dash.py --base 7a7582f03ce5ba7863a90ac342c21be18d90db0b
docs-check|timeout 1800 $md -B scripts/docs_check.py
solution-docs|timeout 1800 python3 -B scripts/check_solution_docs.py
feature-status|timeout 1800 python3 -B scripts/check_feature_status.py
diff-check|git -c core.pager=cat diff --check 7a7582f03ce5ba7863a90ac342c21be18d90db0b 1f039cfe86d5337f5c9b7248696dba1c4bdda67e
diff-check-lane|git -c core.pager=cat diff --check 20aa4eabf310a43b654e0c74c5374c3a0458fd4b 1f039cfe86d5337f5c9b7248696dba1c4bdda67e
LIST
run_one() {
  name=${1%%|*} cmd=${1#*|}
  start=$(date +%s)
  bash -c "$cmd" > "$out/gate-$name.log" 2>&1
  rc=$?
  printf '%s rc=%s seconds=%s cmd=%s\n' "$name" "$rc" "$(( $(date +%s) - start ))" "$cmd" > "$out/gate-$name.rc"
}
export -f run_one
export out
tr '\n' '\0' < "$out/gates.list" | xargs -0 -P 6 -I{} bash -c 'run_one "$@"' _ {}
cat "$out"/gate-*.rc
