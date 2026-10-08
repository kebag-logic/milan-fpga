#!/usr/bin/env bash
# Build probe P1 into a private copy of a tree's tb/aecp_notify.
# Args: SRC_TREE WORK_DIR [RTL_SED_EXPR]. Prints the probe lines for fail_at 0,1,2.
set -euo pipefail
SRC=$1; W=$2; HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W/tb"
cp -a "$SRC/hdl" "$W/hdl"; cp -a "$SRC/tb/common" "$W/tb/common"; cp -a "$SRC/tb/aecp_notify" "$W/tb/aecp_notify"
rm -rf "$W/tb/aecp_notify"/obj*
if [ $# -ge 3 ]; then sed -i "$3" "$W/hdl/aecp/KL_aecp_notify.sv"; fi
F="$W/tb/aecp_notify/sim_main.cpp"
python3 -I - "$F" "$HERE/p1_fail_window.cpp" <<'PY'
import sys
f, probe = sys.argv[1], open(sys.argv[2]).read()
s = open(f).read()
a = "  void cancel_collision();\n"
assert s.count(a) == 1
s = s.replace(a, a + "  void probe_fail_window(int fail_at);\n")
b = "// ---- IX: the identity index (issue #232)"
assert s.count(b) == 1
s = s.replace(b, probe + "\n" + b)
c = "  if (collision_only) {\n"
assert s.count(c) == 1
s = s.replace(c, "  if (getenv(\"PROBE_P1\")) {\n    for (int k = 0; k < 3; ++k) probe_fail_window(k);\n    return 0;\n  }\n" + c)
if "#include <cstdlib>" not in s:
    s = s.replace("#include <cstdint>\n", "#include <cstdint>\n#include <cstdlib>\n", 1)
open(f, "w").write(s)
PY
cd "$W/tb/aecp_notify"
${VERILATOR:-verilator} --cc --exe --build -j 4 --top-module KL_aecp_notify \
  -GN_CTRL_P=2 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 -Wno-fatal -Wno-lint -Wno-style \
  -CFLAGS "-std=c++17 -O2 -I$PWD" ../../hdl/common/pp_pkg.sv ../../hdl/aecp/KL_aecp_notify.sv sim_main.cpp \
  -o Vprobe >build.log 2>&1 || { tail -30 build.log; exit 3; }
PROBE_P1=1 ./obj_dir/Vprobe | grep '^\[probe'
