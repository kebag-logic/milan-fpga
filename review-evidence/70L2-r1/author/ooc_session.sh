#!/bin/bash
# Out-of-context synthesis of KL_pp_shadow at the shipping 1x1 arrays, under
# flock /tmp/milan-vivado.lock: the first step of vivado_session.sh, alone
# (the sweep runs after it through sweep_serial.sh, one seed at a time).
# Usage: ooc_session.sh <repo> <ooc-dir> <n_in> <n_out> <logdir>
set -u
REPO=$1 OOC=$2 NIN=$3 NOUT=$4 LOGS=$5
mkdir -p "$LOGS"
exec 9>/tmp/milan-vivado.lock
echo "waiting for the lock $(date -Is)" >> "$LOGS/ooc-session.log"
flock 9
echo "lock held $(date -Is) head $(git -C "$REPO" rev-parse HEAD) dirty=$(git -C "$REPO" status --porcelain --untracked-files=no | wc -l)" >> "$LOGS/ooc-session.log"
set +u; source "$HOME/Xilinx/2026.1/Vivado/settings64.sh"; set -u
rm -rf "$OOC"; mkdir -p "$OOC"; cd "$OOC" || exit 97
python3 "$REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex > gen.log 2>&1
python3 "$REPO/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o ucode.hex >> gen.log 2>&1
start=$(date +%s)
PP_N_IN=$NIN PP_N_OUT=$NOUT vivado -mode batch -nojournal -log ooc.log -source "$REPO/syn/ooc/pp_shadow_ooc.tcl" > ooc.out 2>&1
rc=$?
echo "ooc rc=$rc seconds=$(( $(date +%s) - start )) $(date -Is)" >> "$LOGS/ooc-session.log"
exit $rc
