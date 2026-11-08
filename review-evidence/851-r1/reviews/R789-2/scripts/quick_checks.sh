#!/usr/bin/env bash
# Run the fast parent checks that read this PR's records, one log and rc each.
# usage: quick_checks.sh <clone-at-head> <out-dir> <md-python>
set -u
C=$1; OUT=$2; MDPY=$3
BASE=0a75aa774b89ac89351700f63dd8cbb89694af6c
mkdir -p "$OUT"; cd "$C" || exit 2
run() { local n=$1; shift; "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"; }
git rev-parse HEAD > "$OUT/head.txt"
run submodule_docs   python3 scripts/check_submodule_docs.py
run diagram_check    python3 docs/diagrams/submodule_boundaries.gen.py --check
run check_baseline   python3 syn/ooc/pp_resource_gate.py check-baseline
run docs_inventory   python3 scripts/docs_inventory.py --check
run diff_check       git diff --check "$BASE" HEAD
run pp_srcs          python3 scripts/pp_srcs.py --check
run em_dash          "$MDPY" scripts/check_em_dash.py --base "$BASE"
run docs_check       "$MDPY" scripts/docs_check.py
run cpp_idiom        python3 scripts/check_cpp_idiom.py
run py_idiom         python3 scripts/check_py_idiom.py
run rom_record       ./syn/yosys/ooc.sh --record-rom-digests
run rom_diff         git diff --exit-code -- syn/yosys/rom_digests.tsv
git status --porcelain > "$OUT/tree-after.txt"
