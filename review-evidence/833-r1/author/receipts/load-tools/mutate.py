#!/usr/bin/env python3
"""usage: mutate.py <clone> <receipts dir>. Scratch only. Reverts one fix at a time in the clone and requires the named control to go red.
Each run is in its own PID namespace, so whatever a mutant leaks dies with it."""
import json, subprocess, sys, time
from pathlib import Path
clone, out = Path(sys.argv[1]), Path(sys.argv[2])
P = clone / "scripts/owned_process.py"
good = P.read_text()
def sub(old, new, text=good):
    assert text.count(old) == 1, old
    return text.replace(old, new)
MUT = {
 "identity-includes-parent": sub('''            for pid, (_parent, start) in owned.items():
                # A notified shell''', '''            for pid, (_parent, start) in owned.items():
                if _identity(pid) != (_parent, start):
                    continue
                if signum != signal.SIGKILL and initial.get((pid, start)) != _parent:
                    continue
                # A notified shell'''),
 "no-reap-after-census": sub('''owned = {pid: entry for pid, entry in census.items() if pid not in reaped}''', '''owned = dict(census)'''),
 "deadline-is-wall-clock": sub('''clock += min(now - last, MAX_PASS_SECONDS)''', '''clock += now - last'''),
 "no-shell-window": sub('''                kill_all = max(kill_all, clock + TRAP_SECONDS)\n''', ''),
 "no-kill-before-fail": sub('''                for pid, (_parent, start) in owned.items():
                    self._send(pid, start, signal.SIGKILL)
                raise RuntimeError(''', '''                raise RuntimeError('''),
 "endless-listing-unbounded": sub('''if clock >= limit and (owned or clock >= limit + REAP_SECONDS):''', '''if clock >= limit and owned:'''),
 "survivor-does-not-fail": sub('''if clock >= limit and (owned or clock >= limit + REAP_SECONDS):''', '''if False:'''),
 "report-without-state": sub(''' state {fields[0]} wchan {wchan} parent''', ''' parent'''),
 "cleanup-does-nothing": sub('''        started = last = time.monotonic()
        clock = 0.0
''', '''        return
        started = last = time.monotonic()
        clock = 0.0
'''),
}
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]
env = dict(__import__("os").environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR="$VALIDATION_STORAGE/833-a726/tmp")
rows = []
def one(name, text, argv, cwd):
    P.write_text(text)
    log = out / f"{name}.log"
    began = time.monotonic()
    with log.open("w") as f:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, *argv], cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (out / f"{name}.rc").write_text(f"{rc}\n")
    tail = [l for l in log.read_text(errors="replace").splitlines() if l.strip()][-1:] or [""]
    rows.append(dict(mutant=name, rc=rc, seconds=round(time.monotonic() - began, 1), last=tail[0][:150]))
    print(json.dumps(rows[-1]), flush=True)
suite = (["python3", "scripts/test_suite_cancellation.py"], clone)
life = (["python3", "test_mutant_lifecycle.py"], clone / "tb/verilator/gptp_shadow")
one("control-unmutated-suite", good, *suite)
for name, text in MUT.items():
    one(name + "-suite", text, *suite)
one("cleanup-does-nothing-lifecycle", MUT["cleanup-does-nothing"], *life)
one("survivor-does-not-fail-lifecycle", MUT["survivor-does-not-fail"], *life)
one("control-unmutated-lifecycle", good, *life)
P.write_text(good)
(out / "summary.json").write_text(json.dumps(rows, indent=1) + "\n")
