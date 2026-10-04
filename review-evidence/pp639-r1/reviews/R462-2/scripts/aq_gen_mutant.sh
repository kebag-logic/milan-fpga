#!/usr/bin/env bash
# Plant one control of R462-1's lockstep_armq/gen.py MUTANTS table (imported unchanged) into
# a disposable copy of an exported tree's protocol_processor_top.sv, then build tb/pp_top
# and run its --arm-queue-only section (AQ1..AQ4). With NAME "none" nothing is planted.
# usage: aq_gen_mutant.sh HDL_TREE TB_TREE WORK NAME GEN_PY
#   HDL_TREE  exported tree whose hdl/ is used (head, or main for the old-RTL run)
#   TB_TREE   exported tree whose tb/common and tb/pp_top are used
#   GEN_PY    R462-1's scripts/lockstep_armq/gen.py
# Needs Verilator 5.050 first on PATH. Exit status is the simulator's.
set -euo pipefail
hdl=$1; tb=$2; work=$3; name=$4; gen=$5
rm -rf "$work"; mkdir -p "$work/tb"
cp -r "$hdl/hdl" "$work/hdl"; cp -r "$tb/tb/common" "$work/tb/common"; cp -r "$tb/tb/pp_top" "$work/tb/pp_top"
rm -rf "$work/tb/pp_top"/obj*
if [ "$name" != "none" ]; then
python3 - "$work/hdl/top/protocol_processor_top.sv" "$name" "$gen" <<'PY'
import importlib.util, sys
p, name, gen = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("gen", gen)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
old, new = mod.MUTANTS[name]
s = open(p).read()
assert s.count(old) == 1, f"{name}: {s.count(old)} occurrences in the full top"
open(p, "w").write(s.replace(old, new, 1))
PY
fi
cd "$work/tb/pp_top" && make gsi-build > build.log 2>&1 && ./obj_dir/Vpp_top_sim --arm-queue-only
