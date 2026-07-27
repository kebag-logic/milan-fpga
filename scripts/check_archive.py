#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the archive stays navigable in both directions.

`historical_now_obsolete/` holds superseded documents, completed plans and
point-in-time snapshots. The USER rule is that obsolete docs are **archived,
never deleted** - history is preserved. That only works if an archived page
stays *reachable* and *labelled*, and both rot the moment someone moves a page
in a hurry:

  * a page with no banner reads as current to whoever lands on it from a
    search engine or an old link, which is worse than deleting it - it is a
    confident answer that stopped being true;
  * a page missing from the index is unreachable by browsing;
  * a "read instead" pointer to a doc that has itself since moved is a dead
    end at exactly the moment someone is trying to find current state.

So every archived page must carry a banner, appear exactly once in the index,
and name a living successor that still exists.

Usage:
    python3 scripts/check_archive.py           # gate (exit 1 on a violation)
    python3 scripts/check_archive.py --list    # show the resolved index
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "historical_now_obsolete"
INDEX = ARCHIVE / "README.md"

#: words that mark a page as not-current. Checked in the opening lines, which
#: is the only part a reader is guaranteed to see before acting on the content.
BANNER_RE = re.compile(
    r"supersed|archiv|historical|read instead|successor|no longer|obsolete"
    r"|frozen|completed plan|snapshot", re.I)
BANNER_SCAN_LINES = 20

#: a link to something inside the archive: `[text](findings/X.md)`
IN_LINK_RE = re.compile(r"\[[^\]]*\]\((?!\.\./)([A-Za-z0-9_./-]+\.md)\)")
#: a link OUT of the archive, i.e. the living successor: `[text](../docs/Y.md)`
OUT_LINK_RE = re.compile(r"\[[^\]]*\]\((\.\./[A-Za-z0-9_./-]+\.md)\)")


def tracked_outside_archive():
    """Committed markdown that is NOT itself in the archive."""
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
                         capture_output=True, text=True, check=True).stdout
    return [REPO / p for p in sorted(out.split("\0"))
            if p and not p.startswith("historical_now_obsolete/")]


def archived():
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", "historical_now_obsolete/*.md"],
        capture_output=True, text=True, check=True).stdout
    return sorted(REPO / p for p in out.split("\0") if p and
                  (REPO / p) != INDEX)


def index_rows():
    """(archived_target, [successor targets]) for each table row in the index."""
    rows = []
    for line in INDEX.read_text().split("\n"):
        if not line.startswith("|") or line.startswith("|--") or "---" in line:
            continue
        ins = IN_LINK_RE.findall(line)
        outs = OUT_LINK_RE.findall(line)
        if ins:
            rows.append((ins[0], outs, line))
    return rows


def main():
    listing = "--list" in sys.argv[1:]
    problems = []

    pages = archived()
    rows = index_rows()
    indexed = {}
    for tgt, outs, line in rows:
        indexed.setdefault(tgt, []).append((outs, line))

    # 1. every archived page: banner + exactly one index row
    for md in pages:
        rel = md.relative_to(ARCHIVE).as_posix()
        head = "\n".join(md.read_text().split("\n")[:BANNER_SCAN_LINES])
        if not BANNER_RE.search(head):
            problems.append(f"NO BANNER   {rel}: nothing in its first "
                            f"{BANNER_SCAN_LINES} lines says it is not current")
        n = len(indexed.get(rel, []))
        if n == 0:
            problems.append(f"UNINDEXED   {rel}: not listed in "
                            f"historical_now_obsolete/README.md")
        elif n > 1:
            problems.append(f"DUPLICATED  {rel}: {n} index rows")
        if listing:
            print(f"  {'ok' if n == 1 else 'BAD':<4} {rel}")

    # 2. every index row points at a real archived page and a LIVING successor
    have = {md.relative_to(ARCHIVE).as_posix() for md in pages}
    for tgt, entries in indexed.items():
        if tgt not in have:
            problems.append(f"STALE ROW   index lists '{tgt}' which is not in "
                            f"the archive")
        for outs, _ in entries:
            if not outs:
                problems.append(f"NO SUCCESSOR {tgt}: the row names no living "
                                f"document to read instead")
            for o in outs:
                if not (ARCHIVE / o).resolve().exists():
                    problems.append(f"DEAD FORWARD {tgt} -> '{o}' does not "
                                    f"exist; the successor moved or was renamed")

    # 3. a link INTO the archive must SAY so in its visible text. `[`X.md`](
    #    ../historical_now_obsolete/findings/X.md)` renders as a bare filename,
    #    so a reader following it has no way to know they are being sent to a
    #    retired document until they land on it - the banner catches them one
    #    click too late, and only if they read it.
    for md in tracked_outside_archive():
        rel = md.relative_to(REPO)
        for line in md.read_text().split("\n"):
            # HEADINGS are exempt: a heading is a structural identifier, and
            # editing its text changes its anchor, which silently breaks every
            # inbound `#fragment` link and the page's own contents list. The
            # three headings in the tree that link into the archive already say
            # "folded from", which conveys the same thing without moving an
            # anchor.
            if line.startswith("#"):
                continue
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
                text, tgt = m.group(1), m.group(2)
                if "historical_now_obsolete" not in tgt:
                    continue
                low = text.lower()
                if "archiv" in low or "historical_now_obsolete" in low:
                    continue
                problems.append(f"UNMARKED    {rel}: link text {text!r} points "
                                f"into the archive but does not say so")

    if problems:
        print(f"archive gate: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        print("\nAn archived page must stay labelled and reachable: a banner in "
              "its opening\nlines, exactly one row in "
              "historical_now_obsolete/README.md, and a successor\nthat still "
              "exists. Archived, never deleted - but never orphaned either.")
        return 1

    print(f"archive gate: OK ({len(pages)} archived page(s), each bannered, "
          f"indexed once, with a living successor)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
