#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Report a merged PR that landed against a NEGATIVE review, or left its Issue open.

WHY THIS EXISTS (issue #180). Two things this repository's process allows, and
nothing detected either:

  1. A PR merged while its last review verdict was NEGATIVE. PR #161 carried an
     `[R0] NEGATIVE` verdict (and an author note that it must stay unmerged as
     historical evidence), and it merged anyway. A maintainer overriding a
     NEGATIVE is a legitimate act - so this does NOT block a merge - but after
     the fact nobody could tell it happened.
  2. A PR whose body says `Closes #N` merged and left #N open. GitHub only
     auto-closes a linked Issue when the PR merges into the DEFAULT branch;
     here PRs merge into `dev`, so `Closes #N` never fires and the Issue sits
     open with its work already shipped (#159 did exactly this).

WHAT IT READS. The verdict is not GitHub's formal review decision - this repo's
reviews are COMMENT-type, so `reviewDecision` is always blank. The `[R<n>]
POSITIVE`/`NEGATIVE` verdict (AGENTS.md section 6) lives in free text, and in
EITHER the formal `reviews[].body` (newer PRs) OR the issue `comments[].body`
(PR #161's verdicts were comments). Both are scanned, ordered by time, and the
last verdict BEFORE the merge decides. An unanswered `BLOCKER` finding - one no
later POSITIVE verdict cleared - counts the same as a NEGATIVE.

TOOL ABSENCE IS UNKNOWN, NEVER A PASS. With no `gh`, or a `gh` that errors, the
gate exits 2 (cannot run), never 0. The `--selftest` needs no network: it drives
the pure `assess_pr` core over fixtures, including the mandated negative control
(a positive verdict + a closed Issue must NOT be reported) and a vacuity arm
that fails if the core is stubbed to find nothing.

    scripts/check_merge_review_integrity.py            # scan the merged-PR window
    scripts/check_merge_review_integrity.py --limit 40 # a wider window
    scripts/check_merge_review_integrity.py --selftest # drive the core over fixtures

Exit 0 = clean, 1 = a finding, 2 = cannot run / usage.
"""

import argparse
import json
import re
import subprocess
import sys

RC_OK, RC_FINDING, RC_CANNOT_RUN = 0, 1, 2

DEFAULT_BASE = "dev"
DEFAULT_LIMIT = 20

#: A verdict line: `[R<n>]` then, somewhere on the line, POSITIVE or NEGATIVE,
#: with or without the markdown bold the comment form uses. `[A<n>]` (author)
#: lines are deliberately not matched - only a reviewer publishes a verdict.
_VERDICT_RE = re.compile(r"^\s*\[R\d+\][^\n]*?\*{0,2}(POSITIVE|NEGATIVE)\*{0,2}",
                         re.M)
#: A BLOCKER finding line, same reviewer-line anchor.
_BLOCKER_RE = re.compile(r"^\s*\[R\d+\][^\n]*?\bBLOCKER\b", re.M)
#: `Closes/Fixes/Resolves #N`. A digit is required, so the PR template's bare
#: "Closes/relates to: #" placeholder names nothing.
_CLOSES_RE = re.compile(
    r"\b(?:clos(?:e|es|ed)|fix(?:e|es|ed)?|resolv(?:e|es|ed))\s+#(\d+)",
    re.I)


class Finding:
    def __init__(self, number, reason, detail):
        self.number = number
        self.reason = reason        # "negative-merge" | "open-blocker" | "open-issue"
        self.detail = detail

    def line(self):
        return "PR #%d: %s - %s" % (self.number, self.reason, self.detail)


def _verdict_events(pr):
    """[(timestamp, 'POSITIVE'|'NEGATIVE', is_blocker)] from reviews and comments.

    Reviews stamp `submittedAt`, comments `createdAt`; both are ISO-8601 UTC,
    so a string sort is chronological. A body can carry a verdict and a BLOCKER
    both; each is recorded so a later POSITIVE can be seen to clear an earlier
    BLOCKER.
    """
    events = []
    for r in pr.get("reviews") or []:
        _scan_body(r.get("body") or "", r.get("submittedAt") or "", events)
    for c in pr.get("comments") or []:
        _scan_body(c.get("body") or "", c.get("createdAt") or "", events)
    events.sort(key=lambda e: e[0])
    return events


def _scan_body(body, when, events):
    for m in _VERDICT_RE.finditer(body):
        events.append((when, m.group(1).upper(), False))
    for _ in _BLOCKER_RE.finditer(body):
        events.append((when, "BLOCKER", True))


def assess_pr(pr, issue_is_open):
    """Every review-integrity finding for one merged PR. Pure.

    `pr` is the gh JSON dict (number, mergedAt, body, reviews[], comments[]);
    `issue_is_open(n)` answers whether Issue #n is open. No I/O here, so the
    self-test drives it directly.
    """
    findings = []
    merged_at = pr.get("mergedAt") or ""
    # Only activity BEFORE the merge decision bears on whether the merge was
    # against a standing objection; a later review is post-merge commentary.
    events = [e for e in _verdict_events(pr) if not merged_at or e[0] <= merged_at]

    verdicts = [e for e in events if not e[2]]
    if verdicts and verdicts[-1][1] == "NEGATIVE":
        findings.append(Finding(
            pr["number"], "negative-merge",
            "merged %s with its last pre-merge review verdict NEGATIVE (%s)"
            % (merged_at or "?", verdicts[-1][0])))
    else:
        # No standing NEGATIVE, but a BLOCKER no later POSITIVE cleared is the
        # same unmet objection wearing a severity instead of a verdict word.
        last_positive = max((e[0] for e in events
                             if not e[2] and e[1] == "POSITIVE"), default="")
        open_blockers = [e for e in events if e[2] and e[0] > last_positive]
        if open_blockers:
            findings.append(Finding(
                pr["number"], "open-blocker",
                "merged %s carrying a BLOCKER no later POSITIVE verdict cleared"
                % (merged_at or "?")))

    for n in sorted({int(x) for x in _CLOSES_RE.findall(pr.get("body") or "")}):
        if issue_is_open(n):
            findings.append(Finding(
                pr["number"], "open-issue",
                "body says it closes #%d, which is still OPEN (a `dev` merge "
                "does not auto-close it)" % n))
    return findings


# ---------------------------------------------------------------- live I/O

class CannotRun(Exception):
    """gh is absent or answered in a way that is not a finding but not a pass."""


def _gh_json(args):
    try:
        p = subprocess.run(["gh"] + args, capture_output=True, text=True)
    except FileNotFoundError:
        raise CannotRun("gh is not installed")
    if p.returncode != 0:
        raise CannotRun("gh %s failed: %s" % (" ".join(args), p.stderr.strip()))
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as exc:
        raise CannotRun("gh %s returned non-JSON: %s" % (" ".join(args), exc))


def fetch_merged_prs(limit, base):
    """The `limit` most-recently-merged PRs into `base`, newest first.

    gh cannot sort by mergedAt, so over-fetch and sort here - the same reason
    check_merge_containment.py over-fetches its window.
    """
    rows = _gh_json(["pr", "list", "--state", "merged", "--base", base,
                     "--limit", str(max(limit * 3, 60)),
                     "--json", "number,mergedAt,body,reviews,comments"])
    rows.sort(key=lambda r: r.get("mergedAt") or "", reverse=True)
    return rows[:limit]


def issue_is_open(number):
    state = _gh_json(["issue", "view", str(number), "--json", "state"])
    return (state.get("state") or "").upper() == "OPEN"


# ------------------------------------------------------------------ selftest

def selftest():
    problems = []

    def openf(open_set):
        return lambda n: n in open_set

    # 1. NEGATIVE last verdict, in COMMENTS (the PR #161 shape).
    p1 = {"number": 161, "mergedAt": "2026-08-20T18:31:33Z", "body": "no closes",
          "reviews": [], "comments": [
              {"body": "[R1] **POSITIVE**", "createdAt": "2026-08-20T16:00:00Z"},
              {"body": "[R0] **NEGATIVE** - cleared-context review of 3cfc04ce",
               "createdAt": "2026-08-20T17:13:59Z"}]}
    f1 = assess_pr(p1, openf(set()))
    if [x.reason for x in f1] != ["negative-merge"]:
        problems.append("case1 negative-in-comments: %s" % [x.line() for x in f1])

    # 2. Closes an open Issue.
    p2 = {"number": 159, "mergedAt": "2026-08-20T10:00:00Z",
          "body": "[A1]\n\nCloses #159. Restores the docs gates.",
          "reviews": [{"body": "[R0] POSITIVE",
                       "submittedAt": "2026-08-20T09:00:00Z"}], "comments": []}
    f2 = assess_pr(p2, openf({159}))
    if [x.reason for x in f2] != ["open-issue"]:
        problems.append("case2 closes-open-issue: %s" % [x.line() for x in f2])

    # 3. Both reasons at once (PR #161 as filed).
    p3 = dict(p1, number=1161, body="Closes #777.")
    f3 = assess_pr(p3, openf({777}))
    if sorted(x.reason for x in f3) != ["negative-merge", "open-issue"]:
        problems.append("case3 both reasons: %s" % [x.line() for x in f3])

    # 4. THE NEGATIVE CONTROL: positive final verdict + closed Issue -> nothing.
    p4 = {"number": 200, "mergedAt": "2026-08-20T12:00:00Z",
          "body": "Closes #201.",
          "reviews": [{"body": "[R0] NEGATIVE",
                       "submittedAt": "2026-08-20T10:00:00Z"},
                      {"body": "[R0] POSITIVE re-review",
                       "submittedAt": "2026-08-20T11:00:00Z"}],
          "comments": []}
    f4 = assess_pr(p4, openf(set()))          # #201 is closed
    if f4:
        problems.append("case4 negative-control must be clean: %s"
                        % [x.line() for x in f4])

    # 5. NEGATIVE in a formal review body (the PR #189 shape).
    p5 = {"number": 189, "mergedAt": "2026-08-21T16:00:00Z", "body": "x",
          "reviews": [{"body": "[R0] NEGATIVE - exact head a8d3f50c",
                       "submittedAt": "2026-08-21T13:10:00Z"}], "comments": []}
    f5 = assess_pr(p5, openf(set()))
    if [x.reason for x in f5] != ["negative-merge"]:
        problems.append("case5 negative-in-review: %s" % [x.line() for x in f5])

    # 6. Unanswered BLOCKER after the last POSITIVE -> reported.
    p6 = {"number": 300, "mergedAt": "2026-08-20T15:00:00Z", "body": "x",
          "reviews": [{"body": "[R1] POSITIVE",
                       "submittedAt": "2026-08-20T12:00:00Z"},
                      {"body": "[R0] BLOCKER Tests - foo.py:1 - it lies",
                       "submittedAt": "2026-08-20T13:00:00Z"}], "comments": []}
    f6 = assess_pr(p6, openf(set()))
    if [x.reason for x in f6] != ["open-blocker"]:
        problems.append("case6 open-blocker: %s" % [x.line() for x in f6])

    # 7. BLOCKER later cleared by a POSITIVE -> nothing.
    p7 = {"number": 301, "mergedAt": "2026-08-20T15:00:00Z", "body": "x",
          "reviews": [{"body": "[R0] BLOCKER - fix it",
                       "submittedAt": "2026-08-20T12:00:00Z"},
                      {"body": "[R0] POSITIVE re-review, fixed",
                       "submittedAt": "2026-08-20T13:00:00Z"}], "comments": []}
    f7 = assess_pr(p7, openf(set()))
    if f7:
        problems.append("case7 cleared-blocker must be clean: %s"
                        % [x.line() for x in f7])

    # 8. A post-merge NEGATIVE does not retroactively condemn the merge.
    p8 = {"number": 302, "mergedAt": "2026-08-20T12:00:00Z", "body": "x",
          "reviews": [{"body": "[R0] POSITIVE",
                       "submittedAt": "2026-08-20T11:00:00Z"},
                      {"body": "[R0] NEGATIVE - found later",
                       "submittedAt": "2026-08-20T13:00:00Z"}], "comments": []}
    if assess_pr(p8, openf(set())):
        problems.append("case8 post-merge verdict must not count")

    # 9. Bare `#` with no number (the template default) names nothing.
    p9 = {"number": 303, "mergedAt": "2026-08-20T12:00:00Z",
          "body": "Closes/relates to: #\n[R0] POSITIVE",
          "reviews": [], "comments": []}
    if assess_pr(p9, lambda n: True):
        problems.append("case9 bare-hash must match no issue")

    # 10. VACUITY: cases 1/2/3/5/6 each assert a SPECIFIC finding, so a core
    # stubbed to return nothing makes them red - the suite cannot pass on a
    # no-op. Stated directly here too: the real core is non-empty on the
    # positive fixture, which is exactly what a stub would break.
    if not assess_pr(p1, openf(set())):
        problems.append("case10 vacuity: the core found nothing on the "
                        "positive fixture, so a stub would pass the suite")

    for p in problems:
        print("  SELFTEST FAILED: %s" % p)
    n = 10
    print("check_merge_review_integrity self-test: %d checks: %d PASS, %d FAIL"
          % (n, n - len(problems), len(problems)))
    return 1 if problems else 0


# ---------------------------------------------------------------------- main

def run(limit, base):
    prs = fetch_merged_prs(limit, base)
    findings = []
    # One issue-state lookup is cached, so a window that closes the same Issue
    # twice does not ask GitHub twice.
    cache = {}

    def open_cached(n):
        if n not in cache:
            cache[n] = issue_is_open(n)
        return cache[n]

    for pr in prs:
        findings += assess_pr(pr, open_cached)
    if findings:
        print("merge review-integrity: %d finding(s) over the last %d merged "
              "PR(s) into %s:" % (len(findings), len(prs), base))
        for f in findings:
            print("  %s" % f.line())
        print("A NEGATIVE merge can be a legitimate maintainer override; this "
              "names it so a reader can tell, and an open linked Issue should "
              "be closed or its divergence recorded (CONTRIBUTING 2.1).")
        return RC_FINDING
    print("merge review-integrity: clean over the last %d merged PR(s) into %s"
          % (len(prs), base))
    return RC_OK


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = ap.parse_args(argv[1:])
    if args.selftest:
        return selftest()
    try:
        return run(args.limit, args.base)
    except CannotRun as exc:
        print("CANNOT VERIFY merge review-integrity: %s" % exc, file=sys.stderr)
        print("  gh is required to read the merged-PR window; a missing tool is",
              file=sys.stderr)
        print("  not a pass.", file=sys.stderr)
        return RC_CANNOT_RUN


if __name__ == "__main__":
    sys.exit(main(sys.argv))
