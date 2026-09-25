#!/usr/bin/env python3
"""Reviewer robustness probe: refused re-declaration WITHOUT a withdrawal.

The shipped [I] case withdraws the admissible 224-byte declaration before the
refused 20,000-byte re-declaration. This probe keeps the 224-byte declaration
standing and ADMITTED (real grant high, no Listener, so ACTIVE low), then
re-declares 20,000 bytes over it with the same wire Listener Ready timing.
It exercises the processor's invalidate-on-declaration path (grant retired at
the accepting edge) rather than the withdrawal path. Only refused cases run.

The head harness is copied and patched in scratch; the clone is not edited.
usage: redeclare_probe.py <clone> <packet> <label> [PP_DIR]
env: VERILATOR, VERILATOR_JOBS
"""
import os
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
packet = Path(sys.argv[2]).resolve()
label = sys.argv[3]
pp_dir = sys.argv[4] if len(sys.argv) > 4 else None
here = clone / "tb/verilator/milan_dp"
pdir = packet / "scratch/probe/tb/verilator/milan_dp"
pdir.mkdir(parents=True, exist_ok=True)
rec = packet / "receipts/redeclare"
rec.mkdir(parents=True, exist_ok=True)

src = (here / "sim_crf_licence.cpp").read_text()


def sub(old: str, new: str) -> None:
    global src
    assert src.count(old) == 1, old
    src = src.replace(old, new)


# 1) preload: declare and keep standing (no withdrawal), require its grant.
sub("""    stage_declaration(uid, previous_frame, true);
    run_until(cyc + 128);
    stage_declaration(uid, previous_frame, false);
    run_until(cyc + ms(kDiagTickMs + 100)); // drain frames and close their last interval
    ck("withdrawal cleared the real grant", admitted[uid].v, 0);
    ck("withdrawal closed ACTIVE", active[uid].v, 0);
""", """    stage_declaration(uid, previous_frame, true);
    run_until(cyc + ms(kDiagTickMs + 100)); // PROBE: keep the declaration standing
    ck("PROBE preload 224-byte declaration holds its real grant", admitted[uid].v, 1);
    ck("PROBE preload has no Listener, so ACTIVE is low", active[uid].v, 0);
""")
# 2) the refused grant check: the standing grant must fall and never rise.
sub("""        ck("the ceiling refused the re-declaration throughout", static_cast<uint64_t>(admitted[uid].rises - grants), 0);
""", """        ck("the ceiling refused the re-declaration throughout", static_cast<uint64_t>(admitted[uid].rises - grants), 0);
        ck("PROBE re-declaration retired the standing grant", admitted[uid].v, 0);
""")
# 3) only the refused changed-TSpec case, over a standing declaration.
sub("""            grant_case(uid, true, phase, delay);
            grant_case(uid, false, phase, delay);
            grant_case(uid, true, phase, delay, true);
            grant_case(uid, false, phase, delay, true);
""", """            grant_case(uid, true, phase, delay, true);  // PROBE: refused over standing 224
            stage_declaration(uid, 224, false);          // PROBE: clean up between cases
            run_until(cyc + ms(kDiagTickMs + 100));
""")
(pdir / "sim_crf_licence_probe.cpp").write_text(src)

mdir = packet / f"scratch/obj_redeclare_{label}"
args = ["make", "-n", "-s", "-C", str(here), "crflic-build",
        f"VERILATOR={os.environ['VERILATOR']}", f"CRFLIC_MDIR={mdir}",
        f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '8')}"]
if pp_dir:
    args.append(f"PP_DIR={pp_dir}")
cmd = subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
assert cmd.count(" sim_crf_licence.cpp ") == 1
cmd = cmd.replace(" sim_crf_licence.cpp ", f" {pdir / 'sim_crf_licence_probe.cpp'} ")
(rec / f"{label}.cmd").write_text(cmd + "\n")
subprocess.run(["rm", "-rf", str(mdir)], check=True)
b = subprocess.run(["sh", "-c", cmd], cwd=here, capture_output=True, text=True)
(rec / f"{label}.build.log").write_text(b.stdout + b.stderr)
exe = mdir / "Vmilan_dp_crflic"
if b.returncode or not exe.is_file():
    print("build failed", b.returncode)
    sys.exit(3)
r = subprocess.run([str(exe)], cwd=here, capture_output=True, text=True)
(rec / f"{label}.run.log").write_text(r.stdout + r.stderr)
out = r.stdout.splitlines()
print(label, "rc", r.returncode, out[-2:] if out else "")
hdr = ""
for ln in out:
    if ln.startswith("[I]") or ln.startswith("[INV]"):
        hdr = ln
    if "[FAIL]" in ln:
        print("  ", hdr[:48], "|", " ".join(ln.split())[:110])
