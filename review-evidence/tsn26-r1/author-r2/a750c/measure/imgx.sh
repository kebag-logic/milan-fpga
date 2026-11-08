#!/bin/bash
S=$VALIDATION_STORAGE/tsn26-a750c
. $S/env.sh
for n in r2:9002bfe mn:d7e6a2a mg:13dd785; do
  IFS=: read a c <<< "$n"
  rm -rf $S/xt-$a $S/rv32x-$a; mkdir -p $S/xt-$a
  git -C $LANES/tsn-c-stack-26-owed archive $c | tar -x -C $S/xt-$a
  ( cd $S/xt-$a && python3 scripts/baremetal.py --work $S/rv32x-$a --jobs 6 > $S/rv32x-$a.log 2>&1; echo $? > $S/rv32x-$a.rc )
done
echo done > $S/imgx.done
