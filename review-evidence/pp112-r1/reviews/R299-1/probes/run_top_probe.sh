#!/bin/sh
# Usage: run_top_probe.sh <tree-root> <work-dir> [probe.inc] [function] [join]
# Copies <tree-root>/tb/srp_top to <work-dir>, makes run() call only the
# reviewer probe function (default: probe_cross_source from
# top_cross_source_probe.inc), builds with the suite Makefile and runs it.
# With a fifth argument "join", a read-only dbg_join_o port exposing the
# engine's T-MRP-JOIN tick (u_dut.p_join_fsm_r) is added to the probe copy
# of the wrapper. The <tree-root> must carry a wrapper with the head dbg_*
# probes (the head tb/srp_top/srp_top_wrap.sv or a copy of it).
set -eu
TREE=$(cd "$1" && pwd); WORK=$2
HERE=$(cd "$(dirname "$0")" && pwd)
INC=${3:-$HERE/top_cross_source_probe.inc}
FN=${4:-probe_cross_source}
JOIN=${5:-}
rm -rf "$WORK"; mkdir -p "$WORK/tb"
cp -r "$TREE/tb/srp_top" "$TREE/tb/common" "$WORK/tb/"
ln -s "$TREE/hdl" "$WORK/hdl"
if [ "$JOIN" = join ]; then
  python3 - "$WORK/tb/srp_top/srp_top_wrap.sv" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
a = "    output wire [7:0]   dbg_sample_index_o,\n"
assert s.count(a) == 1
s = s.replace(a, a + "    output wire         dbg_join_o,\n")
b = "  assign dbg_sample_index_o = 8'(u_dut.u_admission.cidx_r);\n"
assert s.count(b) == 1
s = s.replace(b, b + "  assign dbg_join_o = u_dut.p_join_fsm_r;\n")
open(p, "w").write(s)
EOF
fi
python3 - "$WORK/tb/srp_top/sim_main.cpp" "$INC" "$FN" <<'EOF'
import sys
path, inc, fn = sys.argv[1], open(sys.argv[2]).read(), sys.argv[3]
s = open(path).read()
start = s.index("  int run() {\n")
body_start = s.index("{\n", start) + 2
body_end = s.index('    printf("%d checks', body_start)
s = s[:body_start] + f"    {fn}();\n\n" + s[body_end:]
anchor = "  const milan::tb::Model<Vsrp_top_wrap> model;"
assert s.count(anchor) == 1
s = s.replace(anchor, inc + "\n" + anchor)
open(path, "w").write(s)
EOF
cd "$WORK/tb/srp_top" && make run
