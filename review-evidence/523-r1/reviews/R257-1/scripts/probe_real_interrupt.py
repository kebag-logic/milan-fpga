#!/usr/bin/env python3
"""Interrupt the REAL mutation driver (real make/Verilator/simulator) at an
observable boundary: the first control's defect is present in the private copy
AND an owned build/simulation descendant is running with its cwd inside that
private copy. Then deliver INT, TERM or KILL to the driver and report exit
status, caller integrity (via clone_integrity.py), private-tree survival, and
whether any recorded descendant identity is still alive. KILL survivors are
terminated by identity afterwards and recorded.
Usage: probe_real_interrupt.py <checkout> <head> <INT|TERM|KILL> <outdir>"""
import json, os, signal, subprocess, sys, time
from pathlib import Path
checkout, head, signame, outdir = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
here = Path(__file__).resolve().parent
sys.path.insert(0, str(checkout / "tb/verilator/gptp_shadow")); sys.path.insert(0, str(checkout / "scripts"))
from mutants import MUTATIONS, REPO
tmp = Path(os.environ["TMPDIR"])
def census():
    pop = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            try:
                f = (e / "stat").read_text().rsplit(")", 1)[1].split()
                pop[int(e.name)] = (int(f[1]), f[19], f[0], os.readlink(e / "cwd") if (e / "cwd").exists() else "",
                                    (e / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")[:160])
            except (FileNotFoundError, ProcessLookupError, PermissionError, IndexError):
                pass
    return pop
def subtree(pop, root):
    owned, more = {root}, True
    while more:
        more = {p for p, v in pop.items() if v[0] in owned} - owned; owned |= more
    return {p: pop[p] for p in owned if p in pop and p != root}
def alive(pid, start):
    try:
        f = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return f[19] == start and f[0] != "Z"
    except (FileNotFoundError, ProcessLookupError):
        return False
name, original, old, new, expect = MUTATIONS[0]
rel = original.relative_to(REPO)
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env.update(VERILATOR=os.environ["PROBE_VERILATOR"], VERILATOR_JOBS="8", PYTHONDONTWRITEBYTECODE="1")
outdir.mkdir(parents=True, exist_ok=True)
log = open(outdir / "driver.log", "wb")
proc = subprocess.Popen([sys.executable, str(checkout / "tb/verilator/gptp_shadow/mutants.py")],
                        cwd=checkout / "tb/verilator/gptp_shadow", env=env, stdout=log, stderr=subprocess.STDOUT,
                        start_new_session=True)
deadline = time.monotonic() + 300; boundary = None
while boundary is None:
    assert proc.poll() is None, "driver ended before boundary"
    assert time.monotonic() < deadline, "no boundary"
    for private in tmp.glob("gptp-shadow-mutants-*"):
        f = private / rel
        if f.exists() and new in f.read_text(errors="replace") and new not in original.read_text():
            desc = subtree(census(), proc.pid)
            workers = {p: v for p, v in desc.items() if str(private) in v[3] and
                       any(t in v[4] for t in ("verilator_bin", "g++", "cc1plus", "Vgptp_shadow_sim", "make"))}
            if any(t in v[4] for v in workers.values() for t in ("verilator_bin", "cc1plus", "Vgptp_shadow_sim")):
                boundary = dict(private=str(private), mutation=name, descendants={str(p): [v[1], v[4]] for p, v in desc.items()})
    time.sleep(0.05)
os.kill(proc.pid, getattr(signal, "SIG" + signame))
status = proc.wait(timeout=60)
log.close()
alive_after = {p: v for p, v in boundary["descendants"].items() if alive(int(p), v[0])}
result = dict(signal=signame, exit=status, boundary=boundary, private_exists_after=Path(boundary["private"]).exists(),
              descendants_alive_after_exit=alive_after,
              output_tail=(outdir / "driver.log").read_text().splitlines()[-3:],
              completed_verdict_printed=("RESULT:" in (outdir / "driver.log").read_text()))
# Caller integrity at the moment the driver has exited (before any survivor finishes).
integ = subprocess.run([sys.executable, str(here / "clone_integrity.py"), str(checkout), head,
                        "gptp-processor", "protocol-processor", "third_party/verilog-axis"], capture_output=True, text=True)
result["caller_integrity_exit"] = integ.returncode
result["caller_integrity_problems"] = json.loads(integ.stdout)["problems"]
# KILL survivors: record, then stop them by identity and remove the private tree.
killed = []
for p, v in alive_after.items():
    try:
        fd = os.pidfd_open(int(p))
        if alive(int(p), v[0]):
            signal.pidfd_send_signal(fd, signal.SIGKILL); killed.append(p)
        os.close(fd)
    except ProcessLookupError:
        pass
result["probe_terminated_survivors"] = killed
if Path(boundary["private"]).exists():
    subprocess.run(["rm", "-rf", boundary["private"]], check=True)
(outdir / "result.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps({k: result[k] for k in ("signal", "exit", "private_exists_after", "completed_verdict_printed",
      "caller_integrity_exit", "caller_integrity_problems", "probe_terminated_survivors")}))
print("alive after exit:", {p: v[1][:60] for p, v in alive_after.items()})
print("tail:", result["output_tail"])
