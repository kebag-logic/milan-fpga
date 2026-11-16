#!/bin/bash
# mkseed.sh KIND TAG X: a clone of 10b2fe21 (KIND sync) or of it with the trial merge's patch (KIND trial), the 8x8
# config's MAC set to 02:4b:4c:XX:XX:XX with XXXXXX the 24-bit hex X (an experiment only; never committed).
set -eu
S=<scratch>; K=$1 T=$2 X=$3
D=$S/seeds/c-$K-$T
bash $S/bin/clone.sh 10b2fe21 $D >/dev/null
if [ "$K" = trial ]; then git -C $D apply --index $S/seeds/trial.patch; fi
m=$(printf '%06x' $((16#$X)))
mac="02:4b:4c:${m:0:2}:${m:2:2}:${m:4:2}"
sed -i "s|^  mac_address: \"02:4b:4c:4b:4c:01\"|  mac_address: \"$mac\"|" $D/configs/endstation_ax7101_8x8.yaml
grep -n 'mac_address' $D/configs/endstation_ax7101_8x8.yaml
echo "$K $T $mac dirty $(git -C $D status --porcelain --untracked-files=no | wc -l)"
