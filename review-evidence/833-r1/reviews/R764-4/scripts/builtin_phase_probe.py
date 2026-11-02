#!/usr/bin/env python3
"""Impact probe: a cancelled shell resumed past grace + 1 s whose trap spends BUSY seconds in builtins
before its last step. Prints whether the trap finished. Same set-up as owner_shell_window otherwise.

usage: builtin_phase_probe.py SCRIPTS_DIR BUSY_SECONDS
"""
import os, signal, sys, tempfile, threading, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import test_suite_cancellation as t  # noqa: E402
from owned_process import Cancelled, OwnedProcesses  # noqa: E402
busy = float(sys.argv[2])
with tempfile.TemporaryDirectory(prefix="busy-") as d:
    d = Path(d)
    ready, marker, done = d / "ready", d / "trap-ran", d / "trap-done"
    script = (f"trap 'echo trapped > \"{marker}\"; e=$(( ${{EPOCHREALTIME/./}} + {int(busy * 1e6)} )); "
              f"while (( ${{EPOCHREALTIME/./}} < e )); do :; done; echo done > \"{done}\"; exit 143' TERM\n"
              f"{sys.executable} -c \"$STUBBORN\" \"{ready}\" &\nwait\n")
    env = dict(os.environ, STUBBORN=t.STUBBORN)
    blocked = []
    with t.stages(GRACE_SECONDS=0.2, KILL_ALL_SECONDS=0.2):
        try:
            with OwnedProcesses() as owner:
                send = owner._send

                def late(pid, start, signum):
                    now = time.monotonic()
                    if not blocked:
                        blocked.append(now)
                    if signum == signal.SIGKILL and pid != owner.process.pid and now < blocked[0] + 1.5:
                        return False
                    return send(pid, start, signum)
                owner._send = late

                def cancel():
                    t.published(ready)
                    os.kill(os.getpid(), signal.SIGTERM)
                threading.Thread(target=cancel, daemon=True).start()
                owner.run(["bash", "-c", script], env=env)
        except Cancelled:
            pass
    print(f"busy={busy} trap_started={marker.exists()} trap_finished={done.exists()}", flush=True)
    sys.exit(0 if done.exists() else 1)
