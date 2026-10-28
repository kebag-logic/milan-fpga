#!/usr/bin/env python3
# Verilator 5.050 wrapper used for every reviewer run: maps "-j 0" (all cores)
# to "-j 4" so concurrent builds share the host. Put it first on PATH as
# "verilator". PINNED_VERILATOR names the pinned 5.050 executable.
import os, sys
real = os.environ.get("PINNED_VERILATOR", "verilator-5.050")
a = sys.argv[1:]
for i in range(len(a) - 1):
    if a[i] == "-j" and a[i + 1] == "0":
        a[i + 1] = "4"
os.execvp(real, [real, *a])
