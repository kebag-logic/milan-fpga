#!/usr/bin/env python3
"""Tool identity: the #606 page's tool table against the packet's tools.

Usage: tool_hash_check.py <packet author dir> <repo clone>

Hashes every tool the page names from the packet's tools/ directory, and the
UART grader from the repository at the base commit 13eda870, and compares
each with the page row.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path


def main():
    pkt, repo = Path(sys.argv[1]), Path(sys.argv[2])
    text = (repo / "docs/findings/606_FIRST_BIND_MEASUREMENT.md").read_text()
    rows = re.findall(r"^\| `([\w.]+\.(?:py|sh))` \| [^|]+ \| `([0-9a-f]{64})` \|$", text, re.M)
    ok = bool(rows)
    for name, want in rows:
        got = hashlib.sha256((pkt / "tools" / name).read_bytes()).hexdigest()
        print(name, got == want, got)
        ok &= got == want
    m = re.search(r"\[UART grader\]\(\.\./\.\./scripts/baremetal_uart_smoke\.py\) at `13eda870` \| [^|]+ \| `([0-9a-f]{64})`", text)
    blob = subprocess.run(["git", "-C", str(repo), "show", "13eda870:scripts/baremetal_uart_smoke.py"],
                          capture_output=True, check=True).stdout
    got = hashlib.sha256(blob).hexdigest()
    print("UART grader at 13eda870", got, bool(m) and got == m.group(1))
    ok &= bool(m) and got == m.group(1)
    print("rows", len(rows), "RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
