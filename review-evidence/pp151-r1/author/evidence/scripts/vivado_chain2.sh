#!/usr/bin/env bash
# vivado_chain2.sh: the lane's remaining Vivado runs in priority order, each run alone
# under the exclusive lock (never shared): the bench's campaign through xelab and
# synth_design -rtl at the lane head (its control is the head's full Vivado legs); the
# OOC netlists at the default shape, base and head; the base tree graded by the head's
# bench; the OOC netlists at 9x9. (The first chain's campaign waiter was terminated by
# an outside SIGTERM after 8,740 s in the lock queue, before it ever held the lock.)
set -u
S=<scratch>
L=<lane>
export PYTHONDONTWRITEBYTECODE=1
log() { echo "$(date +%T) $*" >> $S/rec/vivado_chain.out; }

log "start mutants (head $(git -C $L rev-parse HEAD))"
$S/scripts/vivado_mutants.sh
log "mutants rc=$(cat $S/rec/head_vivado_mutants.rc) secs=$(cat $S/rec/head_vivado_mutants.secs)"

log "start ooc default"
$S/scripts/run_ooc2.sh default >> $S/rec/vivado_chain.out 2>&1

log "start base legs"
BENCH=$L/tb/elab_guards/guards.py $S/scripts/vivado_legs2.sh $S/pristine $S/rec/base_vivado
log "base legs rc=$(cat $S/rec/base_vivado.rc) secs=$(cat $S/rec/base_vivado.secs)"

log "start ooc 9x9"
$S/scripts/run_ooc2.sh 9x9 >> $S/rec/vivado_chain.out 2>&1
log "chain done"
