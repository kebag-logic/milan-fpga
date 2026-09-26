#!/usr/bin/env python3
"""Reviewer-owned blocked-stdout cancellation probe for sim_pool.py (#517 F1).

usage: probe_blocked_cancel.py RUNNER OUTDIR
For SIGINT, SIGTERM and SIGHUP: two shell legs run under --jobs=2. Leg 1 writes
~512 KiB and exits; leg 2 starts a new-session `sleep` descendant and a same-
group `sleep`, then waits. The runner's stdout is a pipe whose read end is held
open and never read, so the replay of leg 1 cannot complete. Once the pipe is
full and leg 1 has exited, the signal is sent. PASS requires: runner exit
within 5 s by the same signal while the pipe is still unread; no process that
carries this probe's marker environment variable alive afterwards; per-leg
captures on disk; the partial capture attributed in replay.log.
"""
import json, os, select, signal, subprocess, sys, tempfile, time
from pathlib import Path

LEG1 = "#!/bin/sh\nhead -c 524288 /dev/zero | tr '\\0' 'a'\necho\necho leg1 done\n"
LEG2 = ("#!/bin/sh\necho leg2 partial\nsetsid sleep 1000 &\nsleep 1000 &\n"
        "echo started > leg2.ready\nwait\n")


def marked(marker):
    pids = []
    for e in os.listdir("/proc"):
        if not e.isdigit():
            continue
        try:
            env = open(f"/proc/{e}/environ", "rb").read()
            state = open(f"/proc/{e}/stat", "rb").read().rsplit(b")", 1)[1].split()[0]
        except OSError:
            continue
        if f"PROBE_MARK={marker}".encode() in env.split(b"\0") and state != b"Z":
            pids.append(int(e))
    return pids


def one(runner, root, sig):
    root.mkdir(parents=True)
    for name, body in (("obj_a/Va", LEG1), ("obj_b/Vb", LEG2)):
        p = root / name
        p.parent.mkdir()
        p.write_text(body)
        p.chmod(0o755)
    (root / "sim_pool.py").write_bytes(Path(runner).read_bytes())
    marker = f"{os.getpid()}-{sig.name}"
    r, w = os.pipe()
    env = {k: v for k, v in os.environ.items() if k not in ("MILAN_COUNTER_FRAME_OUT", "MAKEFLAGS")}
    env["PROBE_MARK"] = marker
    proc = subprocess.Popen([sys.executable, "sim_pool.py", "--jobs=2", "./obj_a/Va", "./obj_b/Vb"],
                            cwd=root, stdout=w, stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL, start_new_session=True, env=env)
    os.close(w)
    deadline = time.monotonic() + 30
    # wait: leg 2 ready, leg 1 capture complete, runner blocked (pipe full)
    while time.monotonic() < deadline:
        cap = root / "obj_legs/01-Va.log"
        if (root / "leg2.ready").exists() and cap.exists() and cap.read_bytes().endswith(b"leg1 done\n"):
            break
        time.sleep(0.05)
    time.sleep(1.0)
    import fcntl, termios, array
    q = array.array("i", [0]); fcntl.ioctl(r, termios.FIONREAD, q)
    before = marked(marker)
    t0 = time.monotonic()
    proc.send_signal(sig)
    try:
        rc = proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        rc = "NO-EXIT-WITHIN-5S"
    elapsed = time.monotonic() - t0
    time.sleep(0.3)
    after = marked(marker)
    q2 = array.array("i", [0]); fcntl.ioctl(r, termios.FIONREAD, q2)
    replay = (root / "obj_legs/replay.log").read_bytes() if (root / "obj_legs/replay.log").exists() else b""
    row = dict(signal=sig.name, queued_before_signal=q[0], queued_after_exit=q2[0],
               marked_alive_before=len(before), runner_exit=rc if isinstance(rc, str) else rc,
               seconds_to_exit=round(elapsed, 3), marked_alive_after=after,
               captures=sorted(p.name for p in (root / "obj_legs").iterdir()),
               leg2_attributed=f"./obj_b/Vb was killed by this runner on {sig.name}".encode() in replay)
    ok = (rc == -sig and not after and row["leg2_attributed"] and q[0] > 0 and q2[0] >= q[0]
          and row["marked_alive_before"] >= 3)
    for pid in after:
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
    os.close(r)
    row["verdict"] = "PASS" if ok else "FAIL"
    return row


def main():
    runner, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    rows = [one(runner, out / f"case-{s.name}", s) for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)]
    for row in rows:
        print(json.dumps(row))
    bad = sum(r["verdict"] != "PASS" for r in rows)
    print(f"blocked-stdout cancellation probe: {len(rows) - bad} PASS, {bad} FAIL")
    return 1 if bad else 0


sys.exit(main())
