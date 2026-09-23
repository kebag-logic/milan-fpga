#!/usr/bin/env python3
"""Independent reviewer probe, two sweep edge cases not in the hard-stop set:

1. job-control suspend (SIGTSTP, and uncatchable SIGSTOP) of the launched
   entry at the first-suite handshake: does the loop pause, or do later
   suites run while the caller's job is stopped?
2. INT/TERM while the final summary's tally is running: what has already
   been printed when the CANCELLED lines appear?

Usage: probe_sweep_extra.py CLONE SCRATCH OUTPUT_JSON
Production run_all_suites.sh / owned_process.py / suite_shards.py /
suite_tally.py(+selftest module) are copied byte for byte; make and the
expensive prerequisites are synthetic; the summary tally is wrapped by a shim
that holds at a handshake only when called as the final `--quiet` tally.
"""
import json
import os
import runpy  # noqa: F401  (documented dependency of the shim)
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_sweep_stops import MAKE, STUBBORN, blob, head_blob, identity, running, wait_for  # noqa: E402

TALLY_SHIM = r'''
import os, runpy, sys, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if "--selftest" in sys.argv:
    raise SystemExit(0)  # prerequisite self-test replaced, as the other prerequisites are
if "--quiet" in sys.argv and os.environ.get("PROBE_PHASE") == "summary":
    (control / "ready.json").write_text('{"held": %d}' % os.getpid())
    while not (control / "release").exists():
        time.sleep(0.02)
runpy.run_path(str(Path(__file__).resolve().parent / "real_suite_tally.py"), run_name="__main__")
'''


def fixture(clone, parent, label, shim_tally):
    root = parent / label / "root"
    control = parent / label / "control"
    for d in (root / "scripts", root / "syn/yosys", control / "bin"):
        d.mkdir(parents=True)
    for name in ("scripts/run_all_suites.sh", "scripts/owned_process.py", "scripts/suite_shards.py",
                 "scripts/suite_tally.py", "scripts/suite_tally_selftest.py"):
        data = (clone / name).read_bytes()
        assert blob(data) == head_blob(clone, name), name
        (root / name).write_bytes(data)
        (root / name).chmod((clone / name).stat().st_mode & 0o777)
    if shim_tally:
        (root / "scripts/suite_tally.py").rename(root / "scripts/real_suite_tally.py")
        (root / "scripts/suite_tally.py").write_text(TALLY_SHIM)
    for name in ("check_merge_containment", "check_results_fresh", "xvlog_gate", "check_merge_review_integrity",
                 "test_suite_cancellation"):
        (root / f"scripts/{name}.py").write_text("print('bounded prerequisite fixture')\n")
    (root / "syn/yosys/check_list_hermetic.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
    (root / "syn/yosys/check_list_hermetic.sh").chmod(0o755)
    for suite in ("alpha", "beta", "omega"):
        (root / f"tb/verilator/{suite}").mkdir(parents=True)
        (root / f"tb/verilator/{suite}/Makefile").write_text("all:\n\t@echo fixture\n")
    (control / "bin/make").write_text(MAKE)
    (control / "bin/make").chmod(0o755)
    (control / "stubborn.py").write_text(STUBBORN)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in ("SUITE_TIMEOUT", "SUITE_SWEEP_LOCK")}
    env.update(PROBE_CONTROL=str(control), PATH=str(control / "bin") + os.pathsep + os.environ["PATH"],
               PYTHONDONTWRITEBYTECODE="1")
    return root, control, env


def send(pid, signum):
    fd = os.pidfd_open(pid)
    try:
        signal.pidfd_send_signal(fd, signum)
    finally:
        os.close(fd)


def suspend_case(clone, parent, signame):
    label = f"suspend-{signame}"
    root, control, env = fixture(clone, parent, label, shim_tally=False)
    env["PROBE_PHASE"] = "command"
    log = open(parent / label / "driver.log", "wb")
    entry = subprocess.Popen(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs")], cwd=root,
                             env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    assert wait_for(lambda: (control / "ready.json").exists(), 20)
    send(entry.pid, getattr(signal, signame))
    stopped = wait_for(lambda: identity(entry.pid) and identity(entry.pid)[1] == "T", 5)
    (control / "release").write_text("go\n")
    later_while_stopped = bool(wait_for(lambda: (control / "next-suite-omega").exists(), 10))
    text_while_stopped = (parent / label / "driver.log").read_text()
    entry_still_stopped = identity(entry.pid)[1] == "T"
    send(entry.pid, signal.SIGCONT)
    status = entry.wait(timeout=30)
    return {"label": label, "entry_stopped": bool(stopped), "entry_still_stopped_when_checked": entry_still_stopped,
            "later_suites_ran_while_entry_stopped": later_while_stopped,
            "summary_printed_while_entry_stopped": any(l.startswith("suites: ") for l in text_while_stopped.splitlines()),
            "final_status": status, "transcript": (parent / label / "driver.log").read_text()}


def summary_case(clone, parent, signame):
    label = f"summary-{signame}"
    root, control, env = fixture(clone, parent, label, shim_tally=True)
    env["PROBE_PHASE"] = "summary"
    log = open(parent / label / "driver.log", "wb")
    entry = subprocess.Popen(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs")], cwd=root,
                             env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    assert wait_for(lambda: (control / "ready.json").exists(), 30), (parent / label / "driver.log").read_text()
    held = json.loads((control / "ready.json").read_text())["held"]
    held_id = identity(held)
    send(entry.pid, getattr(signal, signame))
    status = entry.wait(timeout=30)
    text = (parent / label / "driver.log").read_text()
    return {"label": label, "status": status, "held_tally_running_at_status": running(held, held_id[0]),
            "suites_line_printed": any(l.startswith("suites: ") for l in text.splitlines()),
            "checks_line_printed": "checks:" in text, "logs_line_printed": "\nlogs:" in text,
            "cancelled_lines": [l for l in text.splitlines() if "CANCELLED" in l or l.startswith("partial logs")],
            "transcript": text}


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    results = [suspend_case(clone, scratch, s) for s in ("SIGTSTP", "SIGSTOP")]
    results += [summary_case(clone, scratch, s) for s in ("SIGTERM", "SIGINT")]
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if k != "transcript"}))
    output.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
