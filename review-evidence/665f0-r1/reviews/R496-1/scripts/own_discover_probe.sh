#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# own_discover_probe.sh - reviewer probe for PR #668 (#665 F0): the walk row
# RCV_ADP_DISCOVER(own eid) has no arm in ctrl_mutants.py; plant the defect
# (a DISCOVER for this entity treated as foreign) in a copy and show which
# checks catch it.
# usage: own_discover_probe.sh <tree> <workdir>
set -u
T=$(cd "$1" && pwd); W=$2; mkdir -p "$W"; rm -rf "$W/tree"; cp -a "$T" "$W/tree"
python3 - "$W/tree/sw/firmware/ctrl/adp/adp.c" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = 'if (target != 0u && target != a->entity->entity_id) {'
assert s.count(old) == 1
open(p, 'w').write(s.replace(old, 'if (target != 0u) {'))
PY
(cd "$W/tree" && git diff --stat && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --build-dir "$W/build")
echo "rc=$? (1 = the planted defect was caught)"
