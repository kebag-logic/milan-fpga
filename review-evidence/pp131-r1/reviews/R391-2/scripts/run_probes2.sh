#!/usr/bin/env bash
# Reproduce the R391-2 reviewer probes on a processor checkout at 2b38d68e.
# Usage: run_probes2.sh <processor checkout> <scratch dir> <dir holding a Verilator 5.050 'verilator'>
# Nothing is written into the checkout: the tree is exported into the scratch dir.
set -euo pipefail
SRC=$1; S=$2; VDIR=$3; HERE=$(cd "$(dirname "$0")" && pwd)
export PATH="$VDIR:$PATH"
mkdir -p "$S"; rm -rf "$S/tree" "$S/probe" "$S/probe-agg"
mkdir "$S/tree"; git -C "$SRC" archive HEAD | tar -x -C "$S/tree"
hook() {   # $1 = sim_main.cpp, $2 = header to include
python3 - "$1" "$2" <<'PY'
import sys
p, hdr = sys.argv[1], sys.argv[2]; s = open(p).read()
a = '#include "d3_phases.hpp"\n'
b = '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, a + '#include "%s"\n' % hdr, 1)
s = s.replace(b, '  if (argc == 2 && std::strcmp(argv[1], "--r391") == 0) {\n    run_r391(h);\n    return 0;\n  }\n' + b, 1)
open(p, 'w').write(s)
PY
}
# P1-P5 on the unmodified RTL
if [ -z "${R391_P6_MUTANT:-}" ] && [ -z "${R391_P7:-}" ] && [ -z "${R391_P8:-}" ]; then
cp -a "$S/tree" "$S/probe"
hook "$S/probe/tb/pp_top/sim_main.cpp" "$HERE/r391_probe2.hpp"
(cd "$S/probe/tb/pp_top" && make gsi-build >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391)
fi
# P6: the aggregate swept across the walk (a probe copy of the wrap overrides
# NVM_RS_AGG_CYC_P with a small bound and taps the writer's state)
AGG=${R391_AGG:-2800}
rm -rf "$S/probe-agg"; cp -a "$S/tree" "$S/probe-agg"
python3 - "$S/probe-agg/tb/pp_top/pp_top_wrap.sv" "$AGG" <<'PY'
import sys
p, agg = sys.argv[1], sys.argv[2]; s = open(p).read()
a = "    output logic        dbg_nvm_drain_o\n);"
b = "      .CLK_HZ_P     (TB_CLK_HZ_C),\n"
c = "  assign dbg_nvm_drain_o  = u_dut.nvm_drain_nc_w;\n"
assert s.count(a) == 1 and s.count(b) == 1 and s.count(c) == 1
s = s.replace(a, "    output logic        dbg_nvm_drain_o,\n    output logic [3:0]  dbg_r391_ws_o,\n"
                 "    output logic        dbg_r391_pass_o,\n    output logic        dbg_r391_fired_o\n);")
s = s.replace(b, b + "      .NVM_RS_AGG_CYC_P (%s),\n" % agg)
s = s.replace(c, c + "  assign dbg_r391_ws_o   = 4'(u_dut.u_aecp.u_d3.ws_r);\n"
                 "  assign dbg_r391_pass_o = u_dut.u_aecp.u_d3.pass_r;\n"
                 "  assign dbg_r391_fired_o = u_dut.u_aecp.u_d3.agg_fired_r;\n")
open(p, 'w').write(s)
PY
sed "s/R391_AGG_VALUE/$AGG/" "$HERE/r391_aggsweep.hpp" > "$S/probe-agg/tb/pp_top/r391_aggsweep.hpp"
hook "$S/probe-agg/tb/pp_top/sim_main.cpp" "r391_aggsweep.hpp"
if [ -z "${R391_P6_MUTANT:-}" ] && [ -z "${R391_P7:-}" ] && [ -z "${R391_P8:-}" ]; then
(cd "$S/probe-agg/tb/pp_top" && make gsi-build >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391)
fi
# P6 against a planted mutant (R391_P6_MUTANT names one of r391_mutants2.py's)
if [ -n "${R391_P6_MUTANT:-}" ]; then
  d="$S/probe-agg-$R391_P6_MUTANT"; rm -rf "$d"; cp -a "$S/probe-agg" "$d"; rm -rf "$d/tb/pp_top/obj_dir"
  python3 - "$d" "$R391_P6_MUTANT" "$HERE" <<'PY'
