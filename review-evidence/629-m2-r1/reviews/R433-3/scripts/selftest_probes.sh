#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R433-3: the entity-shape self-test with its full log kept (the round-3 arm
# names must appear), and one fault probe on the round-3 frozen-form match.
# Usage: selftest_probes.sh <copy A of the head> <copy B of the head> <make 4.3 dir> <log dir>
set -u
A=$(cd "$1" && pwd); B=$(cd "$2" && pwd); M43=$(cd "$3" && pwd); L=$(cd "$4" && pwd)
# 1. the unmodified self-test, both makes, full logs
(cd "$A" && PATH="$M43:$PATH" python3 scripts/check_entity_shape.py --self-test > "$L/selftest_make43.full.log" 2>&1; echo $? > "$L/selftest_make43.rc") &
(cd "$A" && python3 scripts/check_entity_shape.py --self-test > "$L/selftest_host.full.log" 2>&1; echo $? > "$L/selftest_host.rc") &
# 2. fault: the frozen-form match disabled at its use site (the round-2 gate)
INV="$B/scripts/shape_consumer_inventory.py"
n=$(grep -c '        if target in classified:' "$INV")
echo "anchor count: $n" > "$L/fault_no_frozen_match.anchor"
sed -i 's/^        if target in classified:$/        if False and target in classified:/' "$INV"
(cd "$B" && PATH="$M43:$PATH" python3 scripts/check_entity_shape.py > "$L/fault_no_frozen_match_plain_make43.log" 2>&1; echo $? > "$L/fault_no_frozen_match_plain_make43.rc") &
(cd "$B" && PATH="$M43:$PATH" python3 scripts/check_entity_shape.py --self-test > "$L/fault_no_frozen_match_selftest_make43.log" 2>&1; echo $? > "$L/fault_no_frozen_match_selftest_make43.rc") &
wait
(cd "$B" && git checkout -q -- scripts/shape_consumer_inventory.py && git diff --quiet && echo "copy B restored") >> "$L/fault_no_frozen_match.anchor"
