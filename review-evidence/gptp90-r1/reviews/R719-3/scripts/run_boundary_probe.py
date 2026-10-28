#!/usr/bin/env python3
"""gmPresent boundary plants at head: (a) the mark moved to 0xFE << 3, (b) both
compares shifted by 52 instead of 53, so priority1 127..254 count as absent.
usage: run_boundary_probe.py <head-src> <workdir>"""
import subprocess, sys
from pathlib import Path
src, work = Path(sys.argv[1]), Path(sys.argv[2])
GEN = "hdl/ucode/gen_gptp_ucode.py"
exe = (src / "tb/verilator/engine/obj_dir/Vengine_sim").resolve()
plants = {
  "mark-0xFE": [("SRTO_PASSED_C = 0xFF << 3\n", "SRTO_PASSED_C = 0xFE << 3\n", 1)],
  "shift-52": [("cnd=ALU_SHR, imm=53)  # p1,class[7:5]\n", "cnd=ALU_SHR, imm=52)  # p1,class[7:5]\n", 2)],
}
for name, subs in plants.items():
    d = work / name; (d / "hdl/ucode").mkdir(parents=True, exist_ok=True)
    t = (src / GEN).read_text()
    for old, new, n in subs:
        assert t.count(old) == n, (name, t.count(old)); t = t.replace(old, new)
    (d / GEN).write_text(t)
    for pname, ga, pa in (("shipping", [], []), ("p1-255", ["--p1", "255"], ["+not-gm-capable"])):
        run = d / pname; run.mkdir(exist_ok=True)
        g = subprocess.run([sys.executable, "-I", str(d / GEN), "--clk-hz", "2000000", "--cease-ms", "3000", *ga,
                            "-o", str(run / "gptp_ucode.hex")], capture_output=True, text=True)
        if g.returncode:
            print(f"== {name} [{pname}] GENERATOR REFUSED: {g.stderr.strip().splitlines()[-1]}"); continue
        r = subprocess.run([str(exe), *pa], cwd=run, capture_output=True, text=True)
        out = r.stdout + r.stderr
        tally = [l for l in out.splitlines() if " checks: " in l]
        print(f"== {name} [{pname}] rc={r.returncode} {tally[-1] if tally else 'NO TALLY'}")
        for l in [l for l in out.splitlines() if l.startswith("FAIL ")][:5]: print("   ", l[:200])
