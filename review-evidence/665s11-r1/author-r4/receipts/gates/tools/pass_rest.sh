#!/bin/bash
# pass_rest.sh <head>: the pass's phases 2 to 4 started beside phase 1's last legs (the firmware self-test and the
# docs jobs): the firmware jobs, the CPU simulations and the elaborate and rtl jobs now; the census, S2, the builder
# and the saved-state self-test once elaborate-gates-1's LiteX simulations have finished, as round 1 staged them
set -u
H=$1; S=<scratch>; T=$S/gates/tools; R=$S/gates/pass1
echo "$(date +%T) rest start" >> $R/phase/log
pids=()
$T/drive.sh $H $R A rtl-fast:firmware-boundary rtl-fast:firmware-unit rtl-fast:firmware-control-mutants rtl-fast:firmware-aecp-mutants rtl-fast:firmware-srp-mutants rtl-fast:firmware-verilator > $R/phase/A.out 2>&1 & pids+=($!)
$T/lane_gates.sh $H $R cpu > $R/phase/cpu.out 2>&1 & pids+=($!)
$T/drive.sh $H $R C elaborate:elaborate-gates-1 elaborate:elaborate-gates-0 elaborate:elaborate rtl:full-ci-gate rtl:yosys-shards:0/4 rtl:yosys-shards:1/4 rtl:yosys-shards:2/4 rtl:yosys-shards:3/4 rtl:yosys-portability > $R/phase/C.out 2>&1 & pids+=($!)
until [ -e $R/logs/elaborate.elaborate-gates-1__DONE ]; do sleep 30; done
echo "$(date +%T) elaborate-gates-1 done; census, s2, build, nvm start" >> $R/phase/log
$T/drive.sh $H $R E rtl-fast:publication-census > $R/phase/E.out 2>&1 & pids+=($!)
$T/lane_gates.sh $H $R s2 > $R/phase/s2.out 2>&1 & pids+=($!)
$T/lane_gates.sh $H $R build > $R/phase/build.out 2>&1 & pids+=($!)
$T/lane_gates.sh $H $R nvm > $R/phase/nvm.out 2>&1 & pids+=($!)
for p in "${pids[@]}"; do wait $p; done
echo "REST DONE $(date +%T)" >> $R/phase/log
