#!/bin/bash
# The three cost controls whose fixtures the round's firmware does not change, side by side on the head image.
T=<scratch>
H=$(git -C $T/L-CTL-srp-compared-by-memcmp rev-parse HEAD)
bash $T/scripts/ctl2.sh $H polls-rebuild-in-the-base &
bash $T/scripts/ctl2.sh $H polls-rebuild-twice &
bash $T/scripts/ctl2.sh $H srp-compared-by-memcmp --variant answering-every-port &
wait
