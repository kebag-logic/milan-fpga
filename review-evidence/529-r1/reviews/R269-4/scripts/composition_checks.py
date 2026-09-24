#!/usr/bin/env python3
"""Composition checks for a two-parent merge-train candidate.

  1. For every path changed on BOTH sides since the merge base, a raw
     three-way `git merge-file` of (base, dev, source) must reproduce the
     candidate blob byte for byte, and the two sides' hunks are listed with
     their distance.
  2. Cross-citations: every `path:line` reference that one side ADDS and that
     points into a file the OTHER side changed is resolved at the citing
     side's tree and at the candidate; the cited line text must be the same,
     or the citation went stale in the composition.
  3. Bare path mentions the one side adds of files the other side changed
     (informational: the reader may want to look).

Every git call is made with --no-ext-diff/--no-textconv where it applies, so
the bytes compared are the object bytes.

Usage: composition_checks.py <repo> <candidate> <dev> <source>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CITE = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:sv|svh|v|cpp|hpp|h|py|md|sh|yml|yaml|tcl|mk))"
                  r"(?::(\d+)(?:-(\d+))?)?")


def git(repo, *args, text=True):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          text=text).stdout


def changed(repo, a, b):
    out = git(repo, "diff", "--no-renames", "--name-only", a, b)
    return [l for l in out.splitlines() if l]


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def added_lines(repo, a, b):
    out = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "-U0", a, b)
    cur, res = None, []
    for l in out.splitlines():
        if l.startswith("+++ "):
            cur = l[6:] if l.startswith("+++ b/") else None
        elif l.startswith("+") and not l.startswith("+++") and cur:
            res.append((cur, l[1:]))
    return res


def hunks(repo, a, b, path):
    out = git(repo, "diff", "--no-ext-diff", "--no-textconv", "-U0", a, b, "--", path)
    return re.findall(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", out, re.M)


def resolve(all_paths, name):
    while name.startswith(("../", "./")):
        name = name.split("/", 1)[1]
    if name in all_paths:
        return [name]
    if "/" in name:
        tail = "/" + name
        return [p for p in all_paths if p.endswith(tail)]
    return [p for p in all_paths if p.rsplit("/", 1)[-1] == name]


def main():
    repo, cand, dev, src = sys.argv[1:5]
    mb = git(repo, "merge-base", dev, src).strip()
    dev_ch, src_ch = set(changed(repo, mb, dev)), set(changed(repo, mb, src))
    both = sorted(dev_ch & src_ch)
    print("merge base %s\ncandidate %s\ndev %s\nsource %s" % (mb, cand, dev, src))
    print("\n## 1. paths changed on both sides: %d" % len(both))
    for p in both:
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            for name, rev in (("base", mb), ("dev", dev), ("src", src)):
                (t / name).write_bytes(blob(repo, rev, p) or b"")
            r = subprocess.run(["git", "merge-file", "-p", str(t / "dev"), str(t / "base"), str(t / "src")],
                               capture_output=True)
            ok = r.returncode == 0 and r.stdout == blob(repo, cand, p)
            print("%s: merge-file conflicts=%d, reproduces candidate blob: %s" % (p, r.returncode, ok))
        hd, hs = hunks(repo, mb, dev, p), hunks(repo, mb, src, p)
        print("  dev hunks (base line,count): %s" % [(int(h[0]), int(h[1] or 1)) for h in hd])
        print("  src hunks (base line,count): %s" % [(int(h[0]), int(h[1] or 1)) for h in hs])
        gap = min(abs(int(a[0]) - int(b[0])) for a in hd for b in hs) if hd and hs else None
        print("  nearest base-line distance between the two sides' hunks: %s" % gap)
    cand_paths = set(git(repo, "ls-tree", "-r", "--name-only", "--full-tree", cand).splitlines())
    for side, rev, other_ch, other in (("source", src, dev_ch, "dev"), ("dev", dev, src_ch, "source")):
        print("\n## 2/3. lines the %s side adds that name a file the %s side changed" % (side, other))
        n_line, n_bad = 0, 0
        mentions = {}
        for path, text in added_lines(repo, mb, rev):
            for m in CITE.finditer(text):
                name, lo, hi = m.group(1), m.group(2), m.group(3)
                targets = [t for t in resolve(cand_paths, name) if t in other_ch]
                if not targets:
                    continue
                if not lo:
                    mentions.setdefault(name, set()).add(path)
                    continue
                n_line += 1
                lo_i, hi_i = int(lo), int(hi or lo)
                for tp in targets:
                    at_side = (blob(repo, rev, tp) or b"").decode(errors="replace").splitlines()
                    at_cand = (blob(repo, cand, tp) or b"").decode(errors="replace").splitlines()
                    s = at_side[lo_i - 1:hi_i]
                    c = at_cand[lo_i - 1:hi_i]
                    same = s == c
                    n_bad += 0 if same else 1
                    print("  %s cites %s:%s -> %s: %s" % (path, name, lo + ("-" + hi if hi else ""), tp,
                                                        "SAME at candidate" if same else "STALE at candidate"))
                    if not same:
                        print("     at %s: %r" % (side, s[:3]))
                        print("     at cand: %r" % (c[:3]))
        print("  line citations into the other side's files: %d, stale at candidate: %d" % (n_line, n_bad))
        for name, where in sorted(mentions.items()):
            print("  mention (no line) of %s in: %s" % (name, ", ".join(sorted(where))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
