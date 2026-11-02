#!/usr/bin/env python3
"""Reviewer probe: wall time to a cleanup verdict at the product's stage constants.

usage: bound_probe.py SCRIPTS_DIR MODE CANCEL_AT LIVE_UNTIL
MODE:
  late-listing  root `true` is collected before cleanup; one listed entry dies
                inside every census forever; SIGTERM reaches the owner CANCEL_AT
                seconds into cleanup (the round 2 finding's shape).
  shell-listing a bash root with a TERM trap is cancelled while running (so it is
                stopped and still owned); a fake descendant stays live until
                LIVE_UNTIL s into cleanup, then dies inside every census forever.
  shell-survivor same, but after LIVE_UNTIL the fake entry stays listed and
                owned, never collected and unkillable (a true survivor).
Prints one RESULT line: wall seconds from cleanup start to the RuntimeError,
whether the shell was resumed, and the failure text. No product file is edited;
only instance attributes and the module's _live are replaced.
"""
import os, signal, sys, time
sys.path.insert(0, sys.argv[1])
import owned_process as op  # noqa: E402

mode, cancel_at, live_until = sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
FAKE = 2 ** 22 + 1
consts = {n: getattr(op, n) for n in ("GRACE_SECONDS", "KILL_ALL_SECONDS", "TRAP_SECONDS",
                                       "REAP_SECONDS", "MAX_PASS_SECONDS")}
start = []
resumes = []
sent = []
with op.OwnedProcesses() as owner:
    real_desc, real_reap, real_live, real_signal = owner._descendants, owner._reap, op._live, owner._signal

    def signalling(fd, signum):
        if fd == owner.root_fd and signum == signal.SIGCONT and start:
            resumes.append(round(time.monotonic() - start[0], 2))
        real_signal(fd, signum)
    owner._signal = signalling

    def elapsed():
        if not start:
            start.append(time.monotonic())
        return time.monotonic() - start[0]

    def desc():
        t = elapsed()
        if mode == "late-listing" and t >= cancel_at and not sent:
            sent.append(round(t, 2))
            os.kill(os.getpid(), signal.SIGTERM)
        found = real_desc()
        found[FAKE] = (os.getpid(), "0")
        return found

    def reap():
        got = real_reap()
        t = time.monotonic() - start[0] if start else 0.0
        if mode == "late-listing" or (mode == "shell-listing" and t >= live_until):
            got = set(got) | {FAKE}
        return got

    def live(pid):
        if pid == FAKE:
            t = time.monotonic() - start[0] if start else 0.0
            return t < live_until
        return real_live(pid)
    owner._descendants, owner._reap, op._live = desc, reap, live

    if mode == "late-listing":
        argv = ["true"]
    else:
        # The shell ignores nothing: its TERM trap records and exits after the resume.
        argv = ["bash", "-c", "trap 'exit 0' TERM; sleep 1000 & wait; exit 0"]
    failure = "no failure"
    began = None
    try:
        if mode == "late-listing":
            owner.run(argv)
        else:
            # Cancel while the command runs, so the shell is stopped and owned.
            def later(*_):
                os.kill(os.getpid(), signal.SIGTERM)
            signal.signal(signal.SIGALRM, later)
            signal.setitimer(signal.ITIMER_REAL, 0.5)
            owner.run(argv)
    except RuntimeError as exc:
        failure = str(exc)
    except op.Cancelled as exc:
        failure = f"Cancelled {exc.signum}"
    wall = time.monotonic() - start[0] if start else -1
    owner._descendants, owner._reap, op._live = real_desc, real_reap, real_live
    notified = owner.root_notified
    owner.cancel_signal = 0
print(f"RESULT mode={mode} cancel_at={cancel_at} live_until={live_until} constants={consts} "
      f"wall={wall:.2f} cancel_sent={sent} root_notified={notified} resumes={resumes} failure={failure[:300]}",
      flush=True)
