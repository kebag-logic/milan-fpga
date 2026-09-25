#!/usr/bin/env bash
# R297-3: the Markdown-renderer gates under a private venv holding the pinned
# tools/markdown/requirements.txt (the host interpreter lacks the renderer, so
# static_gates.sh records rc 2 "cannot judge" for these three).
# Usage: venv_gates.sh <repo> <venv-python> <receipt-dir>
set -u
REPO=$1; PY=$2; OUT=$3; mkdir -p "$OUT"; : > "$OUT/summary.txt"
cd "$REPO" || exit 2
gate() { name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1; rc=$?
  printf '%-22s rc=%d  %s\n' "$name" "$rc" "$*" >> "$OUT/summary.txt"; }
gate check_em_dash   "$PY" -B scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
gate gen_toc_check   "$PY" -B scripts/gen_toc.py --check
gate gen_toc_anchors "$PY" -B scripts/gen_toc.py --verify-anchors
gate docs_check_git  "$PY" -B scripts/docs_check.py
gate docs_check_nogit env GIT_DIR=/nonexistent-r297-3-git "$PY" -B scripts/docs_check.py
"$PY" -m pip freeze > "$OUT/venv_freeze.txt" 2>&1
sha256sum tools/markdown/requirements.txt >> "$OUT/venv_freeze.txt"
sed "s#$PY#<venv-python>#" "$OUT/summary.txt"
