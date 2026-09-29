#!/usr/bin/env python3
"""Run the repository's own privacy scrub (docs_check.SCRUB_RULES) over an
extracted evidence packet and the two findings pages, and list extra
bench-identifying shapes the scrub does not own (absolute paths, IPv4,
interface names, serial devices).

usage: scrub_packet.py <repo-checkout> <extracted-packet-dir>
Exit 0 when the scrub is clean; the extra shapes are reported, not graded.
"""
import re
import sys
from pathlib import Path

repo, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import docs_check  # noqa: E402

pages = ["docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"]
f1, n1 = docs_check.scrub_files(repo, pages)
rels = sorted(str(p.relative_to(packet)) for p in packet.rglob("*") if p.is_file())
f2, n2 = docs_check.scrub_files(packet, rels)
print(f"scrub pages: {n1} scanned, {len(f1)} findings")
print(f"scrub packet: {n2} scanned, {len(f2)} findings")
for f in f1 + f2:
    print("  " + f)

EXTRA = [
    ("absolute home path", re.compile(r"/home/\w+|/Users/\w+")),
    ("ipv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("interface name", re.compile(r"\b(?:enp\d+s\d+\w*|eno\d+|ens\d+|eth\d+|wlp\w+)\b")),
    ("serial device", re.compile(r"/dev/tty\w+|/dev/serial/by-id/\S+")),
    ("tmp path", re.compile(r"/tmp/[\w.\-/]+")),
    ("mac address", re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b")),
    ("file-listing owner", re.compile(r"^[-dl][rwxsStT-]{9}\s+\d+\s+(\S+)\s+(\S+)")),
]
PUBLIC_OK = {"00:00:00:00:00:00", "02:00:00:00:00:01", "3c:c0:c6:01:02:03"}  # loopback, DUT, tree-published peer


def mask(label, tok):
    """Never re-publish a leaked token: keep the shape, hide the value."""
    if label in ("tmp path", "ipv4") or tok in PUBLIC_OK:
        return tok
    return tok[:1] + "*" * (len(tok) - 1)
counts = {}
for base, rel_list in ((repo, pages), (packet, rels)):
    for rel in rel_list:
        raw = (base / rel).read_bytes()
        if b"\0" in raw[:8000]:
            continue
        for lineno, line in enumerate(raw.decode(errors="replace").splitlines(), 1):
            for label, pat in EXTRA:
                for m in pat.finditer(line):
                    counts.setdefault((label, mask(label, m.group(0))), []).append(f"{rel}:{lineno}")
print("extra shapes (reported, not graded; private values masked):")
for (label, tok), where in sorted(counts.items()):
    if label == "tmp path":
        continue
    print(f"  {label}: {tok!r} x{len(where)} at {', '.join(where[:4])}{' ...' if len(where) > 4 else ''}")
tmp = sorted({w for (label, _), ws in counts.items() if label == "tmp path" for w in ws})
print(f"  temporary-directory paths: {len(tmp)} lines (raw-artifact index paths and tool paths)")
sys.exit(1 if (f1 or f2) else 0)
