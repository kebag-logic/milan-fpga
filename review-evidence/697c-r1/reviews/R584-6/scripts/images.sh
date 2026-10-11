#!/bin/bash
# Link every image fixture at one checkout with that checkout's own fixture code.
# Usage: images.sh <packet-root> <checkout> <label>   (outputs under scratch/img/<label>, hashes in logs/img.<label>.tsv)
set -u; P=$1; T=$2; N=$3; cd "$T"; source $P/scripts/env.sh
O=$P/scratch/img/$N; mkdir -p $O; H=$P/logs/img.$N.tsv; : > $H
RT=$P/scratch/rt2
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  python3 sw/firmware/ctrl/test/ctrl_image.py --shape $s --out $O/ctrl_image > $O/ctrl_image.$s.log 2>&1; rc=$?
  e=$O/ctrl_image/$s/ctrl_app.elf; [ -f $e ] || e=$(find $O/ctrl_image -path "*$s*" -name ctrl_app.elf | head -1)
  printf 'ctrl_image\t%s\t-\t-\trc=%s\t%s\n' $s $rc "$( [ -n "$e" ] && [ -f "$e" ] && sha256sum < $e | cut -c1-64 || echo none)" >> $H
done
for c in configs/*.yaml; do b=$(basename $c .yaml); for i in 1 2; do for v in plain without-srp with-aecp; do
  fl=""; [ $v = plain ] || fl="--$v"; d=$O/srp/$b/if$i/$v; mkdir -p $d
  python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config $c --interfaces $i $fl --output $d --libc $RT/libc.a --compiler-runtime $RT/libcompiler_rt.a > $d.log 2>&1; rc=$?
  printf 'ctrl_srp_image\t%s\tif%s\t%s\trc=%s\t%s\n' $b $i $v $rc "$( [ -f $d/ctrl_app.elf ] && sha256sum < $d/ctrl_app.elf | cut -c1-64 || echo none)" >> $H
done; done; done
echo done > $P/logs/img.$N.done
