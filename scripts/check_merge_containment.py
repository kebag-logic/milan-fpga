#!/usr/bin/env python3
"""Did the merge actually take the branch?

    python3 scripts/check_merge_containment.py [--base main-push] [<branch>...]
    python3 scripts/check_merge_containment.py --merged-prs [N]
    python3 scripts/check_merge_containment.py --selftest

WHY THIS EXISTS
---------------
A pull request merged while a review round is still running leaves the work
that round produced behind: the merge takes the commit the branch had at the
time, and everything pushed after it stays on the branch.  Nothing reports
this.  ``gh pr view`` says ``MERGED``, CI is green, the issue closes itself,
and the board moves to Done -- while commits sit unmerged on a branch nobody
is looking at any more.

It has happened twice on this repository:

* **#77**, merged 2026-08-16 18:10 during review round 3 of 6.  Rounds 4, 5
  and 6 each returned NEGATIVE afterwards; their fixes had to be re-landed as
  #85.
* **#86**, merged 2026-08-17 07:54 mid-round.  Three commits stranded, tracked
  as #87 and re-landed as #89.

Both were found by a reviewer checking by hand.  This makes the check a
command, because a check that depends on somebody remembering is not a check.

THE TRAP THIS AVOIDS
--------------------
The obvious way to write this is ``git log <branch>..<base>``.  Do not.  In
this environment that returns **empty** when it follows another git command in
the same shell invocation -- the proxy hook swallows the output -- so it
reports "nothing diverged" for a branch that has.  That is exactly how #89's
own description came to claim a fast-forward that was not one.

``git rev-list --count`` and ``git merge-base --is-ancestor`` are used instead:
both answer through the exit code or a bare number, so a swallowed stream
cannot be mistaken for agreement.  Same rule as ``scripts/suite_tally.py``
enforces on the sweep -- silence is not a measurement.
"""

import subprocess
import sys


def _git(*args):
    """Run git, returning (rc, stdout).  Never raises on a non-zero rc."""
    p = subprocess.run(("git",) + args, capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def contained(branch, base):
    """(is_contained, commits_ahead, error).

    ``is_contained`` is True when every commit on ``branch`` is reachable from
    ``base`` -- i.e. the merge took the whole branch.
    """
    rc, _ = _git("rev-parse", "--verify", "--quiet", branch + "^{commit}")
    if rc != 0:
        return (None, None, f"no such ref: {branch}")
    rc, _ = _git("rev-parse", "--verify", "--quiet", base + "^{commit}")
    if rc != 0:
        return (None, None, f"no such ref: {base}")

    #! the count is the actionable number: it says HOW MUCH was left behind
    rc, out = _git("rev-list", "--count", f"{base}..{branch}")
    if rc != 0:
        return (None, None, f"rev-list failed for {base}..{branch}")
    ahead = int(out or "0")

    #! and the ancestry test is the verdict, taken from an exit code so that an
    #! empty stream cannot be read as agreement
    rc, _ = _git("merge-base", "--is-ancestor", branch, base)
    return (rc == 0, ahead, None)


def merged_pr_branches(limit):
    """[(number, branch)] for the most recently merged PRs, via gh."""
    rc, out = _git("--version")          # cheap check that we can run tools
    if rc != 0:
        return None
    p = subprocess.run(
        ["gh", "pr", "list", "--state", "merged", "--limit", str(limit),
         "--json", "number,headRefName"],
        capture_output=True, text=True)
    if p.returncode != 0:
        return None
    import json
    try:
        return [(d["number"], d["headRefName"]) for d in json.loads(p.stdout)]
    except (ValueError, KeyError):
        return None


SELFTEST = [
    # (name, ahead, is_ancestor, expect_ok)
    ("contained",        0, True,  True),
    ("stranded-one",     1, False, False),
    ("stranded-many",    7, False, False),
    #! the case that makes the two signals worth having SEPARATELY: a branch
    #! can be an ancestor and still report commits ahead if a ref moved under
    #! us mid-check. Disagreement is itself a finding, never a pass.
    ("disagreement",     2, True,  False),
]


def selftest():
    bad = 0
    for name, ahead, anc, want in SELFTEST:
        got = bool(anc) and ahead == 0
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<16} "
              f"ahead={ahead} ancestor={anc} -> contained={got}")
        if not ok:
            bad += 1
            print(f"       expected contained={want}")

    #! and one real call, so the git plumbing is exercised rather than assumed:
    #! a ref is trivially contained in itself, and a missing ref is an error
    #! rather than a quiet pass
    ok, ahead, err = contained("HEAD", "HEAD")
    if ok is True and ahead == 0 and err is None:
        print("  ok   self-containment  HEAD is contained in HEAD")
    else:
        print(f"  FAIL self-containment  got ok={ok} ahead={ahead} err={err}")
        bad += 1

    ok, ahead, err = contained("refs/heads/definitely-not-a-branch", "HEAD")
    if ok is None and err:
        print("  ok   missing-ref       a ref that does not exist is an ERROR, "
              "not 'contained'")
    else:
        print(f"  FAIL missing-ref       got ok={ok} err={err}")
        bad += 1

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


def main(argv):
    args = argv[1:]
    if "--selftest" in args:
        return selftest()

    base = "origin/main-push"
    if "--base" in args:
        i = args.index("--base")
        base = args[i + 1]
        del args[i:i + 2]

    if "--merged-prs" in args:
        i = args.index("--merged-prs")
        limit = 20
        if i + 1 < len(args) and args[i + 1].isdigit():
            limit = int(args[i + 1])
            del args[i + 1]
        del args[i]
        prs = merged_pr_branches(limit)
        if prs is None:
            sys.stderr.write("could not list merged PRs (is `gh` available "
                             "and authenticated?)\n")
            return 2
        targets = [(f"#{n} {b}", "origin/" + b) for n, b in prs]
    else:
        branches = [a for a in args if not a.startswith("-")]
        if not branches:
            rc, cur = _git("rev-parse", "--abbrev-ref", "HEAD")
            if rc != 0 or not cur or cur == "HEAD":
                sys.stderr.write("usage: check_merge_containment.py "
                                 "[--base <ref>] <branch>...\n")
                return 2
            branches = [cur]
        targets = [(b, b) for b in branches]

    bad = 0
    unknown = 0
    for label, ref in targets:
        ok, ahead, err = contained(ref, base)
        if err:
            print(f"  UNKNOWN  {label}: {err}")
            unknown += 1
            continue
        if ok and ahead == 0:
            print(f"  contained  {label}")
        else:
            print(f"  STRANDED   {label}: {ahead} commit(s) not in {base}")
            bad += 1

    if bad:
        print()
        print(f"{bad} branch(es) have work that {base} does not.")
        print("  A merge that landed before the branch stopped moving leaves")
        print("  the rest behind, and nothing else reports it. Open a")
        print("  follow-up PR for the remainder -- see CONTRIBUTING.md 2.1")
        print("  step 7.")
    #! an unresolvable ref is an UNKNOWN and fails: a check that cannot run
    #! must not report success
    if unknown:
        print()
        print(f"{unknown} ref(s) could not be resolved. An unknown is not a")
        print("  pass -- fetch, or name the ref that exists.")
    return 1 if (bad or unknown) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
