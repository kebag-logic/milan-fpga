#!/usr/bin/env python3
"""usage: mutate_r3.py (R764-2's mutate_r2.py plus round 3 mutant M16)
   mutate_r2.py <source checkout> <sha> <work dir> <receipts dir> <jobs>
Each mutation edits scripts/owned_process.py in its own fresh clone at <sha>
(made by clone_at.sh), then runs the named test inside its own user+PID
namespace, so anything a mutant leaks dies with that namespace. Every run writes
<name>.log and <name>.rc; summary.json lists the results. Never edits <source>."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path

src, sha, work, out, jobs = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), int(sys.argv[5])
HERE = Path(__file__).resolve().parent
out.mkdir(parents=True, exist_ok=True)
work.mkdir(parents=True, exist_ok=True)
TARGET = "scripts/owned_process.py"

def sub(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)

# name: (list of (old, new) replacements, test, expected "red"|"green")
MUT = {
 "control-A": ([], "suite", "green"),
 "control-B": ([], "suite", "green"),
 "control-lifecycle": ([], "lifecycle", "green"),
 # Identity by start time: restore the parent as part of the identity for SIGTERM.
 "M01-identity-includes-parent": ([("                    if (pid, start) not in initial:\n                        continue",
                                    "                    if initial.get((pid, start)) != _parent:\n                        continue")], "suite", "red"),
 # Identity by start time, the other half: the send-time recheck again includes the parent.
 "M01b-send-recheck-includes-parent": ([("                key = (pid, start, signum)\n",
                                         "                if _identity(pid) != (_parent, start):\n                    continue\n                key = (pid, start, signum)\n")], "suite", "probe"),
 # Both halves together, the whole pre-fix identity.
 "M01c-identity-includes-parent-both": ([("                    if (pid, start) not in initial:\n                        continue",
                                          "                    if initial.get((pid, start)) != _parent:\n                        continue"),
                                         ("                key = (pid, start, signum)\n",
                                          "                if _identity(pid) != (_parent, start):\n                    continue\n                key = (pid, start, signum)\n")], "suite", "red"),
 # Reap after census: judge the census as read, with no second reap.
 "M02-no-reap-after-census": ([("            reaped = self._reap()\n", "            reaped = set()\n")], "suite", "red"),
 # Pass-advanced clock: charge every pass in full.
 "M03-wall-clock": ([("clock += min(now - last, MAX_PASS_SECONDS)", "clock += now - last")], "suite", "red"),
 # The clamp value itself must matter: a 5 s clamp admits the control's 3.2 s stall.
 "M04-clamp-5s": ([("MAX_PASS_SECONDS = 0.5\n", "MAX_PASS_SECONDS = 5.0\n")], "suite", "red"),
 # Resumed-shell window: the resume no longer extends the kill time.
 "M05-no-trap-window": ([("                kill_all = max(kill_all, clock + TRAP_SECONDS)\n", "")], "suite", "red"),
 # Pre-fix root rule: a notified shell is killed at the kill time even if never resumed.
 "M06-root-killed-unresumed": ([("(resumed is None or clock < kill_all)", "clock < kill_all")], "suite", "red"),
 # A trap-started command no longer shares the resumed shell's window.
 "M07-trap-child-no-window": ([("                    if (pid, start) not in initial and resumed is not None:\n                        continue\n", "")], "suite", "red"),
 # Round 2 probe: the clamp at 1.5 s, the smallest that admits the stall control's 2 s stall in one pass.
 "M04c-clamp-1.5s": ([("MAX_PASS_SECONDS = 0.5\n", "MAX_PASS_SECONDS = 1.5\n")], "suite", "red"),
 # Round 2 probe: the clamp at 1.0 s, below what the stall control can see (expected green).
 "M04d-clamp-1.0s": ([("MAX_PASS_SECONDS = 0.5\n", "MAX_PASS_SECONDS = 1.0\n")], "suite", "probe"),
 # Round 2: a trap-started command shares the resumed shell's window for only 1 s.
 "M07b-trap-child-1s-window": ([("                    if (pid, start) not in initial and resumed is not None:\n",
                                 "                    if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:\n")], "suite", "red"),
 # SIGKILL before raising: removed.
 "M08-no-kill-before-fail": ([("                for pid, (_parent, start) in owned.items():\n                    self._send(pid, start, signal.SIGKILL)\n", "")], "suite", "red"),
 # SIGKILL before raising, but sparing the stopped shell.
 "M09-kill-before-fail-spares-shell": ([("                for pid, (_parent, start) in owned.items():\n                    self._send(pid, start, signal.SIGKILL)\n",
                                         "                for pid, (_parent, start) in owned.items():\n                    if self.process is None or pid != self.process.pid:\n                        self._send(pid, start, signal.SIGKILL)\n")], "suite", "red"),
 # Bounded endless listing: removed.
 "M10-endless-unbounded": ([("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):", "if clock >= limit and owned:")], "suite", "red"),
 # A survivor that was sent SIGKILL is trusted to be dead and never fails the run.
 "M11-trust-sigkill": ([("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
                         "if clock >= limit and (any(p not in killed and (self.process is None or p != self.process.pid) for p in owned) or not owned and clock >= limit + REAP_SECONDS):")], "suite", "red"),
 # The report loses state and wait channel.
 "M12-report-without-state": ([(" state {fields[0]} wchan {wchan} parent", " parent")], "suite", "red"),
 # Cleanup does nothing at all.
 "M13-cleanup-does-nothing-suite": ([("        started = last = time.monotonic()\n", "        return\n        started = last = time.monotonic()\n")], "suite", "red"),
 "M13-cleanup-does-nothing-lifecycle": ([("        started = last = time.monotonic()\n", "        return\n        started = last = time.monotonic()\n")], "lifecycle", "red"),
 # Pre-existing safety: signal without rechecking the start time.
 "M14-no-start-recheck": ([("            if identity is None or identity[1] != start:\n", "            if identity is None:\n")], "suite", "probe"),
 # The windows themselves: back to the pre-fix 2 s; no control is expected to see this.
 # Round 3 (#833): a resume again re-arms the trap window after the shell was collected.
 "M16-resume-collected-shell": ([("resumed is None and root_pid in owned and not (live - {root_pid}):", "resumed is None and not (live - {root_pid}):")], "suite", "red"),
 "M15-windows-2s": ([("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 2.0"), ("REAP_SECONDS = 10.0", "REAP_SECONDS = 2.0")], "suite", "probe"),
}
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]
TESTS = {"suite": (["python3", "scripts/test_suite_cancellation.py"], "."),
         "lifecycle": (["python3", "test_mutant_lifecycle.py"], "tb/verilator/gptp_shadow")}

def one(name):
    edits, test, expect = MUT[name]
    clone = work / name
    subprocess.run([str(HERE / "clone_at.sh"), src, sha, str(clone)], check=True)
    path = clone / TARGET
    text = path.read_text()
    for old, new in edits:
        text = sub(text, old, new)
    path.write_text(text)
    argv, cwd = TESTS[test]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(work / "tmp"))
    began = time.monotonic()
    with (out / f"{name}.log").open("w") as log:
        rc = subprocess.run(["timeout", "-k", "5", "400", *NS, *argv], cwd=clone / cwd, env=env,
                            stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (out / f"{name}.rc").write_text(f"{rc}\n")
    lines = [l for l in (out / f"{name}.log").read_text(errors="replace").splitlines() if l.strip()]
    got = "green" if rc == 0 else "red"
    return dict(name=name, test=test, expect=expect, rc=rc, got=got,
                seconds=round(time.monotonic() - began, 1), last=(lines[-1] if lines else "")[:240])

(work / "tmp").mkdir(exist_ok=True)
names = sys.argv[6:] or list(MUT)
rows = []
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for row in pool.map(one, names):
        rows.append(row)
        print(json.dumps(row), flush=True)
(out / "summary.json").write_text(json.dumps(rows, indent=1) + "\n")
