#!/bin/bash
# The three Markdown-renderer gates, run with a disposable interpreter that holds
# the hash-pinned renderer from tools/markdown/requirements.txt.
# Usage: 41_renderer_gates.sh <clone> <python-with-renderer>
set -u
C=${1:?clone}; PY=${2:?python}; cd "$C" || exit 2
for cmd in "scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5" \
           "scripts/gen_toc.py --verify-anchors" "scripts/gen_toc.py --check" "scripts/check_em_dash.py --selftest"; do
  out=$("$PY" $cmd 2>&1); echo "rc $?: $cmd :: $(tail -1 <<<"$out" | cut -c1-200)"; done
