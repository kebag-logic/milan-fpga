#!/bin/sh
# Focused docs gates for a docs-only head: each command unpiped, rc recorded.
# usage: docs_gates.sh <tree> <python> <out>
set -u
tree=$1 py=$2 out=$3
mkdir -p "$out"
cd "$tree" || exit 9
git rev-parse HEAD > "$out/head.txt"
git status --porcelain > "$out/status-before.txt"
run() {
  n=$1; shift
  echo "$*" > "$out/$n.cmd"
  "$py" "$@" > "$out/$n.log" 2>&1
  echo $? > "$out/$n.rc"
  echo "$n rc=$(cat "$out/$n.rc") $*"
}
run 01 scripts/docs_check.py
run 02 scripts/check_em_dash.py --base c6bd08c6f52632c6d33d834ce842ac3cf63f29cc
run 03 scripts/check_doc_style.py
run 04 scripts/check_doc_paths.py
run 05 scripts/gen_toc.py --verify-anchors
run 06 scripts/gen_toc.py --check
run 07 scripts/check_archive.py
run 08 scripts/ci_scope.py --selftest
run 09 syn/ooc/pp_resource_gate.py check-baseline
run 10 scripts/check_solution_docs.py
git status --porcelain > "$out/status-after.txt"
