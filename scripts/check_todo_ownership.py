#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a TODO in first-party code names the issue that owns it.

Why this exists. Rule 7 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a marker either names a concrete issue
or is resolved - it is not an untracked backlog. An unowned marker is worse
than no marker: it reads as a plan, nobody is accountable for it, and it
survives the change that made it wrong. `ptp_ts_top.sv` carried
`//TODO: add DMA engine signals` next to the three DMA streams that already
exist, which Issue #53 records as present and only needing attachment.

WHAT COUNTS AS A MARKER, and why the definition is narrow. The word TODO
appears 27 times in this tree and 26 of them are not markers. A naive search
finds:

  * `TODO.md` - a real, tracked historical document that pages legitimately
    cite by name;
  * `TODO = "TODO describe this section"` in `scripts/gen_toc.py` - an
    IDENTIFIER for the placeholder that gate refuses, and its comparisons
    `d == TODO`;
  * prose ABOUT markers - "as a TODO placeholder", "a TODO belongs in the
    roadmap, not here".

So a marker here is: the word, INSIDE A COMMENT, immediately followed by `:` or
`(`. That is the shape a real marker always has and none of the false positives
above do. The three classes are counted and printed rather than silently
dropped, so a reader can see what the narrowing cost.

Accepted forms: `TODO(#123)`, `FIXME(#123):` - the issue number is the owner.

Files excluded from the RTL half come from `scripts/lint_rtl.py`'s
`LINT_EXCLUDE`, the same list Rules 5 and 6 use; `hdl/milan/milan_top.sv` is an
archived Zynq top that no build compiles, and its markers are part of the
archive, not of maintained code. Markdown is not scanned at all: prose about a
document named TODO.md is not a marker.

Usage:
    python3 scripts/check_todo_ownership.py            # gate
    python3 scripts/check_todo_ownership.py --list     # markers and near-misses
    python3 scripts/check_todo_ownership.py --selftest # fixture arms

Exit 0 = every marker in gated first-party code names an issue.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE

WORDS = "TODO|FIXME|XXX|HACK"
#: the marker shape: the word, then optional space, then `:` or `(`
MARKER = re.compile(r"\b(%s)\b\s*(?=[:(])" % WORDS)
#: the owned form
OWNED = re.compile(r"\b(?:%s)\s*\(\s*#\d+\s*\)" % WORDS)
#: the word anywhere, for the near-miss inventory
ANY = re.compile(r"\b(%s)\b" % WORDS)

SLASH = (".sv", ".v", ".cpp", ".h", ".hpp", ".c")
HASH = (".py", ".sh", ".yml", ".yaml", ".tcl", ".mk")

EXCLUDED_PREFIXES = ("third_party/", "external/", "protocol-processor/",
                     "gptp-processor/", "gen/", "build/",
                     "historical_now_obsolete/")


def comment_text(line, path):
    """The comment part of one line, or "" if the line has none.

    Only the comment is searched, because the false positives that matter are
    an identifier and a string literal, and neither is a comment.
    """
    if path.endswith(SLASH):
        i = line.find("//")
        j = line.find("/*")
        starts = [k for k in (i, j) if k >= 0]
        return line[min(starts):] if starts else ""
    if path.endswith(HASH):
        i = line.find("#")
        return line[i:] if i >= 0 else ""
    return ""


def scannable():
    out = subprocess.run(["git", "ls-files"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    return [p for p in out
            if p.endswith(SLASH + HASH)
            and not p.startswith(EXCLUDED_PREFIXES)
            and p not in LINT_EXCLUDE]


def scan_line(line, path="x.py"):
    """(is_marker, is_owned) for one line."""
    body = comment_text(line, path)
    if not body:
        return False, False
    if not MARKER.search(body):
        return False, False
    return True, bool(OWNED.search(body))


def audit():
    unowned, owned, near = [], [], []
    for rel in scannable():
        for n, line in enumerate((REPO / rel).read_text(errors="replace").splitlines(), 1):
            is_marker, is_owned = scan_line(line, rel)
            if is_marker:
                (owned if is_owned else unowned).append((rel, n, line.strip()[:92]))
            elif ANY.search(line):
                near.append((rel, n, line.strip()[:92]))
    return unowned, owned, near


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    ck("an unowned marker is caught", scan_line("  //TODO: add DMA signals", "a.sv") == (True, False))
    ck("an owned marker is accepted",
       scan_line("  //TODO(#53): attach the DMA streams", "a.sv") == (True, True))
    ck("FIXME is a marker too", scan_line("  # FIXME: broken", "a.py") == (True, False))
    ck("an owned FIXME is accepted",
       scan_line("  # FIXME(#7): broken", "a.py") == (True, True))

    # -- the three false-positive classes, each observed in this tree --
    ck("a TODO.md filename reference is not a marker",
       scan_line("  # see the historical TODO.md for the original plan", "a.py")[0] is False,
       "no colon or paren follows the word")
    ck("an identifier named TODO is not a marker",
       scan_line('TODO = "TODO describe this section"', "a.py")[0] is False,
       "an assignment is not a comment")
    ck("a comparison against that identifier is not a marker",
       scan_line("    if d == TODO or not d:", "a.py")[0] is False)
    ck("prose about markers is not a marker",
       scan_line("  #     yet - a TODO belongs in the roadmap, not here", "a.sh")[0] is False)
    ck("a marker word in a trailing parenthetical is not a marker",
       scan_line("  //! still tied high today (REQ-MAC-03 TODO) so the pulse fires", "a.sv")[0] is False)

    # -- a marker in CODE, not a comment, is not a marker --
    ck("a string literal is not a comment",
       scan_line('    msg = "TODO: fill this in"', "a.py")[0] is False)

    # -- and the live tree must be readable --
    unowned, owned, near = audit()
    ck("the live scan reads the tree", len(near) > 0,
       "no near-miss at all - the scan is not reaching the tree")
    ck("the scan skips markdown", not any(r.endswith(".md") for r, _n, _l in near + unowned))

    n = 12
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="markers and near-misses")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    unowned, owned, near = audit()

    if args.list:
        print(f"owned markers ({len(owned)}):")
        for rel, n, line in owned:
            print(f"   {rel}:{n}  {line}")
        print(f"\nnear-misses - the word, but not a marker ({len(near)}):")
        for rel, n, line in near:
            print(f"   {rel}:{n}  {line}")
        print()

    for rel, n, line in unowned:
        print(f"UNOWNED MARKER: {rel}:{n} — {line}\n"
              f"    A marker names the issue that owns it, as TODO(#N), or it is "
              f"resolved. An unowned marker reads as a plan nobody is accountable for.")

    if unowned:
        return 1
    print(f"TODO ownership gate: OK ({len(owned)} owned marker(s), 0 unowned; "
          f"{len(near)} near-miss(es) correctly not treated as markers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
