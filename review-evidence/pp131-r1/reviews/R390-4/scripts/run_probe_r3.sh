#!/bin/sh
# Build a disposable pp_top bench with the round-3 reviewer knobs and
# probe_r3.hpp, then run --probe-r3.
# Usage: run_probe_r3.sh <packet> <tree> <verilator>
# <tree> is a disposable `git archive` copy of the head (or of a mutant).
set -u
P=$1; T=$2; VL=$3
cat "$P/scripts/probe_r3.hpp" >> "$T/tb/pp_top/d3_phases.hpp"
python3 - "$T/tb/pp_top/sim_main.cpp" "$T/tb/pp_top/pp_top_wrap.sv" <<'PY'
import sys
p, w = sys.argv[1], sys.argv[2]
s = open(p).read()
def sub(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new)
# device knob: the payload READ (offset != 0) of region nv_hold_rid ends
# nv_hold_left cycles after its last byte, once
s = sub(s, "  int      nv_byte_wait = 0;\n",
        "  int      nv_byte_wait = 0;\n  int      nv_hold_rid = -1;   // reviewer knob\n"
        "  long     nv_hold_left = 0;\n")
s = sub(s, "      } else if (--nv_done_lag <= 0) {\n        d->nvm_dev_done_i = 1;\n        nvm_ops.push_back(nv_cur);\n        nv_st = NvState::NV_IDLE;\n      }\n    } else if (nv_st == NvState::NV_WRITE) {",
        "      } else if (nv_cur.region == nv_hold_rid && nv_cur.off != 0 && nv_hold_left > 0) {\n"
        "        --nv_hold_left;                                // reviewer knob\n"
        "      } else if (--nv_done_lag <= 0) {\n        d->nvm_dev_done_i = 1;\n        nvm_ops.push_back(nv_cur);\n        nv_st = NvState::NV_IDLE;\n      }\n    } else if (nv_st == NvState::NV_WRITE) {")
old = '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
s = sub(s, old, '  if (argc == 2 && std::strcmp(argv[1], "--probe-r3") == 0) {\n'
        '    Suite setup(h);\n    setup.load_descriptor_image();\n'
        '    const std::vector<uint8_t> image = h.dram;\n'
        '    ProbeR3{h, image, setup.image_ents}.run();\n    return 0;\n  }\n' + old)
open(p, "w").write(s)
v = open(w).read()
v = sub(v, "    output logic        dbg_d3_agg_fired_o\n);",
        "    output logic        dbg_d3_agg_fired_o,\n"
        "    output logic        dbg_r3_m0_req_o,\n    output logic        dbg_r3_m0_abort_o,\n"
        "    output logic [1:0]  dbg_r3_own_o,\n    output logic [7:0]  dbg_r3_port_st_o,\n"
        "    output logic [7:0]  dbg_r3_hs_o,\n    output logic        dbg_r3_proof_o\n);")
v = sub(v, "  assign dbg_d3_agg_fired_o = u_dut.d3_agg_w;\n",
        "  assign dbg_d3_agg_fired_o = u_dut.d3_agg_w;\n"
        "  assign dbg_r3_m0_req_o   = u_dut.nvm_req_w;\n"
        "  assign dbg_r3_m0_abort_o = u_dut.nvm_abort_w;\n"
        "  assign dbg_r3_own_o      = 2'(u_dut.u_nvm_arb.own_r);\n"
        "  assign dbg_r3_port_st_o  = 8'(u_dut.u_nvm_port.state_r);\n"
        "  assign dbg_r3_hs_o       = 8'(u_dut.u_nvm_shadow.hs_r);\n"
        "  assign dbg_r3_proof_o    = u_dut.u_aecp.u_d3.proof_w;\n")
open(w, "w").write(v)
PY
cd "$T/tb/pp_top" && make gsi-build VERILATOR="$VL" > build-probe.log 2>&1 || { echo "BUILD FAILED"; tail -30 build-probe.log; exit 2; }
./obj_dir/Vpp_top_sim --probe-r3; echo "rc=$?"
