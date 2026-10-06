#!/bin/bash
# Reviewer fault probes for PR #165 (issue #69). Disposable; never committed.
# Usage: probes.sh <clean head extraction> <scratch dir>
#   VERILATOR (env) - the Verilator to build with (the pinned 5.050)
# Each probe copies hdl/, tb/common and one suite into its own scratch tree,
# plants one exact edit (count must be 1), runs one make target, and prints the
# FAIL / probe lines. Exit status is 0 when every probe ran to completion.
set -u
HEAD=$(readlink -f "$1"); SCR=$(readlink -f "$2"); V=${VERILATOR:-verilator}
mkdir -p "$SCR"
plant() {  # plant <tree> <file> <old> <new>
  python3 - "$@" <<'EOF'
import sys
tree, rel, old, new = sys.argv[1:5]
p = f"{tree}/{rel}"
s = open(p).read()
assert s.count(old) == 1, f"{rel}: anchor occurs {s.count(old)} times"
open(p, "w").write(s.replace(old, new, 1))
EOF
}
tree() {  # tree <name> <suite...>
  local t="$SCR/$1"; shift
  rm -rf "$t"; mkdir -p "$t/tb"; cp -r "$HEAD/hdl" "$t/"; cp -r "$HEAD/tb/common" "$t/tb/"
  for s in "$@"; do cp -r "$HEAD/tb/$s" "$t/tb/"; done
  echo "$t"
}
rc=0
# P1: the registry port taken from the latest received frame's interface
# (hdr_if_r) instead of the command's, latched at the engine handshake.
t=$(tree p1 pp_top)
plant "$t" hdl/top/protocol_processor_top.sv \
  "      .rgy_port_i            ((N_AVB_IF_P > 1) ? aecp_cmd_if_r : 2'd0)," \
  "      .rgy_port_i            ((N_AVB_IF_P > 1) ? hdr_if_r : 2'd0),"
( cd "$t/tb/pp_top" && make interfaces VERILATOR="$V" ) > "$SCR/p1.log" 2>&1
echo "P1 rgy port from latest frame: make rc=$?"; grep -E "^FAIL|^IF: " "$SCR/p1.log"
# P2: DEREGISTER matches the OTHER port's entry (KL_aecp_notify walk compare).
t=$(tree p2 pp_top aecp_notify)
plant "$t" hdl/aecp/KL_aecp_notify.sv \
  "                      && (port_r[wk_ix_r] == hold_port_r);" \
  "                      && (port_r[wk_ix_r] == (op_dereg_r ? ~hold_port_r : hold_port_r));"
( cd "$t/tb/pp_top" && make interfaces VERILATOR="$V" ) > "$SCR/p2-top.log" 2>&1
echo "P2 dereg other port, tb/pp_top IF: make rc=$?"; grep -E "^FAIL|^IF: " "$SCR/p2-top.log"
( cd "$t/tb/aecp_notify" && make interfaces VERILATOR="$V" ) > "$SCR/p2-notify.log" 2>&1
echo "P2 dereg other port, tb/aecp_notify PT/CK: make rc=$?"; grep -E "^FAIL|^\[build" "$SCR/p2-notify.log"
# P3: no RTL edit. A probe section appended to tb/aecp_notify's third build:
# two rows of one controller (ports 0 and 1) both probing; one command; which
# probes are cancelled; then the un-cancelled probe fails.
t=$(tree p3 aecp_notify)
python3 - "$t/tb/aecp_notify/port_tuple.hpp" "$(dirname "$0")/probe_ca_dual.hpp" <<'EOF'
import sys
t, probe = sys.argv[1], open(sys.argv[2]).read()
s = open(t).read()
a, b = 'int PortHarness::run() {', '  keyed_counters();\n  return fails ? 1 : 0;'
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, probe + '\n' + a, 1)
s = s.replace(b, '  keyed_counters();\n  probe_ca_dual(*this);\n  return fails ? 1 : 0;', 1)
open(t, 'w').write(s)
EOF
( cd "$t/tb/aecp_notify" && make interfaces VERILATOR="$V" ) > "$SCR/p3.log" 2>&1 || rc=1
echo "P3 two probing rows, one command:"; grep -E "^PROBE|^FAIL|^\[build" "$SCR/p3.log"
exit $rc
