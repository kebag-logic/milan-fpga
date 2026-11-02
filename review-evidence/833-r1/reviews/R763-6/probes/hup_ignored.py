#!/usr/bin/env python3
"""Exec a command with SIGHUP ignored, as a nohup-style launcher would.

Usage: python3 -I hup_ignored.py COMMAND [ARG ...]
"""
import os
import signal
import sys

signal.signal(signal.SIGHUP, signal.SIG_IGN)
os.execvp(sys.argv[1], sys.argv[1:])
