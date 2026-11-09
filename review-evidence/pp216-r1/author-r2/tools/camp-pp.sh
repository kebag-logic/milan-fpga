#!/usr/bin/env bash
# camp-pp.sh <runs> <clone>: the two AECP mutation campaigns CI runs on tb/pp_top (make -C tb/pp_top aecp-mutants,
# aecp-dispatch-mutants), whose controls run the processor top this change touches; outputs under <runs>
R=$1; C=$2
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/camp-pp"
export TMPDIR=$S/tmp/camp-pp MAKEFLAGS=-j8
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" camp-aecp make -C tb/pp_top aecp-mutants MUTANT_OUTPUT="$R/camp-aecp-out"
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" camp-aecp-dispatch make -C tb/pp_top aecp-dispatch-mutants AECP_DISPATCH_MUTANT_OUTPUT="$R/camp-aecp-dispatch-out"
