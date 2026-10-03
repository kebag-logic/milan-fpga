#!/usr/bin/env python3
"""Value-blind privacy scan for the B8 capture's channel count and
sample-format name. Never prints a matched value: only counts, file names and
line numbers.

usage: privacy_scan.py EVIDENCE_GIT_DIR PAGE TREE [TREE ...]
  The channel-count phrase is taken from the line the masking commit
  (36ee6d8a) removed from tools/grade_b8.py relative to 5bad6a43: the words
  that the masked line no longer carries. Each TREE is scanned recursively.
"""
import os, re, subprocess, sys

gitdir, page, trees = sys.argv[1], sys.argv[2], sys.argv[3:]
diff = subprocess.check_output(["git", "-C", gitdir, "diff", "-U0", "5bad6a43", "36ee6d8a", "--",
                                "review-evidence/629-b8-r1/author/tools/grade_b8.py"], text=True)
old = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
new = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
assert len(old) == 1 and len(new) == 1, "expected a one-line mask"
ow, nw = old[0].split(), new[0].split()
removed = [w for w in ow if w not in nw]
digits = [w for w in removed if re.search(r"\d", w)]
print("masked line: words removed", len(removed), "of which with a digit", len(digits))
print("mask label present in retained line:", bool(re.search(r"<[a-z-]+>", new[0])))
# channel-context phrases only: the removed number followed by a capture or
# channel word. A bare neighbour-word phrase is not used, because reporting a
# line it matches would hint at the value.
val = [w for w in digits if re.fullmatch(r"\d+", w)]
assert len(val) == 1, "expected one masked integer"
phr_re = [re.compile(r"(?<![\w.])" + re.escape(val[0]) + r"[\s-]*(?:capture|ch\b|chan|channel)", re.I)]
# generic sound-library sample-format names (signed/unsigned/float with width and endianness)
fmt_re = re.compile(r"\b(?:S|U)(?:8|16|18|20|24|32)(?:_3)?_(?:LE|BE)\b|\bFLOAT(?:64)?_(?:LE|BE)\b", re.I)
# channel-count phrasing tied to the external capture or snippet
cap_re = re.compile(r"(?:capture|snippet|all-channel)[^.\n]{0,40}?\b\d{1,2}\s*(?:-|\s)?ch(?:annel)?s?\b|\b\d{1,2}\s*(?:-|\s)?ch(?:annel)?s?\b[^.\n]{0,40}?(?:capture|snippet)", re.I)

def scan(path, label):
    try:
        data = open(path, "rb").read()
    except OSError:
        return 0
    if b"\0" in data[:4096]:
        return 0
    t = data.decode("utf-8", "replace")
    hits = 0
    for n, line in enumerate(t.splitlines(), 1):
        kinds = []
        if any(r.search(line) for r in phr_re): kinds.append("masked-phrase")
        if fmt_re.search(line): kinds.append("format-name-shape")
        if cap_re.search(line): kinds.append("capture-channel-phrase")
        if kinds:
            hits += 1
            print(f"  HIT {label}:{n} {','.join(kinds)}")
    return hits

total = 0
print("PAGE", page)
total += scan(page, os.path.basename(page))
for tree in trees:
    print("TREE", tree)
    for d, _, fs in os.walk(tree):
        for f in sorted(fs):
            p = os.path.join(d, f)
            total += scan(p, os.path.relpath(p, tree))
print("total hit lines:", total)
