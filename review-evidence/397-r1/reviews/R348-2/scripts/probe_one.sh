#!/bin/bash
# One round-1 probe run (same invocation as round1/probe_runs.sh), foreground.
# usage: probe_one.sh <scratch> <name> <build> <commands> <erase_us> <program_us> <probe-shape>
set -u
S=$1; n=$2; b=$3; c=$4; e=$5; p=$6; k=$7
cd $b/gateware && PROBE_LOG=$S/runs/$n.probe /usr/bin/time -f 'wall %e s' $S/probe-$k/native/Vsim \
  $b/aem_desc.bin $b/slots.bin $c $e $p > $S/runs/$n.log 2> $S/runs/$n.err
echo "$n rc=$?" >> $S/runs/status.txt
