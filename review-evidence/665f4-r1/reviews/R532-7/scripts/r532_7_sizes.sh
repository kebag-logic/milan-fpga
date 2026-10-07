#!/bin/bash
# R532-7 linked-size reproduction: 16 links (head, round 6, round 5 each with its own
# fixture and lwSRP pin; lane base via the head fixture --without-srp), same runtime.
# usage: r532_7_sizes.sh PACKET   (exports under PACKET/scratch/size, runtime in size/runtime)
P=$1; S=$P/scratch; Z=$S/size; mkdir -p $P/receipts/size
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S/tmp MILAN_RV32_CC=$S/sdk/bin/riscv32-buildroot-linux-gnu-gcc
R5=500b8f64443777685e6a54049d933476710d26f0; R6=cce554f64f6bdab1f6d26e5c4d7b46d54d228c52; B=db9aa8c9b135b34ff3d070a979dee70440b37cc6
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do for n in 1 2; do
  for t in head r6 r5 base; do echo "$t $shape $n"; done; done; done |
xargs -P 16 -L 1 bash -c 't=$0 shape=$1 n=$2; Z='"$Z"'; P='"$P"'
  case $t in head) root=$Z/head; extra=;; r6) root=$Z/'"$R6"'; extra=;; r5) root=$Z/'"$R5"'; extra=;;
    base) root=$Z/'"$R5"'; extra="--without-srp --ctrl-source $Z/'"$B"'/sw/firmware/ctrl";; esac
  o=$Z/out/$t-$shape-if$n; rm -rf $o
  python3 -B $root/sw/firmware/ctrl/test/ctrl_image.py --config $root/configs/$shape.yaml --interfaces $n --output $o \
    --libc $Z/runtime/libc.a --compiler-runtime $Z/runtime/libcompiler_rt.a $extra > $P/receipts/size/$t-$shape-if$n.log 2>&1
  echo $? > $P/receipts/size/$t-$shape-if$n.rc; [ -f $o/size.json ] && cp $o/size.json $P/receipts/size/$t-$shape-if$n.json'
cd $P/receipts/size && for f in *.rc; do echo "${f%.rc} $(cat $f)"; done
