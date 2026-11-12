#!/bin/bash
# pass_all.sh <head>: the final gate pass on fresh clean clones of <head>: every workflow driver and lane group at
# once, except the census, S2, the builder and the saved-state self-test, which start once elaborate-gates-1's
# LiteX simulations have finished (as round 1 staged them); the session unit stayed under 7 GB this way at 10b0fe93
set -u
H=$1; S=<scratch>; T=$S/gates/tools; R=$S/gates/pass1
mkdir -p $R/phase; echo "$(date +%T) start $H" >> $R/phase/log
pids=()
go() { name=$1; shift; "$@" > $R/phase/$name.out 2>&1 & pids+=($!); }
go B $T/drive.sh $H $R B rtl-fast:changes rtl-fast:verilator-lint rtl-fast:bdd-conformance rtl-fast:yosys-tool rtl-fast:yosys-elaboration rtl-fast:split-cdc rtl-fast:rtl-fast
go D $T/drive.sh $H $R D docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check
go fw $T/lane_gates.sh $H $R fw
go A $T/drive.sh $H $R A rtl-fast:firmware-boundary rtl-fast:firmware-unit rtl-fast:firmware-control-mutants rtl-fast:firmware-aecp-mutants rtl-fast:firmware-srp-mutants rtl-fast:firmware-verilator
go cpu $T/lane_gates.sh $H $R cpu
go C $T/drive.sh $H $R C elaborate:elaborate-gates-1 elaborate:elaborate-gates-0 elaborate:elaborate rtl:full-ci-gate rtl:yosys-shards:0/4 rtl:yosys-shards:1/4 rtl:yosys-shards:2/4 rtl:yosys-shards:3/4 rtl:yosys-portability
until [ -e $R/logs/elaborate.elaborate-gates-1__DONE ]; do sleep 30; done
echo "$(date +%T) elaborate-gates-1 done; census, s2, build, nvm start" >> $R/phase/log
go E $T/drive.sh $H $R E rtl-fast:publication-census
go s2 $T/lane_gates.sh $H $R s2
go build $T/lane_gates.sh $H $R build
go nvm $T/lane_gates.sh $H $R nvm
for p in "${pids[@]}"; do wait $p; done
echo "ALL DONE $(date +%T)" >> $R/phase/log
