#!/usr/bin/env python3
"""Derive the byte strings an evidence redaction masked, by comparing an
earlier archive extraction with the pinned one, file by file.

usage: derive_masked.py <earlier-root> <pinned-root> <out-dir>

Writes <out-dir>/masked_strings.bin-list (one hex-encoded original string per
line, deduplicated) and <out-dir>/mask_summary.txt (per file: size relation
and masked-run count; never the strings). The strings file is scratch-only:
it holds bench-identifying bytes and must never be published.
"""
import difflib
import os
import sys


def runs_same_len(a, b, gap=3):
    """Differing byte runs of two equal-length buffers, merging near runs."""
    out = []
    i, n = 0, len(a)
    while i < n:
        if a[i] == b[i]:
            i += 1
            continue
        s = i
        e = i
        j = i
        while j < n:
            if a[j] != b[j]:
                e = j
                j += 1
            elif j - e <= gap:
                j += 1
            else:
                break
        out.append((s, e + 1))
        i = e + 1
    return out


def main():
    early, pin, outd = sys.argv[1:4]
    strings = set()
    summary = []
    for dp, _, fns in os.walk(pin):
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), pin)
            if rel == "MANIFEST.json":
                continue
            pe = os.path.join(early, rel)
            if not os.path.exists(pe):
                summary.append(f"{rel}\tabsent-in-earlier")
                continue
            a = open(pe, "rb").read()
            b = open(os.path.join(pin, rel), "rb").read()
            if a == b:
                continue
            if len(a) == len(b):
                rs = runs_same_len(a, b)
                for s, e in rs:
                    strings.add(a[s:e])
                summary.append(f"{rel}\tsame-length\truns={len(rs)}")
            else:
                # line diff first, then a character diff inside each changed
                # line pair, so large files stay linear in practice
                la, lb = a.splitlines(keepends=True), b.splitlines(keepends=True)
                sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
                n = 0
                for tag, i1, i2, j1, j2 in sm.get_opcodes():
                    if tag == "equal":
                        continue
                    xa, xb = la[i1:i2], lb[j1:j2]
                    for k in range(max(len(xa), len(xb))):
                        ra = xa[k] if k < len(xa) else b""
                        rb = xb[k] if k < len(xb) else b""
                        if not ra:
                            continue
                        if len(ra) == len(rb):
                            for s0, e0 in runs_same_len(ra, rb):
                                strings.add(ra[s0:e0])
                                n += 1
                            continue
                        cm = difflib.SequenceMatcher(None, ra, rb, autojunk=False)
                        for t2, a1, a2, b1, b2 in cm.get_opcodes():
                            if t2 in ("replace", "delete") and a2 > a1:
                                strings.add(ra[a1:a2])
                                n += 1
                summary.append(f"{rel}\tlength-changed {len(a)}->{len(b)}\truns={n}")
    with open(os.path.join(outd, "masked_strings.hexlist"), "w") as f:
        for s in sorted(strings):
            f.write(s.hex() + "\n")
    with open(os.path.join(outd, "mask_summary.txt"), "w") as f:
        f.write("\n".join(sorted(summary)) + "\n")
    print(f"files changed: {len(summary)}; distinct masked strings: {len(strings)}")


if __name__ == "__main__":
    main()
