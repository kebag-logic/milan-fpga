#!/usr/bin/env python3
"""Cancel the production sweep while it waits (--wait) for a tree lock held by a
FOREIGN process (its own session, not a sweep descendant). Boundary: a `flock`
process is observed in the sweep's subtree. Reports exit status, whether any
suite/preflight started, foreign holder identity, and the lock owner record.
Usage: probe_lock_wait.py <checkout> <INT|TERM> <outdir>"""
import json, os, signal, subprocess, sys, tempfile, time
from pathlib import Path
checkout, signame, outdir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(checkout / "scripts"))
from owned_process import OwnedProcesses
from process_test_support import identity
from test_suite_cancellation import fixture, DRIVER
def subtree(root):
    pop = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            try:
                f = (e / "stat").read_text().rsplit(")", 1)[1].split()
                pop[int(e.name)] = (int(f[1]), (e / "cmdline").read_bytes().replace(b"\0", b" ").decode())
            except (FileNotFoundError, ProcessLookupError, IndexError):
                pass
    owned, more = {root}, True
    while more:
        more = {p for p, v in pop.items() if v[0] in owned} - owned; owned |= more
    return {p: pop[p][1] for p in owned if p in pop}
res = {}
with tempfile.TemporaryDirectory(prefix="lockwait-", dir=os.environ.get("TMPDIR")) as scratch, OwnedProcesses():
    root, probe = fixture(Path(scratch), "lockwait-" + signame)
    lock = root / ".run_all_suites.lock"
    (root / ".run_all_suites.lock.owner").write_text("pid 0  foreign holder record\n")
    ready = Path(scratch) / "holder-ready"
    holder = subprocess.Popen(["flock", str(lock), "-c", f"echo held > '{ready}'; exec sleep 300"], start_new_session=True)
    while not ready.exists():
        assert holder.poll() is None; time.sleep(0.02)
    holder_id = identity(holder.pid)
    probe.start(["bash", str(root / DRIVER), str(root / "logs"), "--wait"])
    deadline = time.monotonic() + 30
    while not any(cmd.startswith("flock 9") for cmd in subtree(probe.process.pid).values()):
        assert probe.process.poll() is None, probe.log()
        assert time.monotonic() < deadline, "no lock-wait boundary"
        time.sleep(0.02)
    res["boundary"] = subtree(probe.process.pid)
    probe.signal(getattr(signal, "SIG" + signame))
    status, output = probe.finish()
    res.update(signal=signame, exit=status, output=output,
               suite_or_preflight_started=(root / "logs").exists(),
               foreign_holder_same_identity=holder.poll() is None and identity(holder.pid) == holder_id,
               foreign_owner_record_kept=(root / ".run_all_suites.lock.owner").read_text() == "pid 0  foreign holder record\n",
               sweep_descendants_after=subtree(probe.process.pid) if probe.process.poll() is None else {})
    holder.terminate(); holder.wait(timeout=5)
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "result.json").write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps({k: v for k, v in res.items() if k != "boundary"}, indent=1))
