#!/usr/bin/env bash
# camps.sh <runs> <head> <jobs>: the two SRP campaigns first, then every other processor campaign, one after another
R=$1; C=$2; J=$3
T=$(cd "$(dirname "$0")" && pwd)
$T/chain.sh $R $C 8 srp srp-admission
$T/chain.sh $R $C $J aecp-dispatch aecp maap adp aecp-cmds nvm-figures ctr name-wr gsi notify acmp d3 name-state elab-guards acmp-retry
