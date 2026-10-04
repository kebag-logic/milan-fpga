#!/bin/sh
# Start the round-2 runs concurrently, each detached with its own log and rc file.
# usage: launch.sh PACKET CLONE VERILATOR
P=$1 C=$2 V=$3
S=$P/scratch R=$P/receipts
export VERILATOR="$V" TMPDIR="$S/tmp"
bg() { name=$1; shift; ( "$@" >"$R/$name.log" 2>&1; echo $? >"$R/$name.rc" ) </dev/null & }
# head suite in a copy of its own
bg suites/head-adp_engine make -C "$S/suite-head/tb/adp_engine" run
# the full campaign through make, exercising JOBS=N
bg campaign-make-j8/campaign make -C "$S/head-tree/tb/adp_engine" mutants JOBS=8 \
   MUTANT_OUTPUT="$R/campaign-make-j8"
# round-1 probes, unchanged, against the clone (read-only: copies only)
bg probes-r1/run python3 "$P/scripts/probes.py" --root "$C" --scratch "$S/probes-r1" \
   --out "$R/probes-r1" --jobs 4
# round-2 probes
bg probes-r2/run python3 "$P/scripts/probes2.py" --root "$C" --scratch "$S/probes-r2" \
   --out "$R/probes-r2" --jobs 2
wait
