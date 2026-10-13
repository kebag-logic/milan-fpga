#!/usr/bin/env bash
# The Markdown-renderer gates on a composed candidate tree, run with an
# interpreter that has tools/markdown/requirements.txt installed.
# usage: run_md_gates.sh <python> <candidate clone> <receipt dir> <composed parent> <live dev> <PR base>
set -uo pipefail
py=$1 repo=$2 out=$3 parent=$4 dev=$5 prbase=$6
mkdir -p "$out"
cd "$repo"
gate() {
  local name=$1; shift
  ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
}
gate gen_toc_check "$py" scripts/gen_toc.py --check
gate gen_toc_verify_anchors "$py" scripts/gen_toc.py --verify-anchors
gate gen_toc_selftest "$py" scripts/gen_toc.py --selftest
gate em_dash_parent "$py" scripts/check_em_dash.py --base "$parent"
gate em_dash_dev "$py" scripts/check_em_dash.py --base "$dev"
gate em_dash_prbase "$py" scripts/check_em_dash.py --base "$prbase"
gate em_dash_selftest "$py" scripts/check_em_dash.py --selftest
wait
"$py" -m pip freeze >"$out/renderer_freeze.txt"
for rc in "$out"/*.rc; do printf '%s %s\n' "$(basename "$rc" .rc)" "$(cat "$rc")"; done | tee "$out/SUMMARY.txt"
