#!/usr/bin/env python3
"""Real-leg cancellation with a blocked stdout consumer (prior R245-1 F1).

    python3 probe_blocked_cancel.py <clone> <tmpdir> <signal-name>

Starts sim_pool.py --jobs=2 on the composed obj_nxn and obj_aclk legs with
stdout on a pipe nobody reads. Once obj_nxn's capture has been fully copied
into obj_legs/replay.log (so replay to the 64 KiB pipe is blocked while
obj_aclk still runs), it sends the signal and requires: the runner ends within
30 s by that signal, obj_aclk is reported killed, and no process whose cwd is
the suite directory survives. Exit 0 only if all three hold.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def survivors(suite: Path) -> list[str]:
    """Processes whose cwd is the suite directory, other than this one."""
    found = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit() or int(proc.name) == os.getpid():
            continue
        try:
            if os.readlink(proc / "cwd") == str(suite):
                found.append(f"{proc.name}: {(proc / 'cmdline').read_bytes()!r}")
        except OSError:
            continue
    return found


def main(argv: list[str]) -> int:
    """Run the probe and print its verdict lines."""
    suite = Path(argv[0]).resolve() / "tb/verilator/milan_dp"
    tmpdir = Path(argv[1]).resolve()
    signo = signal.Signals[argv[2]]
    tmpdir.mkdir(parents=True, exist_ok=True)
    read_end, write_end = os.pipe()
    env = dict(os.environ, TMPDIR=str(tmpdir))
    runner = subprocess.Popen(
        ["python3", "sim_pool.py", "--jobs=2", "./obj_nxn/Vmilan_dp_nxn",
         "./obj_aclk/Vmilan_dp_aclk"],
        cwd=suite, env=env, stdin=subprocess.DEVNULL, stdout=write_end,
        stderr=subprocess.STDOUT,
        preexec_fn=lambda: [signal.signal(s, signal.SIG_DFL)
                            for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)])
    os.close(write_end)
    transcript = suite / "obj_legs/replay.log"
    capture = suite / "obj_legs/01-Vmilan_dp_nxn.log"
    deadline = time.monotonic() + 540
    while time.monotonic() < deadline:
        time.sleep(1)
        if runner.poll() is not None:
            print(f"runner ended early with {runner.returncode}")
            return 1
        if (capture.exists() and transcript.exists()
                and b"RESULT:" in capture.read_bytes()
                and transcript.stat().st_size > capture.stat().st_size):
            break
    else:
        print("obj_nxn never finished inside the probe window")
        runner.kill()
        return 1
    time.sleep(2)
    print(f"obj_nxn replayed to the transcript ({transcript.stat().st_size} B); "
          f"pipe unread; sending {signo.name}")
    sent = time.monotonic()
    runner.send_signal(signo)
    try:
        code = runner.wait(timeout=30)
    except subprocess.TimeoutExpired:
        print("FAIL runner still alive 30 s after the signal")
        runner.kill()
        return 1
    took = time.monotonic() - sent
    os.close(read_end)
    left = survivors(suite)
    notes = [line for line in transcript.read_text(errors="replace").splitlines()
             if line.startswith("sim_pool:")]
    print(f"runner exit {code} after {took:.2f} s; survivors {len(left)}")
    for line in notes:
        print(f"  {line}")
    for line in left:
        print(f"  SURVIVOR {line}")
    ok = (code == -signo and not left
          and any("Vmilan_dp_aclk was killed by this runner" in n for n in notes))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
