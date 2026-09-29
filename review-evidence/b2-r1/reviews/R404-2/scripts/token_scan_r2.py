#!/usr/bin/env python3
"""Round-2 privacy scan (F4 re-check), built on round 1's token_scan.py.

Usage: token_scan_r2.py <repo-clone> <root> [<root> ...]
Env:   PRIVATE_TOKENS=<file>  controller-host identity patterns (held outside
       the packet; never printed, only hit counts).
       POSITIVE_CONTROL=<dir> a tree that must hit every private class at
       least once (the pre-redaction archive), so an empty result is not a
       broken pattern set.

Scans the three changed pages at the clone's HEAD and every file under each
root with round 1's classes (the repository gate's SCRUB_RULES plus generic
shapes). For every identifier-class token (colon MAC, fffe-form EUI-64,
vendor-prefix 16-hex) it also reports whether the same token occurs in a
tracked file of the clone (git grep), i.e. whether it is already public in
the tree, and the JSON field names it appears under. Tokens stay masked.
"""
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import token_scan as T  # noqa: E402

repo = Path(sys.argv[1])
roots = [Path(p) for p in sys.argv[2:]]
rules = T.load_rules(repo)
private = []
if os.environ.get("PRIVATE_TOKENS"):
    private = [re.compile(l.strip(), re.I) for l in open(os.environ["PRIVATE_TOKENS"]) if l.strip()]
pages = [repo / "docs/findings/606_FIRST_BIND_MEASUREMENT.md",
         repo / "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md",
         repo / "docs/findings/README.md"]
IDCLS = ("colon-mac", "eui64-from-mac", "hex16-vendor")
KEY = re.compile(r'"(\w+)"\s*:\s*"?([0-9a-fA-F:]{12,23})')


def scan(files):
    hits = defaultdict(lambda: defaultdict(set))
    fields = defaultdict(set)
    priv = defaultdict(set)
    for f in files:
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            for pat, cls, _fix in rules:
                if pat.search(line):
                    hits["gate:" + cls]["<gate class>"].add(str(f))
            for i, pat in enumerate(private):
                if pat.search(line):
                    priv[i].add(str(f))
            for cls, pat in T.GENERIC:
                for m in pat.finditer(line):
                    tok = m.group(0)
                    if cls in ("eui64-from-mac", "hex16-vendor") and T.SAFE.match(tok):
                        continue
                    if cls == "hex16-vendor" and (not re.search(r"[a-fA-F]", tok[:6]) or "fffe" in tok.lower()):
                        continue
                    if cls == "colon-mac" and T.SAFE_MAC.match(tok):
                        continue
                    if cls == "ipv4" and not all(int(x) <= 255 for x in tok.split(".")):
                        continue
                    hits[cls][tok].add(str(f))
            for m in KEY.finditer(line):
                fields[m.group(2).lower()].add(m.group(1))
    return hits, fields, priv


def tracked(tok):
    r = subprocess.run(["git", "-C", str(repo), "grep", "-l", "-i", "-F", tok, "HEAD", "--"],
                       capture_output=True, text=True)
    return len([l for l in r.stdout.splitlines() if l.strip()])


def report(label, files, base):
    hits, fields, priv = scan(files)
    print(f"== {label}: {len(files)} files; private patterns {len(private)}")
    print(f"   private-pattern hits: {sum(len(v) for v in priv.values())} file-hits"
          f" over {len(priv)} of {len(private)} patterns")
    if not hits:
        print("   no hit in any class")
    for cls in sorted(hits):
        toks = hits[cls]
        nfiles = len(set().union(*toks.values()))
        print(f"   {cls}: {len(toks)} distinct, {nfiles} files")
        for tok, fs in sorted(toks.items(), key=lambda kv: -len(kv[1]))[:12]:
            shown = T.mask(tok) if cls in IDCLS else tok
            extra = ""
            if cls in IDCLS:
                extra = f"\ttracked files at HEAD containing it: {tracked(tok)}" \
                        f"\tfields: {sorted(fields.get(tok.lower(), set())) or '-'}"
            ex = os.path.relpath(sorted(fs)[0], base)
            print(f"      {shown}\t{len(fs)} files\te.g. {ex}{extra}")
    return priv


report("pages at HEAD", pages, repo)
for r in roots:
    report(f"root {r.name}", sorted(p for p in r.rglob("*") if p.is_file()), r)
if os.environ.get("POSITIVE_CONTROL"):
    pc = Path(os.environ["POSITIVE_CONTROL"])
    priv = report("POSITIVE CONTROL (pre-redaction tree, scratch only)",
                  sorted(p for p in pc.rglob("*") if p.is_file()), pc)
    print("   positive control: private patterns hit ->", "YES" if priv else "NO (pattern set broken)")
