#!/usr/bin/env python3
"""R358-1 probe: public-hygiene sweep of the PR's added lines and of the
published evidence packet, using the repository's own scrub rules plus a few
reviewer patterns (home paths, bench host role names from the issue body,
serial-number fields, absolute toolchain install paths).

usage: probe_hygiene.py <repo_root> <packet_dir> <base> <head>
Prints each hit with file and line; exits 0 always (hits are judged in REPORT.md).
"""
import re
import subprocess
import sys
from pathlib import Path

root, packet, base, head = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(root / "scripts"))
import docs_check  # noqa: E402

EXTRA = [
    ("home path", re.compile(r"/home/|/Users/|/root/|~/")),
    ("toolchain install path", re.compile(r"/opt/|/tools/Xilinx|Vivado|/usr/local/")),
    ("bench host role token", re.compile(r"\bpw[0-9]\b|ubuntu", re.I)),
    ("serial field", re.compile(r"serial[_ ]?(number)?\W{0,4}[:=]\s*\"?[A-Za-z0-9<]", re.I)),
    ("usb by-id", re.compile(r"/dev/serial/by-id|usb-[A-Za-z]")),
    ("tty device", re.compile(r"/dev/tty[A-Za-z]+[0-9]")),
    ("ipv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]


def sweep(label, text):
    hits = 0
    for f in docs_check.scrub_text(label, text):
        print("SCRUB", f)
        hits += 1
    for n, line in enumerate(text.splitlines(), 1):
        for name, rx in EXTRA:
            if rx.search(line):
                print(f"EXTRA {name}: {label}:{n}: {line.strip()[:160]}")
                hits += 1
    return hits


diff = subprocess.run(["git", "diff", "-U0", f"{base}..{head}"], cwd=root,
                      capture_output=True, text=True, check=True).stdout
added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
print("== PR added lines:", len(added.splitlines()))
total = sweep("PR-added-lines", added)
files = sorted(p for p in packet.rglob("*") if p.is_file())
print("== packet files:", len(files))
for p in files:
    total += sweep(str(p.relative_to(packet)), p.read_text(errors="replace"))
print("TOTAL_HITS", total)
