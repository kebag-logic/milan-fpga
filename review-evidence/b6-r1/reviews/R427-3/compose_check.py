#!/usr/bin/env python3
"""Composition check for the B6 merge-train candidate (findings index).

Usage: compose_check.py <repo> <base> <pred> <src> <cand>
  base: merge base of the predecessor and the source
  pred: predecessor head already in the candidate (B5, merged dev)
  src:  this PR's source head
  cand: the composed candidate

Asserts, from git objects only:
  1. every path changed by both pred and src (relative to base) is listed;
  2. the candidate tree equals the mechanical three-way merge of pred and src;
  3. in docs/findings/README.md, each index row's link target appears exactly
     once, the row sequence equals base's with pred's and src's inserted rows
     at the positions their own heads give them, and every row is byte-equal
     to the row in the head that introduced it;
  4. every relative link in the index resolves to a blob in the candidate.
Exit 0 on all pass, 1 otherwise.
"""
import posixpath
import re
import subprocess
import sys

INDEX = "docs/findings/README.md"
ROW = re.compile(r"^\| \[[^\]]*\]\(([^)#]+)[^)]*\)")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


def rows(repo, rev):
    out = []
    for line in git(repo, "show", f"{rev}:{INDEX}").splitlines():
        m = ROW.match(line)
        if m:
            out.append((m.group(1), line))
    return out


def merged_order(base, head):
    """Return {target: predecessor-target-in-head} for rows head adds."""
    base_t = {t for t, _ in base}
    added = {}
    prev = None
    for t, line in head:
        if t not in base_t:
            added[t] = (prev, line)
        prev = t
    return added


def main(repo, base, pred, src, cand):
    fails = []
    ch = lambda a, b: set(git(repo, "diff", "--name-only", a, b).split())
    shared = ch(base, pred) & ch(base, src)
    print(f"shared paths (pred & src vs base): {sorted(shared)}")
    mt = git(repo, "merge-tree", "--write-tree", pred, src).split()[0]
    ct = git(repo, "rev-parse", f"{cand}^{{tree}}").strip()
    print(f"mechanical merge tree {mt}; candidate tree {ct}")
    if mt != ct:
        fails.append("candidate tree differs from mechanical merge")

    b, p, s, c = (rows(repo, r) for r in (base, pred, src, cand))
    ctargets = [t for t, _ in c]
    for t in sorted(set(ctargets)):
        if ctargets.count(t) != 1:
            fails.append(f"row {t} appears {ctargets.count(t)} times")
    expected = [t for t, _ in b]
    for head in (p, s):
        for t, (prev, _) in merged_order(b, head).items():
            expected.insert(expected.index(prev) + 1 if prev else 0, t)
    print(f"candidate rows: {len(ctargets)}; expected rows: {len(expected)}")
    if ctargets != expected:
        fails.append(f"row order {ctargets} != expected {expected}")
    source_line = {t: l for t, l in b}
    for head in (p, s):
        for t, (_, line) in merged_order(b, head).items():
            source_line[t] = line
            print(f"added row: {t}")
    for t, line in c:
        if source_line.get(t) != line:
            fails.append(f"row {t} not byte-equal to its introducing head")

    blobs = set(git(repo, "ls-tree", "-r", "--name-only", cand).split())
    text = git(repo, "show", f"{cand}:{INDEX}")
    n = 0
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target):
            continue
        path = posixpath.normpath(posixpath.join(posixpath.dirname(INDEX),
                                                 target.split("#")[0]))
        n += 1
        if path not in blobs:
            fails.append(f"unresolved link {target} -> {path}")
    print(f"relative links checked: {n}")
    for f in fails:
        print(f"FAIL: {f}")
    print("compose_check: " + ("FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:6]))
