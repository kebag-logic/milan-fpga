#!/usr/bin/env bash
# Focused suites + scoped lint + docs gates, on the archived head copy made by guard_probes.sh.
# Usage: focused_suites.sh <packet-dir> <verilator>
set -u
PKT=$1; VER=$2; S=$PKT/scratch/src; R=$PKT/receipts
export PATH=$(dirname "$VER"):$PATH
( make -C "$S/tb/desc_store" VERILATOR="$VER" > "$R/suite-desc_store.log" 2>&1; echo "desc_store make rc=$?" ) | tee "$R/suite-desc_store.rc"
( make -C "$S/tb/pp_top" VERILATOR="$VER" -j4 > "$R/suite-pp_top.log" 2>&1; echo "pp_top make rc=$?" ) | tee "$R/suite-pp_top.rc"
( "$VER" --lint-only -Wall "$S/hdl/aecp/KL_aecp_desc_mem_guard.sv" --top-module KL_aecp_desc_mem_guard > "$R/lint-guard.log" 2>&1; echo "guard lint -Wall rc=$?" ) | tee "$R/lint-guard.rc"
# docs gates need a git repo for 'stale'; run the non-git ones on the copy
( cd "$S" && python3 scripts/check-links.py > "$R/docs-links.log" 2>&1; echo "links rc=$?" ) | tee "$R/docs-gates.rc"
( cd "$S" && python3 scripts/gen_matrix.py --check > "$R/docs-modmatrix.log" 2>&1; echo "modmatrix rc=$?" ) | tee -a "$R/docs-gates.rc"
( cd "$S" && python3 scripts/check-matrix.py > "$R/docs-reqmatrix.log" 2>&1; echo "reqmatrix rc=$?" ) | tee -a "$R/docs-gates.rc"
grep -hE '[0-9]+ checks: [0-9]+ PASS' "$R"/suite-*.log | tail -5
