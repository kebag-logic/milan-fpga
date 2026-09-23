#!/usr/bin/env python3
"""Reviewer probe: the REAL mutation driver and REAL Verilator build, signalled
at an observed mutation-applied boundary: the first control's mutated bytes
exist in a private copy AND a live descendant build process runs inside it.

Usage: probe_real_driver_signals.py REPO_COPY INTEGRITY_SCRIPT OUT_JSON
Environment: VERILATOR (scoped wrapper), TMPDIR (disposable parent).
"""
import hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
integrity = sys.argv[2]
out = Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
sys.path.insert(0, str(repo / "tb/verilator/gptp_shadow"))
from owned_process import OwnedProcesses
from mutants import MUTATIONS

name, original, old, new, _expect = MUTATIONS[0]
rel = original.relative_to(Path(__file__).resolve().parents[0]) if False else original.relative_to(repo)
mutated = hashlib.sha256(original.read_text().replace(old, new, 1).encode()).hexdigest()

def stat_fields(pid):
    try:
        return (Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split())
    except (FileNotFoundError, ProcessLookupError):
        return None

def descendants(root):
    table = {}
    for e in Path("/proc").iterdir():
        if e.name.isdecimal():
            f = stat_fields(int(e.name))
            if f:
                table[int(e.name)] = (int(f[1]), f[19], f[0])
    owned, grow = {root}, True
    while grow:
        more = {p for p, (pp, _s, _st) in table.items() if pp in owned} - owned
        grow = bool(more)
        owned |= more
    return {p: table[p] for p in owned if p in table and p != root}

def integrity_ok():
    done = subprocess.run([sys.executable, integrity, str(repo), "b5ce20eca8b59709ec5bc6115e5e15bfc312f283"],
                          capture_output=True, text=True)
    return done.returncode == 0, done.stdout.strip().splitlines()[-1]

def case(signum, tmp):
    tmp.mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1", VERILATOR_JOBS="8")
    log = tmp.parent / (tmp.name + ".driver.log")
    before_ok, before = integrity_ok()
    with log.open("wb") as fh:
        proc = subprocess.Popen([sys.executable, str(repo / "tb/verilator/gptp_shadow/mutants.py")],
                                cwd=repo / "tb/verilator/gptp_shadow", env=env, stdout=fh,
                                stderr=subprocess.STDOUT, start_new_session=True)
    deadline, private, seen = time.monotonic() + 120, None, {}
    while time.monotonic() < deadline:
        for d in tmp.glob("gptp-shadow-mutants-*"):
            f = d / rel
            try:
                if hashlib.sha256(f.read_bytes()).hexdigest() == mutated:
                    private = d
            except OSError:
                pass
        if private:
            seen = descendants(proc.pid)
            inside = [p for p in seen if str(private) in (os.readlink(f"/proc/{p}/cwd") if os.path.exists(f"/proc/{p}/cwd") else "")]
            if inside:
                break
        assert proc.poll() is None, log.read_text()
        time.sleep(0.02)
    else:
        raise AssertionError("boundary not reached")
    caller_during_ok, _ = integrity_ok()
    fd = os.pidfd_open(proc.pid)
    t0 = time.monotonic()
    signal.pidfd_send_signal(fd, signum)
    os.close(fd)
    status = proc.wait(timeout=60)
    seconds = round(time.monotonic() - t0, 2)
    output = log.read_text()
    after_ok, after = integrity_ok()
    survivors = {str(p): list(v) for p, v in seen.items()
                 if (lambda f: f is not None and f[19] == v[1] and f[0] != "Z")(stat_fields(p))}
    zombies = {str(p) for p, v in seen.items() if (lambda f: f is not None and f[19] == v[1] and f[0] == "Z")(stat_fields(p))}
    return dict(signal=signal.Signals(signum).name, boundary_mutation=name, owned_at_boundary=len(seen),
                build_inside_private=True, caller_ok_before=before_ok, caller_ok_at_boundary=caller_during_ok,
                exit=status, seconds_to_exit=seconds, caller_ok_after=after_ok, integrity_after=after,
                private_removed=not private.exists(), completed_verdict=("RESULT:" in output or "controls:" in output),
                cancelled_line=[l for l in output.splitlines() if l.startswith(("CANCELLED", "REFUSED"))],
                surviving_identities=survivors, unreaped_zombies=sorted(zombies))

def main():
    parent = Path(os.environ["TMPDIR"])
    rows = []
    with OwnedProcesses():  # containment: adopt KILL survivors, reap them at exit
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):
            rows.append(case(signum, parent / f"real-{signal.Signals(signum).name}"))
            print(json.dumps(rows[-1]), flush=True)
    out.write_text(json.dumps(rows, indent=2) + "\n")
    graceful = [r for r in rows if r["signal"] != "SIGKILL"]
    kill = [r for r in rows if r["signal"] == "SIGKILL"][0]
    ok = all(r["exit"] == 128 + signal.Signals[r["signal"]] and r["private_removed"] and not r["surviving_identities"]
             and not r["unreaped_zombies"] and not r["completed_verdict"] and r["caller_ok_after"] for r in graceful) \
         and kill["exit"] == -9 and kill["caller_ok_after"] and not kill["completed_verdict"]
    print("REAL DRIVER SIGNALS " + ("OK" if ok else "UNEXPECTED"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
