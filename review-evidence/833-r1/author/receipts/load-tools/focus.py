#!/usr/bin/env python3
"""usage: focus.py <worktree> <out jsonl> <budget s> [case ...]

Scratch only. Loops the real cancellation and interruption cases from the production tests, so cleanups happen many
times a minute. Each case's outcome and its exception text go to one JSON line. No test logic is changed.
"""
import json, os, signal, sys, tempfile, time, traceback, shutil
from pathlib import Path
tree, out, budget = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
cases = sys.argv[4:] or ["cancel-selection", "cancel-preflight", "cancel-command", "cancel-transition", "interrupt-KILL"]
sys.path.insert(0, str(tree / "scripts"))
sys.path.insert(0, str(tree / "tb/verilator/gptp_shadow"))
os.chdir(tree)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import test_suite_cancellation as suite
import test_mutant_lifecycle as lifecycle
from owned_process import OwnedProcesses

def one(parent, case):
    if case.startswith("cancel-"):
        phase, _, name = case.removeprefix("cancel-").partition(":")
        suite.cancellation(parent, phase, getattr(signal, name or "SIGTERM"))
    elif case == "interrupt-KILL":
        with OwnedProcesses():
            lifecycle.interrupted(parent, signal.SIGKILL)
    elif case == "interrupt-TERM":
        lifecycle.interrupted(parent, signal.SIGTERM)
    elif case == "nested-TERM":
        lifecycle.outer_cancellation(parent, signal.SIGTERM)
    else:
        raise SystemExit("unknown case " + case)

start = time.monotonic()
n = 0
tally = {}
devnull = os.open(os.devnull, os.O_WRONLY)
with out.open("a") as record, OwnedProcesses():
    while time.monotonic() - start < budget:
        for case in cases:
            with tempfile.TemporaryDirectory(prefix="focus-") as scratch:
                began = time.monotonic()
                saved = os.dup(1); os.dup2(devnull, 1)
                try:
                    one(Path(scratch).resolve(), case)
                    outcome, text = "pass", ""
                except BaseException as exc:
                    outcome = type(exc).__name__
                    text = str(exc)[-3000:]
                finally:
                    os.dup2(saved, 1); os.close(saved)
                row = dict(n=n, case=case, outcome=outcome, seconds=round(time.monotonic() - began, 2),
                           load=Path("/proc/loadavg").read_text().split()[0], text=text)
                record.write(json.dumps(row) + "\n"); record.flush()
                tally[(case, outcome)] = tally.get((case, outcome), 0) + 1
                n += 1
print({f"{k[0]}:{k[1]}": v for k, v in tally.items()})
