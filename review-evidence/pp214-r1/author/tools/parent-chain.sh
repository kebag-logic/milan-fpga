#!/usr/bin/env bash
# parent-chain.sh <runs> <parent> <jobs>: every consumer gate of the scratch parent, in order, then the chain's rc
# (0 only when every gate's rc is 0)
R=$1; P=$2; J=$3
T=$(cd "$(dirname "$0")" && pwd)
$T/parent-gates.sh $R $P $J idiom docs-ratchets changes lint bdd yosys fw-srp milan_dp pp_shadow census fw-unit fw-control fw-aecp fw-boundary fw-verilator
bad=0; for f in $R/*.rc; do [ "$(cat $f)" = 0 ] || { echo "$f rc=$(cat $f)"; bad=1; }; done
echo $bad > $R/../parent_chain.rc
