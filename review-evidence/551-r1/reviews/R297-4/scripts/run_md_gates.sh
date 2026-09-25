#!/bin/sh
# Usage: run_md_gates.sh <clone> <receipt-dir> [python]
# Re-runs the gates that need the locked Markdown renderer (cmarkgfm
# 2025.10.22, html5lib 1.1 per tools/markdown/requirements.txt).
set -u
C=$1; OUT=$2; PY=${3:-$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3}
BASE=d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce
cd "$C" || exit 2
run() {
  name=$1; shift
  log=$OUT/gate_$name.log
  { echo "# cmd: $*"; echo "# head: $(git rev-parse HEAD)";
    echo "# renderer: $("$PY" -c 'from importlib.metadata import version as v; print("cmarkgfm", v("cmarkgfm"), "html5lib", v("html5lib"))')"; } > "$log"
  "$@" >> "$log" 2>&1
  rc=$?
  echo "# rc=$rc" >> "$log"
  echo "$name rc=$rc"
}
run gen_toc_check          "$PY" -B scripts/gen_toc.py --check
run gen_toc_verify_anchors "$PY" -B scripts/gen_toc.py --verify-anchors
run check_em_dash          "$PY" -B scripts/check_em_dash.py --base "$BASE"
run docs_check_git_md      "$PY" -B scripts/docs_check.py
run docs_check_nogit_md    env GIT_DIR=/nonexistent-r297-4-no-git "$PY" -B scripts/docs_check.py
