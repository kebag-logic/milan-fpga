#!/bin/sh
# Reviewer probes for FPGA-gPTP PR #95 (issue #94), exact head 9d509029.
#
# usage: run_probes.sh <fresh clone checked out at the head> [fix|sweep]
#   Inserts probe phases A, B and D (scripts/probe_phases*.cpp) into a COPY's
#   tb/verilator/engine/sim_main.cpp right after
#   raise_ascapable_on_the_second_exchange(), returns early, builds with the
#   `verilator` on PATH (Verilator 5.050 was used) and prints the R729 lines.
#   With "fix", it first applies the disposable candidate change recorded in
#   receipts/probe3-candidate-fix.diff (RTL first-sample reference level and
#   one NOTEN word clearing S_RSPSEQ) to show the probes discriminate.
#   With "sweep", only probe C runs: the rise swept across the cadence
#   timer's expiry in 4-cycle steps, counting requests per rise.
# The clone given is modified; use a disposable one.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
clone=$1
cd "$clone"
if [ "${2:-}" = fix ]; then
  python3 - <<'EOF'
p='hdl/top/KL_gptp_engine.sv'; s=open(p).read()
a="      port_seen_r <= port_seen_r || port_en_r;\n"
assert s.count(a)==1; s=s.replace(a,"      port_seen_r <= 1'b1;\n"); open(p,'w').write(s)
p='hdl/ucode/gen_gptp_ucode.py'; s=open(p).read()
a='    p.label("tail")\n    p.emit("WRST", ra=0, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)\n'
assert s.count(a)==1
s=s.replace(a,'    p.emit("WRST", ra=0, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)\n'+a)
open(p,'w').write(s)
EOF
fi
cd tb/verilator/engine
python3 - "$here/probe_phases.cpp" "$here/probe_phases2.cpp" "${2:-}" <<'EOF'
import sys
p='sim_main.cpp'; s=open(p).read()
probe=open(sys.argv[1]).read()+open(sys.argv[2]).read()
a="    raise_ascapable_on_the_second_exchange();\n"
i=s.index("  void run_every_phase() {"); j=s.index(a,i)
ins=("    r729_probe_warm_reset_port_low(true, \"R729 D low-at-release\");\n"
     "    r729_probe_warm_reset_port_low(false, \"R729 D fall-after-release\");\n"
     "    r729_probe_fu_after_fall();\n"
     "    r729_probe_glitch(1, \"R729 B1\");\n"
     "    r729_probe_glitch(3, \"R729 B3\");\n"
     "    return;\n")
if sys.argv[3] == "sweep":
    ins = "    r729_probe_rise_near_the_beat();\n    return;\n"
s=s[:j+len(a)]+ins+s[j+len(a):]
anchor="  // ---- 41: #89, sync receipt ageing needs gmPresent"
assert s.count(anchor)==1
s=s.replace(anchor, probe+"\n"+anchor)
open(p,'w').write(s)
EOF
python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex
verilator --cc --exe --build -j 4 --Mdir obj_probe --top-module KL_gptp_engine \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='"gptp_ucode.hex"' \
  -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I$PWD" \
  ../../../hdl/ucpu/gptp_ucpu_pkg.sv ../../../hdl/ucpu/KL_gptp_ucpu.sv \
  ../../../hdl/wire/KL_gptp_rx_parser.sv ../../../hdl/wire/KL_gptp_tx_slot.sv \
  ../../../hdl/common/KL_gptp_timer.sv ../../../hdl/top/KL_gptp_engine.sv \
  sim_main.cpp -o Vengine_probe >/dev/null
./obj_probe/Vengine_probe | grep -E "R729|checks:|^FAIL" || true
