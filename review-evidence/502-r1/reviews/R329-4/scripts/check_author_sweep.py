#!/usr/bin/env python3
"""Reproduce the round-4 author's sweep and compare it to the HANDOFF table.

Usage: check_author_sweep.py <repo> <rev> <HANDOFF.md> [extra-file:line ...]

Runs each published pattern S1-S7 with `git grep -n -i -I -E` at <rev>,
prints per-pattern counts, then compares the union of distinct file:line
hits with the table rows of HANDOFF.md. Extra file:line arguments are
reported as covered by some pattern or not.
"""
import html
import re
import subprocess
import sys

PATTERNS = {
    "S1": r"NVM_MARK|aecp_mark_pend_r|mark[^\n]*pend|pend[^\n]*mark",
    "S2": r"commit[- ]beats?|conservative[^\n]*duplicat|duplicat[^\n]*conservative",
    "S3": r"#502|late[- ]mark|mark[- ]tail|durable[^\n]*tail|tail[^\n]*durable",
    "S4": (r"NVM_MARK|aecp_mark_pend_r|commit marks?|command[- ]marks?|"
           r"mark[- ]trigger|\bmarks?\b.*\b(pending|pend_i)\b|"
           r"\b(pending|pend_i)\b.*\bmarks?\b|class[- ]?[67]"),
    "S5": (r"conservative.*duplicat|duplicat.*conservative|every.*commit|"
           r"commit.*every|late[- ]mark|mark[- ]tail|durable.*tail|"
           r"tail.*durable"),
    "S6": r"aecp_mark_pend_r",
    "S7": (r"conservative|aecp_mark_pend_r|every (accepted )?(map )?commit|"
           r"commit[- ]beats?|late[-_ ]mark|mark[-_ ]tail"),
}


def grep(repo, rev, pat):
    out = subprocess.run(["git", "-C", repo, "grep", "-n", "-i", "-I", "-E",
                          "-e", pat, rev, "--", "."],
                         capture_output=True, text=True).stdout
    hits = set()
    for line in out.splitlines():
        _, path, num, _ = line.split(":", 3)
        hits.add(f"{path}:{num}")
    return hits


def main():
    repo, rev, handoff, *extra = sys.argv[1:]
    union, total = set(), 0
    for key, pat in PATTERNS.items():
        hits = grep(repo, rev, pat)
        total += len(hits)
        union |= hits
        print(f"{key}: {len(hits)} hits")
    print(f"total pattern hits {total}; distinct file:line {len(union)}")
    rows = set()
    for line in open(handoff, encoding="utf-8"):
        m = re.match(r"\| [S0-9, ]+ \| `([^`]+:\d+)` \|", html.unescape(line))
        if m:
            rows.add(m.group(1))
    print(f"HANDOFF table rows {len(rows)}")
    print(f"hits missing from table: {sorted(union - rows)}")
    print(f"table rows not hit: {sorted(rows - union)}")
    for item in extra:
        print(f"extra {item}: {'COVERED' if item in union else 'NOT HIT'}"
              f" by S1-S7")
    return 0 if union == rows else 1


if __name__ == "__main__":
    sys.exit(main())
