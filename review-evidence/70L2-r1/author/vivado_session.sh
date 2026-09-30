#!/bin/bash
# One Vivado session under flock /tmp/milan-vivado.lock, for #70 lane 2:
#   1. out-of-context synthesis of KL_pp_shadow at the shipping 1x1 arrays
#      (syn/ooc/pp_shadow_ooc.tcl, PP_N_IN/PP_N_OUT from the generated shape),
#   2. the 3-seed AX7101 1x1 TDM8 place sweep (sw/litex/sweep.sh ax7101 TAG,
#      32 threads per seed, three seeds),
# then waits until every build process has exited. The lock fd is inherited by
# the detached builds, so the lock is held until the last one ends.
# Usage: vivado_session.sh <repo> <tag> <ooc-dir> <n_in> <n_out> <logdir>
set -u
REPO=$1 TAG=$2 OOC=$3 NIN=$4 NOUT=$5 LOGS=$6
mkdir -p "$LOGS"
exec 9>/tmp/milan-vivado.lock
echo "waiting for the lock $(date -Is)" > "$LOGS/session.log"
flock 9
echo "lock held $(date -Is) head $(git -C "$REPO" rev-parse HEAD)" >> "$LOGS/session.log"
set +u; source "$HOME/Xilinx/2026.1/Vivado/settings64.sh"; set -u
export PATH="$HOME/.local/bin:$PATH"
rm -rf "$OOC"; mkdir -p "$OOC"; cd "$OOC" || exit 97
python3 "$REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex > gen.log 2>&1
python3 "$REPO/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o ucode.hex >> gen.log 2>&1
start=$(date +%s)
PP_N_IN=$NIN PP_N_OUT=$NOUT vivado -mode batch -nojournal -log ooc.log -source "$REPO/syn/ooc/pp_shadow_ooc.tcl" > ooc.out 2>&1
echo "ooc rc=$? seconds=$(( $(date +%s) - start )) $(date -Is)" >> "$LOGS/session.log"
cd "$REPO" || exit 97
"$REPO/sw/litex/sweep.sh" ax7101 "$TAG" > "$LOGS/sweep-launch.log" 2>&1
echo "sweep launch rc=$? $(date -Is)" >> "$LOGS/session.log"
sleep 60
while pgrep -f "build_ax7101_(asl|eto|eppo)_${TAG}" > /dev/null; do sleep 60; done
echo "all builds exited $(date -Is)" >> "$LOGS/session.log"
