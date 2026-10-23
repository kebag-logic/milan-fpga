#!/usr/bin/env python3
"""Plant one defect in a copy of milan_datapath.sv, build the nxn leg against it
through the suite's own recipe (DP_SRC overridden), run it, and require the named
#632 check to fail. Scratch evidence for round 5; the copy lives outside the tree.
usage: nxn_plant.py <repo> <mutant> <out dir>"""
import subprocess
import sys
from pathlib import Path

repo, name, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
DP = repo / "hdl/milan/milan_datapath.sv"
ROUNDER = (
    "  wire [N_STREAMS*32-1:0] mut_aaf_rnd_w;\n"
    "  KL_mtt_round #(.N_P (N_STREAMS), .BASE_HZ_P (AUDIO_IF_FS_HZ_P)) mut_aaf_round (\n"
    "    .clk_i (axis_clk), .rst_n (axis_resetn), .raw_ns_i (aecp_pres_offset[N_STREAMS*32-1:0]),\n"
    "    .ofs_ns_o (mut_aaf_rnd_w), .ofs_c_o (), .rb_row_i ('0), .rb_ns_o ());\n")
MUTANTS = {
    # the CRF output stamps its row as set, not rounded by Equation 14
    "crf_stamp_as_set": (
        [("    .transit_ns_i  (pres_crf_ns_w),\n", "    .transit_ns_i  (aecp_pres_offset[32*CRF_TUID_C +: 32]),\n"),
         ("    .transit_c_i   (pres_crf_c_w),\n", "    .transit_c_i   (1'b0),\n")],
        "#632 every CRF timestamp, all 64 bits, is a domain media event's instant plus its offset applied"),
    # the AAF talkers stamp their rows rounded by Equation 14 (round 4's binding)
    "aaf_stamp_rounded": (
        [("  KL_aaf_packetizer #(.N_TALKERS_P(N_STREAMS),\n",
          ROUNDER + "  KL_aaf_packetizer #(.N_TALKERS_P(N_STREAMS),\n"),
         ("    .transit_ns_i (aecp_pres_offset[N_STREAMS*32-1:0]),\n", "    .transit_ns_i (mut_aaf_rnd_w),\n")],
        "#632 every AAF timestamp is a domain media event's instant plus its offset as set, to the ns"),
}
edits, must = MUTANTS[name]
text = DP.read_text()
for old, new in edits:
    if text.count(old) != 1:
        sys.exit(f"[FAIL] {name}: anchor found {text.count(old)} times")
    text = text.replace(old, new)
out.mkdir(parents=True, exist_ok=True)
mut = out / "milan_datapath.sv"
mut.write_text(text)
suite = repo / "tb/verilator/milan_dp"
b = subprocess.run(["make", "-s", "build-nxn", f"DP_SRC={mut}"], cwd=suite, capture_output=True, text=True)
(out / "build.log").write_text(b.stdout + b.stderr)
if b.returncode != 0:
    sys.exit(f"[FAIL] {name}: build rc={b.returncode}")
r = subprocess.run(["./obj_nxn/Vmilan_dp_nxn"], cwd=suite, capture_output=True, text=True)
(out / "run.log").write_text(r.stdout + r.stderr)
fails = [ln for ln in r.stdout.splitlines() if "[FAIL]" in ln]
tally = [ln for ln in r.stdout.splitlines() if "checks:" in ln and "failures:" in ln]
caught = r.returncode != 0 and any(must in ln for ln in fails)
print(f"[{'PASS' if caught else 'FAIL'}] {name}: rc={r.returncode}, {len(fails)} [FAIL] line(s), "
      f"{tally[-1].strip() if tally else 'no tally'}; named check {'among them' if caught else 'NOT among them'}: {must}")
for ln in fails[:6]:
    print("   ", ln.strip())
sys.exit(0 if caught else 1)
