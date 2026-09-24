#!/bin/sh
# Reviewer probe runner: copies r295_probe.hpp into an extracted tree's
# tb/pp_top, adds a --r295-probe mode, builds with the given Verilator, runs.
# usage: run_probe.sh <extracted-tree> <verilator> <log>
set -eu
T=$1; V=$2; LOG=$3
HERE=$(cd "$(dirname "$0")" && pwd)
B=$T/tb/pp_top
cp "$HERE/r295_probe.hpp" "$B/r295_probe.hpp"
if ! grep -q r295_probe.hpp "$B/sim_main.cpp"; then
  python3 - "$B/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("int main(int argc, char** argv) {",
              '#include "r295_probe.hpp"\nint main(int argc, char** argv) {', 1)
anchor = "#else\n"
i = s.rfind(anchor, 0, s.index('const char* const build = "default";'))
s = s[:i + len(anchor)] + ('  if (argc == 2 && std::strcmp(argv[1], "--r295-probe") == 0) {\n'
    '    R295Probe{h}.run();\n'
    '    printf("[r295 probe] %d checks, %d failures\\n", h.checks, h.fails);\n'
    '    return h.fails ? 1 : 0;\n  }\n') + s[i + len(anchor):]
if "<cstring>" not in s: s = "#include <cstring>\n" + s
open(p, "w").write(s)
PY
fi
cd "$B"
make ltn_rom.hex ucode.hex >/dev/null
make -s gsi-build VERILATOR="$V" >"$LOG.build" 2>&1 || \
  "$V" --version >/dev/null  # gsi-build absent at base: fall back below
if [ ! -x obj_dir/Vpp_top_sim ]; then
  make -n run VERILATOR="$V" | grep -m1 -- '--exe' | sh >>"$LOG.build" 2>&1
fi
set +e
./obj_dir/Vpp_top_sim --r295-probe >"$LOG" 2>&1
echo "rc=$?" >>"$LOG"
