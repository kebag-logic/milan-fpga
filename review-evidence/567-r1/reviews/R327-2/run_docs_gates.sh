#!/usr/bin/env bash
# R327-2 docs gate runner. Usage: run_docs_gates.sh <checkout> <python> <receipt-dir>
# Runs each gate in the foreground, records rc and output per gate.
set -u
REPO=${1:?checkout}; PY=${2:?python}; OUT=${3:?receipt dir}
BASE=7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
mkdir -p "$OUT"
cd "$REPO" || exit 2
SUMMARY="$OUT/summary.txt"
{ echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"; "$PY" --version; } > "$SUMMARY" 2>&1
run() { # <name> <cmd...>
  local name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1
  local rc=$?
  printf '%-28s rc=%s  %s\n' "$name" "$rc" "$*" >> "$SUMMARY"
}
run docs_check_git      "$PY" -B scripts/docs_check.py
run em_dash             "$PY" -B scripts/check_em_dash.py --base "$BASE"
run doc_style           "$PY" -B scripts/check_doc_style.py
run toc_check           "$PY" -B scripts/gen_toc.py --check
run toc_anchors         "$PY" -B scripts/gen_toc.py --verify-anchors
run doc_paths           "$PY" -B scripts/check_doc_paths.py
run submodule_docs      "$PY" -B scripts/check_submodule_docs.py
run submodule_diagram   "$PY" -B docs/diagrams/submodule_boundaries.gen.py --check
run diagram_pngs        "$PY" -B scripts/check_diagram_pngs.py
run diff_check_wt       git diff --check
run diff_check_range    git diff --check "$BASE" HEAD
# Metadata-free (filesystem) mode: archive export, no .git.
EXP="${EXPORT_DIR:-$OUT/../scratch/export}"
rm -rf "$EXP"; mkdir -p "$EXP"
git archive HEAD | tar -x -C "$EXP"
( cd "$EXP" && "$PY" -B scripts/docs_check.py ) > "$OUT/docs_check_nogit.log" 2>&1
printf '%-28s rc=%s  %s\n' docs_check_nogit "$?" "docs_check.py in git-archive export" >> "$SUMMARY"
cat "$SUMMARY"
