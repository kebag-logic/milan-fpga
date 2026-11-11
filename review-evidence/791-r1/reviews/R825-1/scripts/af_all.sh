#!/bin/bash
# af_all.sh: every shipped config's all-fabric export at base and at head, five at a time.
P=${P:-$REVIEWS/791-r825-1-packet}; . $P/scripts/env.sh
for side in base head; do for c in endstation_arty_4x4 endstation_arty_8ch endstation_arty_current endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  $PY -B $P/scripts/af_side.py $P/scratch/clone-$side $c $P/scratch/af/$side/$c > $P/scratch/af/$side-$c.out 2>&1 &
done; wait; done
echo done
