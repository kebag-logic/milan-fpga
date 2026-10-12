#!/usr/bin/env bash
# Rerun the gates that need the pinned Markdown renderer (cmarkgfm 2025.10.22,
# html5lib 1.1, tools/markdown/requirements.txt) with an interpreter that has it.
# Usage: gates_renderer.sh <repo> <outdir> <base-for-em-dash> <python-with-renderer>
set -u
repo=$1; out=$2; base=$3; py=$4
cd "$repo" || exit 2
for g in "toc_self:scripts/gen_toc.py --selftest" "toc_anchors:scripts/gen_toc.py --verify-anchors" \
         "toc_check:scripts/gen_toc.py --check" "em_dash:scripts/check_em_dash.py --base $base" \
         "docs_check:scripts/docs_check.py"; do
  n=${g%%:*}; c=${g#*:}
  $py $c >"$out/$n.log" 2>&1; echo $? >"$out/$n.rc"
done
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2 >"$out/SUMMARY.txt"
