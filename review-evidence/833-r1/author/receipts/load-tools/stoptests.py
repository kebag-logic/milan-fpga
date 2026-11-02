#!/usr/bin/env python3
"""usage: stoptests.py  Scratch only. Stop this lane's leftover load and test runs: exact PIDs from this unit's cgroup, matched on the
program actually running (argv[0] and its script), so a shell whose text merely mentions these names is never matched."""
import collections
import os
import signal
import time
from pathlib import Path

CG = Path("/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-833-a726.service/cgroup.procs")
SCRIPTS = ("test_mutant_lifecycle.py", "test_suite_cancellation.py", "par.py", "focus.py", "worker.py", "mutants.py",
           "owned_process.py", "under.py", "withbuilds.py", "killlat.py", "buildloop.sh")


def rows():
    out = []
    for p in CG.read_text().split():
        try:
            argv = Path(f"/proc/{p}/cmdline").read_bytes().decode(errors="replace").split("\0")
            comm = Path(f"/proc/{p}/comm").read_text().strip()
        except OSError:
            continue
        out.append((int(p), comm, argv))
    return out


def victim(pid, comm, argv):
    if pid == os.getpid():
        return False
    if comm == "spin":
        return True
    if comm == "make" and any(a == "N=48" or a.endswith("compile.mk") for a in argv):
        return True
    if comm == "make" and "gptp_shadow" in " ".join(argv):
        return True
    if comm in ("bash", "sh", "<session agent>", "<shell proxy>"  # redacted: the session's own process names):
        return False
    return any(Path(a).name in SCRIPTS for a in argv[:3])


print("before", collections.Counter(c for _, c, _ in rows()).most_common(8))
for _ in range(30):
    found = [p for p, c, a in rows() if victim(p, c, a)]
    if not found:
        break
    for p in found:
        try:
            os.kill(p, signal.SIGKILL)
        except ProcessLookupError:
            pass
    time.sleep(0.3)
print("after", collections.Counter(c for _, c, _ in rows()).most_common(8))
