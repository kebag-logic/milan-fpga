#!/usr/bin/env python3
"""Hard-stop probe of the production sweep driver.

Uses the production fixture (real driver, selector and tally; synthetic make)
from the checkout under test. At the published first-suite command handshake it
delivers KILL (uncatchable) or HUP (default-fatal, the terminal-hangup signal)
to the PID the caller launched, then releases the held command and observes,
without any timing oracle, whether a later suite starts and whether a completed
summary reaches the caller's output after the caller has already observed the
death. The observation ends when every process from the pre-signal tree has
exited (bounded), never on a sleep.

Usage: probe_sweep_hardstop.py <checkout> <KILL|HUP> <driver-file> <outdir>
  <driver-file> replaces scripts/run_all_suites.sh in the fixture (pass the
  checkout's own copy for the head behaviour, or a base copy)."""
import json, os, shutil, signal, sys, tempfile, time
from pathlib import Path

checkout, signame, driver, outdir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(checkout / "scripts"))
from owned_process import OwnedProcesses  # containment of whatever this probe orphans
from process_test_support import identity
from test_suite_cancellation import fixture, start

def tree(root_pid):
    pop = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            try:
                f = (e / "stat").read_text().rsplit(")", 1)[1].split()
                cmd = (e / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
                pop[int(e.name)] = (int(f[1]), f[19], f[0], cmd)
            except (FileNotFoundError, ProcessLookupError, IndexError):
                pass
    owned, more = {root_pid}, True
    while more:
        more = {p for p, v in pop.items() if v[0] in owned} - owned
        owned |= more
    return {p: pop[p] for p in owned if p in pop}

def alive(pid, start):
    cur = identity(pid)
    return cur is not None and cur[0] == start and cur[1] != "Z"

outdir.mkdir(parents=True, exist_ok=True)
result = {"signal": signame, "driver": str(driver)}
with tempfile.TemporaryDirectory(prefix="hardstop-", dir=os.environ.get("TMPDIR")) as scratch:
    with OwnedProcesses():
        root, probe = fixture(Path(scratch), "hardstop-" + signame)
        shutil.copy2(driver, root / "scripts/run_all_suites.sh")
        probe.env["PROBE_MODE"] = "orphan"   # held at handshake; completes with a real tally on release
        start(probe)
        data = probe.ready()
        before = tree(probe.process.pid)
        result["tree_before_signal"] = {str(p): [v[1], v[2], v[3][:120]] for p, v in before.items()}
        probe.signal(getattr(signal, "SIG" + signame))
        status = probe.process.wait(timeout=12)
        result["caller_status"] = status
        log_at_death = probe.log()
        result["caller_output_at_death"] = log_at_death
        survivors = {p: v for p, v in before.items() if p != probe.process.pid and alive(p, v[1])}
        result["survivors_after_caller_death"] = {str(p): v[3][:120] for p, v in survivors.items()}
        (probe.control / "release").write_text("released after caller death\n")
        # Wait for every non-stubborn survivor to finish; the detached stubborn
        # fixture child never exits and is reaped by this probe's owner.
        stubborn = data["child"]
        deadline = time.monotonic() + 60
        while any(alive(p, v[1]) for p, v in survivors.items() if p != stubborn):
            assert time.monotonic() < deadline, "survivors did not finish"
            time.sleep(0.05)
        after = probe.log()
        result["output_after_caller_death"] = after[len(log_at_death):]
        result["later_suite_started"] = (probe.control / "next-suite").exists()
        result["completed_summary_after_death"] = "\nsuites:" in after[len(log_at_death):] or after[len(log_at_death):].startswith("suites:")
        result["suite_logs"] = sorted(str(p.relative_to(root / "logs")) for p in (root / "logs").rglob("*.log")) if (root / "logs").exists() else []
        result["lock_owner_left"] = (root / ".run_all_suites.lock.owner").exists()
        probe.save(dict(caller_status=status, later_suite_started=result["later_suite_started"]))
        shutil.copytree(probe.control / "..", outdir / "fixture", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("*.py", "bin", "__pycache__", "tb", "syn"))
(outdir / "result.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps({k: result[k] for k in ("signal", "caller_status", "survivors_after_caller_death",
      "later_suite_started", "completed_summary_after_death")}, indent=1))
print("output after caller death:\n" + result["output_after_caller_death"])
