#!/usr/bin/env bash
# R300-4: Markdown-renderer gates, run with an interpreter that has the
# hash-pinned renderer from tools/markdown/requirements.txt.
# Usage: run_md_gates.sh <clone> <packet> <python-with-pinned-renderer>
set -u
CLONE=${1:?clone}; PKT=${2:?packet}; PY=${3:?python}
OUT="$PKT/receipts/static"; mkdir -p "$OUT"
cd "$CLONE" || exit 2
run() {
  local name=$1; shift
  { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$OUT/$name.txt" 2>&1
  tail -n 1 "$OUT/$name.txt" | sed "s/^/$name: /"
}
{ echo "\$ $PY -c 'import cmarkgfm, html5lib; print versions'"; "$PY" -c 'import cmarkgfm, html5lib, importlib.metadata as m; print("cmarkgfm", m.version("cmarkgfm"), "html5lib", m.version("html5lib"), "cffi", m.version("cffi"))'; echo "rc=$?"; } > "$OUT/md_renderer_identity.txt" 2>&1
tail -n 2 "$OUT/md_renderer_identity.txt"
run gen_toc_check           "$PY" scripts/gen_toc.py --check
run gen_toc_verify_anchors  "$PY" scripts/gen_toc.py --verify-anchors
run check_em_dash_base_dev  "$PY" scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8
run docs_check_git_pinned_py "$PY" -B scripts/docs_check.py
