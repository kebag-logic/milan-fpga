#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build tb/srp_top of a source tree in a disposable copy with the reviewer
# probe section added and the suite's run() list replaced by the probe only.
# Usage: run.sh <tb-source-tree> <verilator> <work-dir> [hdl-source-tree]
# With a 4th argument (e.g. the pre-fix base), the bench of <tb-source-tree>
# runs against that tree's hdl/, and the wrap's read-only invalidation probe
# (absent before the fix) is tied to zero; nothing else changes.
set -uo pipefail
SRC=$1; VL=$2; W=$3; HDLSRC=${4:-$1}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
cp -a "$HDLSRC/hdl" "$W/hdl"; mkdir -p "$W/tb"
cp -a "$SRC/tb/common" "$W/tb/common"; cp -a "$SRC/tb/srp_top" "$W/tb/srp_top"
rm -rf "$W/tb/srp_top/obj_dir"
if [ "$HDLSRC" != "$SRC" ]; then
  sed -i "s/u_dut\.adm_invalidate_w/8'd0/g" "$W/tb/srp_top/srp_top_wrap.sv"
fi
python3 - "$W/tb/srp_top/sim_main.cpp" "$HERE/probe_section.inc" <<'EOF'
import re, sys
p, inc = sys.argv[1], open(sys.argv[2]).read()
s = open(p).read()
start = s.index("  int run() {")
body_start = s.index("{", start) + 1
end = s.index('    printf("%d checks:', body_start)
s = s[:body_start] + "\n    probe_r298_cross_source();\n" + s[end:]
anchor = "  const milan::tb::Model<Vsrp_top_wrap> model;"
assert s.count(anchor) == 1
s = s.replace(anchor, inc + "\n" + anchor)
open(p, "w").write(s)
EOF
cd "$W/tb/srp_top" && make VERILATOR="$VL"
