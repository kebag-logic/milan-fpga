#!/usr/bin/env python3
"""Scan the two findings pages and every archived packet file for bench-identifying text.

usage: privacy_scan.py <repo-root at the reviewed head> <packet-root: .../review-evidence/b1-r1>

Applies the repository's own deny-list (scripts/docs_check.py SCRUB_RULES: identity
rules plus local-info shapes) and a few generic shapes. Prints file, line and the
rule name only, never the matched text, so this receipt carries no identifying token.
"""
import re, sys
from pathlib import Path

repo, pk = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import docs_check  # noqa: E402

rules = [(rx, "repo:" + name) for rx, name, _ in docs_check.SCRUB_RULES]
rules += [
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "generic:IPv4 address"),
    (re.compile(r"\b[a-z0-9-]+\.(?:lan|local|home|internal|corp|intra)\b", re.I), "generic:local hostname"),
    (re.compile(r"/(?:home|Users|root)/[A-Za-z]"), "generic:account path"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}"), "generic:email"),
    (re.compile(r"\b(?:eth|ens|enp|eno|enx|wlp|wlan)\d\w*"), "generic:interface name"),
    (re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b", re.I), "generic:colon MAC address"),
]
files = [repo / "docs/findings/599_394_E1_LINK_CYCLES.md", repo / "docs/findings/387_SOFTWARE_GM_STEP.md"]
files += sorted(p for p in pk.rglob("*") if p.is_file())
hits = {}
for f in files:
    try:
        text = f.read_text(errors="replace")
    except OSError:
        continue
    rel = str(f.relative_to(repo)) if str(f).startswith(str(repo)) else str(f.relative_to(pk.parent.parent))
    for n, line in enumerate(text.splitlines(), 1):
        for rx, name in rules:
            if rx.search(line):
                hits.setdefault(name, []).append("%s:%d" % (rel, n))
print("scanned %d files with %d rules" % (len(files), len(rules)))
for name in sorted(r[1] for r in rules):
    h = hits.get(name, [])
    print("%-40s %4d hit lines%s" % (name, len(h), ("; first: " + ", ".join(h[:6])) if h else ""))
