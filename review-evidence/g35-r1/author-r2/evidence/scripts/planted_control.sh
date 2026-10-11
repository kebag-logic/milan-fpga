#!/usr/bin/env bash
# Build the planted control by hand (head RTL with the latch line deleted,
# exactly the edit mutants.py makes) against the head parser bench, and keep
# its full output so the failing words can be quoted.
set -u
S=$VALIDATION_STORAGE/g35-a599
LANE=$LANES/g35-rx-err
D=$S/planted
mkdir -p "$D/hdl/wire" "$D/hdl/ucpu" "$D/tb/common" "$D/tb/verilator/parser"
cp "$LANE/hdl/ucpu/gptp_ucpu_pkg.sv" "$D/hdl/ucpu/"
cp "$LANE/tb/common/verilator_harness.hpp" "$D/tb/common/"
cp "$LANE/tb/verilator/parser/sim_main.cpp" "$LANE/tb/verilator/parser/Makefile" "$D/tb/verilator/parser/"
python3 - "$LANE/hdl/wire/KL_gptp_rx_parser.sv" "$D/hdl/wire/KL_gptp_rx_parser.sv" <<'EOF'
import sys
src = open(sys.argv[1]).read()
latch = "        if (rx_err_i) bad_r <= 1'b1;\n"
assert src.count(latch) == 1
open(sys.argv[2], "w").write(src.replace(latch, ""))
EOF
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd "$D/tb/verilator/parser" || exit 2
make run > "$S/planted-control.log" 2>&1
echo "rc=$?"
diff <(git -C "$LANE" show HEAD:hdl/wire/KL_gptp_rx_parser.sv) "$D/hdl/wire/KL_gptp_rx_parser.sv"
grep -E "^FAIL|checks:" "$S/planted-control.log"
