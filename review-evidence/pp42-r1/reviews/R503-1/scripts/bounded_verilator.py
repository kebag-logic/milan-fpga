#!/usr/bin/env python3
"""Keep each nested native build to four workers; change no model options."""
import os
import sys

args = sys.argv[1:]
for i in range(len(args) - 1):
    if args[i] == "-j":
        args[i + 1] = "4"
os.execv(os.environ["PINNED_VERILATOR"], [os.environ["PINNED_VERILATOR"], *args])
