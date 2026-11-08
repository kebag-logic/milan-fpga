#!/bin/bash
# Export the round 2 sync head and the round 3 head at paths of equal length and build each with baremetal.py.
S=$VALIDATION_STORAGE/tsn26-a750d
. $S/env.sh
for n in xa:968a164 xb:b7a5988; do
  IFS=: read a c <<< "$n"
  rm -rf $S/$a $S/rv32-$a; mkdir -p $S/$a
  git -C $LANES/tsn-c-stack-26-owed archive $c | tar -x -C $S/$a
  ( cd $S/$a && python3 scripts/baremetal.py --work $S/rv32-$a --jobs 4 > $S/rv32-$a.log 2>&1; echo $? > $S/rv32-$a.rc )
done
echo done > $S/imgx.done