import sys, importlib.util
d, name, here = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("m", here + "/r391_mutants2.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
path, old, new = m.MUTANTS[name]; f = d + "/" + path; s = open(f).read()
assert s.count(old) == 1; open(f, "w").write(s.replace(old, new))
PY
  (cd "$d/tb/pp_top" && make gsi-build >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391 | sed "s/^/$R391_P6_MUTANT /")
fi
# P7: past the bound after a COMPLETE terminal, golden and the mutant
if [ -n "${R391_P7:-}" ]; then
  for v in golden agg_not_stopped_at_terminal; do
    d="$S/probe-p7-$v"; rm -rf "$d"; cp -a "$S/probe-agg" "$d"; rm -rf "$d/tb/pp_top/obj_dir"
    python3 - "$d" "$v" "$HERE" <<'PY'
import sys, importlib.util
d, name, here = sys.argv[1:4]
p = d + "/tb/pp_top/sim_main.cpp"; s = open(p).read()
s = s.replace('#include "r391_aggsweep.hpp"\n', '#include "r391_postterm.hpp"\n'); open(p, "w").write(s)
if name != "golden":
    spec = importlib.util.spec_from_file_location("m", here + "/r391_mutants2.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    path, old, new = m.MUTANTS[name]; f = d + "/" + path; t = open(f).read()
    assert t.count(old) == 1; open(f, "w").write(t.replace(old, new))
PY
    sed "s/R391_AGG_VALUE_L/${AGG}L/" "$HERE/r391_postterm.hpp" > "$d/tb/pp_top/r391_postterm.hpp"
    (cd "$d/tb/pp_top" && make gsi-build >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391 | sed "s/^/$v /")
  done
fi
# P8: a device slow on every grant and every byte, at the derived deadlines
if [ -n "${R391_P8:-}" ]; then
  d="$S/probe-p8"; rm -rf "$d"; mkdir -p "$d"; git -C "$SRC" archive HEAD | tar -x -C "$d"
  python3 - "$d/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
a = "  int      nv_gnt_every = 0;\n"
b = ("      } else if (nv_left) {\n"
     "        d->nvm_dev_rvalid_i = 1;\n"
     "        d->nvm_dev_rdata_i = nv_mem[nv_cur.region][nv_rd_pos & 0xFF];\n"
     "        if (d->nvm_dev_rready_o) { nv_left--; nv_rd_pos++; nv_rd_sent++; }\n")
g = "        nv_rd_pos = nv_cur.off;\n"
assert s.count(a) == 1 and s.count(b) == 1 and s.count(g) == 1
s = s.replace(g, g + "        nv_byte_wait = (nv_rd_pos < 8) ? nv_hdr_gap : nv_byte_gap;\n")
s = s.replace(a, a + "  int      nv_byte_gap = 0;   // R391 probe: cycles withheld before each READ payload byte\n"
                     "  int      nv_hdr_gap = 0;    // R391 probe: ... before each of the 8 header bytes\n"
                     "  int      nv_byte_wait = 0;\n")
s = s.replace(b, "      } else if (nv_left && nv_byte_wait > 0) {\n        --nv_byte_wait;\n"
                 "      } else if (nv_left) {\n"
                 "        d->nvm_dev_rvalid_i = 1;\n"
                 "        d->nvm_dev_rdata_i = nv_mem[nv_cur.region][nv_rd_pos & 0xFF];\n"
                 "        if (d->nvm_dev_rready_o) { nv_left--; nv_rd_pos++; nv_rd_sent++;\n"
                 "          nv_byte_wait = (nv_rd_pos < 8) ? nv_hdr_gap : nv_byte_gap; }\n")
open(p, "w").write(s)
PY
  hook "$d/tb/pp_top/sim_main.cpp" "$HERE/r391_byteslow.hpp"
  (cd "$d/tb/pp_top" && make gsi-build >/dev/null 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391)
fi
