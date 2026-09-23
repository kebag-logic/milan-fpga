#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build a disposable probe harness: the head's sim_main.cpp with the reviewer
# probe phases (probe_phases.inc) inserted after phase 21, and the run
# truncated right after them, against the head RTL. Then run it on the head
# generator's shipping image and on each extra generator given.
#
# usage: build_probe.sh <exported-tree> <work-dir> [label=gen.py ...]
# env:   VERILATOR  path of the Verilator wrapper to use (default: verilator)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
TREE=$(cd "$1" && pwd)
mkdir -p "$2"
WORK=$(cd "$2" && pwd)
shift 2
VERILATOR=${VERILATOR:-verilator}
E="$TREE/tb/verilator/engine"
RTL="$TREE/hdl"

python3 - "$E/sim_main.cpp" "$HERE/probe_phases.inc" "$WORK/sim_probe.cpp" <<'EOF'
import sys
src, inc, out = sys.argv[1:]
text = open(src, encoding="utf-8").read()
probe = open(inc, encoding="utf-8").read()
anchor = "  // ---- 21b: become resets the best record -- no ghost GM"
call = "    stop_consuming_sync_when_ascapable_falls();\n"
assert text.count(anchor) == 1 and text.count(call) == 1, "anchors moved"
text = text.replace(anchor, probe + "\n" + anchor)
first = text.index(call)                      # the run() list's call
text = (text[:first] + call +
        "    reviewer_probes();\n"
        "    printf(\"%d checks: %d PASS, %d FAIL\\n\", checks, checks - fails,"
        " fails);\n"
        "    return fails ? 1 : 0;\n" + text[first + len(call):])
open(out, "w", encoding="utf-8").write(text)
EOF

"$VERILATOR" --cc --exe --build -j 8 --top-module KL_gptp_engine \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$E -Wall -Wextra" \
  --Mdir "$WORK/obj_dir" \
  "$RTL/ucpu/gptp_ucpu_pkg.sv" "$RTL/ucpu/KL_gptp_ucpu.sv" \
  "$RTL/wire/KL_gptp_rx_parser.sv" "$RTL/wire/KL_gptp_tx_slot.sv" \
  "$RTL/common/KL_gptp_timer.sv" "$RTL/top/KL_gptp_engine.sv" \
  "$WORK/sim_probe.cpp" -o Vprobe >"$WORK/build.log" 2>&1

runone() { # label, generator
  d="$WORK/run_$1"
  mkdir -p "$d"
  python3 "$2" --clk-hz 2000000 --cease-ms 3000 -o "$d/gptp_ucode.hex" \
    >/dev/null
  set +e
  (cd "$d" && "$WORK/obj_dir/Vprobe") >"$d/run.log" 2>&1
  r=$?
  set -e
  echo "### $1: exit $r; $(tail -n 1 "$d/run.log")"
  grep -E '^FAIL' "$d/run.log" | cut -c1-110 || true
}
runone head "$RTL/ucode/gen_gptp_ucode.py" &
for spec in "$@"; do
  runone "${spec%%=*}" "${spec#*=}" &
done
wait
