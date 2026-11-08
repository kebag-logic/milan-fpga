#!/bin/sh
S=$VALIDATION_STORAGE/tsn26-a750d
. $S/env.sh
$S/scripts/rv32_plants.sh $S/xt-final $S/rv32pf $S/rv32-plant-exit-codes.txt owed-timer-probe-not-held owed-hold-skips-delay owed-hold-skips-retry owed-held-probe-lost owed-bind-wait-unset owed-bind-wait-kept owed-hold-uncounted owed-hold-rearmed-late owed-held-flag-kept
echo done > $S/rv32pf.done
