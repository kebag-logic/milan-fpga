#!/bin/sh
# run_window_probe.sh TREE VERILATOR : apply the reviewer's window probe to a copy of an
# exact-head tree TREE and run section RBT's probe scenarios (non-advertising, advertising)
set -e
P=$(cd "$(dirname "$0")/.." && pwd)
W=$(mktemp -d -p "$P/scratch"); cp -a "$1"/. "$W"/
(cd "$W" && patch -p1 < "$P/probes/window-after-notification-round.patch")
make -C "$W/tb/pp_top" reboot VERILATOR="$2" || true
rm -rf "$W"
