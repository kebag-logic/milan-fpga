#!/usr/bin/env bash
# Round 2 head: the processor gates in the lane, then every campaign that builds a changed file
R=<data>/tmp/pp181-a635/r2; L=<data>/lanes/pp181-cut
$R/gates.sh $L head
$R/campaigns.sh $L head
echo HEAD-CHAIN-DONE > $R/chain-head.done
