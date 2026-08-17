#!/usr/bin/env python3
"""Did the merge actually take the branch?

    python3 scripts/check_merge_containment.py [--base <ref>] <branch>...
    python3 scripts/check_merge_containment.py --merged-prs [N]
    python3 scripts/check_merge_containment.py --selftest
    python3 scripts/check_merge_containment.py --no-fetch ...   (offline)

WHY THIS EXISTS
---------------
A pull request merged while a review round is still running leaves the work
that round produced behind: the merge takes the commit the branch had at the
time, and everything pushed after it stays on the branch.  Nothing reports
this.  ``gh pr view`` says ``MERGED``, CI is green, the issue closes itself and
the board moves to Done, while commits sit unmerged on a branch nobody is
looking at any more.

It has happened twice here: **#77** (merged mid-review; two of the rounds that
followed returned blocking defects, re-landed as #85) and **#86** (three
commits stranded, tracked as #87, re-landed as #89).  Both were found by a
reviewer checking by hand, which is why this is a command.

THREE WAYS TO GET THE WRONG ANSWER, ALL OF WHICH THIS HAS DONE
--------------------------------------------------------------
1. **Answering from a stale remote-tracking ref.**  The first cut never
   fetched, so a maintainer whose clone predated the review round's push was
   told ``contained`` -- rc 0 -- for a branch with work stranded on it.  That
   is the incident shape verbatim.  It fetches now, and ``--no-fetch`` is
   explicit rather than accidental.
2. **Treating a squash or rebase merge as stranded.**  Those land the *content*
   without making the branch commits ancestors, so an ancestry test alone calls
   them stranded forever.  This repository allows all three merge buttons, so
   that is one press away from a permanently red check -- and a check that
   cries wolf is ignored, which is the failure this file exists to prevent.
   Content equivalence is tested before anything is called stranded.
3. **Reading silence as agreement.**  ``int(out or "0")`` was in the first cut:
   empty output from ``rev-list`` became "0 commits ahead", i.e. contained.
   Anything this tool cannot measure is an UNKNOWN and fails, the same rule
   ``scripts/suite_tally.py`` enforces on the sweep.

THE ONE CASE IT STILL GETS WRONG, AND IN WHICH DIRECTION
--------------------------------------------------------
A branch squash-merged as **two or more** commits, whose paths were then edited
again on the base, reads ``STRANDED`` although nothing is missing: the squash
left no matching patch-id, and the later edit means the paths no longer agree,
so neither equivalence test can prove the work landed.

That is a false **alarm**, not a false pass -- the direction that costs a
reader a minute rather than costing them a regression -- and the verdict names
the differing paths so it can be settled by looking.  It cannot be fixed by
comparing harder: once the base has moved on, "these changes were applied and
then superseded" and "these changes were never applied" are the same tree.
Deciding it needs the merge commit, which only the sweep has.

WHY EXIT CODES AND BARE NUMBERS
-------------------------------
``git rev-list --count`` prints one integer and ``git merge-base
--is-ancestor`` answers only through its exit status.  Neither needs its prose
parsed, so neither can be half-read or mis-scraped, and both are checked here
for having actually produced an answer.  That is the whole reason those two
are used rather than reading ``git log`` output.
"""

import subprocess
import sys

USAGE = __doc__.split("WHY THIS EXISTS")[0].strip()

#! rc 0 contained · rc 1 something is stranded or unknown · rc 2 cannot run
RC_OK, RC_FINDING, RC_CANNOT_RUN = 0, 1, 2


def _git(*args):
    """Run git, returning (rc, stdout).  Never raises on a non-zero rc."""
    p = subprocess.run(("git",) + args, capture_output=True, text=True)
    return p.returncode, p.stdout.rstrip("\n")


def refreshed_origin_ref(ref):
    """Prefer the fetched origin tip when ``ref`` names a branch.

    ``git fetch origin`` refreshes ``refs/remotes/origin/*``; it deliberately
    does not move a checked-out local branch.  Checking that local ref after a
    fetch therefore gives exactly the stale answer this command exists to
    prevent.  Full non-branch refs remain exact, and callers using
    ``--no-fetch`` do not call this helper.
    """
    if ref.startswith("refs/remotes/origin/"):
        return ref
    if ref.startswith("origin/"):
        return "refs/remotes/" + ref
    if ref.startswith("refs/heads/"):
        name = ref[len("refs/heads/"):]
    elif ref.startswith("refs/"):
        return ref
    else:
        name = ref

    remote_ref = "refs/remotes/origin/" + name
    rc, _ = _git("rev-parse", "--verify", "--quiet",
                 remote_ref + "^{commit}")
    return remote_ref if rc == 0 else ref


