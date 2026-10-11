#!/usr/bin/env bash
# vivado_chain.sh: every remaining Vivado run of the lane, one at a time, each run under
# the exclusive lock (never shared). Order: the bench's campaign through xelab and
# synth_design -rtl at the lane head (its control is the head's full Vivado legs), the
# base tree graded by the head's bench, then the OOC netlists, base and head.
set -u
S=<scratch>
L=<lane>
export PYTHONDONTWRITEBYTECODE=1
log() { echo "$(date +%T) $*" >> $S/rec/vivado_chain.out; }

log "start mutants (head $(git -C $L rev-parse HEAD))"
$S/scripts/vivado_mutants.sh
log "mutants rc=$(cat $S/rec/head_vivado_mutants.rc) secs=$(cat $S/rec/head_vivado_mutants.secs)"

log "start base legs"
BENCH=$L/tb/elab_guards/guards.py $S/scripts/vivado_legs2.sh $S/pristine $S/rec/base_vivado
log "base legs rc=$(cat $S/rec/base_vivado.rc) secs=$(cat $S/rec/base_vivado.secs)"

log "start ooc"
$S/scripts/run_ooc2.sh >> $S/rec/vivado_chain.out 2>&1
log "chain done"
