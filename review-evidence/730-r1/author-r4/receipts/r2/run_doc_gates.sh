#!/usr/bin/env bash
# Run the documentation gates of lane 730 in parallel; one log and one rc file per gate.
set -u
G=$1
cd $LANES/730-act-cpusets || exit 2
mkdir -p "$G"
export PATH=$VALIDATION_STORAGE/730-a607/venv312/bin:$PATH
run() { local name=$1; shift; ( "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
run docs-check python3 scripts/docs_check.py
run doc-style python3 scripts/check_doc_style.py
run toc-check python3 scripts/gen_toc.py --check
run toc-anchors python3 scripts/gen_toc.py --verify-anchors
run em-dash python3 scripts/check_em_dash.py --base dc4d06cb
run doc-paths python3 scripts/check_doc_paths.py
run ci-events-check python3 scripts/ci_events.py --check
run diff-check git diff --check dc4d06cb
wait
for f in "$G"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") | $(tail -1 "${f%.rc}.log" | cut -c1-120)"; done
