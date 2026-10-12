#!/usr/bin/env bash
# Run the composition-relevant gates on a checkout concurrently; one log + rc per gate.
# Usage: run_gates.sh <repo> <outdir> <base-sha>
set -u
repo=$1; out=$2; base=$3
mkdir -p "$out"
cd "$repo" || exit 2
declare -A G=(
  [docs_check]="python3 scripts/docs_check.py"
  [em_dash]="python3 scripts/check_em_dash.py --base $base"
  [doc_style]="python3 scripts/check_doc_style.py"
  [gen_toc_selftest]="python3 scripts/gen_toc.py --selftest"
  [gen_toc_anchors]="python3 scripts/gen_toc.py --verify-anchors"
  [gen_toc_check]="python3 scripts/gen_toc.py --check"
  [ci_events_check]="python3 scripts/ci_events.py --check"
  [ci_events_selftest]="python3 scripts/ci_events.py --selftest"
  [ci_events_fw_census]="python3 scripts/ci_events.py --firmware-census"
  [ci_scope_selftest]="python3 scripts/ci_scope.py --selftest"
  [py_idiom]="python3 scripts/check_py_idiom.py"
  [py_idiom_selftest]="python3 scripts/check_py_idiom.py --selftest"
  [doc_map_check]="python3 docs/DOC_MAP.gen.py --check"
  [doc_paths]="python3 scripts/check_doc_paths.py"
  [fw_shards]="python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"
  [hygiene]="python3 scripts/check_hygiene.py --check"
)
for k in "${!G[@]}"; do
  ( start=$(date +%s); bash -c "${G[$k]}" >"$out/$k.log" 2>&1; rc=$?
    echo "$rc $(( $(date +%s) - start ))s ${G[$k]}" >"$out/$k.rc" ) &
done
wait
for f in "$out"/*.rc; do printf '%-22s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
