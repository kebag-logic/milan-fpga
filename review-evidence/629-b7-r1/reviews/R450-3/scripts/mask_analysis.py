#!/usr/bin/env python3
"""Value-blind description of the two masking commits on the B7 evidence branch.

For each masking commit (parent -> commit), for every changed file under
review-evidence/629-b7-r1/author/, pair the removed and added lines and
record, per pair: the file, whether the line sits in a docstring/comment or in
code (Python tools only), and an opaque ID for the removed span.  The removed
spans themselves are NEVER printed; they are written to a private token file
(argument 2, under scratch/) for the scan in privacy_scan.py.

Usage: mask_analysis.py <repo> <private-token-file>
"""
import difflib, json, subprocess, sys

REPO, TOKFILE = sys.argv[1], sys.argv[2]
COMMITS = [("d36de704456713fb89b39a59151b72015fa00c6d", None),
           ("c6ad37e7d9163b5a85aef935a7d8e7f7f6686f7f", None)]
PFX = "review-evidence/629-b7-r1/author/"


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], check=True,
                          capture_output=True).stdout


def in_docstring(lines, idx):
    """True if line idx (0-based) is inside a triple-quoted string or is a comment."""
    if lines[idx].lstrip().startswith("#"):
        return True
    open_q = False
    for i, ln in enumerate(lines[:idx]):
        open_q ^= (ln.count('"""') + ln.count("'''")) % 2 == 1
    if open_q:
        return True
    ln = lines[idx]
    return ('"""' in ln or "'''" in ln)


def oid(s):
    # neutral label by first appearance; no digest of the value is ever printed
    for k, v in tokens.items():
        if v == s:
            return k
    return f"SPAN{len(tokens) + 1}"


tokens = {}
out = []
for c, _ in COMMITS:
    parent = git("rev-parse", c + "^").decode().strip()
    names = git("diff", "--name-only", parent, c).decode().split()
    files = [n for n in names if n.startswith(PFX)]
    out.append(f"commit {c} parent {parent}: {len(files)} packet files changed "
               f"(+ {len(names) - len(files)} outside the packet: "
               f"{[n for n in names if not n.startswith(PFX)]})")
    for f in files:
        a = git("show", f"{parent}:{f}").decode().splitlines()
        b = git("show", f"{c}:{f}").decode().splitlines()
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            for k in range(max(i2 - i1, j2 - j1)):
                la = a[i1 + k] if i1 + k < i2 else ""
                lb = b[j1 + k] if j1 + k < j2 else ""
                cm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
                rem = []
                for t2, x1, x2, y1, y2 in cm.get_opcodes():
                    if t2 in ("replace", "delete"):
                        rem.append(la[x1:x2])
                kind = "-"
                if f.endswith(".py"):
                    kind = "docstring/comment" if in_docstring(a, i1 + k) else "code"
                ids = []
                for r in rem:
                    lab = oid(r)
                    tokens.setdefault(lab, r)
                    ids.append(lab)
                out.append(f"  {f[len(PFX):]} line {i1 + k + 1}: {kind}; removed spans {ids}")
json.dump(tokens, open(TOKFILE, "w"))
print("\n".join(out))
print(f"distinct removed span IDs: {sorted(tokens)}")
