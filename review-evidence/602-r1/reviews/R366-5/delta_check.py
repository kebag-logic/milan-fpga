#!/usr/bin/env python3
"""Check the R366-5 delta (6c5ca18f..d09c72ea) is exactly the disposed page edit.

Usage: delta_check.py CLONE
Asserts: one commit, one parent, one-line message without trailers; the only
changed path is the finding page; all gitlinks are unchanged; the page's table
rows (lines starting with '|') are byte-identical to the prior head and to dev
0eff6d2e; every changed line falls in the two disposed regions; the link
targets named by the new text exist. Prints each changed line pair.
"""
import difflib
import re
import subprocess
import sys

OLD = "6c5ca18f12191a252447ec7c7c75363b851f2771"
NEW = "d09c72ea2b0be1a2df3e18e77774f14f6df3242c"
DEV = "0eff6d2e"
PAGE = "docs/findings/394_387_E1_SWITCH_CYCLES.md"
REGIONS_NEW = [(165, 177), (349, 355)]   # disposed regions at the new head


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], capture_output=True,
                          check=True).stdout


def main():
    clone = sys.argv[1]
    fails = []

    def check(ok, msg):
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            fails.append(msg)

    parents = git(clone, "rev-list", "--parents", "-n", "1", NEW).decode().split()
    check(parents == [NEW, OLD], f"single parent {OLD[:8]}")
    msg = git(clone, "log", "-1", "--format=%B", NEW).decode().rstrip("\n")
    check("\n" not in msg, f"one-line message: {msg!r}")
    check(not re.search(r"(?im)^[\w-]+-by:", msg), "no trailers")
    names = git(clone, "diff", "--name-status", "--no-renames", OLD, NEW).decode().split("\n")
    names = [n for n in names if n]
    check(names == [f"M\t{PAGE}"], f"only changed path is {PAGE}: {names}")
    links = lambda c: [l for l in git(clone, "ls-tree", "-r", c).decode().splitlines()
                       if l.startswith("160000")]
    check(links(OLD) == links(NEW), f"gitlinks unchanged ({len(links(NEW))})")

    old = git(clone, "show", f"{OLD}:{PAGE}").split(b"\n")
    new = git(clone, "show", f"{NEW}:{PAGE}").split(b"\n")
    dev = git(clone, "show", f"{DEV}:{PAGE}").split(b"\n")
    rows = lambda ls: [l for l in ls if l.startswith(b"|")]
    check(rows(old) == rows(new), f"table rows identical to {OLD[:8]}: {len(rows(new))} rows, "
          f"{sum(len(r) + 1 for r in rows(new))} bytes incl. newlines")
    check(rows(dev) == rows(new), f"table rows identical to dev {DEV}")
    check(old == dev, f"page at {OLD[:8]} equals dev {DEV} (delta is the only lane edit)")

    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        inside = all(any(lo <= j + 1 <= hi for lo, hi in REGIONS_NEW) for j in range(j1, j2))
        check(inside, f"{tag} old {i1 + 1}-{i2} -> new {j1 + 1}-{j2} inside disposed regions")
        for i in range(i1, i2):
            print(f"   - {i + 1}: {old[i].decode()}")
        for j in range(j1, j2):
            print(f"   + {j + 1}: {new[j].decode()}")

    text = b"\n".join(new).decode()
    check(text.count("issues/602#issuecomment-5859297355") == 2, "two ruling links")
    for doc, slug in (("docs/design/GM_LOSS_RECOVERY.md", "media-re-base-on-a-phc-step"),
                      ("docs/design/TIME_SYNC.md", "step-policy")):
        heads = git(clone, "show", f"{NEW}:{doc}").decode().splitlines()
        slugs = {re.sub(r"[^\w\- ]", "", h.lstrip("#").strip().lower()).replace(" ", "-")
                 for h in heads if h.startswith("#")}
        check(slug in slugs, f"anchor {doc}#{slug} exists")
    print(f"== {len(fails)} failed assertion(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