def contained(branch, base):
    """(is_contained, commits_ahead, note_or_error).

    ``is_contained`` is True when ``base`` already has this branch's work --
    either because every commit is an ancestor, or because the content landed
    by another route (squash, rebase).  None means the question could not be
    answered, which is a finding, never a pass.
    """
    for ref in (branch, base):
        rc, _ = _git("rev-parse", "--verify", "--quiet", ref + "^{commit}")
        if rc != 0:
            return (None, None, f"no such ref: {ref}")
        #! An ambiguous name (a tag AND a branch called the same thing) is
        #! resolved silently by git's own precedence -- the tag wins, and a
        #! stranded branch reads as contained. git says so on stderr, which
        #! _git discards, so ask explicitly instead of trusting the default.
        hits = [k for k in ("refs/heads/", "refs/remotes/", "refs/tags/")
                if _git("rev-parse", "--verify", "--quiet", k + ref)[0] == 0]
        if len(hits) > 1:
            return (None, None,
                    f"{ref!r} is ambiguous ({', '.join(h + ref for h in hits)})"
                    f" -- name the full ref")

    rc, _ = _git("merge-base", "--is-ancestor", branch, base)
    if rc == 0:
        return (True, 0, None)

    rc, out = _git("rev-list", "--count", f"{base}..{branch}")
    if rc != 0:
        return (None, None, f"rev-list failed for {base}..{branch}")
    #! empty is NOT zero -- rev-list always prints a number when it succeeds,
    #! so nothing means the plumbing failed and the answer is unknown
    if not out.isdigit():
        return (None, None,
                f"rev-list printed {out!r} rather than a count; treating as "
                f"UNKNOWN rather than as zero")
    ahead = int(out)

    #! Not an ancestor -- but is the WORK there? A squash or rebase merge lands
    #! every change without keeping the commits, and reporting those as
    #! stranded forever is how this check would come to be ignored.
    #!
    #! Compare only the PATHS THIS BRANCH TOUCHED. A whole-tree `git diff base
    #! branch` was the first cut and it is true only while base's tree is still
    #! byte-identical -- one unrelated commit later and every squash-merged
    #! branch reads stranded again. A review demonstrated exactly that: five
    #! sequential squash merges, only the newest passing.
    mb_rc, mb = _git("merge-base", base, branch)
    if mb_rc == 0 and mb:
        #! Disable rename folding so a move contributes both the deleted and
        #! added path.  Comparing only the destination can certify a base that
        #! copied the file but never removed the source.  NUL delimiters keep
        #! unusual but valid path names exact.
        rc, names = _git("diff", "--name-only", "--no-renames", "-z",
                         mb, branch)
        paths = [n for n in names.split("\0") if n]
        if rc == 0 and paths:
            rc, _ = _git("diff", "--quiet", base, branch, "--", *paths)
            if rc == 0:
                return (True, ahead,
                        f"every path this branch touched is identical in "
                        f"{base} ({ahead} commit(s) not ancestors -- squash "
                        f"or rebase merge)")

    #! Rebase keeps one commit per change, so patch-ids still match.  `cherry`
    #! omits merge commits, however.  Accepting its output for a history that
    #! contains a merge can hide unique conflict-resolution content and turn
    #! real stranded work into rc 0.  Use the patch-id fallback only when every
    #! commit being assessed is linear.
    rc, merge_count = _git("rev-list", "--min-parents=2", "--count",
                           f"{base}..{branch}")
    if rc != 0 or not merge_count.isdigit():
        return (None, None,
                f"could not determine whether {branch} contains merge commits")
    if int(merge_count) == 0:
        rc, cherry = _git("cherry", base, branch)
        if (rc == 0 and cherry
                and all(l.startswith("-") for l in cherry.splitlines())):
            return (True, ahead,
                    f"every commit has an equivalent in {base} ({ahead} not "
                    f"ancestors -- rebase merge)")

    #! NAME THE PATHS. "3 commits not in base" does not tell anyone whether
    #! this is real, and there is one case that reads STRANDED without being
    #! so: a multi-commit squash whose paths were later edited on base. No
    #! patch-id matches (the squash collapsed them) and the paths no longer
    #! agree (the later edit), so neither arm above can prove it landed. That
    #! is a false ALARM rather than a false pass -- the safe direction -- and
    #! naming the paths is what lets a reader settle it in one look instead of
    #! learning to ignore the check.
    differing = []
    if mb_rc == 0 and mb:
        rc2, names = _git("diff", "--name-only", "--no-renames", "-z",
                          base, branch)
        differing = [n for n in names.split("\0") if n][:6]
    return (False, ahead, ("paths differing: " + ", ".join(differing))
            if differing else None)


