#!/bin/bash
# Run probe/test files against head export and each planted copy at IF=1/2.
# usage: r532_matrix.sh PACKET LWSRP JOBS ; writes receipts/plants/<root>-<test>-if<n>.{log,rc}
P=$1; LW=$2; J=$3; S=$P/scratch; mkdir -p $P/receipts/plants
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S/tmp
for root in head retry-removed retain-dropped overtake reset-keeps reset-any-interface refusal-malformed retry-ignores-order; do
  for t in $P/scripts/r533_5_independent.cpp $P/scripts/r532_retry_probes.cpp $S/root-$root/sw/firmware/ctrl/test/srp_rx_retry.cpp; do
    for n in 1 2; do echo "$root $t $n"; done; done; done |
xargs -P "$J" -L 1 bash -c 'root=$0 t=$1 n=$2; b=$(basename $t .cpp); o='"$S"'/plants/$root-$b-if$n;
  python3 -B '"$P"'/scripts/r532_probe.py '"$S"'/root-$root '"$LW"' $o $n $t > '"$P"'/receipts/plants/$root-$b-if$n.log 2>&1; echo $? > '"$P"'/receipts/plants/$root-$b-if$n.rc'
cd $P/receipts/plants && for f in *.rc; do printf '%s %s\n' "${f%.rc}" "$(cat $f)"; done
