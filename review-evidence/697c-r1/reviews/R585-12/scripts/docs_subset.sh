#!/usr/bin/env bash
# Run a subset of the docs job's commands in a submodule-free clone, concurrently,
# each with its own log and rc. usage: docs_subset.sh <clone> <logdir> <em-dash base>
set -uo pipefail
clone=$1 logs=$2 base=$3
mkdir -p "$logs"
cd "$clone" || exit 2
cmds=(
  "docs_check|python3 scripts/docs_check.py"
  "em_dash|python3 scripts/check_em_dash.py --base $base"
  "submodule_docs|python3 scripts/check_submodule_docs.py"
  "submodule_docs_selftest|python3 scripts/check_submodule_docs.py --selftest"
  "diagram_check|python3 docs/diagrams/submodule_boundaries.gen.py --check"
  "diagram_selftest|python3 docs/diagrams/submodule_boundaries.gen.py --selftest"
  "diagram_pngs|python3 scripts/check_diagram_pngs.py"
  "ci_events_check|python3 scripts/ci_events.py --check"
  "ci_events_selftest|python3 scripts/ci_events.py --selftest"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "doc_style|python3 scripts/check_doc_style.py"
  "toc_check|python3 scripts/gen_toc.py --check"
  "toc_anchors|python3 scripts/gen_toc.py --verify-anchors"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "hygiene|python3 scripts/check_hygiene.py --check"
  "doc_map|python3 docs/DOC_MAP.gen.py --check"
)
for entry in "${cmds[@]}"; do
  name=${entry%%|*} cmd=${entry#*|}
  ( bash -c "$cmd" > "$logs/$name.log" 2>&1; echo $? > "$logs/$name.rc" ) &
done
wait
for entry in "${cmds[@]}"; do
  name=${entry%%|*}
  printf '%-26s rc=%s  %s\n' "$name" "$(cat "$logs/$name.rc")" "$(tail -n 1 "$logs/$name.log" | cut -c1-140)"
done
