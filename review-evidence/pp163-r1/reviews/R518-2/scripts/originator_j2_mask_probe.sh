#!/bin/sh
# Disposable probe: in a copy of hdl/, tb/common and tb/originator from TREE, log the
# originator's withdraw mask and release per clock through test J2 (a response and
# another entry's cancellation in one clock), then run the unit suite.
# usage: originator_j2_mask_probe.sh TREE WORKDIR VERILATOR LOG
set -eu
tree=$1; work=$2; verilator=$3; log=$4
rm -rf "$work"; mkdir -p "$work/tb"
cp -r "$tree/hdl" "$work/"; cp -r "$tree/tb/common" "$tree/tb/originator" "$work/tb/"
rm -rf "$work/tb/originator/obj_dir"
python3 - "$work/tb/originator/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = ('  dut->cancel_valid_i = 1; dut->cancel_owner_i = 14;\n  h.tick();\n  h.clr();\n  h.idle(3);\n')
new = ('  dut->cancel_valid_i = 1; dut->cancel_owner_i = 14;\n  for (int k = 0; k < 4; ++k) {\n'
       '    dut->eval();\n'
       '    printf("PROBE J2 clock c+%d: withdraw_slot_mask 0x%02x release_valid %d release_slot %d\\n", k,\n'
       '           unsigned(dut->withdraw_slot_mask_o), int(dut->release_valid_o), int(dut->release_slot_o));\n'
       '    h.tick();\n    if (k == 0) h.clr();\n  }\n')
assert s.count(old) == 1, "J2 anchor"
open(p, "w").write(s.replace(old, new))
PY
cd "$work/tb/originator" && make VERILATOR="$verilator" > "$log" 2>&1
grep -E 'PROBE|checks' "$log"
