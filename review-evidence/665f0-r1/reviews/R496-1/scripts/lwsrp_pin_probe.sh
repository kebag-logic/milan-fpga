#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# lwsrp_pin_probe.sh - reviewer probe for PR #668 (#665 F0): does the lwsrp
# arm notice a lwSRP checkout that is not the 19f5796b pin, unmodified?
# Copies a lwSRP checkout, adds one comment line to src/core/mrp_mad.c (a
# local modification), and runs test_ctrl_firmware.py --lwsrp on the copy.
# usage: lwsrp_pin_probe.sh <tree> <lwSRP checkout at 19f5796b> <workdir>
set -u
T=$(cd "$1" && pwd); L=$(cd "$2" && pwd); W=$3; mkdir -p "$W"
rm -rf "$W/lwSRP_dirty"; cp -a "$L" "$W/lwSRP_dirty"
sed -i '1i /* reviewer probe: a local modification the arm should notice */' "$W/lwSRP_dirty/src/core/mrp_mad.c"
echo "lwSRP copy HEAD $(git -C "$W/lwSRP_dirty" rev-parse HEAD); status: $(git -C "$W/lwSRP_dirty" status --short | tr '\n' ' ')"
(cd "$T" && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp "$W/lwSRP_dirty" --build-dir "$W/build")
echo "rc=$?"