def merged_pr_heads(limit, base):
    """([(number, branch, head_oid)], error).

    Scoped to PRs that actually targeted ``base``.  Sweeping every merged PR
    asks about branches that were never meant to be in this integration
    branch at all, and answers "diverged" for all of them -- noise that would
    bury the one real finding.

    GitHub's head OID is the head that was merged, not the branch tip after the
    merge.  It is retained only as evidence for diagnostics.  The sweep must
    check the fetched branch ref instead: commits pushed after the merge are
    precisely the stranded work this command exists to find.  A deleted branch
    has no observable post-merge tip and is therefore UNKNOWN, never guessed
    from the merge-time OID.
    """
    import json
    #! gh wants a branch NAME; `base` is a git ref and usually carries the
    #! remote. Passing "origin/main-push" here silently matched nothing, so the
    #! sweep printed an empty list and exited 0 -- a pass by vacancy.
    if base.startswith("refs/remotes/origin/"):
        base_name = base[len("refs/remotes/origin/"):]
    elif base.startswith("origin/"):
        base_name = base[len("origin/"):]
    elif base.startswith("refs/heads/"):
        base_name = base[len("refs/heads/"):]
    else:
        base_name = base
    try:
        p = subprocess.run(
            ["gh", "pr", "list", "--state", "merged", "--base", base_name,
             "--limit", str(limit),
             "--json", "number,headRefName,headRefOid",
             "--search", "sort:updated-desc"],
            capture_output=True, text=True)
    except FileNotFoundError:
        #! distinct from "stranded": a tool we cannot run is not a finding
        return (None, "gh is not installed, so merged PRs cannot be listed")
    if p.returncode != 0:
        return (None, "gh could not list merged PRs (authenticated?): "
                      + (p.stderr or "").strip()[:200])
    try:
        return ([(d["number"], d["headRefName"], d["headRefOid"])
                 for d in json.loads(p.stdout)], None)
    except (ValueError, KeyError) as exc:
        return (None, f"could not parse gh output: {exc}")


