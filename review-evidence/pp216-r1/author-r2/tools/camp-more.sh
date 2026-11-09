#!/usr/bin/env bash
# camp-more.sh <runs> <clone>: the processor's other mutation campaigns: the three CI runs beside the SRP and AECP
# ones (make -C tb/maap mutants, tb/adp_engine mutants, tb/aecp_cmds mutants), and the elaboration-guard bench's own
# campaign (make -C tb/elab_guards mutants: five arms per guard, with Verilator and, sv2v and Yosys on PATH, Yosys),
# which this change adds a guard to
R=$1; C=$2
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/camp-more"
export TMPDIR=$S/tmp/camp-more MAKEFLAGS=-j8
P="$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$VL:$BASE"
g "$R" "$C" "$V" "$P" camp-maap make -C tb/maap mutants MUTANT_OUTPUT="$R/camp-maap-out"
g "$R" "$C" "$V" "$P" camp-adp make -C tb/adp_engine mutants MUTANT_OUTPUT="$R/camp-adp-out"
g "$R" "$C" "$V" "$P" camp-aecp-cmds make -C tb/aecp_cmds mutants MUTANT_OUTPUT="$R/camp-aecp-cmds-out"
g "$R" "$C" "$V" "$P" camp-elab-guards make -C tb/elab_guards mutants MUTANT_OUTPUT="$R/camp-elab-guards-out" JOBS=6
