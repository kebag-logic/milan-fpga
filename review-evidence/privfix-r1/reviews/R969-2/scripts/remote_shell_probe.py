#!/usr/bin/env python3
"""Show the remote-root-shell detector is address-agnostic: the head fixture still fires, controls do not.

Usage: remote_shell_probe.py <repo>   (reads REMOTE_ROOT_SHELL_RE from scripts/check_baremetal_only.py at the checkout)
"""
import ast
import pathlib
import re
import sys

src = (pathlib.Path(sys.argv[1]) / "scripts/check_baremetal_only.py").read_text()
node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assign)
            and getattr(n.targets[0], "id", "") == "REMOTE_ROOT_SHELL_RE")
pattern, flags = node.value.args[0].value, re.IGNORECASE
rx = re.compile(pattern, flags)
for s, want in [("ssh -p 2222 root@192.0.2.2 reboot", True),       # head fixture (arm expects a finding)
                ("ssh -p 2222 root@203.0.113.9 reboot", True),     # any other address
                ("ssh -p 2222 root@board reboot", True),           # a hostname
                ("ssh build-host make lint", False),               # the near-miss-clean arm
                ("ssh -p 2222 admin@192.0.2.2 reboot", False)]:    # non-root login
    got = bool(rx.search(s))
    print(f"{'OK ' if got == want else 'BAD'} match={got!s:5} expected={want!s:5} {s}")
