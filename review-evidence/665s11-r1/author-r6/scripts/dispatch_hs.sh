#!/bin/bash
# Launch the harness self-test unit once an 8-wide range is free; books nothing while waiting.
until P=$(python3 -I <management>/2026-09-23/cpu_ranges.py pick) && [ -n "$P" ]; do sleep 60; done
bash <scratch>/r6/scripts/unit.sh HS $P bash <scratch>/r6/scripts/lane_gates_r6.sh 33b0d03a4ac899ed1601cd2cd97efbf66e293c9e harness
echo "$(date +%T) HS on $P"
