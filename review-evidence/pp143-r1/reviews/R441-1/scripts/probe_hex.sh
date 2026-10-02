#!/bin/bash
# P1: a probe copy whose tb/ucpu and tb/pp_top carry poisoned ROM images newer
# than their generators. A direct `make run` in tb/ucpu must fail on the poison
# (so the poison is live); the campaign, whose copies skip *.hex, must still
# pass its control and kill its arm at the README count.
set -u
T=$1
cd "$T/tb/ucpu" && make run > "$T/../probe-hex-direct.log" 2>&1; echo "direct make run in poisoned tb/ucpu: rc=$?"
cd "$T" && python3 tb/pp_top/aecp_mutants.py --output "$T/../out-probe-hex" --only ucpu-preempt-repeats,dl-preempt-after-effect --jobs 2; echo "campaign rc=$?"
