#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Processor-top stale-grant probe. Copies tb/pp_top of <tb-tree> into a
# disposable work dir, adds three read-only wrap outputs (top-level
# srp_sr_admitted_o / srp_active_o and KL_srp_top.gate_acc_w), replaces the
# default build's Suite(h).run() with the reviewer probe, and runs only the
# default build. <hdl-tree> selects the RTL (head or pre-fix base).
# Usage: run.sh <tb-tree> <hdl-tree> <verilator> <work-dir>
set -uo pipefail
TB=$1; HDLSRC=$2; VL=$3; W=$4
HERE=$(cd "$(dirname "$0")/../r298-1/probe_pp_top" && pwd)
rm -rf "$W"; mkdir -p "$W/tb"
cp -a "$HDLSRC/hdl" "$W/hdl"
cp -a "$TB/tb/common" "$W/tb/common"; cp -a "$TB/tb/pp_top" "$W/tb/pp_top"
cd "$W/tb/pp_top" || exit 3
python3 - "$HERE/probe_main.inc" <<'EOF'
import sys
inc = open(sys.argv[1]).read()
w = open("pp_top_wrap.sv").read()
a = "    output logic        dbg_notify_enq_o\n);"
assert w.count(a) == 1
w = w.replace(a, "    output logic        dbg_notify_enq_o,\n"
              "    output wire  [7:0]  r298_adm_o,\n"
              "    output wire  [7:0]  r298_active_o,\n"
              "    output wire         r298_gate_acc_o\n);")
a2 = "endmodule"
i = w.rindex(a2)
w = w[:i] + ("  assign r298_adm_o      = u_dut.srp_sr_admitted_o;\n"
             "  assign r298_active_o   = u_dut.srp_active_o;\n"
             "  assign r298_gate_acc_o = u_dut.u_srp.gate_acc_w;\n") + w[i:]
open("pp_top_wrap.sv", "w").write(w)
s = open("sim_main.cpp").read()
m = "int main(int argc, char** argv) {"
assert s.count(m) == 1
s = s.replace(m, inc + "\n" + m)
r = "  if (!gsi_only) Suite(h).run();\n"
assert s.count(r) == 1
s = s.replace(r, "  if (!gsi_only) r298_top_probe(h);\n")
open("sim_main.cpp", "w").write(s)
mk = open("Makefile").read()
mk += ("\nprobe: ltn_rom.hex ucode.hex\n"
       "\t@rm -f obj_dir/build_tally.txt\n"
       "\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n"
       "\t./obj_dir/Vpp_top_sim\n")
open("Makefile", "w").write(mk)
EOF
make VERILATOR="$VL" probe
