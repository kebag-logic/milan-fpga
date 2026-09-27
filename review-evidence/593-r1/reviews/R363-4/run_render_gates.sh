#!/usr/bin/env bash
# Renderer-dependent doc gates, run with an interpreter that has the pinned
# tools/markdown/requirements.txt installed. Usage: run_render_gates.sh <clone> <outdir> <python>
set -u
C="$1"; O="$2"; PY="$3"; mkdir -p "$O"; cd "$C" || exit 2
run() { n="$1"; shift; "$@" > "$O/$n.log" 2>&1; rc=$?; printf '%s\trc=%s\t%s\n' "$n" "$rc" "$*" | tee -a "$O/summary_render.tsv"; }
: > "$O/summary_render.tsv"
run r_freeze "$PY" -m pip freeze
run r_gen_toc_check "$PY" -B scripts/gen_toc.py --check
run r_gen_toc_anchors "$PY" -B scripts/gen_toc.py --verify-anchors
run r_gen_toc_selftest "$PY" -B scripts/gen_toc.py --selftest
run r_em_dash_vs_train "$PY" -B scripts/check_em_dash.py --base 1304205cfc9fa4c9e69a32130fb366895c5f883b
run r_em_dash_vs_prbase "$PY" -B scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04
run r_em_dash_selftest "$PY" -B scripts/check_em_dash.py --selftest
run r_docs_check "$PY" -B scripts/docs_check.py
