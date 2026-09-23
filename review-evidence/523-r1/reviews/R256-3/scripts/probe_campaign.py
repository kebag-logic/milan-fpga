#!/usr/bin/env python3
"""Reviewer-owned signal probes of the real gPTP shadow mutation driver.

Usage:
  probe_campaign.py hold  SOURCE_CLONE WORKDIR RECEIPT.json
      Copies SOURCE_CLONE (a disposable clone at the exact head with its pinned
      submodules), commits there a Makefile whose `run` recipe holds at a
      published handshake AFTER the driver applied the first mutation to its
      private copy, then signals the real `mutants.py` (INT/TERM/KILL/HUP/QUIT,
      entry and process group, and a second signal during cleanup).
  probe_campaign.py real  SOURCE_CLONE WORKDIR RECEIPT.json SIGNAL...
      Uses SOURCE_CLONE unmodified (the exact-head Makefile) and signals the
      real driver while a real Verilator/C++ compile runs in private scratch.
Independent of the lane's fixture helpers; its own /proc oracle.
"""
import hashlib, json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

# Parsed only when run as a script; importers use the helpers alone.
if __name__ == "__main__":
    MODE = sys.argv[1]
    SOURCE = Path(sys.argv[2]).resolve()
    WORK = Path(sys.argv[3]).resolve()
    RECEIPT = Path(sys.argv[4]).resolve()
INTEGRITY = Path(__file__).resolve().with_name("integrity.py")
# The scoped Verilator 5.050 selector; this round ran it from $PINNED_TOOLS/verilator.
VERILATOR = os.environ.get("REVIEW_VERILATOR", "verilator")
TARGET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"

HOLDER = r'''
import hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path
probe = Path(os.environ["RPROBE"]); caller = Path(os.environ["RCALLER"])
if sys.argv[1:] == ["stubborn"]:
    for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(s, signal.SIG_IGN)
    (probe / "stubborn-ready").write_text(str(os.getpid()))
    while True:
        time.sleep(0.05)
private = Path.cwd().parents[2]
rel = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
plain = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
det = subprocess.Popen([sys.executable, __file__, "stubborn"], start_new_session=True)
t = time.monotonic() + 20
while not (probe / "stubborn-ready").exists():
    assert time.monotonic() < t
    time.sleep(0.01)
data = dict(pid=os.getpid(), plain=plain.pid, detached=det.pid, private=str(private),
            private_target_sha256=h(private / rel), caller_target_sha256=h(caller / rel),
            private_is_caller=private.resolve() == caller.resolve(),
            same_inode=os.stat(private / rel).st_ino == os.stat(caller / rel).st_ino)
(probe / "hold.tmp").write_text(json.dumps(data)); os.replace(probe / "hold.tmp", probe / "hold.json")
print("PARTIAL: holding inside the first mutant build", flush=True)
while not (probe / "release").exists():
    time.sleep(0.02)
plain.kill(); plain.wait()
print("1 checks: 1 PASS, 0 FAIL")
'''


