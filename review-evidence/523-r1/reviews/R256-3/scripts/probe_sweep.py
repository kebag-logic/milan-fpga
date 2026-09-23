#!/usr/bin/env python3
"""Reviewer-owned process probes of the sweep entry (scripts/run_all_suites.sh).

Independent of the lane's fixture helpers: this file builds its own disposable
roots from the exact-head blobs (`git show HEAD:<path>` of the review clone),
uses real GNU make, the real driver, owner, tally and selector, and its own
/proc identity oracle. Only preflight prerequisite scripts are replaced by
bounded stubs, and a `hold` point is inserted with a published handshake.

Usage: probe_sweep.py CLONE WORKDIR RECEIPT.json
"""
import fcntl, json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()

HOLDER = r'''
import json, os, signal, subprocess, sys, time
from pathlib import Path
probe = Path(os.environ["RPROBE"])
tag = sys.argv[1]
if tag == "a1" and os.environ.get("RHOLD", "") not in ("", "command"):
    print("PARTIAL a1 started (not the hold point)", flush=True)
    print("1 checks: 1 PASS, 0 FAIL", flush=True)
    raise SystemExit(0)
if len(sys.argv) > 2 and sys.argv[2] == "stubborn":
    for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(s, signal.SIG_IGN)
    (probe / f"{tag}-stubborn-ready").write_text(str(os.getpid()))
    while True:
        time.sleep(0.05)
print(f"PARTIAL {tag} started pid={os.getpid()}", flush=True)
plain = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
detached = subprocess.Popen([sys.executable, __file__, tag, "stubborn"], start_new_session=True)
t = time.monotonic() + 20
while not (probe / f"{tag}-stubborn-ready").exists():
    assert time.monotonic() < t
    time.sleep(0.01)
(probe / f"{tag}-hold.tmp").write_text(json.dumps(dict(pid=os.getpid(), plain=plain.pid, detached=detached.pid)))
os.replace(probe / f"{tag}-hold.tmp", probe / f"{tag}-hold.json")
while not (probe / "release").exists():
    time.sleep(0.02)
plain.kill(); plain.wait()
print("1 checks: 1 PASS, 0 FAIL", flush=True)
'''

SENTINEL = r'''
import os, sys
from pathlib import Path
Path(os.environ["RPROBE"], "ran-" + sys.argv[1]).write_text("executed\n")
print("1 checks: 1 PASS, 0 FAIL", flush=True)
'''

# Wraps a real tool: hold at a chosen boundary, otherwise run the real one.
WRAP = r'''
import os, runpy, subprocess, sys
from pathlib import Path
probe = Path(os.environ["RPROBE"])
hold = os.environ.get("RHOLD", "")
if "--selftest" in sys.argv:
    print("{tool} selftest stub (prerequisite, not under test)", flush=True)
    raise SystemExit(0)
if (hold == "selection" and "{tool}" == "suite_shards" and "--selftest" not in sys.argv) or \
   (hold == "transition" and "{tool}" == "suite_tally" and "--verdict" in sys.argv and sys.argv[-1].endswith("a1.log")):
    subprocess.call([sys.executable, str(probe / "holder.py"), "{tool}"])
runpy.run_path(str(Path(__file__).with_name("real_{tool}.py")), run_name="__main__")
'''

PREFLIGHT_STUB = r'''
import os, subprocess, sys
from pathlib import Path
probe = Path(os.environ["RPROBE"])
print("preflight stub {name} partial output", flush=True)
if os.environ.get("RHOLD") == "preflight" and "{name}" == "test_suite_cancellation":
    raise SystemExit(subprocess.call([sys.executable, str(probe / "holder.py"), "preflight"]))
'''


def head_blob(rel):
    return subprocess.run(["git", "-C", str(CLONE), "show", f"HEAD:{rel}"], check=True,
                          capture_output=True).stdout


