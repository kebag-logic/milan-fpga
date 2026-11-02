#!/usr/bin/env python3
"""usage: probe_owner.py <clone> <trap-child|late-survivor> <scratch dir>
Disposable probes of scripts/owned_process.py at production constants.
Run inside a user+PID namespace so anything left behind dies with it.

trap-child: a shell is cancelled while its child ignores SIGTERM and only dies
  about 4.6 s after cleanup starts, past the 4 s kill time. The shell is resumed
  late, and its terminal trap runs one leaf command that takes 1 s. The
  claimed contract: that command shares the resumed shell's window, so it
  completes and writes its marker.
late-survivor: the same late resume at about 12.5 s, but the trap starts a
  descendant whose SIGKILL never takes effect. Reports when the run fails, in
  owner seconds, against the documented "up to 24 s".
"""
import json, os, signal, sys, threading, time
from pathlib import Path

clone, mode, scratch = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(clone / "scripts"))
import owned_process
from owned_process import Cancelled, OwnedProcesses

scratch.mkdir(parents=True, exist_ok=True)
STUBBORN = r'''
import os, signal, sys, time
from pathlib import Path
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
Path(sys.argv[1]).write_text(str(os.getpid()))
while True:
    time.sleep(0.02)
'''
ready_a, ready_b, marker = scratch / "ready-a", scratch / "ready-b", scratch / "trap-command-ran"
if mode == "trap-child":
    # One leaf process does the trap's work, so no live child protects it.
    leaf = scratch / "leaf.py"
    leaf.write_text("import sys, time\ntime.sleep(1)\nopen(sys.argv[1], 'w').write('ran')\n")
    trap = f"{sys.executable} {leaf} {marker}; exit 143"
    release_a = 4.6
else:
    trap = f"{sys.executable} -c \"$STUBBORN\" \"{ready_b}\" & wait; exit 143"
    release_a = 12.5
script = f"trap '{trap}' TERM\n" if mode == "late-survivor" else f"trap \"{trap}\" TERM\n"
script += f"{sys.executable} -c \"$STUBBORN\" \"{ready_a}\" &\nwait\n"
env = dict(os.environ, STUBBORN=STUBBORN)

def watchdog():
    time.sleep(120)
    print(json.dumps(dict(mode=mode, result="WATCHDOG: no verdict in 120 s")), flush=True)
    os._exit(3)
threading.Thread(target=watchdog, daemon=True).start()

def pid_of(path):
    return int(path.read_text()) if path.exists() and path.read_text() else None

first = []
result = dict(mode=mode, constants=dict(GRACE=owned_process.GRACE_SECONDS, KILL_ALL=owned_process.KILL_ALL_SECONDS,
                                        TRAP=owned_process.TRAP_SECONDS, REAP=owned_process.REAP_SECONDS))
began = None
try:
    with OwnedProcesses() as owner:
        send = owner._send

        def hooked(pid, start, signum):
            """SIGKILL to A only lands after release_a; SIGKILL to B never lands."""
            now = time.monotonic()
            if not first:
                first.append(now)
            if signum == signal.SIGKILL and pid == pid_of(ready_a) and now < first[0] + release_a:
                return False
            if signum == signal.SIGKILL and pid == pid_of(ready_b):
                return True
            return send(pid, start, signum)
        owner._send = hooked

        def cancel():
            global began
            while pid_of(ready_a) is None:
                time.sleep(0.01)
            began = time.monotonic()
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=cancel, daemon=True).start()
        owner.run(["bash", "-c", script], env=env)
    result["result"] = "run returned without cancellation"
except Cancelled as exc:
    result["result"] = f"Cancelled({exc.signum})"
except RuntimeError as exc:
    result["result"] = str(exc)[:600]
result["wall_seconds_from_cancel"] = round(time.monotonic() - began, 2) if began else None
result["trap_command_marker"] = marker.exists()
b = pid_of(ready_b)
if b is not None:
    try:
        os.kill(b, signal.SIGKILL)
    except ProcessLookupError:
        pass
print(json.dumps(result), flush=True)
