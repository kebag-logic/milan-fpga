#!/usr/bin/env python3
"""Run a command with SIGHUP ignored, as a nohup launcher leaves it.

usage: python3 -I -B ign_hup.py COMMAND [ARG ...]
"""
import os
import signal
import sys

signal.signal(signal.SIGHUP, signal.SIG_IGN)
os.execvp(sys.argv[1], sys.argv[1:])
