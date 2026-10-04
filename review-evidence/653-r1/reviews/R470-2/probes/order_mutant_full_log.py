#!/usr/bin/env python3
"""Reviewer probe P7: rebuild unb_mutants.py's first mutant (the ACMP lane held
6,000 cycles) exactly as that driver plants it, but KEEP the leg's full output,
so the claim "its 4 failures are exactly the four U2 order checks" can be read.

Usage: order_mutant_full_log.py <reviewed clone> <scratch work dir> <log>
Writes only under <scratch work dir> and <log>.
"""
import shutil
import subprocess
import sys
from pathlib import Path

clone, work, log = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
here = clone / "tb/verilator/milan_dp"
sys.path.insert(0, str(here))
import unb_mutants as um  # noqa: E402  (the driver's own pattern text)

work.mkdir(parents=True, exist_ok=True)
pp = work / "pp_hdl_order"
if pp.exists():
    shutil.rmtree(pp)
shutil.copytree(clone / "protocol-processor/hdl", pp)
top = pp / um.PP_TOP
text = top.read_text()
assert text.count(um.PP_ACMP_REQ) == 1, "pattern moved"
top.write_text(text.replace(um.PP_ACMP_REQ, um.PP_ACMP_HELD))
mdir = work / "obj_order"
b = subprocess.run(["make", "-s", "-C", str(here), "-o", "ltn_rom.hex", "-o", "ucode.hex",
                    "notify-build", f"PP_DIR={pp}", f"NOTIFY_MDIR={mdir}"],
                   capture_output=True, text=True, check=False)
if b.returncode != 0:
    log.write_text(b.stdout + b.stderr)
    sys.exit(f"build failed rc={b.returncode}")
r = subprocess.run([str(mdir / um.EXE_NAME)], cwd=str(here), capture_output=True,
                   text=True, check=False)
log.write_text(r.stdout + r.stderr)
fails = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("[FAIL]")]
print(f"rc={r.returncode} fails={len(fails)}")
for f in fails:
    print("  " + f[:220])
