#!/usr/bin/env python3
"""Compare two renderings of docs/DOCUMENTATION_AUDIT.md: page statuses and finding rows.

usage: compare_audit.py <repo> <before rev> <after rev>
Reads both pages with `git show`, so nothing in the work tree is used.
A finding row is keyed by (ID, page); its line and its statement cell are compared.
"""
import re, subprocess, sys

repo, before, after = sys.argv[1:4]


def page(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:docs/DOCUMENTATION_AUDIT.md"],
                          check=True, capture_output=True, text=True).stdout


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def parse(text):
    pages, findings, section = {}, {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:]
            continue
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        c = cells(line)
        link = re.match(r"\[([^\]]+?)(?: \(historical\))?\]\(", c[1] if section == "Findings" else c[0])
        if section == "Inventory" and link and len(c) == 9:
            pages[link.group(1)] = (c[1], c[5], c[6])
        elif section == "Findings" and link and len(c) == 6:
            copy = c[4].startswith("Copy of the ")
            findings[(c[0], link.group(1))] = (c[2], c[3], "copy" if copy else "recorded")
    return pages, findings


bp, bf = parse(page(before))
ap, af = parse(page(after))
print(f"pages: before {len(bp)}, after {len(ap)}")
for state in ("current", "stale", "superseded", "obsolete"):
    print(f"  {state}: before {sum(v[1] == state for v in bp.values())}, after {sum(v[1] == state for v in ap.values())}")
print(f"finding rows: before {len(bf)} ({sum(v[2] == 'copy' for v in bf.values())} copies), "
      f"after {len(af)} ({sum(v[2] == 'copy' for v in af.values())} copies)")
print("\n## Pages added or removed")
for p in sorted(set(ap) - set(bp)):
    print(f"added   {p}: {ap[p][1]} ({ap[p][2]})")
for p in sorted(set(bp) - set(ap)):
    print(f"removed {p}: was {bp[p][1]}")
print("\n## Pages whose status changed")
for p in sorted(set(ap) & set(bp)):
    if ap[p][1] != bp[p][1]:
        print(f"{p}: {bp[p][1]} ({bp[p][2]}) -> {ap[p][1]} ({ap[p][2]})")
print("\n## Finding rows removed (the generator no longer finds the statement on that page)")
for k in sorted(set(bf) - set(af)):
    print(f"{k[0]} {k[1]}: was line {bf[k][0]}, {bf[k][2]}")
print("\n## Finding rows added")
for k in sorted(set(af) - set(bf)):
    print(f"{k[0]} {k[1]}: line {af[k][0]}, {af[k][2]}")
print("\n## Finding rows whose line moved or now reads re-verify")
for k in sorted(set(af) & set(bf)):
    if af[k][0] != bf[k][0] or af[k][1] != bf[k][1]:
        print(f"{k[0]} {k[1]}: line {bf[k][0]} -> {af[k][0]}" + ("" if af[k][1] == bf[k][1] else " (statement cell changed)"))
print("\n## Line counts of pages carrying a finding row, before -> after")
for p in sorted({k[1] for k in set(af) | set(bf)}):
    print(f"{p}: {bp.get(p, ('--',))[0]} -> {ap.get(p, ('--',))[0]}")
