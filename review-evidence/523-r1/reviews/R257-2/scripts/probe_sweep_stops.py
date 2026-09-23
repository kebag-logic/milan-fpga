#!/usr/bin/env python3
"""Independent reviewer probe: signal the production sweep entry, or its
process group, at observable boundaries and record what survives.

Usage: probe_sweep_stops.py CLONE SCRATCH OUTPUT_JSON

The fixture copies the production `scripts/run_all_suites.sh` and
`scripts/owned_process.py` byte for byte (checked against the clone's HEAD
blobs) and the real `suite_shards.py` / `suite_tally.py`. Only `make` (on
PATH) and the expensive prerequisite self-tests are synthetic. Three suites
exist: alpha (holds at a handshake with a detached, TERM/INT-ignoring
grandchild), beta and omega (write next-suite sentinels). Nothing here uses
a sleep as an oracle: handshakes are files written by the held command.
"""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

MAKE = r'''#!/usr/bin/env python3
import json, os, signal, subprocess, sys, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
suite = Path(sys.argv[sys.argv.index("-C") + 1]).name
with (control / "events").open("a") as ev:
    ev.write(f"start {suite} {os.getpid()}\n")
if suite != "alpha":
    (control / f"next-suite-{suite}").write_text("executed\n")
    print("1 checks: 1 PASS, 0 FAIL", flush=True)
    raise SystemExit(0)
print("PARTIAL: alpha entered", flush=True)
if os.environ.get("PROBE_PHASE") != "command":
    print("1 checks: 1 PASS, 0 FAIL", flush=True)
    raise SystemExit(0)
child = subprocess.Popen([sys.executable, str(control / "stubborn.py")], start_new_session=True)
while not (control / "stubborn-ready").exists():
    time.sleep(0.01)
(control / "ready.tmp").write_text(json.dumps({"held": os.getpid(), "stubborn": child.pid}))
(control / "ready.tmp").replace(control / "ready.json")
while not (control / "release").exists():
    time.sleep(0.02)
print("1 checks: 1 PASS, 0 FAIL", flush=True)
'''

STUBBORN = r'''
import os, signal, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
signal.signal(signal.SIGHUP, signal.SIG_IGN)
(control / "stubborn-ready").write_text(str(os.getpid()))
while not (control / "release").exists():
    time.sleep(0.02)
'''

# Holds a preflight prerequisite at a handshake (the preflight phase).
HOLD_PREFLIGHT = r'''
import json, os, subprocess, sys, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if os.environ.get("PROBE_PHASE") == "preflight":
    child = subprocess.Popen([sys.executable, str(control / "stubborn.py")], start_new_session=True)
    while not (control / "stubborn-ready").exists():
        time.sleep(0.01)
    (control / "ready.tmp").write_text(json.dumps({"held": os.getpid(), "stubborn": child.pid}))
    (control / "ready.tmp").replace(control / "ready.json")
    while not (control / "release").exists():
        time.sleep(0.02)
print("bounded prerequisite fixture")
'''


