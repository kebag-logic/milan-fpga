#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Show how the head gate's command line parses the argument orders its self-test uses.

Usage: <python> argparse_order_repro.py <repo-checkout> <some-existing-directory>
Calls pp_resource_gate.main() for `record --write <dir> ...` (the order the new all-fabric
self-test uses) and `record <dir> ... --write` (the documented order) with a missing baseline,
and prints the exit status and whether argparse rejected the command line.
"""
import contextlib
import io
import sys
from pathlib import Path

repo, folder = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402

print(sys.version.split()[0])
for argv in (["record", "--write", folder, "--endpoint", "route-1x1", "--baseline", "/nonexistent.json"],
             ["record", folder, "--endpoint", "route-1x1", "--baseline", "/nonexistent.json", "--write"],
             ["check", folder, "--endpoint", "route-1x1", "--baseline", "/nonexistent.json"]):
    err, out = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            status = gate.main(argv)
        verdict = f"parsed; exit {status}"
    except SystemExit as error:
        verdict = f"argparse exit {error.code}: {err.getvalue().strip().splitlines()[-1]}"
    print(f"{' '.join(argv[:3])} ... -> {verdict}")
