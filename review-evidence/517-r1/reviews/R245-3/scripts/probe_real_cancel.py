#!/usr/bin/env python3
"""Real-model cancellation probe through the actual milan_dp Makefile (#517).

usage: probe_real_cancel.py TREE TOOLBIN SIGNAL OUTDIR [blocked|file]
Runs `make run SIM_JOBS=2` on real Verilated legs in TREE (models already
built; the three gPTP prerequisite targets are marked up to date with -o so the
probe reaches the pool quickly). stdout is either a pipe that is held open and
never read (blocked) or a regular file. When two ordinary legs are alive in the
suite directory, SIGNAL is sent to make's process group, as coreutils timeout
does. PASS: make exits within 10 s; no Vmilan_dp_* process whose working
directory is in TREE survives; each started leg's capture exists; replay.log
names the killed legs and the unstarted ones; render_mutants.py did not run.
"""
import array, fcntl, json, os, signal, subprocess, sys, termios, time
from pathlib import Path


def legs(tree):
    out = []
    for e in os.listdir("/proc"):
        if not e.isdigit():
            continue
        try:
            cwd = os.readlink(f"/proc/{e}/cwd")
            argv = open(f"/proc/{e}/cmdline", "rb").read().split(b"\0")[0].decode()
            st = open(f"/proc/{e}/stat", "rb").read().rsplit(b")", 1)[1].split()[0]
        except OSError:
            continue
        if cwd.startswith(tree) and "Vmilan_dp_" in argv and st != b"Z":
            out.append((int(e), argv))
    return out


def main():
    tree, toolbin, signame, out = os.path.realpath(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
    mode = sys.argv[5] if len(sys.argv) > 5 else "blocked"
    sig = getattr(signal, signame)
    out.mkdir(parents=True, exist_ok=True)
    suite = f"{tree}/tb/verilator/milan_dp"
    env = {k: v for k, v in os.environ.items() if k not in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL", "MILAN_COUNTER_FRAME_OUT")}
    env["PATH"] = f"{toolbin}:{env['PATH']}"
    argv = ["make", "run", "SIM_JOBS=2", "VERILATOR_JOBS=6", "-o", "gptp", "-o", "gptp-lat", "-o", "gmstep"]
    if mode == "blocked":
        r, w = os.pipe()
        fcntl.fcntl(w, fcntl.F_SETPIPE_SZ, 4096)
    else:
        w = os.open(out / "make.stdout", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        r = None
    proc = subprocess.Popen(argv, cwd=suite, env=env, stdout=w, stderr=w, stdin=subprocess.DEVNULL,
                            start_new_session=True)
    os.close(w)
    if mode == "blocked":
        # keep the pipe drained until the pool starts, then stop reading
        os.set_blocking(r, False)
    sink = open(out / "make.stdout-before-block", "wb") if mode == "blocked" else None
    deadline = time.monotonic() + 1500
    seen = []
    while time.monotonic() < deadline:
        alive = [a for _, a in legs(tree) if "/obj_" in a]
        if len(alive) >= 2:
            seen = alive
            break
        if mode == "blocked":
            try:
                chunk = os.read(r, 65536)
                sink.write(chunk)
            except BlockingIOError:
                pass
        if proc.poll() is not None:
            break
        time.sleep(0.2)
    row = {"signal": signame, "mode": mode, "argv": argv, "alive_at_signal": seen}
    if mode == "blocked":
        sink.close()
        # stop reading. obj_dir's replay (~20 KB) exceeds the 4096-byte pipe,
        # so once obj_dir has exited the runner is blocked on output. Signal
        # while another ordinary leg is still alive; prove the block from the
        # on-disk transcript being longer than everything delivered.
        blocked_by = time.monotonic() + 300
        while time.monotonic() < blocked_by:
            alive = [a for _, a in legs(tree)]
            if "./obj_dir/Vmilan_dp_sim" not in alive and alive:
                break
            time.sleep(0.1)
        time.sleep(1)
        q = array.array("i", [0]); fcntl.ioctl(r, termios.FIONREAD, q); row["queued_before_signal"] = q[0]
        drained = (out / "make.stdout-before-block").stat().st_size
        replay_path = Path(suite) / "obj_legs" / "replay.log"
        row["make_bytes_read_before_block"] = drained
        row["transcript_bytes_before_signal"] = replay_path.stat().st_size
        try:
            row["runner_wchan"] = [open(f"/proc/{pid}/wchan").read() for pid, a in
                                   [(int(e), open(f"/proc/{e}/cmdline", "rb").read()) for e in os.listdir("/proc") if e.isdigit() and os.path.exists(f"/proc/{e}/cmdline")]
                                   if b"sim_pool.py" in a and os.readlink(f"/proc/{pid}/cwd").startswith(tree)]
        except OSError:
            row["runner_wchan"] = "unreadable"
    row["alive_before_signal"] = [a for _, a in legs(tree)]
    t0 = time.monotonic()
    if proc.poll() is None:
        os.killpg(proc.pid, sig)
    try:
        rc = proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        rc = "NO-EXIT-WITHIN-10S"
    row["make_exit"] = rc
    row["seconds_to_exit"] = round(time.monotonic() - t0, 3)
    time.sleep(0.5)
    survivors = legs(tree)
    row["survivors"] = [a for _, a in survivors]
    for pid, _ in survivors:
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
    logs = Path(suite) / "obj_legs"
    row["captures"] = sorted(p.name for p in logs.iterdir())
    replay = (logs / "replay.log").read_text(errors="replace")
    row["replay_runner_lines"] = [l for l in replay.splitlines() if l.startswith("sim_pool:")]
    row["render_ran_marker"] = "#386 render law" in (open(out / "make.stdout", errors="replace").read() if mode == "file" else "")
    if r is not None:
        rest = b""
        try:
            while True:
                chunk = os.read(r, 65536)
                if not chunk:
                    break
                rest += chunk
        except BlockingIOError:
            pass
        os.close(r)
        stream = (out / "make.stdout-before-block").read_bytes() + rest
        (out / "make.stdout-all").write_bytes(stream)
        start = stream.find(b"\n./obj_dir/Vmilan_dp_sim\n")
        row["transcript_bytes_delivered_by_exit"] = len(stream) - (start + 1) if start >= 0 else 0
    (out / "replay.log").write_text(replay)
    killed = [l for l in row["replay_runner_lines"] if f"killed by this runner on {signame}" in l]
    ok = ((mode != "blocked" or row["transcript_bytes_before_signal"] > row["transcript_bytes_delivered_by_exit"]) and isinstance(rc, int) and rc != 0 and not row["survivors"] and len(seen) >= 2
          and len(killed) >= 1 and any("was not started before" in l for l in row["replay_runner_lines"])
          and not row["render_ran_marker"])
    row["verdict"] = "PASS" if ok else "FAIL"
    (out / "result.json").write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row))
    return 0 if ok else 1


sys.exit(main())
