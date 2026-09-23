#!/usr/bin/env python3
"""Independent reviewer probe with REAL builds: signal the production mutation
driver, or the production sweep entry running the real gptp_shadow suite,
while a real Verilator/C++ compile of a planted mutation is in progress.

Usage: probe_real_nested.py CLONE SCRATCH VERILATOR OUTPUT_JSON [LABEL,...]

Caller checkouts are disposable clones of the review clone at the exact head
with the two required submodules initialised at their pins. For the sweep
cases only, the disposable caller's other suites are removed, a sentinel
suite `zz_sentinel` is added (it must never run), and the expensive
prerequisite self-tests are replaced by bounded stubs: the sweep script,
owner, selector, tally and the whole gptp_shadow suite (lifecycle test,
baseline, real mutations) run unmodified. The handshake is observable
process state: a `cc1plus` whose working directory is inside the driver's
private `gptp-shadow-mutants-*` tree.
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


def run(argv, **kw):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv, env=env, capture_output=True, check=True, **kw)


def build_caller(clone, dest):
    run(["git", "clone", "-q", "--no-local", "--no-checkout", str(clone), str(dest)])
    run(["git", "-C", str(dest), "checkout", "-q", "--detach", HEAD])
    for name in ("gptp-processor", "third_party/verilog-axis"):
        run(["git", "-C", str(dest), "config", f"submodule.{name}.url", str(clone / ".git/modules" / name)])
        run(["git", "-C", str(dest), "-c", "protocol.file.allow=always", "submodule", "update", "-q", "--init", "--", name])


def snapshot(root, only=None):
    """Index digest plus bytes/modes of tracked files (optionally a subset of paths)."""
    out = {}
    for repo, prefix in ((root, ""), (root / "gptp-processor", "gptp-processor/"),
                         (root / "third_party/verilog-axis", "third_party/verilog-axis/")):
        idx = run(["git", "--no-optional-locks", "-C", str(repo), "ls-files", "--stage", "-z"]).stdout
        out[prefix + "<index>"] = hashlib.sha256(idx).hexdigest()
        for row in idx.split(b"\0"):
            if not row:
                continue
            meta, name = row.split(b"\t", 1)
            name = prefix + os.fsdecode(name)
            if meta.startswith(b"160000") or (only and not name.startswith(only)):
                continue
            p = root / name
            if not p.exists():
                out[name] = "absent"
                continue
            st = p.lstat()
            out[name] = (st.st_mode, hashlib.sha256(p.read_bytes()).hexdigest())
    return out


def fields(pid):
    try:
        return (Path("/proc") / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
    except (FileNotFoundError, ProcessLookupError):
        return None


def identity(pid):
    f = fields(pid)
    return None if f is None else (f[19], f[0])


def running(pid, start):
    i = identity(pid)
    return i is not None and i[0] == start and i[1] != "Z"


def census():
    pop = {}
    for p in Path("/proc").iterdir():
        if p.name.isdecimal():
            f = fields(int(p.name))
            if f:
                try:
                    comm = (p / "comm").read_text().strip()
                except OSError:
                    comm = "?"
                try:
                    cwd = os.readlink(p / "cwd")
                except OSError:
                    cwd = ""
                pop[int(p.name)] = (int(f[1]), f[19], f[0], comm, cwd)
    return pop


def subtree(root_pid):
    pop = census()
    owned = {root_pid}
    while True:
        more = {pid for pid, v in pop.items() if v[0] in owned} - owned
        if not more:
            return {pid: pop[pid] for pid in owned if pid in pop and pid != root_pid}
        owned |= more


def wait_for(cond, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        v = cond()
        if v:
            return v
        time.sleep(0.05)
    return cond()


def compiling_private(root_pid):
    tree = subtree(root_pid)
    hits = [pid for pid, v in tree.items() if v[3] == "cc1plus" and "gptp-shadow-mutants-" in v[4]]
    return (tree, hits) if hits else None


def contain(pids):
    for pid, (_pp, start, _st, _c, _w) in pids.items():
        try:
            fd = os.pidfd_open(pid)
        except ProcessLookupError:
            continue
        try:
            if running(pid, start):
                signal.pidfd_send_signal(fd, signal.SIGKILL)
        finally:
            os.close(fd)


def prepare_sweep(caller):
    tb = caller / "tb/verilator"
    for d in tb.iterdir():
        if d.is_dir() and d.name != "gptp_shadow" and (d / "Makefile").exists():
            shutil.rmtree(d)
    (tb / "zz_sentinel").mkdir()
    (tb / "zz_sentinel/Makefile").write_text("all:\n\t@touch $(CURDIR)/../../../SENTINEL_RAN\n\t@echo '1 checks: 1 PASS, 0 FAIL'\n")
    # test_suite_cancellation.py stays real: the lifecycle test imports its fixture.
    for name in ("check_merge_containment", "check_results_fresh", "xvlog_gate", "check_merge_review_integrity"):
        (caller / f"scripts/{name}.py").write_text("print('reviewer stub: bounded prerequisite')\n")
    (caller / "syn/yosys/check_list_hermetic.sh").write_text("#!/usr/bin/env bash\nexit 0\n")


def one(caller, scratch, label, argv, signame, let_orphan_finish=False):
    tmp = scratch / (label + "-tmp")
    tmp.mkdir()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(TMPDIR=str(tmp), VERILATOR=os.environ["PROBE_VERILATOR"], VERILATOR_JOBS=os.environ.get("PROBE_JOBS", "4"),
               PYTHONDONTWRITEBYTECODE="1")
    env.pop("SUITE_TIMEOUT", None)
    before = snapshot(caller, only=("hdl/", "gptp-processor/", "third_party/", "tb/common/"))
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(900)"], start_new_session=True)
    fid = identity(foreign.pid)
    log = open(scratch / (label + ".log"), "wb")
    entry = subprocess.Popen(argv, cwd=caller, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    found = wait_for(lambda: compiling_private(entry.pid) or (entry.poll() is not None and ("exit", None)), 900)
    assert found and found[0] != "exit", (scratch / (label + ".log")).read_text()[-3000:]
    tree, hits = found
    rec = {"label": label, "signal": signame, "descendants_at_signal": len(tree),
           "comms_at_signal": sorted({v[3] for v in tree.values()}),
           "private_roots": sorted({v[4].split("gptp-shadow-mutants-")[0] + "gptp-shadow-mutants-" +
                                    v[4].split("gptp-shadow-mutants-")[1].split("/")[0]
                                    for v in tree.values() if "gptp-shadow-mutants-" in v[4]})}
    t0 = time.monotonic()
    fd = os.pidfd_open(entry.pid)
    signal.pidfd_send_signal(fd, getattr(signal, signame))
    os.close(fd)
    status = entry.wait(timeout=60)
    rec["status"] = status
    rec["seconds_to_status"] = round(time.monotonic() - t0, 2)
    alive = {pid: v for pid, v in tree.items() if running(pid, v[1])}
    rec["alive_at_status"] = sorted({v[3] for v in alive.values()})
    rec["alive_count_at_status"] = len(alive)
    rec["private_exists_at_status"] = [Path(p).exists() for p in rec["private_roots"]]
    if let_orphan_finish:
        # A suite already running may finish: wait for every survivor to end.
        rec["orphans_finished"] = bool(wait_for(lambda: not any(running(p, v[1]) for p, v in alive.items()), 900))
    else:
        time.sleep(5)
    later = {pid: v for pid, v in alive.items() if running(pid, v[1])}
    rec["alive_after_wait"] = sorted({v[3] for v in later.values()})
    text = (scratch / (label + ".log")).read_text(errors="replace")
    rec["summary_line"] = any(l.startswith("suites: ") for l in text.splitlines())
    rec["result_line"] = "RESULT:" in text
    rec["sentinel_ran"] = (caller / "SENTINEL_RAN").exists()
    rec["caller_unchanged"] = snapshot(caller, only=("hdl/", "gptp-processor/", "third_party/", "tb/common/")) == before
    rec["private_exists_after"] = [Path(p).exists() for p in rec["private_roots"]]
    rec["tmp_left"] = sorted(p.name for p in tmp.iterdir())
    fc = identity(foreign.pid)
    rec["foreign_preserved"] = foreign.poll() is None and fc is not None and fc[0] == fid[0] and fc[1] != "Z"
    rec["transcript_tail"] = text[-1500:]
    suite_log = caller / "logs/gptp_shadow.log"
    rec["suite_log_tail"] = suite_log.read_text(errors="replace")[-1500:] if suite_log.exists() else None
    foreign.kill()
    foreign.wait()
    contain(later)
    return rec


def main():
    clone, scratch, verilator, output = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                         sys.argv[3], Path(sys.argv[4]))
    os.environ["PROBE_VERILATOR"] = verilator
    only = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
    scratch.mkdir(parents=True, exist_ok=True)
    results = []
    plans = [
        ("campaign-KILL-real", "campaign", "SIGKILL", False),
        ("campaign-TERM-real", "campaign", "SIGTERM", False),
        ("sweep-TERM-nested-real", "sweep", "SIGTERM", False),
        ("sweep-KILL-nested-real", "sweep", "SIGKILL", True),
    ]
    for label, kind, signame, finish in plans:
        if only and label not in only:
            continue
        caller = scratch / (label + "-caller")
        build_caller(clone, caller)
        if kind == "campaign":
            argv = [sys.executable, str(caller / "tb/verilator/gptp_shadow/mutants.py")]
        else:
            prepare_sweep(caller)
            argv = ["bash", str(caller / "scripts/run_all_suites.sh"), str(caller / "logs")]
        r = one(caller, scratch, label, argv, signame, finish)
        results.append(r)
        print(json.dumps({k: v for k, v in r.items() if k not in ("transcript_tail", "suite_log_tail")}), flush=True)
    output.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
