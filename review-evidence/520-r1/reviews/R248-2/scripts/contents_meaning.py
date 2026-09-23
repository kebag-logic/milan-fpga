#!/usr/bin/env python3
"""Compare a page's Contents block between two commits.

usage: contents_meaning.py <repo> <old-rev> <new-rev> <page>

Reports, per entry: label equality, anchor equality, anchor resolution against
the page's own headings at the new revision (GitHub slug rule), separator used,
any U+2014 outside the label span, and a word-level description diff with the
punctuation that carries no words (dashes, colons, parentheses, stops, commas)
removed and case folded, so a punctuation-only rewrite reports "same words".
Exit 0 when labels and anchors are unchanged, every anchor resolves, every new
separator is `--`, and no U+2014 remains outside a label.
"""
import difflib
import re
import subprocess
import sys

ENTRY = re.compile(r"^- \*\*\[(?P<label>.+?)\]\(#(?P<anchor>[^)]+)\)\*\* (?P<sep>\S+) (?P<desc>.*)$")
EM = "—"


def show(repo, rev, page):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], check=True,
                          capture_output=True, text=True).stdout


def contents(text):
    lines = text.splitlines()
    start = lines.index("## Contents")
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            m = ENTRY.match(line)
            if not m:
                raise SystemExit(f"unparsed entry: {line}")
            out.append(m.groupdict())
    return out


def slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def words(desc):
    desc = desc.replace(EM, " ").replace("--", " ")
    desc = re.sub(r"[:;().,]", " ", desc)
    return desc.lower().split()


def main():
    repo, old_rev, new_rev, page = sys.argv[1:5]
    old_text, new_text = show(repo, old_rev, page), show(repo, new_rev, page)
    old, new = contents(old_text), contents(new_text)
    slugs = {slug(l[3:]) for l in new_text.splitlines() if l.startswith("## ")}
    ok = len(old) == len(new)
    print(f"entries old={len(old)} new={len(new)}")
    for o, n in zip(old, new):
        same_label = o["label"] == n["label"]
        same_anchor = o["anchor"] == n["anchor"]
        resolves = n["anchor"] in slugs
        em_outside = EM in n["desc"] or EM in n["sep"]
        ok &= same_label and same_anchor and resolves and n["sep"] == "--" and not em_outside
        print(f"\n[{n['label']}] label_same={same_label} anchor_same={same_anchor} "
              f"anchor_resolves={resolves} sep_old={o['sep']!r} sep_new={n['sep']!r} "
              f"em_dash_outside_label={em_outside}")
        ow, nw = words(o["desc"]), words(n["desc"])
        if ow == nw:
            print("  description: same words (punctuation-only change)" if o["desc"] != n["desc"]
                  else "  description: byte-identical")
        else:
            for op in difflib.SequenceMatcher(a=ow, b=nw).get_opcodes():
                if op[0] != "equal":
                    print(f"  {op[0]}: -[{' '.join(ow[op[1]:op[2]])}] +[{' '.join(nw[op[3]:op[4]])}]")
    print("\nCONTENTS-OK" if ok else "\nCONTENTS-FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
