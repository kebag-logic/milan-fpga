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
    return p.returncode, p.stdout.strip()


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

    #! Not an ancestor, but is the WORK there? A squash or rebase merge lands
    #! every change without keeping the commits, and calling that stranded is
    #! how this check would come to be ignored.
    rc, diff = _git("diff", "--quiet", base, branch)
    if rc == 0:
        return (True, ahead,
                f"content is identical to {base} ({ahead} commit(s) not "
                f"ancestors -- squash or rebase merge)")
    rc, cherry = _git("cherry", base, branch)
    if rc == 0 and cherry and all(l.startswith("-") for l in cherry.splitlines()):
        return (True, ahead,
                f"every commit has an equivalent in {base} ({ahead} not "
                f"ancestors -- rebase merge)")

    return (False, ahead, None)


def merged_pr_heads(limit, base):
    """([(number, branch, head_oid)], error).

    Scoped to PRs that actually targeted ``base``.  Sweeping every merged PR
    asks about branches that were never meant to be in this integration
    branch at all, and answers "diverged" for all of them -- noise that would
    bury the one real finding.

    THE HEAD OID, NOT THE BRANCH REF: deleting a branch after merge is normal
    housekeeping and leaves no ``origin/<name>`` to resolve.  The OID is not
    fetchable either once the ref is gone, so containment for those is asked
    of GitHub directly -- see ``contained_via_api``.
    """
    import json
    #! gh wants a branch NAME; `base` is a git ref and usually carries the
    #! remote. Passing "origin/main-push" here silently matched nothing, so the
    #! sweep printed an empty list and exited 0 -- a pass by vacancy.
    base_name = base.split("/", 1)[1] if base.startswith("origin/") else base
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


def contained_via_api(head_oid, base):
    """(is_contained, ahead, note_or_error) asked of GitHub, not the clone.

    For a branch deleted after its merge there is no local ref AND no local
    object: `git fetch` will not retrieve an OID that nothing points at.  The
    first cut reported every such PR as UNKNOWN, which on a repository that
    tidies up its branches meant the prescribed command was red for 12 of the
    last 20 PRs with nothing actually wrong -- a check that cries wolf, which
    is the failure this file exists to prevent.

    GitHub's compare endpoint still knows: `ahead_by == 0` means the base has
    everything, and an empty file list means the content landed even though
    the commits did not (squash or rebase).
    """
    import json
    ref = base.split("/", 1)[1] if base.startswith("origin/") else base
    try:
        p = subprocess.run(
            ["gh", "api", f"repos/{{owner}}/{{repo}}/compare/{ref}...{head_oid}",
             "--jq", "{ahead: .ahead_by, files: (.files | length)}"],
            capture_output=True, text=True)
    except FileNotFoundError:
        return (None, None, "gh is not installed")
    if p.returncode != 0:
        return (None, None,
                "GitHub could not compare it: "
                + (p.stderr or "").strip().splitlines()[-1][:120])
    try:
        d = json.loads(p.stdout)
        ahead, files = int(d["ahead"]), int(d["files"])
    except (ValueError, KeyError, IndexError):
        return (None, None, "could not read the compare result")
    if ahead == 0:
        return (True, 0, None)
    if files == 0:
        return (True, ahead,
                f"content landed ({ahead} commit(s) not ancestors -- squash "
                f"or rebase merge)")
    return (False, ahead, None)


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
        if i + 1 >= len(args):
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
        #! the OID is the ref we ask about; the branch name is for the reader,
        #! and may well no longer exist
        if not prs:
            sys.stderr.write(
                f"no merged PRs found targeting {base}. That is not a pass -- "
                f"check the base name.\n")
            return RC_CANNOT_RUN
        targets = [(f"#{n} {b}", oid) for n, b, oid in prs]
        api_fallback = True
    else:
        branches = [a for a in args if not a.startswith("-")]
        if not branches:
            rc, cur = _git("rev-parse", "--abbrev-ref", "HEAD")
            if rc != 0 or not cur or cur == "HEAD":
                sys.stderr.write(USAGE + "\n")
                return RC_CANNOT_RUN
            branches = [cur]
        targets = [(b, b) for b in branches]
        api_fallback = False

    stranded = 0
    unknown = 0
    for label, ref in targets:
        ok, ahead, note = contained(ref, base)
        #! a deleted branch leaves no local object to ask about, so ask GitHub
        if ok is None and api_fallback and note and note.startswith("no such ref"):
            ok, ahead, note = contained_via_api(ref, base)
        if ok is None:
            print(f"  UNKNOWN    {label}: {note}")
            unknown += 1
        elif ok:
            print(f"  contained  {label}" + (f"  [{note}]" if note else ""))
        else:
            print(f"  STRANDED   {label}: {ahead} commit(s) not in {base}")
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
