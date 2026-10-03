#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exec argv with SIGINT, SIGQUIT and SIGHUP restored to their defaults.

A non-interactive shell's `&` starts a job with SIGINT/SIGQUIT ignored, and an
ignored signal survives exec; the suite sweep's cancellation preflight needs
them at default. Usage: sigdfl_exec.py <command> [args...]
"""
import os
import signal
import sys

for s in (signal.SIGINT, signal.SIGQUIT, signal.SIGHUP):
    signal.signal(s, signal.SIG_DFL)
os.execvp(sys.argv[1], sys.argv[1:])
