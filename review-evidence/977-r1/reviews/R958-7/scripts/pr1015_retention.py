#!/usr/bin/env python3
"""Round R958-7: is PR #1015's delta still in the reviewed head's tree?

Usage: python3 -I pr1015_retention.py <superproject-clone>

For every path PR #1015 changed on dev-soft-core (71bad8c0..0b594023, the
first-parent delta of its merge commit) this compares three blobs: the
dev-soft-core tip's, the previously reviewed head's (a5b19f70) and the
merge head's (25132e30). A path whose head blob is the tip's is retained
verbatim. For a path the #977 branch changed afterwards, every line #1015
added is looked up in the head blob; a line no longer present is listed
with the count of branch-side commits that touched the path, so a reader
can tell a later deliberate edit from a dropped hunk. Read-only.
"""
import subprocess
import sys

REPO = sys.argv[1]
BASE = "71bad8c0b973a15ee5f993a74f893ff7ff947c33"
TIP = "0b5940237e8de8bd5912db87e5e036a78f59b5a6"
PR1015 = "35d29eb71d2cc76717a4550787ef53ff2b72181f"
PREV = "a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35"
HEAD = "25132e3029557d2d992dc42f2a77c6840e5c05d3"


def git(*args, text=True):
    out = subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True)
    return out.stdout.decode("utf-8", "replace") if text else out.stdout


def blob(rev, path):
    try:
        return git("rev-parse", "-q", "--verify", f"{rev}:{path}").strip()
    except subprocess.CalledProcessError:
        return "absent"


def main():
    paths = git("diff", "--name-only", "--no-renames", BASE, TIP).split("\n")[:-1]
    verbatim = later = missing_total = 0
    print(f"paths in PR #1015's delta: {len(paths)}")
    for path in paths:
        tip, prev, head = blob(TIP, path), blob(PREV, path), blob(HEAD, path)
        if prev != head:
            print(f"FAIL {path}: head blob differs from the previously reviewed head's")
            return 1
        if tip == head:
            verbatim += 1
            print(f"VERBATIM   {path}")
            continue
        later += 1
        mode = git("ls-tree", HEAD, "--", path).split()[0]
        touched = git("rev-list", "--count", f"{PR1015}..{PREV}", "--", path).strip()
        if mode == "160000":
            print(f"LATER-PIN  {path}: tip {tip[:8]} head {head[:8]} ({touched} branch-side commits)")
            continue
        numstat = git("diff", "--numstat", "--no-renames", BASE, TIP, "--", path).split()
        if numstat[0] == "-":
            print(f"LATER-BIN  {path}: binary, regenerated on the branch ({touched} branch-side commits)")
            continue
        added = [ln[1:] for ln in git("diff", "-U0", "--no-renames", BASE, TIP, "--", path).split("\n")
                 if ln.startswith("+") and not ln.startswith("+++")]
        head_lines = set(git("show", f"{HEAD}:{path}").split("\n"))
        gone = [ln for ln in added if ln.strip() and ln not in head_lines]
        missing_total += len(gone)
        print(f"LATER-TEXT {path}: {len(added)} lines added by #1015, {len(gone)} not verbatim at head "
              f"({touched} branch-side commits)")
        for ln in gone:
            print(f"             - {ln[:150]}")
    print(f"verbatim {verbatim}; changed later on the branch {later}; "
          f"#1015 added lines not verbatim at head {missing_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
