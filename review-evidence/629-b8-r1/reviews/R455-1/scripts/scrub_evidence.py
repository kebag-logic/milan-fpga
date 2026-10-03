#!/usr/bin/env python3
"""Apply the repository's own identity/local-info scrub (scripts/docs_check.py
SCRUB_RULES via scrub_text) plus generic private-shape patterns to the
published B8 evidence tree, the PR body and the B8 page section.

usage: scrub_evidence.py <repo-root> <evidence-dir> <pr-body-file> <out.txt>
"""
import re
import sys
from pathlib import Path

repo, ev, prbody, out = map(Path, sys.argv[1:5])
sys.path.insert(0, str(repo / "scripts"))
import docs_check as D  # noqa: E402

GENERIC = {
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "mac": re.compile(r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b"),
    "home": re.compile(r"/home/|/Users/|/root/"),
    "usb-serial": re.compile(r"\bserial[-_ ]?(?:no|number)?\s*[:=]\s*\S+", re.I),
    "dev-node": re.compile(r"/dev/(?:tty\w+|snd/\w+|serial/\S+)"),
    "iface": re.compile(r"\b(?:enp\w+|eno\d\w*|ens\d\w*|enx[0-9a-f]+|wlp\w+|eth\d)\b"),
    "alsa-card": re.compile(r"\bhw:(?!0,0\b)\S+|plughw:\S+|card\s*\d+:", re.I),
}
lines = []
files = sorted(p for p in ev.rglob("*") if p.is_file())
texts = [(str(p.relative_to(ev)), p) for p in files]
texts.append(("PR-BODY(live)", prbody))
total = 0
for rel, p in texts:
    try:
        t = p.read_text(errors="replace")
    except Exception as e:  # noqa: BLE001
        lines.append(f"UNREADABLE {rel}: {e}")
        continue
    total += 1
    for f in D.scrub_text(rel, t):
        lines.append(f"SCRUB {f}")
    for name, rx in GENERIC.items():
        for m in rx.finditer(t):
            lines.append(f"GENERIC {name} {rel}: {m.group(0)[:60]}")
lines.append(f"files scanned: {total}")
out.write_text("\n".join(lines) + "\n")
print("\n".join(lines[-40:]))