def put(path, data, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    path.chmod(mode)


def stat_of(pid):
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except (FileNotFoundError, ProcessLookupError):
        return None
    head, tail = raw.rsplit(")", 1)
    f = tail.split()
    return dict(state=f[0], ppid=int(f[1]), pgrp=int(f[2]), sid=int(f[3]), start=f[19],
                comm=head.split("(", 1)[1])


def cmdline(pid):
    try:
        return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")[:160]
    except OSError:
        return ""


def tree(root_pid):
    kids = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            s = stat_of(int(e.name))
            if s:
                kids.setdefault(s["ppid"], []).append(int(e.name))
    out, todo = {}, [root_pid]
    while todo:
        p = todo.pop()
        for c in kids.get(p, []):
            s = stat_of(c)
            if s and c not in out:
                out[c] = dict(start=s["start"], comm=s["comm"], sid=s["sid"], pgrp=s["pgrp"], cmd=cmdline(c))
                todo.append(c)
    return out


def alive(pid, start):
    s = stat_of(pid)
    return s is not None and s["start"] == start and s["state"] != "Z"


def exists_same(pid, start):
    s = stat_of(pid)
    return s is not None and s["start"] == start


def wait_for(cond, secs):
    t = time.monotonic() + secs
    while time.monotonic() < t:
        if cond():
            return True
        time.sleep(0.02)
    return cond()


def kill_identity(pid, start, sig=signal.SIGKILL):
    try:
        fd = os.pidfd_open(pid)
    except ProcessLookupError:
        return
    try:
        if exists_same(pid, start):
            signal.pidfd_send_signal(fd, sig)
    finally:
        os.close(fd)


def lock_free(root):
    with open(root / ".run_all_suites.lock", "a") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        fcntl.flock(fh, fcntl.LOCK_UN)
        return True


def build(label):
    base = WORK / label
    if base.exists():
        shutil.rmtree(base)
    root = base / "root with space"
    probe = base / "probe"
    probe.mkdir(parents=True)
    for rel in ("scripts/run_all_suites.sh", "scripts/owned_process.py"):
        put(root / rel, head_blob(rel), 0o755 if rel.endswith(".sh") else 0o644)
    for tool in ("suite_tally", "suite_shards"):
        put(root / f"scripts/real_{tool}.py", head_blob(f"scripts/{tool}.py"))
        put(root / f"scripts/{tool}.py", WRAP.replace("{tool}", tool))
    for name in ("test_suite_cancellation", "check_merge_containment", "check_results_fresh",
                 "xvlog_gate", "check_merge_review_integrity"):
        put(root / f"scripts/{name}.py", PREFLIGHT_STUB.replace("{name}", name))
    put(root / "syn/yosys/check_list_hermetic.sh", "#!/usr/bin/env bash\necho hermetic stub\n", 0o755)
    put(probe / "holder.py", HOLDER)
    put(probe / "sentinel.py", SENTINEL)
    put(root / "tb/verilator/a1/Makefile", "all:\n\tpython3 \"$(RPROBE)/holder.py\" a1\n")
    for s in ("a2", "a3"):
        put(root / f"tb/verilator/{s}/Makefile", f"all:\n\tpython3 \"$(RPROBE)/sentinel.py\" {s}\n")
    # stale evidence from an earlier sweep
    put(root / "logs/a2.log", "OLD COMPLETED a2\nsuites: 3 passed: 3\n")
    put(root / "logs/preflight/old.log", "OLD PREFLIGHT\n")
    env = {k: v for k, v in os.environ.items() if k not in ("SUITE_TIMEOUT", "SUITE_SWEEP_LOCK")}
    env.update(RPROBE=str(probe), PYTHONDONTWRITEBYTECODE="1")
    return root, probe, env


def launch(root, probe, env, extra=()):
    out = open(probe / "entry.out", "wb")
    # Own process group, same session as this probe, so a foreign sibling can
    # share that group; the entry is the group leader.
    p = subprocess.Popen(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs"), *extra],
                         cwd=root, env=env, stdout=out, stderr=subprocess.STDOUT, process_group=0)
    return p, out


def handshake(probe, tag, p, secs=30):
    path = probe / f"{tag}-hold.json"
    ok = wait_for(lambda: path.exists() or p.poll() is not None, secs)
    assert ok and path.exists(), (tag, (probe / "entry.out").read_text())
    return json.loads(path.read_text())


def send(p, sig, group):
    if group:
        os.killpg(p.pid, sig)
    else:
        fd = os.pidfd_open(p.pid)
        try:
            signal.pidfd_send_signal(fd, sig)
        finally:
            os.close(fd)


def one(label, phase, sig, group=False, graceful=True, target="entry"):
    root, probe, env = build(label)
    if phase in ("selection", "preflight", "transition"):
        env["RHOLD"] = phase
    tag = {"selection": "suite_shards", "preflight": "preflight", "transition": "suite_tally",
           "command": "a1", "lockwait": None}[phase]
    lockfh = None
    if phase == "lockwait":
        lockfh = open(root / ".run_all_suites.lock", "a")
        fcntl.flock(lockfh, fcntl.LOCK_EX)
    # foreign siblings: one in the entry's process group, one in its own session
    p, outfh = launch(root, probe, env, ("--wait",) if phase == "lockwait" else ())
    foreign_group = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], process_group=p.pid)
    foreign_session = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    fg_start = stat_of(foreign_group.pid)["start"]; fs_start = stat_of(foreign_session.pid)["start"]
    rec = dict(label=label, phase=phase, signal=signal.Signals(sig).name, group=group, target=target)
    if phase == "lockwait":
        assert wait_for(lambda: any(v["comm"] == "flock" for v in tree(p.pid).values()), 30), "no lock wait"
        hs = None
    else:
        hs = handshake(probe, tag, p)
    census = tree(p.pid)
    rec["census"] = {str(k): dict(v) for k, v in census.items()}
    shell = [pid for pid, v in census.items() if v["comm"] == "bash" and "--owned-sweep" in v["cmd"]
             and stat_of(pid)["ppid"] == p.pid]
    assert len(shell) == 1, census
    shell = shell[0]; shell_start = census[shell]["start"]
    rec["entry_comm"] = stat_of(p.pid)["comm"]
    rec["shell_sid_differs_from_entry"] = census[shell]["sid"] != stat_of(p.pid)["sid"]
    t0 = time.monotonic()
    if target == "entry":
        send(p, sig, group)
    elif target == "entry-observe":
        send(p, sig, group)
        time.sleep(3.0)
        rec["entry_running_3s_after_signal"] = p.poll() is None
        (probe / "release").write_text("go\n")
    else:  # the inner sweep shell only
        kill_identity(shell, shell_start, sig)
        time.sleep(3.0)
        rec["entry_running_3s_after_inner_signal"] = p.poll() is None
        rec["a1_hold_running_3s_after_inner_signal"] = alive(hs["pid"], census[hs["pid"]]["start"])
        (probe / "release").write_text("go\n")
    try:
        status = p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        status = "NO-EXIT-60s"
    rec["exit"] = status
    rec["entry_exit_seconds"] = round(time.monotonic() - t0, 3)
    outfh.close()
    at_exit = (probe / "entry.out").read_text()
    rec["output_at_exit"] = at_exit
    rec["shell_gone_within_5s"] = wait_for(lambda: not alive(shell, shell_start), 5)
    if lockfh:
        fcntl.flock(lockfh, fcntl.LOCK_UN); lockfh.close()
    # Release every hold so an in-flight command that survived may complete.
    (probe / "release").write_text("go\n")
    # Let anything surviving finish; then observe for a further settle window.
    survivors = {pid: v for pid, v in census.items() if alive(pid, v["start"])}
    rec["survivors_right_after_exit"] = {str(k): v["cmd"] for k, v in survivors.items()}
    wait_for(lambda: all(not alive(pid, v["start"]) or v["cmd"].endswith("stubborn") or "time.sleep(600)" in v["cmd"]
                         for pid, v in census.items()), 30)
    wait_for(lambda: lock_free(root), 30)
    time.sleep(3.0)
    final = (probe / "entry.out").read_text()
    rec["output_after_exit"] = final[len(at_exit):]
    rec["sentinels"] = sorted(x.name for x in probe.glob("ran-*"))
    rec["summary_printed"] = any(l.startswith("suites:") or l.startswith("logs:") for l in final.splitlines())
    rec["cancelled_line"] = "CANCELLED:" in final
    rec["lock_free_after"] = lock_free(root)
    rec["lock_owner_file_left"] = (root / ".run_all_suites.lock.owner").exists()
    logs = root / "logs"
    rec["logs"] = sorted(str(x.relative_to(logs)) for x in logs.rglob("*") if x.is_file()) if logs.exists() else []
    rec["a1_log"] = (logs / "a1.log").read_text() if (logs / "a1.log").exists() else None
    rec["stale_a2_log_present"] = (logs / "a2.log").exists() and "OLD COMPLETED" in (logs / "a2.log").read_text()
    live_after = {str(pid): v["cmd"] for pid, v in census.items() if alive(pid, v["start"])}
    zombies_after = {str(pid): v["cmd"] for pid, v in census.items()
                     if exists_same(pid, v["start"]) and stat_of(pid)["state"] == "Z"}
    rec["census_live_after"] = live_after
    rec["census_zombie_after"] = zombies_after
    rec["foreign_group_untouched"] = alive(foreign_group.pid, fg_start) if not group else "group-signalled"
    rec["foreign_session_untouched"] = alive(foreign_session.pid, fs_start)
    # reviewer cleanup of anything its own probe created that survived
    for pid, v in census.items():
        kill_identity(pid, v["start"])
    for f in (foreign_group, foreign_session):
        try:
            f.kill()
        except ProcessLookupError:
            pass
        f.wait()
    return rec


