#!/usr/bin/env python3
"""Independent reviewer probe: signal the production gPTP shadow mutation
driver (entry or its process group) at the mutation-applied handshake.

Usage: probe_campaign_stops.py CLONE SCRATCH OUTPUT_JSON

The caller checkout is a disposable clone of the review clone at the exact
head, with the two required submodules initialised from the clone's local
module repositories. `mutants.py`, `private_inputs.py` and `owned_process.py`
run unmodified from that checkout. Only `make run` is synthetic (on PATH);
`make print-inputs` is forwarded to real make. The synthetic build records
which planted mutation it sees, starts a detached TERM/INT/HUP-ignoring
grandchild, publishes a handshake file and holds until released.
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

HEAD = "26353960ae2763cc09741d0f7bcc720621bd5148"

MAKE = r'''#!/usr/bin/env python3
import hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent
if "print-inputs" in sys.argv:
    real = shutil.which("make", path=os.pathsep.join(
        e for e in os.environ["PATH"].split(os.pathsep) if Path(e).resolve() != here))
    os.execv(real, [real, *sys.argv[1:]])
control = Path(os.environ["PROBE_CONTROL"])
private = Path.cwd().parents[2]
txret = (private / "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv").read_text()
seen = "abort_counts_as_completion" if "(epi_done_i || !epi_busy_i) && epi_cover_r" in txret else "other"
with (control / "seen").open("a") as f:
    f.write(f"{seen} {os.getpid()}\n")
if (control / "seen").read_text().count("\n") > 1:
    # a later mutation build started: record it and complete quickly
    print("1 checks: 0 PASS, 1 FAIL"); raise SystemExit(1)
child = subprocess.Popen([sys.executable, str(control / "stubborn.py")], start_new_session=True)
while not (control / "stubborn-ready").exists():
    time.sleep(0.01)
(control / "ready.tmp").write_text(json.dumps({"held": os.getpid(), "stubborn": child.pid, "private": str(private)}))
(control / "ready.tmp").replace(control / "ready.json")
while not (control / "release").exists():
    time.sleep(0.02)
print("FAIL aborted episode: the demand survives it got 0 exp 1")
print("1 checks: 0 PASS, 1 FAIL")
raise SystemExit(1)
'''

STUBBORN = r'''
import os, signal, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(s, signal.SIG_IGN)
(control / "stubborn-ready").write_text(str(os.getpid()))
while not (control / "release").exists():
    time.sleep(0.02)
'''


def run(argv, **kw):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv, env=env, capture_output=True, check=True, **kw)


def build_caller(clone, dest):
    run(["git", "clone", "-q", "--no-local", "--no-checkout", str(clone), str(dest)])
    run(["git", "-C", str(dest), "checkout", "-q", "--detach", HEAD])
    for name in ("gptp-processor", "third_party/verilog-axis"):
        run(["git", "-C", str(dest), "config", f"submodule.{name}.url", str(clone / ".git/modules" / name)])
        run(["git", "-C", str(dest), "-c", "protocol.file.allow=always", "submodule", "update", "-q", "--init", "--", name])


def snapshot(root):
    """Index records plus on-disk bytes/modes of every tracked file, recursing into the two submodules."""
    out = {}
    for repo, prefix in ((root, ""), (root / "gptp-processor", "gptp-processor/"),
                         (root / "third_party/verilog-axis", "third_party/verilog-axis/")):
        idx = run(["git", "--no-optional-locks", "-C", str(repo), "ls-files", "--stage", "-z"]).stdout
        out[prefix + "<index>"] = hashlib.sha256(idx).hexdigest()
        for row in idx.split(b"\0"):
            if not row:
                continue
            meta, name = row.split(b"\t", 1)
            if meta.startswith(b"160000"):
                continue
            p = repo / os.fsdecode(name)
            st = p.lstat()
            out[prefix + os.fsdecode(name)] = (st.st_mode, hashlib.sha256(p.read_bytes()).hexdigest())
    return out


def stat_fields(pid):
    try:
        return (Path("/proc") / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
    except (FileNotFoundError, ProcessLookupError):
        return None


def identity(pid):
    f = stat_fields(pid)
    return None if f is None else (f[19], f[0], int(f[1]))


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


def kill_identity(pid, start):
    try:
        fd = os.pidfd_open(pid)
    except ProcessLookupError:
        return
    try:
        i = identity(pid)
        if i and i[0] == start:
            signal.pidfd_send_signal(fd, signal.SIGKILL)
    finally:
        os.close(fd)


def case(caller, before, parent, how, signame):
    label = f"campaign-{how}-{signame}"
    control = parent / label
    control.mkdir(parents=True)
    (control / "bin").mkdir()
    (control / "bin/make").write_text(MAKE)
    (control / "bin/make").chmod(0o755)
    (control / "stubborn.py").write_text(STUBBORN)
    tmp = control / "tmp"
    tmp.mkdir()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(PROBE_CONTROL=str(control), PATH=str(control / "bin") + os.pathsep + os.environ["PATH"],
               TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    foreign_id = identity(foreign.pid)
    log = open(control / "driver.log", "wb")
    entry = subprocess.Popen([sys.executable, str(caller / "tb/verilator/gptp_shadow/mutants.py")],
                             cwd=caller, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    assert wait_for(lambda: (control / "ready.json").exists() or entry.poll() is not None, 60), label
    assert entry.poll() is None, (control / "driver.log").read_text()
    ready = json.loads((control / "ready.json").read_text())
    held, stub, private = ready["held"], ready["stubborn"], Path(ready["private"])
    held_id, stub_id = identity(held), identity(stub)
    rec = {"label": label, "target": how, "signal": signame,
           "caller_unchanged_at_handshake": snapshot(caller) == before,
           "private_is_under_tmp": str(private).startswith(str(tmp)),
           "held_parent_is_entry": held_id[2] == entry.pid}
    signum = getattr(signal, signame)
    if how == "group":
        os.killpg(entry.pid, signum)
    else:
        fd = os.pidfd_open(entry.pid)
        signal.pidfd_send_signal(fd, signum)
        os.close(fd)
    status = entry.wait(timeout=30)
    rec["status"] = status
    rec["at_status"] = {"held_running": running(held, held_id[0]), "stubborn_running": running(stub, stub_id[0]),
                        "private_exists": private.exists()}
    rec["held_gone_within_5s"] = wait_for(lambda: not running(held, held_id[0]), 5)
    (control / "release").write_text("go\n")
    rec["stubborn_gone_within_10s"] = wait_for(lambda: not running(stub, stub_id[0]), 10)
    time.sleep(2)
    text = (control / "driver.log").read_text(errors="replace")
    rec["seen"] = (control / "seen").read_text().split("\n")
    rec["later_mutation_started"] = len([s for s in rec["seen"] if s]) > 1
    rec["result_line"] = "RESULT:" in text or "controls:" in text
    rec["cancelled_line"] = "CANCELLED:" in text
    rec["transcript"] = text
    rec["caller_unchanged_after"] = snapshot(caller) == before
    rec["scratch_left"] = sorted(p.name for p in tmp.iterdir())
    fcur = identity(foreign.pid)
    rec["foreign_preserved"] = foreign.poll() is None and fcur is not None and fcur[0] == foreign_id[0] and fcur[1] != "Z"
    foreign.kill()
    foreign.wait()
    for pid, ident in ((held, held_id), (stub, stub_id)):
        if running(pid, ident[0]):
            kill_identity(pid, ident[0])
    return rec


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    caller = scratch / "caller"
    build_caller(clone, caller)
    before = snapshot(caller)
    cases = []
    for how in ("entry", "group"):
        for signame in ("SIGKILL", "SIGHUP", "SIGTERM", "SIGINT", "SIGALRM", "SIGUSR1"):
            c = case(caller, before, scratch, how, signame)
            cases.append(c)
            print(f"{c['label']:26s} status={c['status']:4d} caller_same={c['caller_unchanged_at_handshake']}/"
                  f"{c['caller_unchanged_after']} make@status={c['at_status']['held_running']} "
                  f"make_gone5s={c['held_gone_within_5s']} stub@status={c['at_status']['stubborn_running']} "
                  f"private@status={c['at_status']['private_exists']} later={c['later_mutation_started']} "
                  f"result={c['result_line']} scratch_left={c['scratch_left']} foreign={c['foreign_preserved']}",
                  flush=True)
    output.write_text(json.dumps(cases, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
