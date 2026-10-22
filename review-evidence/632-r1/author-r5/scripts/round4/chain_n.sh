#!/usr/bin/env bash
# After the sweep, at 2389506a: (1) milan_dp's legs one by one at the processor pin
# (all but notify through the pool, then notify alone), in the sweep's clean clone;
# (2) the notify leg and its planted control with the processor head's E_SINFO
# spliced into a scratch clone's submodule (the round 3b method).
set -u
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final/notify
mkdir -p $L
S=$VALIDATION_STORAGE/scratch/632-a659/r4/clone-sweep-2389506
cd $S/tb/verilator/milan_dp
git -C $S rev-parse HEAD > $L/legs.head
date -Is > $L/legs.start
make run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk" > $L/legs.log 2>&1; echo $? > $L/legs.rc
make run-notify > $L/notify_pin.log 2>&1; echo $? > $L/notify_pin.rc
date -Is > $L/legs.end
C=$VALIDATION_STORAGE/scratch/632-a659/r4/clone-notify-2389506
bash $MANAGEMENT/2026-09-23/632-a659/scripts/round4/make_clone.sh $C 2389506ac > $L/clone.txt 2>&1
P=$C/protocol-processor
test "$(git -C $P rev-parse --show-toplevel)" = "$P" || { echo "submodule toplevel mismatch" > $L/abort.txt; exit 1; }
git -C $P remote get-url origin > $L/submodule_origin.txt
git -C $P rev-parse HEAD > $L/submodule_pin.txt
python3 $MANAGEMENT/2026-09-23/632-a659/scripts/round3b/splice_sinfo.py \
  $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-final/hdl/aecp/ucode/gen_ucode.py $P/hdl/aecp/ucode/gen_ucode.py $L/gen_ucode.spliced.py > $L/splice.txt 2>&1
cp $L/gen_ucode.spliced.py $P/hdl/aecp/ucode/gen_ucode.py
git -C $P diff > $L/submodule_applied.diff
cd $C/tb/verilator/milan_dp
make notify > $L/notify_fix.log 2>&1; echo $? > $L/notify_fix.rc
sha256sum ucode.hex | cut -d' ' -f1 > $L/ucode_fix.sha256
python3 gsi_mutants.py 9 > $L/gsi9.log 2>&1; echo $? > $L/gsi9.rc
echo DONE > $L/DONE
