#!/usr/bin/env bash
# R607-1: focused documentation and quality gates at the head, concurrently,
# each with its own log and rc.  gates.sh <tree> <out> <py312> <md-python> <base>
set -u
tree=$1 out=$2 py312=$3 md=$4 base=$5
mkdir -p "$out"
cd "$tree" || exit 9
run() {   # run <name> <command...>
  local name=$1; shift
  ( "$@" > "$out/$name.log" 2>&1; echo "$?" > "$out/$name.rc" ) &
}
run docs_check        python3 scripts/docs_check.py
run em_dash           "$md" scripts/check_em_dash.py --base "$base"
run em_dash_selftest  "$md" scripts/check_em_dash.py --selftest
run toc_check         "$md" scripts/gen_toc.py --check
run toc_anchors       "$md" scripts/gen_toc.py --verify-anchors
run doc_paths         python3 scripts/check_doc_paths.py
run doc_style         python3 scripts/check_doc_style.py
run py_idiom          "$py312" scripts/check_py_idiom.py
run hygiene           python3 scripts/check_hygiene.py --check
run todo              python3 scripts/check_todo_ownership.py
run fail_fast         python3 scripts/measure_fail_fast.py --check
run soc_sources       python3 scripts/check_soc_sources.py
run ci_events         python3 scripts/ci_events.py --check
run feature_status    python3 scripts/check_feature_status.py
run sh_idiom          python3 scripts/check_sh_idiom.py
run diff_check        git diff --check "$base" HEAD
wait
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
