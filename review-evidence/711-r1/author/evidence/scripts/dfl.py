"""Restore default signal dispositions (nohup and async shells ignore some), then exec the command."""
import os
import signal
import sys
for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM, signal.SIGPIPE):
    signal.signal(sig, signal.SIG_DFL)
os.execvp(sys.argv[1], sys.argv[1:])