def run(*argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout


def stat_of(pid):
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except (FileNotFoundError, ProcessLookupError):
        return None
    head, tail = raw.rsplit(")", 1)
    f = tail.split()
    return dict(state=f[0], ppid=int(f[1]), pgrp=int(f[2]), sid=int(f[3]), start=f[19], comm=head.split("(", 1)[1])


def tree(root_pid):
    kids = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            s = stat_of(int(e.name))
            if s:
                kids.setdefault(s["ppid"], []).append(int(e.name))
    out, todo = {}, [root_pid]
    while todo:
        for c in kids.get(todo.pop(), []):
            s = stat_of(c)
            if s and c not in out:
                out[c] = dict(start=s["start"], comm=s["comm"], sid=s["sid"])
                todo.append(c)
    return out


def alive(pid, start):
    s = stat_of(pid)
    return s is not None and s["start"] == start and s["state"] != "Z"


def present(pid, start):
    s = stat_of(pid)
    return s is not None and s["start"] == start


def referencing(path):
    """Every process whose cwd or command line names `path` (any owner)."""
    hits = {}
    needle = str(path)
    for e in Path("/proc").iterdir():
        if not e.name.isdecimal():
            continue
        try:
            cwd = os.readlink(e / "cwd")
        except OSError:
            cwd = ""
        try:
            cmd = (e / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
        except OSError:
            cmd = ""
        if cwd.startswith(needle) or needle in cmd:
            s = stat_of(int(e.name))
            if s and s["state"] != "Z":
                hits[e.name] = dict(comm=s["comm"], cwd=cwd[:120])
    return hits


def wait_for(cond, secs):
    t = time.monotonic() + secs
    while time.monotonic() < t:
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
        if present(pid, start):
            signal.pidfd_send_signal(fd, signal.SIGKILL)
    finally:
        os.close(fd)


def integrity(repo, out):
    subprocess.run([sys.executable, str(INTEGRITY), str(repo), str(out)], check=True, capture_output=True)
    data = json.loads(Path(out).read_text())
    data.pop("ignored", None)
    return data


def prepare_hold(base):
    repo = base / "repo"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    shutil.copytree(SOURCE, repo, symlinks=True)
    probe = base / "probe"
    probe.mkdir()
    (probe / "holder.py").write_text(HOLDER)
    mk = repo / "tb/verilator/gptp_shadow/Makefile"
    text = mk.read_text()
    old = "run: gptp_ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_shadow_sim\n\t./obj_dir/Vgptp_shadow_sim\n"
    assert old in text
    mk.write_text(text.replace(old, "run:\n\tpython3 \"$(RPROBE)/holder.py\"\n"))
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    run("git", "-C", str(repo), "-c", "user.name=Reviewer probe", "-c", "user.email=probe@example.invalid",
        "commit", "-qam", "reviewer disposable hold point", env=env)
    return repo, probe


def launch(repo, probe, extra_env=None):
    env = {k: v for k, v in os.environ.items()}
    env.update(RPROBE=str(probe), RCALLER=str(repo), TMPDIR=str(probe / "tmp"), PYTHONDONTWRITEBYTECODE="1",
               VERILATOR=VERILATOR, VERILATOR_JOBS="8")
    (probe / "tmp").mkdir(exist_ok=True)
    env.update(extra_env or {})
    out = open(probe / "driver.out", "wb")
    p = subprocess.Popen([sys.executable, str(repo / "tb/verilator/gptp_shadow/mutants.py")], cwd=repo,
                         env=env, stdout=out, stderr=subprocess.STDOUT, process_group=0)
    return p, out


def send(p, sig, group):
    if group:
        os.killpg(p.pid, sig)
    else:
        fd = os.pidfd_open(p.pid)
        try:
            signal.pidfd_send_signal(fd, sig)
        finally:
            os.close(fd)


def hold_arm(label, sig, group=False, second=None):
    base = WORK / label
    repo, probe = prepare_hold(base)
    before = integrity(repo, base / "integrity-before.json")
    p, out = launch(repo, probe)
    assert wait_for(lambda: (probe / "hold.json").exists() or p.poll() is not None, 60), "no handshake"
    assert (probe / "hold.json").exists(), (probe / "driver.out").read_text()
    hs = json.loads((probe / "hold.json").read_text())
    census = tree(p.pid)
    make = [pid for pid, v in census.items() if v["comm"] == "make" and stat_of(pid)["ppid"] == p.pid]
    rec = dict(label=label, signal=signal.Signals(sig).name, group=group, second=second and signal.Signals(second).name,
               handshake=hs, census={str(k): v for k, v in census.items()},
               mutation_applied_privately=hs["private_target_sha256"] != hs["caller_target_sha256"]
               and not hs["private_is_caller"] and not hs["same_inode"],
               make_in_own_session=bool(make) and census[make[0]]["sid"] != stat_of(p.pid)["sid"])
    t0 = time.monotonic()
    send(p, sig, group)
    if second:
        time.sleep(0.5)
        if p.poll() is None:
            send(p, second, False)
    try:
        rec["exit"] = p.wait(timeout=30)
    except subprocess.TimeoutExpired:
        rec["exit"] = "NO-EXIT-30s"
    rec["exit_seconds"] = round(time.monotonic() - t0, 3)
    out.close()
    rec["output"] = (probe / "driver.out").read_text()
    rec["verdict_printed"] = "RESULT:" in rec["output"] or "controls:" in rec["output"]
    rec["make_gone_within_5s"] = wait_for(lambda: all(not alive(pid, census[pid]["start"]) for pid in make), 5)
    rec["census_live_after"] = {str(k): v["comm"] for k, v in census.items() if alive(k, v["start"])}
    rec["census_zombie_after"] = {str(k): v["comm"] for k, v in census.items()
                                  if present(k, v["start"]) and stat_of(k)["state"] == "Z"}
    rec["private_exists_after"] = Path(hs["private"]).exists()
    rec["processes_referencing_private_after"] = referencing(hs["private"])
    after = integrity(repo, base / "integrity-after.json")
    rec["caller_tracked_state_unchanged"] = before == after
    rec["caller_clean"] = after["clean"]
    rec["tmp_leftovers"] = sorted(x.name for x in (probe / "tmp").iterdir())
    (probe / "release").write_text("go\n")
    for k, v in census.items():
        kill_identity(k, v["start"])
    return rec


def expected_hold(rec):
    sig = signal.Signals[rec["signal"]]
    graceful = sig in (signal.SIGINT, signal.SIGTERM)
    probs = []
    if not rec["mutation_applied_privately"]:
        probs.append("handshake did not prove a private mutation")
    if not rec["caller_tracked_state_unchanged"] or not rec["caller_clean"]:
        probs.append("caller tracked state changed")
    if rec["verdict_printed"]:
        probs.append("completed verdict printed")
    if graceful:
        want = 128 + (sig if not rec["second"] else sig)
        if rec["exit"] != want:
            probs.append(f"exit {rec['exit']} != {want}")
        if rec["census_live_after"] or rec["census_zombie_after"]:
            probs.append("owned identities survived")
        if rec["private_exists_after"] or rec["tmp_leftovers"]:
            probs.append("private work left")
        if rec["processes_referencing_private_after"]:
            probs.append("processes still reference private work")
    else:
        if rec["exit"] != -sig:
            probs.append(f"exit {rec['exit']} != {-sig}")
        if not rec["make_gone_within_5s"]:
            probs.append("direct make outlived the killed driver")
    return probs


def real_arm(label, sig):
    base = WORK / label
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    probe = base / "probe"
    probe.mkdir()
    repo = SOURCE
    before = integrity(repo, base / "integrity-before.json")
    p, out = launch(repo, probe)
    compilers = ("cc1plus", "verilator_bin", "g++", "c++", "ld", "as")

    def compiling():
        t = tree(p.pid)
        privs = [d for d in (probe / "tmp").iterdir()] if (probe / "tmp").exists() else []
        return privs and any(v["comm"] in compilers or v["comm"].startswith("verilator") for v in t.values())
    assert wait_for(lambda: compiling() or p.poll() is not None, 240), "no compile seen"
    assert p.poll() is None, (probe / "driver.out").read_text()
    time.sleep(1.0)
    census = tree(p.pid)
    private = [d for d in (probe / "tmp").iterdir()][0]
    rec = dict(label=label, signal=signal.Signals(sig).name, private=str(private),
               census={str(k): v for k, v in census.items()},
               compiler_comms=sorted({v["comm"] for v in census.values()}))
    t0 = time.monotonic()
    send(p, sig, False)
    try:
        rec["exit"] = p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        rec["exit"] = "NO-EXIT-60s"
    rec["exit_seconds"] = round(time.monotonic() - t0, 3)
    out.close()
    rec["output_tail"] = (probe / "driver.out").read_text()[-600:]
    rec["verdict_printed"] = "RESULT:" in rec["output_tail"]
    if sig == signal.SIGKILL:
        make = [k for k, v in census.items() if v["comm"] == "make" and stat_of(k) and stat_of(k)["ppid"] == p.pid]
        rec["direct_make_gone_within_5s"] = wait_for(lambda: all(not alive(k, census[k]["start"]) for k in make), 5)
        # deeper build steps may finish; wait for them before checking the tree
        wait_for(lambda: not referencing(private), 180)
    rec["census_live_after"] = {str(k): v["comm"] for k, v in census.items() if alive(k, v["start"])}
    rec["census_zombie_after"] = {str(k): v["comm"] for k, v in census.items()
                                  if present(k, v["start"]) and stat_of(k)["state"] == "Z"}
    rec["processes_referencing_private_after"] = referencing(private)
    rec["private_exists_after"] = private.exists()
    after = integrity(repo, base / "integrity-after.json")
    rec["caller_tracked_state_unchanged"] = before == after
    probs = []
    if not rec["caller_tracked_state_unchanged"]:
        probs.append("caller tracked state changed")
    if rec["verdict_printed"]:
        probs.append("verdict printed")
    if sig in (signal.SIGINT, signal.SIGTERM):
        if rec["exit"] != 128 + sig:
            probs.append(f"exit {rec['exit']}")
        if rec["census_live_after"] or rec["census_zombie_after"] or rec["processes_referencing_private_after"]:
            probs.append("owned processes survived")
        if rec["private_exists_after"]:
            probs.append("private work left")
    else:
        if rec["exit"] != -sig:
            probs.append(f"exit {rec['exit']}")
        if not rec["direct_make_gone_within_5s"]:
            probs.append("direct make outlived driver")
    rec["problems"] = probs
    for k, v in census.items():
        kill_identity(k, v["start"])
    if private.exists():
        shutil.rmtree(private, ignore_errors=True)
    return rec


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    results = []
    if MODE == "hold":
        plan = [("hold-INT", signal.SIGINT, False, None), ("hold-TERM", signal.SIGTERM, False, None),
                ("hold-INT-group", signal.SIGINT, True, None), ("hold-TERM-group", signal.SIGTERM, True, None),
                ("hold-TERM-then-INT", signal.SIGTERM, False, signal.SIGINT),
                ("hold-KILL", signal.SIGKILL, False, None), ("hold-KILL-group", signal.SIGKILL, True, None),
                ("hold-HUP", signal.SIGHUP, False, None), ("hold-QUIT", signal.SIGQUIT, False, None)]
        for label, sig, group, second in plan:
            rec = hold_arm(label, sig, group, second)
            rec["problems"] = expected_hold(rec)
            results.append(rec)
            print(f"{label:22s} exit={rec['exit']!s:5s} t={rec['exit_seconds']:5.2f}s private_mut={rec['mutation_applied_privately']} "
                  f"caller_unchanged={rec['caller_tracked_state_unchanged']} private_left={rec['private_exists_after']} "
                  f"live={sorted(rec['census_live_after'].values())} make_own_session={rec['make_in_own_session']} "
                  f"problems={rec['problems']}", flush=True)
    else:
        for name in sys.argv[5:]:
            sig = signal.Signals["SIG" + name]
            rec = real_arm("real-" + name, sig)
            results.append(rec)
            print(f"real-{name:6s} exit={rec['exit']!s:5s} t={rec['exit_seconds']:5.2f}s comms={rec['compiler_comms']} "
                  f"caller_unchanged={rec['caller_tracked_state_unchanged']} private_left={rec['private_exists_after']} "
                  f"live={sorted(rec['census_live_after'].values())} refs={rec['processes_referencing_private_after']} "
                  f"problems={rec['problems']}", flush=True)
    RECEIPT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    bad = [r["label"] for r in results if r["problems"]]
    print("PROBLEM ARMS:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
