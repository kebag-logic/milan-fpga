#!/usr/bin/env python3
"""Multi-line companion to stale_scan.py: statements split across lines.

Usage: window_scan.py CLONE [COMMIT] [WINDOW]
The R366-4 F1 statement spanned lines ("The contract requires one counted
event per step." ... "One `mr` toggle and one MEDIA_RESET record that
event."), which a single-line co-mention scan only half sees. This lists every
window of WINDOW lines (default 7) in a tracked text file outside
docs/history/** where a PHC-step term and an `mr`/MEDIA_RESET term both occur,
merged into regions. A region is marked [NEG] if it contains a #602-consistent
marker (unchanged, preserves, no step-only, #602, excluded, ...), else [READ].
Every region, both kinds, is for reading in context; the mark only orders it.
"""
import re
import subprocess
import sys

STEP = re.compile(r"PHC|\bstep|re-?base|settime|adjtime", re.I)
MR = re.compile(r"`mr`|\bmr\b|MEDIA_RESET|media event|media re-?start")
NEG = re.compile(r"#602|602 ruling|unchanged|preserv|leaves? .{0,20}(mr|MEDIA_RESET)|no step-only|"
                 r"exclud|not an? .?mr|without changing|adds no|neither|never requests|pre-#602", re.I)
SUFFIX = (".md", ".sv", ".svh", ".v", ".cpp", ".hpp", ".h", ".py", ".feature", ".c", ".json",
          ".yml", ".yaml", ".tsv", ".txt", "Makefile")


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], capture_output=True,
                          check=True).stdout


def main():
    clone = sys.argv[1]
    commit = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    win = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    files = git(clone, "ls-tree", "-r", "--name-only", commit).decode().splitlines()
    files = [f for f in files if f.endswith(SUFFIX) and not f.startswith(("docs/history/", "third_party/"))]
    total = {"NEG": 0, "READ": 0}
    for path in files:
        try:
            lines = git(clone, "show", f"{commit}:{path}").decode("utf-8").splitlines()
        except (UnicodeDecodeError, subprocess.CalledProcessError):
            continue
        s = [bool(STEP.search(l)) for l in lines]
        m = [bool(MR.search(l)) for l in lines]
        hits = []
        for i in range(len(lines)):
            lo, hi = i, min(len(lines), i + win)
            if any(s[lo:hi]) and any(m[lo:hi]):
                hits.append((lo, hi))
        regions = []
        for lo, hi in hits:
            if regions and lo <= regions[-1][1]:
                regions[-1][1] = max(regions[-1][1], hi)
            else:
                regions.append([lo, hi])
        for lo, hi in regions:
            body = lines[lo:hi]
            mark = "NEG" if any(NEG.search(l) for l in body) else "READ"
            total[mark] += 1
            print(f"[{mark}] {path}:{lo + 1}-{hi}")
            for k, l in enumerate(body):
                if s[lo + k] or m[lo + k]:
                    print(f"    {lo + k + 1}: {l[:220]}")
    print(f"== regions at {commit}: {total['NEG']} with a #602-consistent marker, "
          f"{total['READ']} without (all read in context)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
