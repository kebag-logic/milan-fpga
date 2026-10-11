#!/bin/bash
# images.sh TREE OUT : link every shipped RV32 image of TREE (5 shapes x ctrl_image.py, and 5 shapes x 1|2
# interfaces x without-srp|srp|with-aecp ctrl_srp_image.py) with the reviewer runtime, then list ELF sha256.
P=$REVIEWS/697c-r585-6-packet; . $P/scripts/env.sh
TREE=$1; OUT=$2; RT=$P/scratch/runtime; mkdir -p $OUT
cd $TREE
jobs=()
for c in configs/*.yaml; do s=$(basename $c .yaml)
  jobs+=("python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape $s --out $OUT/img-$s")
  for i in 1 2; do for m in --without-srp srp --with-aecp; do
    a=$m; [ $m = srp ] && a=""
    jobs+=("python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config $c --interfaces $i --output $OUT/srp-$s-if$i$m --libc $RT/libc.a --compiler-runtime $RT/libcompiler_rt.a $a")
  done; done
done
printf '%s\n' "${jobs[@]}" | xargs -P 6 -I{} bash -c '{} > /dev/null 2>"$0/err.$$.$RANDOM" || echo "FAIL: {}"' $OUT
cd $OUT && find . -name '*.elf' | sort | xargs sha256sum
