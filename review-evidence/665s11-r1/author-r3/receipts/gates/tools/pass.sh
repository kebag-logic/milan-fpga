#!/bin/bash
# pass.sh <head>: the final gate pass on fresh clean clones of <head>, in phases so the session unit stays under
# 10 GB: each phase's drivers and lane groups run concurrently, the next phase starts when they have all ended
set -u
H=$1; S=<scratch>; T=$S/gates/tools; R=$S/gates/pass1
mkdir -p $R/phase
phase() {  # phase <name> <cmd>... : each cmd in the background, then wait for all of them
  name=$1; shift; echo "$(date +%T) phase $name start" >> $R/phase/log
  pids=()
  for c in "$@"; do bash -c "$c" > $R/phase/$name.$(echo "$c" | md5sum | cut -c1-6).out 2>&1 & pids+=($!); done
  for p in "${pids[@]}"; do wait $p; done
  echo "$(date +%T) phase $name end" >> $R/phase/log
}
phase 1 "$T/drive.sh $H $R B rtl-fast:changes rtl-fast:verilator-lint rtl-fast:bdd-conformance rtl-fast:yosys-tool rtl-fast:yosys-elaboration rtl-fast:split-cdc rtl-fast:rtl-fast" \
        "$T/drive.sh $H $R D docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check" \
        "$T/lane_gates.sh $H $R fw"
phase 2 "$T/drive.sh $H $R A rtl-fast:firmware-boundary rtl-fast:firmware-unit rtl-fast:firmware-control-mutants rtl-fast:firmware-aecp-mutants rtl-fast:firmware-srp-mutants rtl-fast:firmware-verilator" \
        "$T/lane_gates.sh $H $R cpu"
phase 3 "$T/drive.sh $H $R C elaborate:elaborate-gates-1 elaborate:elaborate-gates-0 elaborate:elaborate rtl:full-ci-gate rtl:yosys-shards:0/4 rtl:yosys-shards:1/4 rtl:yosys-shards:2/4 rtl:yosys-shards:3/4 rtl:yosys-portability" \
        "$T/lane_gates.sh $H $R nvm"
phase 4 "$T/drive.sh $H $R E rtl-fast:publication-census" \
        "$T/lane_gates.sh $H $R s2" \
        "$T/lane_gates.sh $H $R build"
echo "PASS DONE $(date +%T)" >> $R/phase/log
