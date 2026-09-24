#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R304-2 row-mapped anchor check for docs/SOURCE_EVIDENCE.md.

The unchanged round-1 static_checks.sh compares the SAME line number at base
and head, which by construction reports a refreshed anchor as moved. This
equivalent maps each ledger row (claim) instead:
  * a row present at base: the head anchor's head line must equal the base
    anchor's base line (the construct the claim was bound to before the PR),
    unless the base anchor itself was already off-construct at base, in which
    case the reviewer-stated construct below is used;
  * a row new at head: the head line must equal the reviewer-stated construct.
Every local #L anchor in the head ledger is covered, for every source file.

usage: anchor_rows_r2.py REPO BASE HEAD
"""
import re
import subprocess
import sys

ANCHOR = re.compile(r"\]\(\.\./([^)#]+)#L(\d+)\)")

# Reviewer-stated constructs, written from reading the head sources, used for
# new rows and for base anchors that were already off-construct at base.
STATED = {
    ("Deferred receive event", 0): "if (fin_r) begin",
    ("Registered policy slew level", 0): "output logic        phc_slew_active_o,",
    ("Registered policy slew level", 1): "2'd2: begin",
    ("Registered policy slew level", 2): "2'd3: begin",
    ("Registered policy slew level", 3): "def prog_leg_slew(base: int) -> Prog:",
}


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True,
                          text=True).stdout.splitlines()


def rows(repo, rev):
    out = {}
    for row in show(repo, rev, "docs/SOURCE_EVIDENCE.md"):
        if row.startswith("|"):
            links = ANCHOR.findall(row)
            if links:
                out[row.split("|")[1].strip()] = links
    return out


def line(repo, rev, path, n):
    lines = show(repo, rev, path)
    return lines[n - 1] if 0 < n <= len(lines) else None


def main():
    repo, base, head = sys.argv[1:4]
    b_rows, h_rows = rows(repo, base), rows(repo, head)
    bad = total = 0
    for claim, links in h_rows.items():
        for k, (rel, num) in enumerate(links):
            total += 1
            path, n = rel, int(num)
            got = line(repo, head, path, n)
            got_s = None if got is None else got.strip()
            want, how = None, ""
            if claim in b_rows and k < len(b_rows[claim]):
                bpath, bn = b_rows[claim][k]
                b = line(repo, base, bpath, int(bn))
                if (claim, k) in STATED:
                    want = STATED[(claim, k)]
                    how = (f"stated (base anchor {bpath}#L{bn} was "
                           f"{'' if b is None else b.strip()!r})")
                else:
                    want = None if b is None else b.strip()
                    how = f"base {bpath}#L{bn}"
            else:
                want = STATED.get((claim, k))
                how = "stated (new row)"
            ok = want is not None and got_s == want and bool(want)
            bad += not ok
            print(f"{'EXACT' if ok else 'WRONG'} {path}#L{n} [{claim}] "
                  f"<- {how} :: head={got_s!r}"
                  + ("" if ok else f" want={want!r}"))
    dropped = set(b_rows) - set(h_rows)
    for claim in sorted(dropped):
        bad += 1
        print(f"DROPPED row with anchors at base: {claim}")
    print(f"anchors: {total} checked, {total - bad} exact, {bad} not exact")
    return int(bad != 0)


if __name__ == "__main__":
    sys.exit(main())