def stat_fields(pid):
    try:
        return (Path("/proc") / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
    except (FileNotFoundError, ProcessLookupError):
        return None


def identity(pid):
    f = stat_fields(pid)
    return None if f is None else (f[19], f[0], int(f[1]), int(f[2]), int(f[3]))  # start, state, ppid, pgrp, sid


def running(pid, start):
    i = identity(pid)
    return i is not None and i[0] == start and i[1] != "Z"


def wait_for(cond, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if cond():
            return True
        time.sleep(0.02)
    return cond()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def head_blob(clone, name):
    out = subprocess.run(["git", "-C", str(clone), "ls-tree", "HEAD", "--", name], capture_output=True,
                         text=True, check=True, env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    return out.stdout.split()[2]


def fixture(clone, parent, label):
    root = parent / label / "root"
    control = parent / label / "control"
    (root / "scripts").mkdir(parents=True)
    (root / "syn/yosys").mkdir(parents=True)
    control.mkdir(parents=True)
    for name in ("scripts/run_all_suites.sh", "scripts/owned_process.py", "scripts/suite_shards.py",
                 "scripts/suite_tally.py", "scripts/suite_tally_selftest.py"):
        data = (clone / name).read_bytes()
        assert blob(data) == head_blob(clone, name), name
        (root / name).write_bytes(data)
        (root / name).chmod((clone / name).stat().st_mode & 0o777)
    for name in ("check_merge_containment", "check_results_fresh", "xvlog_gate",
                 "check_merge_review_integrity"):
        (root / f"scripts/{name}.py").write_text(
            HOLD_PREFLIGHT if name == "check_merge_containment" else "print('bounded prerequisite fixture')\n")
    (root / "scripts/test_suite_cancellation.py").write_text("print('reviewer fixture: recursion replaced')\n")
    (root / "syn/yosys/check_list_hermetic.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
    (root / "syn/yosys/check_list_hermetic.sh").chmod(0o755)
    for suite in ("alpha", "beta", "omega"):
        (root / f"tb/verilator/{suite}").mkdir(parents=True)
        (root / f"tb/verilator/{suite}/Makefile").write_text("all:\n\t@echo fixture\n")
    (control / "bin").mkdir()
    (control / "bin/make").write_text(MAKE)
    (control / "bin/make").chmod(0o755)
    (control / "stubborn.py").write_text(STUBBORN)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in ("SUITE_TIMEOUT", "SUITE_SWEEP_LOCK")}
    env.update(PROBE_CONTROL=str(control), PATH=str(control / "bin") + os.pathsep + os.environ["PATH"],
               PYTHONDONTWRITEBYTECODE="1")
    return root, control, env


def sweep_shell_of(entry):
    """The bash child of the entry owner that carries --owned-sweep."""
    for p in Path("/proc").iterdir():
        if p.name.isdecimal():
            f = stat_fields(int(p.name))
            if f and int(f[1]) == entry:
                try:
                    cmd = (p / "cmdline").read_bytes().split(b"\0")
                except OSError:
                    continue
                if b"--owned-sweep" in cmd:
                    return int(p.name)
    return None


def kill_identity(pid, start):
    """Reviewer containment: SIGKILL an exact identity via pidfd."""
    try:
        fd = os.pidfd_open(pid)
    except ProcessLookupError:
        return False
    try:
        i = identity(pid)
        if i and i[0] == start:
            signal.pidfd_send_signal(fd, signal.SIGKILL)
            return True
    finally:
        os.close(fd)
    return False


def run_case(clone, parent, phase, how, signame):
    label = f"{phase}-{how}-{signame}"
    root, control, env = fixture(clone, parent, label)
    env["PROBE_PHASE"] = phase
    signum = getattr(signal, signame)
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    foreign_id = identity(foreign.pid)
    lock_holder = None
    if phase == "lockwait":
        lock_holder = subprocess.Popen(["flock", str(root / ".run_all_suites.lock"), "-c",
                                        f"touch {control}/lock-held; while [ ! -e {control}/release-lock ]; do sleep 0.05; done"],
                                       start_new_session=True)
        assert wait_for(lambda: (control / "lock-held").exists(), 10)
    out = open(parent / label / "driver.log", "wb")
    argv = ["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs")]
    if phase == "lockwait":
        argv.append("--wait")
    entry = subprocess.Popen(argv, cwd=root, env=env, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    rec = {"label": label, "phase": phase, "target": how, "signal": signame, "entry": entry.pid}
    # Boundary
    if phase in ("command", "preflight"):
        assert wait_for(lambda: (control / "ready.json").exists() or entry.poll() is not None, 20), label
        assert entry.poll() is None, (parent / label / "driver.log").read_text()
        ready = json.loads((control / "ready.json").read_text())
        held, stub = ready["held"], ready["stubborn"]
        held_id, stub_id = identity(held), identity(stub)
        rec["held"] = [held, held_id]
        rec["stubborn"] = [stub, stub_id]
    else:
        # lock wait: the shell's flock child blocks on the held lock
        def flock_child():
            sh = sweep_shell_of(entry.pid)
            if sh is None:
                return None
            for p in Path("/proc").iterdir():
                if p.name.isdecimal():
                    f = stat_fields(int(p.name))
                    if f and int(f[1]) == sh:
                        try:
                            if (p / "comm").read_text().strip() == "flock":
                                return int(p.name)
                        except OSError:
                            pass
            return None
        assert wait_for(lambda: flock_child() is not None, 20), (parent / label / "driver.log").read_text()
        held = flock_child()
        held_id = identity(held)
        rec["held"] = [held, held_id]
        stub, stub_id = None, None
    shell = sweep_shell_of(entry.pid)
    shell_id = identity(shell)
    rec["shell"] = [shell, shell_id]
    rec["entry_identity"] = identity(entry.pid)
    rec["shell_in_new_session"] = shell_id[4] != rec["entry_identity"][4]
    t0 = time.monotonic()
    if how == "group":
        os.killpg(entry.pid, signum)
    else:
        fd = os.pidfd_open(entry.pid)
        signal.pidfd_send_signal(fd, signum)
        os.close(fd)
    status = entry.wait(timeout=30)
    rec["caller_status"] = status
    rec["caller_seconds"] = round(time.monotonic() - t0, 3)
    at_death = (parent / label / "driver.log").read_bytes()
    # State of owned identities at the moment the caller sees the status
    rec["at_status"] = {
        "shell_running": running(shell, shell_id[0]),
        "held_running": running(held, held_id[0]),
        "stubborn_running": running(stub, stub_id[0]) if stub else None,
        "held_identity": identity(held),
        "stubborn_identity": identity(stub) if stub else None,
    }
    rec["shell_gone_within_5s"] = wait_for(lambda: not running(shell, shell_id[0]), 5)
    # Release every held command, as a still-running suite would finish.
    (control / "release").write_text("go\n")
    if lock_holder:
        (control / "release-lock").write_text("go\n")
        lock_holder.wait(timeout=10)
    rec["held_finished_within_10s"] = wait_for(lambda: not running(held, held_id[0]), 10)
    if stub:
        rec["stubborn_finished_within_10s"] = wait_for(lambda: not running(stub, stub_id[0]), 10)
    # Quiet period measured by observable state: give any detached loop a
    # full chance to reach the next suite; the sentinels are the oracle.
    time.sleep(3)
    after = (parent / label / "driver.log").read_bytes()[len(at_death):]
    text = (parent / label / "driver.log").read_text(errors="replace")
    rec["next_suite_beta"] = (control / "next-suite-beta").exists()
    rec["next_suite_omega"] = (control / "next-suite-omega").exists()
    rec["events"] = (control / "events").read_text().split("\n") if (control / "events").exists() else []
    rec["summary_line"] = any(line.startswith("suites: ") for line in text.splitlines())
    rec["output_after_status"] = after.decode(errors="replace")
    rec["cancelled_line"] = "CANCELLED:" in text
    rec["transcript"] = text
    logs = root / "logs"
    rec["logs"] = sorted(str(p.relative_to(logs)) for p in logs.rglob("*")) if logs.exists() else None
    alpha = logs / "alpha.log"
    rec["alpha_log"] = alpha.read_text() if alpha.exists() else None
    rec["lock_owner_file_left"] = (root / ".run_all_suites.lock.owner").exists()
    fcur = identity(foreign.pid)
    rec["foreign_preserved"] = foreign.poll() is None and fcur is not None and fcur[0] == foreign_id[0] and fcur[1] != "Z"
    foreign.kill()
    foreign.wait()
    # reviewer containment of anything still running from this case
    leftovers = []
    for pid, ident in ((held, held_id), (stub, stub_id), (shell, shell_id)):
        if pid and running(pid, ident[0]):
            leftovers.append(pid)
            kill_identity(pid, ident[0])
    rec["reviewer_contained"] = leftovers
    # A second sweep in the same tree must be able to take the lock again.
    (control / "release").write_text("go\n")
    env2 = dict(env, PROBE_PHASE="none")
    second = subprocess.run(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs2")], cwd=root, env=env2,
                            capture_output=True, text=True, timeout=60)
    rec["second_sweep_status"] = second.returncode
    rec["second_sweep_summary"] = [l for l in second.stdout.splitlines() if l.startswith("suites: ")]
    return rec


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    cases = []
    for phase in ("command", "preflight", "lockwait"):
        for how in ("entry", "group"):
            for signame in ("SIGKILL", "SIGHUP", "SIGTERM", "SIGINT", "SIGALRM", "SIGUSR1"):
                if phase == "lockwait" and signame in ("SIGALRM", "SIGUSR1"):
                    continue
                cases.append(run_case(clone, scratch, phase, how, signame))
                c = cases[-1]
                print(f"{c['label']:28s} status={c['caller_status']:4d} shell_gone={c['shell_gone_within_5s']} "
                      f"beta={c['next_suite_beta']} omega={c['next_suite_omega']} summary={c['summary_line']} "
                      f"held@status={c['at_status']['held_running']} stub@status={c['at_status']['stubborn_running']} "
                      f"after={c['output_after_status']!r:.60} foreign={c['foreign_preserved']} "
                      f"lockowner={c['lock_owner_file_left']} second={c['second_sweep_status']}", flush=True)
    output.write_text(json.dumps(cases, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
