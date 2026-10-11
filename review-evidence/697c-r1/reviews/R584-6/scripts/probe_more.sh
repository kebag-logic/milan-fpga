#!/bin/bash
# N1B: the N1 plant left in place, the measured image still builds (the escape is a green build).
# S1: stack side on a real bump path: a commit in the submodule whose src/maap.c includes the mailbox HAL and
#     whose src/acmp.c includes the saved-state store's port, staged as the gitlink; the boundary must refuse both.
# Every step restores the checkout (working tree, index, submodule HEAD) afterwards.
# Usage: probe_more.sh <packet-root> <checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
LINE='#include "../../../third_party/tsn-c-stack/examples/adp_port.h"'
sed -i "1a $LINE" sw/firmware/ctrl_nvm/nvm_store.c
python3 sw/firmware/ctrl/test/ctrl_image.py --shape endstation_ax7101_1x1_tdm8 --out $P/scratch/probe_img > $P/logs/probe.N1B.log 2>&1; echo $? > $P/logs/probe.N1B.rc
git checkout -q -- sw/firmware; git status --short
S=third_party/tsn-c-stack; PIN=$(git -C $S rev-parse HEAD)
sed -i '1a #include "mbx_hal.h"' $S/src/maap.c; sed -i '1a #include "nvm_state.h"' $S/src/acmp.c
git -C $S -c user.name=probe -c user.email=probe@invalid commit -q -am "probe S1" && git add $S
git ls-files --stage $S
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --only verilator > $P/logs/probe.S1.log 2>&1; echo $? > $P/logs/probe.S1.rc
git -C $S checkout -q $PIN; git reset -q -- $S; git ls-files --stage $S; git -C $S rev-parse HEAD; git status --short
echo done > $P/logs/probe.more.done
