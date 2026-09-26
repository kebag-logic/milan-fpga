#!/usr/bin/env python3
"""Reviewer mutation driver for PR #524 at the head under review.

    mutate.py SUITE_DIR OUTDIR NAME...
Each mutant rewrites ONE tracked file in place (exact-string substitution that
must match once, or a whole-blob replacement from git), runs the named test
scripts under a guard, then restores the exact original bytes and re-verifies
their sha256 before the next mutant. A mutant is KILLED by an assertion when a
script exits non-zero with at least one [FAIL] line or failing assertion, and
HANG when only the guard stopped it (reported separately, never as PASS).
"""
import hashlib
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

SUITE, OUT, NAMES = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3:]
REPO = SUITE.parents[2]
GUARD = 240
UNIT, BP = "test_sim_pool.py", "test_sim_pool_backpressure.py"

MUTANTS = {
    # runner
    "R0-r245-1-runner-761ec858": ("sim_pool.py", "blob:761ec858", None, [BP], "default"),
    "R1-no-exclusion": ("sim_pool.py", "group_busy = any(leg.exclusive for leg in running)",
                        "group_busy = False", [UNIT], "default"),
    "R2-no-independent-overlap": ("sim_pool.py", "if not leg.exclusive or not group_busy), None)",
                                  "if not group_busy), None)", [UNIT], "default"),
    "R3-blocking-stdout": ("sim_pool.py", "        os.set_blocking(self.fd, False)\n",
                           "", [BP], "default"),
    "R4-flags-not-restored": ("sim_pool.py", "            os.set_blocking(self.fd, blocking)\n",
                              "            pass\n", [BP], "default"),
    "R5-final-drain-waits": ("sim_pool.py", "replay.drain(wait=interrupt is None)",
                             "replay.drain(wait=True)", [BP], "default"),
    # recipe
    "M1-restore-one-exclusive-mark": ("Makefile", "\t  ./obj_nxn/Vmilan_dp_nxn \\\n",
                                      "\t  --exclusive ./obj_nxn/Vmilan_dp_nxn \\\n", [UNIT], "default"),
    "M2-drop-crflic": ("Makefile", "\t  ./$(CRFLIC_MDIR)/Vmilan_dp_crflic \\\n", "", [UNIT, BP], "default"),
    "M3-default-one-worker": ("Makefile", "SIM_JOBS ?= 2", "SIM_JOBS ?= 1", [UNIT], "default"),
    # the F2 fixture correction must be load-bearing under an inherited ignore
    "T0-round4-fixture-f36b40dd-ign-int": (BP, "blob:3d9d9c9a937af8c7e9f98594fa028b86ef0d7d0f",
                                           None, [BP], "ign-int"),
    "T1-no-signal-state-ign-int": (BP, "start_new_session=True,\n                                           preexec_fn=signal_state)",
                                   "start_new_session=True)", [BP], "ign-int"),
}


def state(mode: str):
    def apply() -> None:
        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(s, signal.SIG_DFL)
        signal.pthread_sigmask(signal.SIG_SETMASK, set())
        if mode == "ign-int":
            signal.signal(signal.SIGINT, signal.SIG_IGN)
        os.setsid()
    return apply


def run_script(script: str, mode: str, log: Path) -> dict:
    p = subprocess.Popen([sys.executable, script], cwd=SUITE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, preexec_fn=state(mode))
    try:
        out, _ = p.communicate(timeout=GUARD)
        verdict = None
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, _ = p.communicate()
        verdict = "HANG"
    text = out.decode(errors="replace")
    log.write_text(text)
    fails = [l for l in text.splitlines() if l.startswith("[FAIL]") or "AssertionError" in l]
    if verdict is None:
        verdict = ("KILLED" if fails else "KILLED-NONZERO") if p.returncode else "SURVIVED"
    last = text.strip().splitlines()[-1] if text.strip() else ""
    return {"script": script, "exit": p.returncode, "verdict": verdict,
            "fail_lines": len(fails), "last": last[:200]}


OUT.mkdir(parents=True, exist_ok=True)
for name in NAMES:
    rel, old, new, scripts, mode = MUTANTS[name]
    path = SUITE / rel
    original = path.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    if old.startswith("blob:"):
        mutated = subprocess.run(["git", "-C", str(REPO), "cat-file", "blob", old[5:]],
                                 check=True, capture_output=True).stdout
    else:
        assert text.count(old) == 1, f"{name}: anchor matches {text.count(old)} times"
        mutated = text.replace(old, new).encode()
    try:
        path.write_bytes(mutated)
        rows = [run_script(s, mode, OUT / f"{name}--{s}.log") for s in scripts]
    finally:
        path.write_bytes(original)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"{name}: restore failed"
    print(json.dumps({"mutant": name, "file": rel, "mode": mode, "results": rows}), flush=True)
