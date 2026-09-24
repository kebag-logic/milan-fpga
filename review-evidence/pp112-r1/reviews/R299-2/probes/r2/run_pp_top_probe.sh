#!/bin/sh
# Usage: run_pp_top_probe.sh <tree-root> <work-dir> <cross|gsi|gsi-storm>
# Copies <tree-root>/tb/pp_top (+ tb/common) to <work-dir>, symlinks hdl/,
# and adds OBSERVE-ONLY debug ports to the copied wrapper (hierarchical reads
# of protocol_processor_top's SRP admission nets). No RTL is modified.
#   cross      : runs only ReviewerCrossProbe (pp_top_cross_probe.inc)
#   gsi        : runs only the unchanged #111 InternalStreamInfoPhase
#   gsi-storm  : same phase, while the harness re-declares SRP source 6
#                through svc_* every ~STORM_GAP clocks (alternating an
#                admitted and a refused TSpec), so admission verdicts are
#                held for much of the run.
set -eu
TREE=$(cd "$1" && pwd); WORK=$2; MODE=$3
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$WORK"; mkdir -p "$WORK/tb"
cp -r "$TREE/tb/pp_top" "$TREE/tb/common" "$WORK/tb/"
ln -s "$TREE/hdl" "$WORK/hdl"
python3 - "$WORK/tb/pp_top" "$HERE/pp_top_cross_probe.inc" "$MODE" <<'PY'
import sys, pathlib
d, inc, mode = pathlib.Path(sys.argv[1]), open(sys.argv[2]).read(), sys.argv[3]
w = d / "pp_top_wrap.sv"; s = w.read_text()
a = "    output logic        srp_domain_change_o,\n"
assert s.count(a) == 1
s = s.replace(a, a + "    output logic [7:0]  dbg_p_adm_o,\n    output logic [7:0]  dbg_p_act_o,\n"
              "    output logic [15:0] dbg_p_tkdecl_o,\n    output logic [31:0] dbg_p_sum_o,\n"
              "    output logic        dbg_p_over_o,\n    output logic [7:0]  dbg_p_sample_o,\n"
              "    output logic        dbg_p_round_o,\n")
b = "  assign dbg_streaming0_o = u_dut.aecp_streaming_w[0];\n"
assert s.count(b) == 1
s = s.replace(b, b + "  assign dbg_p_adm_o    = u_dut.srp_sr_admitted_w;\n"
              "  assign dbg_p_act_o    = u_dut.srp_active_w;\n"
              "  assign dbg_p_tkdecl_o = u_dut.srp_tk_decl_state_w;\n"
              "  assign dbg_p_sum_o    = u_dut.srp_sum_slope_w;\n"
              "  assign dbg_p_over_o   = u_dut.srp_over_limit_w;\n"
              "  assign dbg_p_sample_o = 8'(u_dut.u_srp.u_admission.cidx_r);\n"
              "  assign dbg_p_round_o  = u_dut.u_srp.u_admission.round_done_o;\n")
w.write_text(s)
m = d / "sim_main.cpp"; s = m.read_text()
# storm hook (inactive unless PP_STORM_GAP is set in the environment)
a = "  void step() {\n    d->clk_i = 0; d->eval();\n"
assert s.count(a) == 1
hook = '''  long storm_gap = std::getenv("PP_STORM_GAP") ? std::atol(std::getenv("PP_STORM_GAP")) : 0;
  long storm_ctr = 0, storm_ops = 0, storm_rsp = 0, storm_held = 0, storm_rounds = 0;
  bool storm_busy = false;
  void storm_tick() {
    d->svc_valid_i = 0;
    if (d->dbg_p_round_o) ++storm_rounds;
    if (!(d->dbg_p_adm_o & 0x40u)) ++storm_held;
    if (storm_busy) { if (d->svc_rsp_valid_o) { storm_busy = false; ++storm_rsp; } return; }
    if (++storm_ctr < storm_gap || !d->svc_ready_o) return;
    storm_ctr = 0; storm_busy = true; ++storm_ops;
    d->svc_valid_i = 1; d->svc_op_i = 0; d->svc_index_i = 6;
    d->svc_stream_id_i = (OWN_MAC << 16) | 0x0606; d->svc_da_i = 0x91E0F0000646ull;
    d->svc_vid_i = 2; d->svc_max_frame_i = (storm_ops & 1) ? 224 : 20000;
    d->svc_lstn_state_i = 0;
  }
'''
s = s.replace(a, hook + a)
a = "    serve_milan_info_face();\n\n    d->eval();\n"
assert s.count(a) == 1
s = s.replace(a, "    serve_milan_info_face();\n    if (storm_gap > 0) storm_tick();\n\n    d->eval();\n")
a = '#include "gsi_internal.hpp"\n'
assert s.count(a) == 1
s = s.replace(a, a + inc + "\n")
a = "  if (!gsi_only) Suite(h).run();\n  InternalStreamInfoPhase{h}.run();\n"
assert s.count(a) == 1
if mode == "cross":
    s = s.replace(a, "  (void)gsi_only;\n  ReviewerCrossProbe{h}.run();\n")
else:
    s = s.replace(a, "  (void)gsi_only;\n  { InternalStreamInfoPhase ph{h}; ph.run();\n"
                  '    printf("STORM gap=%ld ops=%ld responses=%ld rounds=%ld clocks_src6_not_admitted=%ld\\n",\n'
                  "           ph.io.storm_gap, ph.io.storm_ops, ph.io.storm_rsp, ph.io.storm_rounds, ph.io.storm_held); }\n")
if "#include <cstdlib>" not in s:
    s = "#include <cstdlib>\n" + s
m.write_text(s)
PY
cd "$WORK/tb/pp_top"
VERILATOR=${VERILATOR:-verilator}
make ltn_rom.hex ucode.hex >/dev/null
make gsi-build VERILATOR="$VERILATOR" >build.log 2>&1 || { tail -40 build.log; exit 3; }
if [ "$MODE" = gsi-storm ]; then PP_STORM_GAP=${STORM_GAP:-60} ./obj_dir/Vpp_top_sim
else ./obj_dir/Vpp_top_sim; fi