# --- self-test ---------------------------------------------------------------
# The cases below call contained() FOR REAL against this repository's own
# history. An earlier cut had a table that re-implemented the predicate and
# never called it, so mutating the shipped code -- swapping the two signals,
# hard-coding the count -- left every case printing ok. The advertised number
# had no coverage at all, which is the "test that cannot fail" this repo's own
# review rounds keep finding.
def selftest():
    bad = 0

    def case(name, got, want, why):
        nonlocal bad
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<26} {why}")
        if not ok:
            bad += 1
            print(f"       got {got!r}, expected {want!r}")

    rc, head = _git("rev-parse", "HEAD")
    rc2, parent = _git("rev-parse", "HEAD~1")
    if rc != 0 or rc2 != 0:
        print("  FAIL selftest needs at least two commits of history")
        return 1

    ok, ahead, note = contained(head, head)
    case("self-containment", (ok, ahead), (True, 0),
         "a commit is contained in itself")

    #! the STRANDED verdict AND the count, against real history: HEAD is one
    #! commit ahead of its parent. The count is what the output advertises and
    #! it had no coverage until this case existed.
    ok, ahead, note = contained(head, parent)
    case("stranded-count", (ok, ahead), (False, 1),
         "HEAD is 1 commit ahead of HEAD~1, and says so")

    ok, ahead, note = contained(parent, head)
    case("contained-backwards", (ok, ahead), (True, 0),
         "...and the parent IS contained in HEAD")

    ok, ahead, note = contained("refs/heads/definitely-not-a-branch", head)
    case("missing-ref", (ok, ahead), (None, None),
         "a ref that cannot be resolved is UNKNOWN, never contained")

    ok, ahead, note = contained(head, "refs/heads/definitely-not-a-base")
    case("missing-base", (ok, ahead), (None, None),
         "...and so is a base that cannot be resolved")

    # --- END TO END, through main() -----------------------------------------
    # Everything above calls contained() directly, and a review showed that
    # leaves the whole verdict-aggregation path uncovered: the exit code could
    # be pinned to 0, STRANDED could be printed and not counted, the advertised
    # number could be printed as a literal 0, and UNKNOWN could be made a pass
    # -- SEVEN mutations, all silent. These run the tool and assert both the
    # exit code and what it printed.
    import io
    import contextlib
    import tempfile

    def run(argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = main([sys.argv[0], *argv])
        return rc, buf.getvalue()

    with tempfile.TemporaryDirectory() as td:
        import os
        cwd = os.getcwd()
        try:
            os.chdir(td)
            _git("init", "-q", "-b", "base")
            _git("config", "user.email", "s@s")
            _git("config", "user.name", "s")
            open("f", "w").write("1")
            _git("add", "-A"); _git("commit", "-qm", "c0")
            _git("checkout", "-qb", "work")
            #! THREE commits, so a count hard-coded to 1 -- the mutation the
            #! previous round named and that still survived -- cannot pass
            for i in range(3):
                open(f"w{i}", "w").write(str(i))
                _git("add", "-A"); _git("commit", "-qm", f"w{i}")

            rc, out = run(["--no-fetch", "--base", "base", "work"])
            case("e2e-stranded-rc", rc, RC_FINDING,
                 "a stranded branch exits non-zero through main()")
            case("e2e-stranded-count", "3 commit(s)" in out, True,
                 "...and prints the real count, not a placeholder")
            case("e2e-stranded-word", "STRANDED" in out, True,
                 "...and says STRANDED")

            rc, out = run(["--no-fetch", "--base", "work", "base"])
            case("e2e-contained-rc", rc, RC_OK,
                 "a contained branch exits 0")

            rc, out = run(["--no-fetch", "--base", "base", "no-such-branch"])
            case("e2e-unknown-rc", rc, RC_FINDING,
                 "an unresolvable ref FAILS -- an unknown is not a pass")
            case("e2e-unknown-word", "UNKNOWN" in out, True,
                 "...and says UNKNOWN")

            rc, out = run(["--no-fetch", "--bogus", "work"])
            case("e2e-unknown-flag", rc, RC_CANNOT_RUN,
                 "an unrecognised flag is refused, never read as a branch")

            # Fetch updates origin/work but not the checked-out local work
            # branch.  The default path must assess the fetched tip, or the
            # exact incident this command guards becomes a quiet rc 0.
            rc, base_oid = _git("rev-parse", "base")
            with tempfile.TemporaryDirectory() as remote:
                _git("init", "--bare", "-q", remote)
                _git("remote", "add", "origin", remote)
                _git("push", "-q", "origin", "base", "work")
                _git("checkout", "-q", "work")
                _git("reset", "--hard", "base")

                rc, local_work = _git("rev-parse", "work")
                rc2, remote_ahead = _git(
                    "rev-list", "--count", "base..refs/remotes/origin/work")
                case("fresh-fixture-local", local_work == base_oid, True,
                     "the local branch is deliberately stale at base")
                case("fresh-fixture-remote", (rc2, remote_ahead), (0, "3"),
                     "the fetched branch has three later commits")

                rc, out = run(["--base", "base", "work"])
                case("fresh-local-ref-rc", rc, RC_FINDING,
                     "fetch checks origin/work, not the stale local branch")
                case("fresh-local-ref-word", "STRANDED" in out, True,
                     "...and reports the work on the fetched tip")

                # A merged PR's head OID is frozen at merge time.  The live
                # branch tip is the only ref that can expose later pushes.
                saved_merged_pr_heads = globals()["merged_pr_heads"]
                globals()["merged_pr_heads"] = lambda _limit, _base: (
                    [(86, "work", base_oid)], None)
                try:
                    rc, out = run(["--no-fetch", "--base", "base",
                                   "--merged-prs", "1"])
                    case("merged-live-tip-rc", rc, RC_FINDING,
                         "the merged sweep ignores the frozen head OID")
                    case("merged-live-tip-word", "STRANDED" in out, True,
                         "...and assesses origin/work instead")
                finally:
                    globals()["merged_pr_heads"] = saved_merged_pr_heads

            # A multi-commit squash remains contained after unrelated work
            # advances the base, because only branch-touched paths matter.
            _git("checkout", "-qb", "squash-feature", "base")
            open("sq0", "w").write("0")
            _git("add", "sq0"); _git("commit", "-qm", "sq0")
            open("sq1", "w").write("1")
            _git("add", "sq1"); _git("commit", "-qm", "sq1")
            _git("checkout", "-qb", "squash-base", "base")
            _git("merge", "-q", "--squash", "squash-feature")
            _git("commit", "-qm", "squash")
            open("unrelated", "w").write("later")
            _git("add", "unrelated"); _git("commit", "-qm", "later")
            rc, out = run(["--no-fetch", "--base", "squash-base",
                           "squash-feature"])
            case("squash-base-advanced", rc, RC_OK,
                 "unrelated base work does not hide a squash merge")
            case("squash-path-equivalence",
                 "every path this branch touched" in out, True,
                 "...through the path-scoped content check")

            # A copied destination is not equivalent to a rename because the
            # source path still exists.  Rename folding must not hide it.
            _git("checkout", "-qb", "rename-feature", "base")
            _git("mv", "f", "renamed")
            _git("commit", "-qm", "rename")
            _git("checkout", "-qb", "rename-base", "base")
            open("renamed", "w").write("1")
            _git("add", "renamed"); _git("commit", "-qm", "copy")
            rc, out = run(["--no-fetch", "--base", "rename-base",
                           "rename-feature"])
            case("rename-source-remains", rc, RC_FINDING,
                 "a copied destination cannot hide a missing deletion")

            # Patch-id equivalence is valid for a linear rebased history even
            # when the base later edits the same path.
            _git("checkout", "-qb", "linear-feature", "base")
            open("linear", "w").write("landed\n")
            _git("add", "linear"); _git("commit", "-qm", "linear")
            rc, linear_commit = _git("rev-parse", "HEAD")
            _git("checkout", "-qb", "linear-base", "base")
            open("advance", "w").write("first")
            _git("add", "advance"); _git("commit", "-qm", "advance")
            _git("cherry-pick", linear_commit)
            open("linear", "a").write("superseded\n")
            _git("add", "linear"); _git("commit", "-qm", "supersede")
            rc, out = run(["--no-fetch", "--base", "linear-base",
                           "linear-feature"])
            case("linear-patch-fallback", rc, RC_OK,
                 "patch equivalence handles a linear rebase")
            case("linear-patch-word", "every commit has an equivalent" in out,
                 True, "...through the patch-id fallback")

            # git cherry intentionally omits merge commits.  An equivalent
            # normal commit must not hide unique merge-resolution content.
            _git("checkout", "-qb", "merge-side", "base")
            open("side", "w").write("side")
            _git("add", "side"); _git("commit", "-qm", "side")
            _git("checkout", "-qb", "merge-feature", "base")
            open("normal", "w").write("normal")
            _git("add", "normal"); _git("commit", "-qm", "normal")
            _git("checkout", "-qb", "merge-replayed", "merge-side")
            open("normal", "w").write("normal")
            _git("add", "normal"); _git("commit", "-qm", "replayed")
            _git("checkout", "-q", "merge-feature")
            _git("merge", "-q", "--no-ff", "--no-commit", "merge-side")
            open("resolution", "w").write("unique")
            _git("add", "resolution"); _git("commit", "-qm", "merge")
            rc, merge_count = _git(
                "rev-list", "--min-parents=2", "--count",
                "merge-replayed..merge-feature")
            rc2, cherry = _git("cherry", "merge-replayed", "merge-feature")
            case("merge-fixture-count", (rc, merge_count), (0, "1"),
                 "the fixture contains one unique merge commit")
            case("merge-fixture-cherry",
                 rc2 == 0 and bool(cherry)
                 and all(line.startswith("-") for line in cherry.splitlines()),
                 True, "git cherry hides that merge behind equivalent commits")
            rc, out = run(["--no-fetch", "--base", "merge-replayed",
                           "merge-feature"])
            case("merge-resolution-rc", rc, RC_FINDING,
                 "a merge commit cannot disappear from the patch fallback")
            case("merge-resolution-path", "resolution" in out, True,
                 "...and its unique path is reported as stranded")
        finally:
            os.chdir(cwd)

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


KNOWN_FLAGS = {"--selftest", "--base", "--merged-prs", "--no-fetch"}


def main(argv):
    args = argv[1:]
    if "--selftest" in args:
        return selftest()

    #! Reject unknown options rather than silently treating them as branches.
    #! `--bse 43a4c417 origin/foo` used to check TWO branches called
    #! "43a4c417" and "origin/foo" against the default base -- both contained,
    #! rc 0 -- where the same command spelled correctly reported 4 stranded.
    for a in args:
        if a.startswith("-") and a not in KNOWN_FLAGS:
            sys.stderr.write(f"unknown option: {a}\n{USAGE}\n")
            return RC_CANNOT_RUN

    base = "origin/main-push"
    if "--base" in args:
        i = args.index("--base")
        if i + 1 >= len(args) or args[i + 1].startswith("-"):
            #! `--base --no-fetch origin/x` used to set base to "--no-fetch"
            #! AND consume the flag, so the fetch ran despite being asked not
            #! to, and the run failed for the wrong reason
            sys.stderr.write(f"--base needs a ref\n{USAGE}\n")
            return RC_CANNOT_RUN
        base = args[i + 1]
        del args[i:i + 2]

    do_fetch = "--no-fetch" not in args
    args = [a for a in args if a != "--no-fetch"]
    if do_fetch:
        #! Answering from a stale remote-tracking ref is how this tool once
        #! reported `contained` for a branch that had work stranded on it.
        rc, _ = _git("fetch", "--prune", "--quiet", "origin")
        if rc != 0:
            sys.stderr.write(
                "could not fetch origin. Re-run with --no-fetch only if you "
                "are certain the refs are current: a stale ref reports "
                "'contained' for stranded work.\n")
            return RC_CANNOT_RUN
        base = refreshed_origin_ref(base)

    if "--merged-prs" in args:
        i = args.index("--merged-prs")
        limit = 20
        if i + 1 < len(args) and args[i + 1].isdigit():
            limit = int(args[i + 1])
            del args[i + 1]
        del args[i]
        prs, err = merged_pr_heads(limit, base)
        if err:
            sys.stderr.write(err + "\n")
            return RC_CANNOT_RUN
        if not prs:
            sys.stderr.write(
                f"no merged PRs found targeting {base}. That is not a pass -- "
                f"check the base name.\n")
            return RC_CANNOT_RUN
        #! headRefOid is frozen at merge time and therefore cannot reveal work
        #! pushed afterwards.  Always assess the fetched live branch tip.  A
        #! deleted branch becomes UNKNOWN through contained(), which is safer
        #! than certifying the old merge-time OID.
        targets = [(f"#{n} {b}", f"refs/remotes/origin/{b}")
                   for n, b, _oid in prs]
    else:
        branches = [a for a in args if not a.startswith("-")]
        if not branches:
            rc, cur = _git("rev-parse", "--abbrev-ref", "HEAD")
            if rc != 0 or not cur or cur == "HEAD":
                sys.stderr.write(USAGE + "\n")
                return RC_CANNOT_RUN
            branches = [cur]
        targets = [(b, refreshed_origin_ref(b) if do_fetch else b)
                   for b in branches]

    stranded = 0
    unknown = 0
    for label, ref in targets:
        ok, ahead, note = contained(ref, base)
        if ok is None:
            print(f"  UNKNOWN    {label}: {note}")
            unknown += 1
        elif ok:
            print(f"  contained  {label}" + (f"  [{note}]" if note else ""))
        else:
            print(f"  STRANDED   {label}: {ahead} commit(s) not in {base}"
                  + (f"  [{note}]" if note else ""))
            stranded += 1

    if stranded:
        print()
        print(f"{stranded} branch(es) have work that {base} does not.")
        print("  A merge that landed before the branch stopped moving leaves")
        print("  the rest behind, and nothing else reports it. Open a")
        print("  follow-up PR for the remainder -- see CONTRIBUTING.md 2.1")
        print("  step 7.")
    if unknown:
        print()
        print(f"{unknown} ref(s) could not be resolved, so the question was")
        print("  not answered. An unknown is not a pass.")
    return RC_FINDING if (stranded or unknown) else RC_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
