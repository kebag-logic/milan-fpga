#!/usr/bin/env bash
# Usage: run_gates.sh <repo> <python-with-locked-markdown-renderer> <receipt-dir> <em-dash-base>
# Runs the round-3 documentation gates and the baseline helper self-test at the
# repository's checked-out head; one raw log and one rc line per gate.
set -u
repo=$1; py=$2; out=$3; base=$4
mkdir -p "$out"; : > "$out/gate_rc.tsv"
run() { name=$1; shift
  ( cd "$repo" && "$@" ) > "$out/$name.log" 2>&1; rc=$?
  printf '%s\t%s\t%s\n' "$name" "$rc" "$*" >> "$out/gate_rc.tsv"; }
run head            git rev-parse HEAD HEAD^{tree}
run gen_toc_selftest "$py" scripts/gen_toc.py --selftest
run gen_toc_anchors "$py" scripts/gen_toc.py --verify-anchors
run gen_toc_check   "$py" scripts/gen_toc.py --check
run docs_check      "$py" scripts/docs_check.py
run doc_style       "$py" scripts/check_doc_style.py
run doc_style_selftest "$py" scripts/check_doc_style.py --selftest
run em_dash         "$py" scripts/check_em_dash.py --base "$base"
run pp_baseline_selftest "$py" syn/ooc/pp_baseline.py --selftest
run diff_check      git diff --check e21c1ca024d37ea188ad15b5c8f9c2dae18628df HEAD
run status          git status --porcelain=v1 --untracked-files=all
cat "$out/gate_rc.tsv"