def verdict(rec, graceful):
    sig = signal.Signals[rec["signal"]]
    problems = []
    if graceful:
        if rec["exit"] != 128 + sig:
            problems.append(f"exit {rec['exit']} != {128 + sig}")
        if not rec["cancelled_line"]:
            problems.append("no CANCELLED line")
        if rec["census_live_after"] or rec["census_zombie_after"]:
            problems.append("owned identities survived")
        if rec["lock_owner_file_left"]:
            problems.append("lock owner file left")
    else:
        if rec["exit"] != -sig:
            problems.append(f"exit {rec['exit']} != {-sig}")
        if not rec["shell_gone_within_5s"]:
            problems.append("sweep shell outlived entry")
        if rec["output_after_exit"]:
            problems.append("output after caller saw exit")
    if rec["sentinels"]:
        problems.append("later suite ran: " + ",".join(rec["sentinels"]))
    if rec["summary_printed"]:
        problems.append("completed summary printed")
    if rec["foreign_session_untouched"] is not True:
        problems.append("foreign session sibling touched")
    if rec["foreign_group_untouched"] not in (True, "group-signalled"):
        problems.append("foreign group sibling touched")
    if not rec["lock_free_after"]:
        problems.append("lock still held after settle")
    return problems


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    plan = []
    for phase in ("command", "preflight", "transition", "selection", "lockwait"):
        for sig in (signal.SIGINT, signal.SIGTERM):
            plan.append((f"g-{phase}-{sig.name}", phase, sig, False, True))
    for phase in ("command", "preflight", "transition"):
        for sig in (signal.SIGINT, signal.SIGTERM):
            plan.append((f"g-{phase}-{sig.name}-group", phase, sig, True, True))
    for sig in (signal.SIGKILL, signal.SIGHUP, signal.SIGQUIT, signal.SIGUSR1, signal.SIGALRM):
        plan.append((f"h-command-{sig.name}", "command", sig, False, False))
    for sig in (signal.SIGKILL, signal.SIGHUP):
        plan.append((f"h-command-{sig.name}-group", "command", sig, True, False))
        plan.append((f"h-preflight-{sig.name}", "preflight", sig, False, False))
        plan.append((f"h-transition-{sig.name}", "transition", sig, False, False))
    results = []
    for label, phase, sig, group, graceful in plan:
        rec = one(label, phase, sig, group, graceful)
        rec["graceful_expected"] = graceful
        rec["problems"] = verdict(rec, graceful)
        results.append(rec)
        print(f"{label:34s} exit={rec['exit']!s:6s} t={rec['entry_exit_seconds']:6.2f}s "
              f"sentinels={rec['sentinels']} summary={rec['summary_printed']} "
              f"live={len(rec['census_live_after'])} zomb={len(rec['census_zombie_after'])} "
              f"lockowner_left={rec['lock_owner_file_left']} problems={rec['problems']}", flush=True)
    # Observation arm: TERM to the inner sweep shell only (not the launched entry).
    rec = one("o-command-TERM-inner-shell", "command", signal.SIGTERM, target="shell")
    rec["problems"] = []
    results.append(rec)
    print(f"{'o-command-TERM-inner-shell':34s} exit={rec['exit']!s:6s} t={rec['entry_exit_seconds']:6.2f}s "
          f"sentinels={rec['sentinels']} summary={rec['summary_printed']} live={len(rec['census_live_after'])}",
          flush=True)
    # Observation arm: SIGPIPE to the entry. The owner is a Python process, which ignores SIGPIPE.
    rec = one("o-command-PIPE-entry", "command", signal.SIGPIPE, target="entry-observe")
    rec["problems"] = []
    results.append(rec)
    print(f"{'o-command-PIPE-entry':34s} exit={rec['exit']!s:6s} running_3s_after={rec['entry_running_3s_after_signal']} "
          f"sentinels={rec['sentinels']} summary={rec['summary_printed']}", flush=True)
    # Leftover scan: no process may still run from this probe's tree.
    leftovers = []
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            try:
                cwd = os.readlink(e / "cwd")
            except OSError:
                continue
            if cwd.startswith(str(WORK)):
                leftovers.append((e.name, cwd))
    print("LEFTOVER PROCESSES UNDER WORKDIR:", leftovers)
    RECEIPT.write_text(json.dumps(dict(arms=results, leftovers_under_workdir=leftovers), indent=1, sort_keys=True) + "\n")
    bad = [r["label"] for r in results if r["problems"]]
    print("PROBLEM ARMS:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
