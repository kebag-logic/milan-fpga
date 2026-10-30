#!/usr/bin/env bash
# #814: the remaining Vivado banks in order, after the cut-1 bank ends (one Vivado run at a time; route_bank.sh
# takes the exclusive lock around each run and starts it only above 20 GB MemAvailable).
#   route-8x8 at the final synthesis inputs first (whether the 8x8 fits decides a STOP), then cut 2's route-1x1,
#   then the final route-1x1 with the recipe's directive comparison and the two standalone endpoints.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/814-a703
until grep -q BANK-DONE "$S/viv-cut1/bank.out" 2>/dev/null; do sleep 30; done
bash "$here/route_bank.sh" final 139949e2c3 r8 paths
bash "$here/route_bank.sh" cut2 a166465bdd r1 paths
bash "$here/route_bank.sh" final 139949e2c3 r1 dir paths o1 o8
echo QUEUE-DONE
