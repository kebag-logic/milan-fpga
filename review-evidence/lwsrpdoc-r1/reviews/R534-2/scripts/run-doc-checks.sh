#!/usr/bin/env bash
# Run the published documentation checks against a checkout; record rc per command.
# Usage: run-doc-checks.sh CHECKOUT OUTDIR
set -u
src=$1; out=$2; mkdir -p "$out"
cd "$src" || exit 2
run() { name=$1; shift; "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc"; }
run sentences python3 doc/tools/check_sentences.py &
run references python3 doc/tools/check_references.py &
run references-selftest python3 doc/tools/check_references.py --self-test &
run links-auth python3 doc/tools/check_links.py --github-auth &
run links-anon python3 doc/tools/check_links.py &
run render python3 doc/tools/render_mermaid.py --output "$out/graphs" &
wait
for f in "$out"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
