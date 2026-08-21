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

The verdict LEXICON is wider than the bare word and case-folded: `REQUEST
CHANGES`, `DO NOT MERGE` (PR #123, #128) and "not [yet] a positive review" are
rejections too, and PR #128 merged over exactly those while an
uppercase-`NEGATIVE`-only reader saw nothing. Clean-lens and finding lines
(`[R<n>] PASS/BLOCKER/MAJOR/...`) are NOT verdicts and are skipped for verdict
purposes, and `NEGATIVE` excludes the compound "negative control", so a PASS
line reading "PASS ... negative-control" is not mistaken for a rejection, and
"not validated (for merge)" / "cannot validate" are rejections while
"VALIDATED" is the positive pole of that axis (#111, #112). See _line_verdict.

SCOPE. This is a NAMED-DIALECT parser, not an NLP one: it reads the AGENTS.md
section 6 convention (`[R<n>] POSITIVE`/`NEGATIVE`, `[R<n>] BLOCKER`) plus the
handful of rejection phrasings this corpus actually uses. It deliberately does
NOT try to understand arbitrary prose - a reviewer who states a rejection only
as free text ("this needs more work", an unprefixed `**Verdict: ...**` line)
is off-convention and can be missed; the fix for that is to publish the verdict
as `[R<n>] NEGATIVE`, not to grow this regex without bound. That boundary is
the honest one after three rounds of dialect-chasing ([R]/[R1]/[R2]).

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

#: A reviewer line. `[A<n>]` (author) lines are deliberately not matched - only
#: a reviewer publishes a verdict. A leading markdown header (`##`/`###`) or
#: bold (`**`) is allowed, because reviews write findings as `### [R1] BLOCKER`
#: and verdicts as `## [R1] POSITIVE` headers ([R2] on this PR).
_LEAD = r"^\s*#*\s*\**\s*"
_RLINE_RE = re.compile(_LEAD + r"\[R\d+\]")
#: A findings / clean-lens line: `[R<n>]` then one of the section-6 severity
#: or PASS tokens. These are NOT the top verdict, and their PROSE routinely
#: contains verdict words that are not verdicts - a `PASS` lens line says
#: "PASS ... negative-control", a finding says "the blockers remain". Reading
#: those as a verdict flips a POSITIVE-reviewed clean merge to negative-merge
#: (PR #199 did exactly that under the first cut of this parser, [R1]).
_FINDING_LEAD_RE = re.compile(
    _LEAD + r"\[R\d+\]\s*(?:\*\*\s*)?(PASS|BLOCKER|MAJOR|MINOR|SUGGESTION)\b",
    re.I)
#: A rejection, in the dialects this corpus actually uses: `NEGATIVE` (but not
#: the compound "negative control", this repo's own test vocabulary),
#: `DO NOT MERGE`, `REQUEST CHANGES`, and "not validated (for merge)" /
#: "cannot validate" ([R2]: PR #111 merged over "still not validated for merge").
#: This is a NAMED-DIALECT parser, not a prose NLP one - see the WHAT IT READS /
#: SCOPE note in the module docstring.
_NEG_RE = re.compile(
    r"\bNEGATIVE\b(?![-\s]control)|\bDO\s+NOT\s+MERGE\b|\bREQUEST[-\s]CHANGES\b"
    r"|\bnot\s+validated\b|\bcannot\s+validate\b",
    re.I)
#: "not [yet] a positive [review]" - a rejection (PR #128). The `a` keeps it
#: off praise like "not only positive but excellent".
_NOT_A_POSITIVE_RE = re.compile(r"\bnot\b(?:\s+yet)?\s+a\s+positive\b", re.I)
#: An acceptance: `POSITIVE`, or `VALIDATED` (the positive pole of the same
#: axis as "not validated"; #112 clears its blockers with "... VALIDATED"). The
#: `not validated` rejection is checked FIRST in _line_verdict, so it wins over
#: the `VALIDATED` substring it contains.
_POSITIVE_RE = re.compile(r"\bPOSITIVE\b|\bVALIDATED\b", re.I)
#: `Closes/Fixes/Resolves` (optional `:`) then one or more `#N`, comma- or
#: `and`-separated. A digit is required, so the template's bare
#: "Closes/relates to: #" placeholder names nothing. `\b` before the keyword
#: keeps `discloses`/`prefixes` from matching.
_CLOSES_RE = re.compile(
    r"\b(?:clos(?:e|es|ed)|fix(?:e|es|ed)?|resolv(?:e|es|ed))\b\s*:?\s*"
    r"(#\d+(?:\s*(?:,|and)\s*#\d+)*)", re.I)


def _line_verdict(line):
    """(verdict, is_blocker) for one `[R<n>]` line.

    A FINDINGS or CLEAN-LENS line (`[R<n>] PASS/BLOCKER/MAJOR/MINOR/SUGGESTION
    ...`) is never a top verdict: its prose carries verdict words that are not
    verdicts, so it is skipped for verdict purposes - a `BLOCKER` finding line
    is still recorded as an (uncleared) blocker, but a `PASS ... negative-
    control` line is neither. Otherwise the rejection lexicon is wider than the
    bare word and case-folded: `REQUEST CHANGES`, `DO NOT MERGE` (PR #123,
    #128) and "not [yet] a positive review" are rejections too, and #128
    MERGED over exactly those while an uppercase-`NEGATIVE`-only parser saw
    nothing. `NEGATIVE` is word-anchored and excludes the compound "negative
    control", which is this repo's own test vocabulary ([R1] re-review: reading
    it as a verdict flipped the clean, POSITIVE-reviewed PR #199 to
    negative-merge).
    """
    lead = _FINDING_LEAD_RE.match(line)
    if lead:
        return None, lead.group(1).upper() == "BLOCKER"
    if _NEG_RE.search(line) or _NOT_A_POSITIVE_RE.search(line):
        return "NEGATIVE", False
    if _POSITIVE_RE.search(line):
        return "POSITIVE", False
    return None, False


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
    for line in body.splitlines():
        if not _RLINE_RE.match(line):
            continue
        verdict, blocker = _line_verdict(line)
        if verdict:
            events.append((when, verdict, False))
        if blocker:
            events.append((when, "BLOCKER", True))


def _closed_issue_numbers(body):
    """Every issue number a `Closes/Fixes #a, #b` names, comma/`and` lists too."""
    nums = set()
    for m in _CLOSES_RE.finditer(body or ""):
        nums.update(int(x) for x in re.findall(r"#(\d+)", m.group(1)))
    return nums


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

    for n in sorted(_closed_issue_numbers(pr.get("body") or "")):
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

    # 11. THE #128 CORPUS CASE: merged over `REQUEST CHANGES / DO NOT MERGE`
    # then a `not yet a positive review`, with no bare-word NEGATIVE anywhere.
    # This is verbatim what merged over the old parser (it saw zero verdicts).
    p11 = {"number": 128, "mergedAt": "2026-08-19T20:06:28Z", "body": "x",
           "comments": [
               {"body": "[R0] REQUEST CHANGES / DO NOT MERGE at head `b1e0b37`.",
                "createdAt": "2026-08-19T18:55:40Z"},
               {"body": "[R0] ROUND 2: the leak is RESOLVED, but this is not "
                        "yet a positive review.",
                "createdAt": "2026-08-19T19:07:32Z"}], "reviews": []}
    f11 = assess_pr(p11, openf(set()))
    if [x.reason for x in f11] != ["negative-merge"]:
        problems.append("case11 request-changes/not-positive: %s"
                        % [x.line() for x in f11])

    # 12. A lowercase verdict is still a verdict.
    p12 = {"number": 129, "mergedAt": "2026-08-20T10:00:00Z", "body": "x",
           "reviews": [{"body": "[R0] negative - the boot order is wrong",
                        "submittedAt": "2026-08-20T09:00:00Z"}], "comments": []}
    if [x.reason for x in assess_pr(p12, openf(set()))] != ["negative-merge"]:
        problems.append("case12 lowercase-negative")

    # 13. A comma-separated `Closes #a, #b`: the TRAILING one, still open, must
    # be reported - the old `\s+#` form dropped everything after the first.
    p13 = {"number": 130, "mergedAt": "2026-08-20T10:00:00Z",
           "body": "Closes #12, #13.\n[R0] POSITIVE",
           "reviews": [], "comments": []}
    f13 = assess_pr(p13, openf({13}))          # #12 closed, #13 open
    if [x.reason for x in f13] != ["open-issue"] or "#13" not in f13[0].detail:
        problems.append("case13 comma-list-closes: %s" % [x.line() for x in f13])

    # 14. `Closes: #14` (colon) and `discloses #99` (must NOT match).
    p14 = {"number": 131, "mergedAt": "2026-08-20T10:00:00Z",
           "body": "Fixes: #14. This discloses #99 as related.\n[R0] POSITIVE",
           "reviews": [], "comments": []}
    f14 = assess_pr(p14, lambda n: True)       # both would be open if matched
    if [x.reason for x in f14] != ["open-issue"] or "#14" not in f14[0].detail:
        problems.append("case14 colon-closes / discloses false-match: %s"
                        % [x.line() for x in f14])

    # 15. THE #199 REGRESSION: a POSITIVE review whose PASS-lens line mentions
    # "negative-control" (this repo's own test vocabulary) must NOT be read as a
    # merge against a NEGATIVE. The first cut of the widened lexicon flipped
    # exactly this clean, POSITIVE-reviewed PR to negative-merge ([R1]).
    p15 = {"number": 199, "mergedAt": "2026-08-21T19:28:18Z", "body": "x",
           "reviews": [], "comments": [
               {"body": "[R0] Cleared-context review. **POSITIVE.** All met.\n"
                        "[R0] PASS Conformance - prints PASS positive + PASS "
                        "negative-control + OK, exit 0.\n"
                        "[R0] MINOR Robustness - the grep is looser than needed.",
                "createdAt": "2026-08-21T19:19:54Z"}]}
    if assess_pr(p15, openf(set())):
        problems.append("case15 negative-control-in-a-PASS-line must not flag: "
                        "%s" % [x.line() for x in assess_pr(p15, openf(set()))])

    # 16. THE #111 MISS: merged over a standing "still not validated for merge
    # / the blockers remain" with only author [A1] follow-ups after ([R2]).
    p16 = {"number": 111, "mergedAt": "2026-08-18T19:15:59Z", "body": "x",
           "reviews": [], "comments": [
               {"body": "[R0] this PR is not validated for merge yet. "
                        "Blocking: 1.",
                "createdAt": "2026-08-18T16:28:07Z"},
               {"body": "[R0] Status recheck: still not validated for merge. "
                        "The blockers remain.",
                "createdAt": "2026-08-18T17:33:45Z"},
               {"body": "[A1] Every blocker is answered at de4b319.",
                "createdAt": "2026-08-18T18:53:59Z"}]}
    if [x.reason for x in assess_pr(p16, openf(set()))] != ["negative-merge"]:
        problems.append("case16 not-validated: %s"
                        % [x.line() for x in assess_pr(p16, openf(set()))])

    # 17. ...and the positive pole clears: #112 iterates "cannot validate" then
    # ends "[R1] VALIDATED" before merge, so it must NOT be flagged.
    p17 = {"number": 112, "mergedAt": "2026-08-18T18:31:48Z", "body": "x",
           "reviews": [{"body": "[R0] cannot validate: a store leaks.",
                        "submittedAt": "2026-08-18T15:49:43Z"},
                       {"body": "[R1] VALIDATED. Every outstanding item "
                                "verified.",
                        "submittedAt": "2026-08-18T18:31:45Z"}], "comments": []}
    if assess_pr(p17, openf(set())):
        problems.append("case17 validated-clears must be clean: %s"
                        % [x.line() for x in assess_pr(p17, openf(set()))])

    # 18. A `### [R1] BLOCKER` markdown-header finding line is still a finding
    # (not a verdict), and a `## [R1] POSITIVE` header is still the verdict.
    p18 = {"number": 900, "mergedAt": "2026-08-21T00:00:03Z", "body": "x",
           "reviews": [{"body": "## [R1] POSITIVE\n### [R1] MINOR Docs - a nit",
                        "submittedAt": "2026-08-21T00:00:00Z"}], "comments": []}
    if assess_pr(p18, openf(set())):
        problems.append("case18 header-formatted POSITIVE must be clean: %s"
                        % [x.line() for x in assess_pr(p18, openf(set()))])

    for p in problems:
        print("  SELFTEST FAILED: %s" % p)
    n = 18
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
