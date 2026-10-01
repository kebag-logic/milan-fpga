#!/usr/bin/env bash
# Reviewer gate runner for PR #631 at the exact head; run from the clone root.
# Usage: run_gates.sh <clone> <outdir> <python>
set -u
clone=$1; out=$2; py=$3
cd "$clone" || exit 2
git rev-parse HEAD > "$out/HEAD"
run() { name=$1; shift; "$@" > "$out/$name.out" 2>&1; echo $? > "$out/$name.rc"; printf '%-28s rc=%s\n' "$name" "$(cat "$out/$name.rc")"; }
run check_entity_shape   "$py" scripts/check_entity_shape.py
run docs_check           "$py" scripts/docs_check.py
run check_doc_style      "$py" scripts/check_doc_style.py
run gen_toc_check        "$py" scripts/gen_toc.py --check
run gen_toc_anchors      "$py" scripts/gen_toc.py --verify-anchors
run check_em_dash        "$py" scripts/check_em_dash.py --base d4dd742679b902b2bc5eedf89d525066d59aafbb
run check_doc_paths      "$py" scripts/check_doc_paths.py
run check_gptp_docs      "$py" scripts/check_gptp_docs.py
run doc_map_check        "$py" docs/DOC_MAP.gen.py --check
run timesync_chain_check "$py" docs/diagrams/timesync_chain.gen.py --check
run diff_check_base      git diff --check d4dd742679b902b2bc5eedf89d525066d59aafbb c554ae51b1dcc2285863f0f0117cb025971a594c
run diff_check_wt        git diff --check
