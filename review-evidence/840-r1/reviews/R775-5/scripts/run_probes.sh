#!/bin/sh
# usage: run_probes.sh <packet dir>
# Builds and runs the reviewer's fault probes; one log and rc per probe.
P=$1; T=$P/scratch/tree; M=$P/scratch/faults; L=$P/receipts/probes
PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH; export PATH
export VERILATOR_JOBS=2
one() { # name dir mdir extra-make-args...
  n=$1; d=$2; m=$3; shift 3
  ( cd "$d" && make -s bootsa-build BOOTSA_MDIR="$m" "$@" > "$L/$n.build.log" 2>&1; b=$?
    if [ $b -eq 0 ]; then ./"$m"/Vmilan_dp_bootsa > "$L/$n.log" 2>&1; echo $? > "$L/$n.rc"; else echo "build-failed:$b" > "$L/$n.rc"; fi ) &
}
A=$T/pA/tb/verilator/milan_dp; B=$T/pB/tb/verilator/milan_dp; D=$T/pD/tb/verilator/milan_dp
(cd $A && make -s ci-prepare > $L/pA.prepare.log 2>&1)
(cd $B && make -s ci-prepare > $L/pB.prepare.log 2>&1)
(cd $D && make -s ci-prepare > $L/pD.prepare.log 2>&1)
one flapbuild $A obj_bootsa
one fw_no_hi $A obj_f1 BOOTSA_FW=$M/fw_no_hi.c
one fw_hi_first $A obj_f2 BOOTSA_FW=$M/fw_hi_first.c
one dp_reversed $A obj_f4 DP_SRC=$M/dp_reversed.sv
one stale_gptp_rom $B obj_bootsa
( cd $D && make -s build-gptp > $L/gptp_no_pair.build.log 2>&1; b=$?
  if [ $b -eq 0 ]; then ./obj_gptp/Vmilan_dp_gptp > $L/gptp_no_pair.log 2>&1; echo $? > $L/gptp_no_pair.rc; else echo "build-failed:$b" > $L/gptp_no_pair.rc; fi ) &
wait
echo done > $L/ALL.done
