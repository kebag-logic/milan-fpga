#!/bin/sh
# Build an instrumented copy of a tree's engine harness that prints every
# check it evaluates ("CHK <name>"), then run the shipping and priority1 255
# passes. Usage: list_checks.sh <tree> <workdir>
# The tree is not modified: the engine directory is copied into <workdir>.
set -eu
TREE=$(cd "$1" && pwd)
W=$2
mkdir -p "$W"
W=$(cd "$W" && pwd)
rm -rf "$W/tb"
cp -r "$TREE/tb" "$W/tb"
E="$W/tb/verilator/engine"
python3 -I - "$E/sim_main.cpp" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
old = "  void expect(const char *what, uint64_t got, uint64_t exp) {\n    checks++;\n"
assert s.count(old) == 1
s = s.replace(old, old + '    printf("CHK %s%s\\n", check_prefix, what);\n')
open(p, "w").write(s)
EOF
cd "$E"
GEN="$TREE/hdl/ucode/gen_gptp_ucode.py"
python3 -I "$GEN" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex >/dev/null
verilator --cc --exe --build -j 4 --top-module KL_gptp_engine \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$E -Wall -Wextra" \
  "$TREE/hdl/ucpu/gptp_ucpu_pkg.sv" "$TREE/hdl/ucpu/KL_gptp_ucpu.sv" \
  "$TREE/hdl/wire/KL_gptp_rx_parser.sv" "$TREE/hdl/wire/KL_gptp_tx_slot.sv" \
  "$TREE/hdl/common/KL_gptp_timer.sv" "$TREE/hdl/top/KL_gptp_engine.sv" \
  sim_main.cpp -o Vengine_chk >"$W/build.log" 2>&1
./obj_dir/Vengine_chk >"$W/ship.log" 2>&1 || true
mkdir -p p1run
python3 -I "$GEN" --clk-hz 2000000 --cease-ms 3000 --p1 255 -o p1run/gptp_ucode.hex >/dev/null
(cd p1run && ../obj_dir/Vengine_chk +not-gm-capable) >"$W/p1.log" 2>&1 || true
grep -h '^CHK ' "$W/ship.log" "$W/p1.log" | sed 's/^CHK //' | sort -u >"$W/checks.txt"
tail -n 1 "$W/ship.log" "$W/p1.log"
wc -l <"$W/checks.txt"
