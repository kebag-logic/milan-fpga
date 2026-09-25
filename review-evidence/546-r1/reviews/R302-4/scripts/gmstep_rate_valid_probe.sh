#!/bin/sh
# Disposable probe: does the milan_dp gmstep leg exercise the receiver's rate
# validity (crf_rate_valid_w) at the merge head? Copies the leg, marks the wire
# public in a COPY of milan_datapath.sv, and prints its level every 500k cycles.
# Usage: gmstep_rate_valid_probe.sh <exported-tree-with-submodules> <log>
# (the export needs git indexes in the three submodule dirs for scripts/pp_srcs.py)
set -eu
X=$1; LOG=$2
cd "$X/tb/verilator"; rm -rf milan_dp_probe; cp -a milan_dp milan_dp_probe; rm -rf milan_dp_probe/obj_gmstep
cp ../../hdl/milan/milan_datapath.sv milan_dp_probe/probe_datapath.sv
cd milan_dp_probe
python3 - <<'PY'
p='probe_datapath.sv'; s=open(p).read(); o='  wire crf_rate_valid_w;\n'; assert s.count(o)==1
open(p,'w').write(s.replace(o,'  wire crf_rate_valid_w /* verilator public_flat_rd */;\n'))
p='sim_gmstep.cpp'; s=open(p).read(); o='    trace_.tu_prev = tu;\n'; assert s.count(o)==1
open(p,'w').write(s.replace(o,o+'''    { static bool pv = false; static bool init = false;
      const bool v = root->milan_datapath__DOT__crf_rate_valid_w;
      if (init && pv != v) std::printf("PROBE: crf_rate_valid -> %d at cycle %llu\\n", (int)v, (unsigned long long)cyc_);
      if ((cyc_ % 500000) == 0) std::printf("PROBE: cycle %llu rate_valid=%d media_epoch=%llu\\n", (unsigned long long)cyc_, (int)v, (unsigned long long)media_epoch_);
      pv = v; init = true; }
'''))
PY
taskset -c 0-7 make VERILATOR_JOBS=8 DP_SRC=probe_datapath.sv gmstep > "$LOG" 2>&1
grep -E 'PROBE|EVENT|checks:|RESULT' "$LOG"
