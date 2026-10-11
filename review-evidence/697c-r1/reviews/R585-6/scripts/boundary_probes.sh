#!/bin/bash
# boundary_probes.sh : reviewer plants judged by ctrl_boundary.py against the reviewer's capture of the
# firmware steps (--without verilator, no --selftest). Each plant is applied in the clone, judged, and
# removed; the tracked tree is verified clean after each. Each judgement's log: receipts/probe_<Qn>.log.
P=$REVIEWS/697c-r585-6-packet; . $P/scripts/env.sh; R=$REVIEWS/r585-6-697c; cd $R
judge(){ local label=$1 tag=${1%% *}; local s=$(date +%s)
  python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture $P/scratch/capture \
    --without verilator > $P/receipts/probe_$tag.log 2>&1; local rc=$?
  echo "== $label: rc=$rc ($(( $(date +%s)-s )) s)"
  grep -v -E '^\s+[0-9]+ \||^\s+\||LEFT OUT|^\[ok\]|^\s+\^|^In file|warning:|^\s*$' $P/receipts/probe_$tag.log \
    | tail -n 3 | cut -c1-360; }
restore(){ git checkout -q -- sw/firmware; "$@"
  if [ -z "$(git status --porcelain --untracked-files=all -- sw/firmware)" ]; then echo "   restored: clean"
  else echo "   NOT CLEAN"; git status --short; exit 1; fi; }
# Q1 control: nothing planted
judge "Q1 nothing planted (control)"
# Q2 a firmware source reaches a stack non-public header through a symbolic link with another name in its tree
ln -s ../../../../third_party/tsn-c-stack/examples/rv32/include/string.h sw/firmware/ctrl/adp/port_string.h
sed -i '0,/^#include/s||#include "port_string.h"\n#include|' sw/firmware/ctrl/adp/adp_mbx.c
judge "Q2 adp_mbx.c includes a firmware-tree symlink to the stack's examples/rv32/include/string.h"
restore rm -f sw/firmware/ctrl/adp/port_string.h
# Q3 a firmware source reaches a stack non-public header through include/../examples
sed -i '0,/#include "wire.h"/s||#include "wire.h"\n#include "../../../../third_party/tsn-c-stack/include/../examples/rv32/include/string.h"|' \
  sw/firmware/ctrl/srp/srp_mbx.c
judge "Q3 srp_mbx.c includes the stack's include/../examples/rv32/include/string.h"
restore true
# Q4 a platform header named like a C library header shadows it for the stack's sources (firmware -I first)
printf '#pragma once\n#ifndef __cplusplus\n#define bool _Bool\n#define true 1\n#define false 0\n#define __bool_true_false_are_defined 1\n#include "ctrl_debug.h"\n#endif\n' > sw/firmware/ctrl/port/stdbool.h
judge "Q4 sw/firmware/ctrl/port/stdbool.h (including ctrl_debug.h) shadows the C library's for the stack"
restore rm -f sw/firmware/ctrl/port/stdbool.h
# Q5 the saved-state store (sw/firmware/ctrl_nvm, outside sw/firmware/ctrl) reaches a stack non-public header
sed -i '0,/^#include/s||#include "../../../third_party/tsn-c-stack/examples/rv32/include/string.h"\n#include|' sw/firmware/ctrl_nvm/nvm_store.c
judge "Q5 sw/firmware/ctrl_nvm/nvm_store.c includes the stack's examples/rv32/include/string.h"
restore true
judge "Q6 nothing planted after the probes (control)"
