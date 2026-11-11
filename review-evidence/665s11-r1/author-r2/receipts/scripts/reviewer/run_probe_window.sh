#!/bin/sh
# Disposable probe: does the split firmware take an ACMP BIND_RX between the REBOOT's SUCCESS
# leaving the mailbox and the reset port's write, and send frames after its ENTITY_DEPARTING?
# Usage: run_probe_window.sh <checkout at the head> <build-dir> <packet-dir>
# Appends probe_window.cpp.inc to the checkout's test_plat_boot.cpp, runs the host firmware gate,
# runs the probe binary alone, then restores the file and checks its blob id.
set -eu
co=$1 build=$2 packet=$3
f="$co/sw/firmware/ctrl/test/test_plat_boot.cpp"
want=$(git -C "$co" rev-parse HEAD:sw/firmware/ctrl/test/test_plat_boot.cpp)
cp "$f" "$build.orig"
trap 'cp "$build.orig" "$f"; [ "$(git -C "$co" hash-object "$f")" = "$want" ] || echo "RESTORE MISMATCH" >&2' EXIT
cat "$packet/receipts/probe_window.cpp.inc" >> "$f"
(cd "$co" && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --build-dir "$build" --jobs 4) || true
"$build/checkout/test_plat_boot_if1" --gtest_filter='Boot.Probe*' 2>&1 | grep 'PROBE\|OK\|FAILED' || true
