#!/usr/bin/env python3
"""sigclean.py CMD...: exec CMD with every signal at its default disposition and none blocked, as a fresh service
starts it. A command launched from this agent's session otherwise inherits SIGQUIT ignored and SIGCHLD blocked,
and the sweep runner's own cancellation controls (run_all_suites.sh preflight) then time out."""
import os
import signal
import sys

signal.pthread_sigmask(signal.SIG_SETMASK, set())
for number in signal.valid_signals():
    if number in (signal.SIGKILL, signal.SIGSTOP):
        continue
    try:
        if signal.getsignal(number) == signal.SIG_IGN:
            signal.signal(number, signal.SIG_DFL)
    except (OSError, ValueError):
        pass
os.execvp(sys.argv[1], sys.argv[1:])
