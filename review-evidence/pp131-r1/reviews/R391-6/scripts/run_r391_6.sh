#!/usr/bin/env bash
# Reviewer probes R391-6 (the R391-5 probes re-run) on processor PR #132 (disposable; nothing is written
# into the checkout: each tree is exported with git archive into the scratch dir).
# Usage:
#   run_r391_5.sh <checkout> <rev> <scratch> <dir holding a Verilator 5.050 'verilator'> <probe> [args]
# probes:
#   d1 [MUTANT]           full-scale probe D1 arms (r391_4_d1.hpp), no override
#   sweep AGG STEP SCENS [MUTANT]
#                         the aggregate swept across both walks (r391_4_sweep.hpp);
#                         SCENS is a comma list of scenarios 0..5; MUTANT names one of
#                         r391_6_mutants.py's edits planted first
#   d3 [MUTANT]           tb/pp_top --d3-only, optionally with a planted mutant
#   full [MUTANT]         the default pp_top build's whole run, optionally with a planted mutant
#   acmp [MUTANT]         tb/acmp_nvm's graded run (make run), optionally with a planted mutant
set -euo pipefail
SRC=$1; REV=$2; S=$3; VDIR=$4; PROBE=$5; shift 5
HERE=$(cd "$(dirname "$0")" && pwd)
export PATH="$VDIR:$PATH"
mkdir -p "$S"
tag="$PROBE-$(echo "$*" | tr ' ,' '__')-$REV"
d="$S/$tag"; rm -rf "$d"; mkdir -p "$d"
git -C "$SRC" archive "$REV" | tar -x -C "$d"
# at most two compile jobs per build (the reviewer runs up to four builds at once)
grep -rl -- '--build -j 0' "$d/tb" | xargs -r sed -i 's/--build -j 0/--build -j 2/'
plant() {   # $1 = mutant name
python3 - "$d" "$1" "$HERE" <<'PY'
import sys, importlib.util
d, name, here = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("m", here + "/r391_6_mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for path, old, new in m.MUTANTS[name]:
    f = d + "/" + path; s = open(f).read()
    assert s.count(old) == 1, (name, path, s.count(old)); open(f, "w").write(s.replace(old, new))
print("planted", name)
PY
}
hook() {   # $1 = header to include
python3 - "$d/tb/pp_top/sim_main.cpp" "$1" <<'PY'
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
case "$PROBE" in
d1)
  MUT=${1:-}
  [ -n "$MUT" ] && plant "$MUT"
  cp "$HERE/r391_4_d1.hpp" "$d/tb/pp_top/"
  hook r391_4_d1.hpp
  (cd "$d/tb/pp_top" && make gsi-build >build.log 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391 \
     | sed "s/^/${MUT:-golden} /")
  ;;
sweep)
  AGG=$1; STEP=$2; SCENS=$3; MUT=${4:-}
  [ -n "$MUT" ] && plant "$MUT"
  python3 - "$d/tb/pp_top/pp_top_wrap.sv" "$AGG" <<'PY'
import sys
p, agg = sys.argv[1], sys.argv[2]; s = open(p).read()
a = "    output logic        dbg_d3_agg_fired_o\n);"
b = "      .CLK_HZ_P     (TB_CLK_HZ_C),\n"
c = "  assign dbg_nvm_drain_o  = u_dut.nvm_drain_nc_w;\n"
assert s.count(a) == 1 and s.count(b) == 1 and s.count(c) == 1
s = s.replace(a, "    output logic        dbg_d3_agg_fired_o,\n    output logic [3:0]  dbg_r391_ws_o,\n"
                 "    output logic        dbg_r391_pass_o,\n    output logic [4:0]  dbg_r391_hs_o,\n"
                 "    output logic        dbg_r391_bdone_o,\n    output logic        dbg_r391_bfail_o,\n"
                 "    output logic        dbg_r391_brvalid_o,\n    output logic        dbg_r391_bstall_o,\n"
                 "    output logic        dbg_r391_aggf_o,\n    output logic        dbg_r391_m1both_o\n);")
s = s.replace(b, b + "      .NVM_RS_AGG_CYC_P (%s),\n" % agg)
s = s.replace(c, c + "  assign dbg_r391_ws_o   = 4'(u_dut.u_aecp.u_d3.ws_r);\n"
                 "  assign dbg_r391_pass_o = u_dut.u_aecp.u_d3.pass_r;\n"
                 "  assign dbg_r391_hs_o   = 5'(u_dut.u_nvm_shadow.hs_r);\n"
                 "  assign dbg_r391_bdone_o = u_dut.u_nvm_shadow.done_r;\n"
                 "  assign dbg_r391_bfail_o = u_dut.u_nvm_shadow.fail_r;\n"
                 "  assign dbg_r391_brvalid_o = u_dut.u_nvm_shadow.nvm_rvalid_i;\n"
                 "  assign dbg_r391_bstall_o = u_dut.u_nvm_shadow.rs_stall_w;\n"
                 "  assign dbg_r391_aggf_o = u_dut.u_aecp.u_d3.agg_fired_r;\n"
                 "  assign dbg_r391_m1both_o = u_dut.u_aecp.u_d3.m_req_o && u_dut.u_aecp.u_d3.m_abort_o;\n")
open(p, 'w').write(s)
PY
  sed -e "s/R391_AGG_VALUE/$AGG/" -e "s/R391_STEP/$STEP/" -e "s/R391_SCENS_STR/$SCENS/" \
      -e "s/R391_SCENS/$SCENS/" "$HERE/r391_4_sweep.hpp" > "$d/tb/pp_top/r391_4_sweep.hpp"
  hook r391_4_sweep.hpp
  (cd "$d/tb/pp_top" && make gsi-build >build.log 2>&1 && ./obj_dir/Vpp_top_sim --r391 | grep R391 \
     | sed "s/^/${MUT:-golden} /")
  ;;
full)
  MUT=${1:-}
  [ -n "$MUT" ] && plant "$MUT"
  (cd "$d/tb/pp_top" && make gsi-build >build.log 2>&1 && { ./obj_dir/Vpp_top_sim && echo "rc=0" || echo "rc=$?"; } \
     | grep -E 'FAIL|checks|rc=|R391MON' | sed "s/^/${MUT:-golden} /")
  ;;
d3)
  MUT=${1:-}
  [ -n "$MUT" ] && plant "$MUT"
  (cd "$d/tb/pp_top" && make gsi-build >build.log 2>&1 && { ./obj_dir/Vpp_top_sim --d3-only && echo "rc=0" || echo "rc=$?"; } \
     | sed "s/^/${MUT:-golden} /")
  ;;
acmp)
  MUT=${1:-}
  [ -n "$MUT" ] && plant "$MUT"
  (cd "$d/tb/acmp_nvm" && { make run >run.log 2>&1 && echo "rc=0" || echo "rc=$?"; } \
     | sed "s/^/${MUT:-golden} /"; grep -E 'FAIL|checks:|R391MON|R391OWN' "$d/tb/acmp_nvm/run.log" | sed "s/^/${MUT:-golden} /")
  ;;
*) echo "unknown probe $PROBE"; exit 2 ;;
esac
