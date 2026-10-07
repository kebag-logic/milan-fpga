#!/usr/bin/env bash
# Run the documented documentation checks concurrently from a checkout root.
# Usage: run_doc_checks.sh CHECKOUT OUT
set -u
SRC=$(cd "$1" && pwd); OUT=$2
mkdir -p "$OUT"; rm -rf "$OUT/graphs"
export PYTHONDONTWRITEBYTECODE=1
cd "$SRC"
job() { local n=$1; shift; ( "$@" ) > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"; }
job sentences python3 doc/tools/check_sentences.py &
job references python3 doc/tools/check_references.py &
job references-selftest python3 doc/tools/check_references.py --self-test &
job links-auth python3 doc/tools/check_links.py --github-auth &
job links-anon python3 doc/tools/check_links.py &
job mermaid python3 doc/tools/render_mermaid.py --output "$OUT/graphs" &
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") :: $(tail -n 1 "${f%.rc}.log")"; done
