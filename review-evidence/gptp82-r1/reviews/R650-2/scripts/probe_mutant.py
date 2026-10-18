#!/usr/bin/env python3
"""Reviewer probe: copy an extracted head tree, apply ONE textual mutation
(pattern must occur exactly once), regenerate the engine suite image, build
the engine harness and run it once (base image only). Prints the harness
summary and every FAIL line. Usage:
  probe_mutant.py HEAD_TREE WORK_DIR NAME   (NAME from PROBES below, or 'clean')"""
import shutil, subprocess, sys
from pathlib import Path
GEN = "hdl/ucode/gen_gptp_ucode.py"
RTL = "hdl/top/KL_gptp_engine.sv"
PROBES = {
  # BECGATE's incapable drop goes through BECOME (mastership, PHC word 3,
  # Sync/Announce cadences) instead of SELF
  "drop_via_become": (GEN,
    '    p.emit("WRST", ra=0, imm=RG_PUB | 2, fmt=FMT_Q)\n'
    '    p.emit("BR", label=LB["SELF"])\n',
    '    p.emit("BR", label=LB["BECOME"])\n'),
  # the drop publishes thisClock but keeps the presence/sync flags
  "drop_keeps_flags": (GEN,
    '    p.emit("WRST", ra=0, imm=RG_PUB | 2, fmt=FMT_Q)\n'
    '    p.emit("BR", label=LB["SELF"])\n',
    '    p.emit("BR", label=LB["SELF"])\n'),
  # the asCapable hook waits a full receipt interval
  "hook_delta_3000": (RTL,
    "                  tmr_arm_delta_w <= 32'd1;\n",
    "                  tmr_arm_delta_w <= 32'd3000;\n"),
  # BECGATE's incapable branch no longer re-arms the receipt watch, so a
  # port that regains asCapable without Announces never becomes master
  "held_no_rearm": (GEN,
    '    p.emit("MOVE", rd=RU, ra=0, imm=3000)\n'
    '    p.emit("WRST", ra=RU, imm=RG_TMR | 2, fmt=FMT_Q)  # keep watching\n',
    ''),
  # publish word 15 does not serve thisClock
  "word15_zero": (RTL,
    "          4'd15: st_rd_mux_w = rom_clock_id_w;\n",
    "          4'd15: st_rd_mux_w = 64'd0;\n"),
}
head, work, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
if work.exists(): shutil.rmtree(work)
shutil.copytree(head, work, symlinks=True)
if name.startswith("m:"):
    # a control taken verbatim from the head tree's own mutants.py
    import ast
    src = (head / "tb/verilator/engine/mutants.py").read_text()
    tree = ast.parse(src)
    muts = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "MUTATIONS":
            muts = node.value
    gen_names = {"GENERATOR": "ucode/gen_gptp_ucode.py"}
    for el in muts.elts:
        vals = [gen_names.get(getattr(e, "id", ""), None) if isinstance(e, ast.Name) else ast.literal_eval(e) for e in el.elts]
        if vals[0] == name[2:]:
            PROBES[name] = ("hdl/" + vals[1], vals[2], vals[3])
if name != "clean":
    f, pat, rep = PROBES[name]
    p = work / f
    t = p.read_text()
    assert t.count(pat) == 1, (name, t.count(pat))
    p.write_text(t.replace(pat, rep))
eng = work / "tb/verilator/engine"
r = subprocess.run(["make", "-C", str(eng), "gptp_ucode.hex", "-B"], capture_output=True, text=True)
if r.returncode:
    print("GENERATOR REFUSED\n", r.stdout[-2000:], r.stderr[-2000:]); sys.exit(3)
vf = ["--cc", "--exe", "--build", "-j", "4", "--top-module", "KL_gptp_engine", "-Wall", "-Wno-fatal",
      "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
      "-GUCODE_HEX_P=\"gptp_ucode.hex\"", "-GCLK_HZ_P=2000000",
      "-CFLAGS", f"-std=c++17 -O2 -I{eng} -Wall -Wextra"]
srcs = [str(work / "hdl" / s) for s in ("ucpu/gptp_ucpu_pkg.sv", "ucpu/KL_gptp_ucpu.sv",
        "wire/KL_gptp_rx_parser.sv", "wire/KL_gptp_tx_slot.sv", "common/KL_gptp_timer.sv", "top/KL_gptp_engine.sv")]
r = subprocess.run(["verilator", *vf, *srcs, str(eng / "sim_main.cpp"), "-o", "Vengine_sim"],
                   cwd=str(eng), capture_output=True, text=True)
if r.returncode:
    print("BUILD FAILED\n", r.stdout[-3000:], r.stderr[-3000:]); sys.exit(4)
r = subprocess.run([str(eng / "obj_dir/Vengine_sim")], cwd=str(eng), capture_output=True, text=True)
out = r.stdout + r.stderr
print(f"probe={name} harness_rc={r.returncode}")
for line in out.splitlines():
    if line.startswith(("FAIL ", "INFO #82")) or "checks:" in line or "%Error" in line or "Assertion" in line:
        print(line)
