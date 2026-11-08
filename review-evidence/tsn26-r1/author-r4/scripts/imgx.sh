#!/bin/sh
# usage: imgx.sh   (bare-metal images of b7a5988 (xa) and the final head (xb), exported to paths of equal length)
S=<scratch>
. $S/env.sh
for t in xa xb; do (cd $S/$t && python3 scripts/baremetal.py --work $S/$t-rv32 --jobs 4 > $S/$t-rv32.log 2>&1; echo $? > $S/$t-rv32.rc); done
echo done > $S/imgx.done
