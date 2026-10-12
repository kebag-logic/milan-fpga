#!/bin/bash
# R585-6's boundary_probes2.sh (Q7, Q8, Q9), its plants and gate command unchanged, against a capture of the
# firmware steps made in the same checkout, inside the CI-parity image (round 7).
# usage: probe7_q.sh <checkout> <capture> <log directory>
set -u; cd "$1"; CAP=$2; L=$3; mkdir -p "$L"
judge(){ local label=$1 tag=${1%% *}; local s=$SECONDS
  python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture "$CAP" \
    --without verilator > "$L/probe_$tag.log" 2>&1; local rc=$?
  echo "== $label: rc=$rc ($((SECONDS - s)) s)"
  grep -E '^\s+\[FAIL\]|^ctrl_boundary|REFUSED' "$L/probe_$tag.log" | tail -n 4 | cut -c1-360; }
restore(){ "$@"
  if [ -z "$(git status --porcelain --untracked-files=all -- sw/firmware/ctrl_nvm)" ]; then echo "   restored: clean"
  else echo "   NOT CLEAN"; git status --short; exit 1; fi; }
SHADOW='#pragma once\n#ifndef __cplusplus\n#define bool _Bool\n#define true 1\n#define false 0\n#define __bool_true_false_are_defined 1\n#endif\n'
printf "$SHADOW" > sw/firmware/ctrl_nvm/plat/stdbool.h
judge "Q7 sw/firmware/ctrl_nvm/plat/stdbool.h shadows the C library's in the image build"
restore rm -f sw/firmware/ctrl_nvm/plat/stdbool.h
printf "$SHADOW" > sw/firmware/ctrl_nvm/stdbool.h
judge "Q8 sw/firmware/ctrl_nvm/stdbool.h shadows the C library's (comparison)"
restore rm -f sw/firmware/ctrl_nvm/stdbool.h
judge "Q9 nothing planted after the probes (control)"
