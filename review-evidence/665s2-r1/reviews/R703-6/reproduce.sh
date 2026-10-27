#!/bin/sh
# Reproduce this review's own probes. $1 = a clean checkout at e0e1b4649ea3af908a8f32eccaad7903fa2cc134,
# $2 = this packet directory, $3 = a sparse checkout of review-evidence/665s2-r1 at bfc68ced (optional).
set -eu
R=$1; P=$2
python3 -I "$P/probe_held.py" "$R"                               # entries load-bearing; drop-all == hosted refusal
(cd "$R" && python3 -B tb/verilator/ctrl_service_budget/run.py --self-test)
(cd "$R" && python3 scripts/check_baremetal_only.py --check)
(cd "$R" && git diff --check f58d049beb377c3f535628067022d4d5b51e8208 HEAD)
[ $# -ge 3 ] && python3 -I "$P/check_manifest.py" "$3" author-r6/
# Full boundary gate exactly as rtl-fast.yml (runs longer than one 10-minute foreground call here):
#   (cd "$R" && python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator)
