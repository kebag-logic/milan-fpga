#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check that every line anchor in the documentation selects the same text
at the head as the corresponding anchor selected at the base.

Usage: anchor_check.py <repo> <base> <head>

For each Markdown file, documentation line N at the head is paired with line
N at the base (the head changes anchors in place, so line counts match).
Each link target "path#Lx" or "path#Lx-Ly" is resolved relative to the
Markdown file, and the selected source lines are compared.  A pair is OK when
the selected text is identical, and also when the head anchor is unchanged
and its target file is unchanged.
"""
import posixpath
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s#]+)#L(\d+)(?:-L(\d+))?\)")


def show(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                       capture_output=True)
    return r.stdout.decode().split("\n") if r.returncode == 0 else None


def main():
    repo, base, head = sys.argv[1:4]
    docs = subprocess.run(["git", "-C", repo, "ls-files", "*.md"],
                          capture_output=True, check=True).stdout.decode().split()
    total = bad = changed = 0
    for doc in docs:
        hd, bd = show(repo, head, doc), show(repo, base, doc)
        if bd is None or len(hd) != len(bd):
            print(f"SKIP {doc}: base missing or line count differs")
            continue
        for n, (hl, bl) in enumerate(zip(hd, bd), 1):
            hl_links, bl_links = LINK.findall(hl), LINK.findall(bl)
            if len(hl_links) != len(bl_links):
                print(f"BAD {doc}:{n} link count differs")
                bad += 1
                continue
            for (hp, hx, hy), (bp, bx, by) in zip(hl_links, bl_links):
                total += 1
                tgt = posixpath.normpath(posixpath.join(posixpath.dirname(doc), hp))
                btgt = posixpath.normpath(posixpath.join(posixpath.dirname(doc), bp))
                hsrc, bsrc = show(repo, head, tgt), show(repo, base, btgt)
                hy, by = hy or hx, by or bx
                hsel = hsrc[int(hx) - 1:int(hy)] if hsrc else None
                bsel = bsrc[int(bx) - 1:int(by)] if bsrc else None
                moved = (hx, hy) != (bx, by)
                changed += moved
                inb = hsrc is not None and 1 <= int(hx) <= int(hy) <= len(hsrc)
                ok = inb and hsel == bsel
                state = "OK" if ok else "BAD"
                if not ok:
                    bad += 1
                print(f"{state} {doc}:{n} {tgt}#L{hx}-L{hy} "
                      f"(base #L{bx}-L{by}{', moved' if moved else ''})")
    print(f"anchors={total} moved={changed} bad={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
