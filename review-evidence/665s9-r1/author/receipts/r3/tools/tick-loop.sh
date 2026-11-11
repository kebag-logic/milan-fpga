#!/usr/bin/env bash
# tick-loop.sh <head> <max-units>: launch ready replay instances as their own units (ci_replay.py tick, CPU ranges from
# cpu_ranges.py pick), every 90 s, until every instance has a result
S=<scratch>
until python3 $S/tools/replay/ci_replay.py tick "$1" "$2"; do sleep 90; done
echo "$(date +%T) tick-loop: every instance has a result"
