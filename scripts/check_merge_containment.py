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

import os
import subprocess
import sys

USAGE = __doc__.split("WHY THIS EXISTS")[0].strip()

#! rc 0 contained · rc 1 something is stranded or unknown · rc 2 cannot run
RC_OK, RC_FINDING, RC_CANNOT_RUN = 0, 1, 2
RAW_DIFF_FLAGS = ("--no-ext-diff", "--no-textconv",
                  "--ignore-submodules=none")


def _git(*args):
    """Run git, returning (rc, stdout).  Never raises on a non-zero rc."""
    #! Replacement objects rewrite the commit graph for every plumbing command.
    #! A local refs/replace entry can otherwise make a stranded branch appear
    #! to be an ancestor of the base.  Containment must measure stored commits,
    #! not a caller-specific alternate history.
    p = subprocess.run(("git", "--no-replace-objects") + args,
                       capture_output=True, text=True)
    return p.returncode, p.stdout.rstrip("\n")


def active_graft_error():
    """Explain an active legacy graft file, or return None."""
    rc, path = _git("rev-parse", "--git-path", "info/grafts")
    if rc != 0 or not path:
        return "could not locate Git's legacy graft file"
    try:
        with open(path, "rb") as grafts:
            active = bool(grafts.read().strip())
    except FileNotFoundError:
        return None
    except OSError as exc:
        return f"could not inspect Git's legacy graft file: {exc}"
    if active:
        return (f"legacy Git grafts are active in {path}; remove the grafts "
                f"before measuring stored commit ancestry")
    return None


def exact_ref_syntax(ref):
    """True for a ref name or full object ID, never a revision expression."""
    if len(ref) in (40, 64) and all(c in "0123456789abcdefABCDEF" for c in ref):
        rc, oid = _git("rev-parse", "--verify", "--quiet", ref + "^{commit}")
        return rc == 0 and oid.lower() == ref.lower()
    if ref.startswith("refs/"):
        return _git("check-ref-format", ref)[0] == 0
    if ref in ("HEAD", "@"):
        return False
    return _git("check-ref-format", "--branch", ref)[0] == 0


def _verbatim_patch_id(commit):
    """Return a whitespace-preserving patch ID for one commit."""
    rc, patch = _git("show", *RAW_DIFF_FLAGS, "--format=medium", "--binary",
                     "--full-index", "--no-renames", commit)
    if rc != 0:
        return (None, f"git show could not read {commit}")
    p = subprocess.run(("git", "--no-replace-objects", "patch-id",
                        "--verbatim"), input=patch, capture_output=True,
                       text=True)
    fields = p.stdout.strip().split()
    if p.returncode != 0 or len(fields) != 2:
        return (None, f"git patch-id could not measure {commit}")
    return (fields[0], None)


def _commit_paths(commit):
    """Return the literal paths one commit changed, with renames unfolded."""
    rc, names = _git("diff-tree", *RAW_DIFF_FLAGS, "--root",
                     "--no-commit-id", "--name-only", "--no-renames", "-z",
                     "-r", commit)
    if rc != 0:
        return (None, f"diff-tree could not enumerate {commit}")
    return ([name for name in names.split("\0") if name], None)


def _same_patch_postimage(branch_commit, base_commit):
    """Require candidate replays to produce the same touched-path trees."""
    branch_paths, err = _commit_paths(branch_commit)
    if err:
        return (None, err)
    base_paths, err = _commit_paths(base_commit)
    if err:
        return (None, err)
    paths = list(dict.fromkeys(branch_paths + base_paths))
    if not paths:
        return (True, None)
    rc, _ = _git("--literal-pathspecs", "diff", *RAW_DIFF_FLAGS, "--quiet",
                 branch_commit, base_commit, "--", *paths)
    if rc == 0:
        return (True, None)
    if rc == 1:
        return (False, None)
    return (None, f"git diff could not compare {branch_commit} with "
                  f"{base_commit}")


def _linear_patches_contained(branch, base):
    """Prove linear replay equivalence without ignoring whitespace."""
    rc, branch_out = _git("rev-list", "--no-merges", f"{base}..{branch}")
    if rc != 0:
        return (None, f"rev-list could not enumerate {branch}")
    rc, base_out = _git("rev-list", "--no-merges", f"{branch}..{base}")
    if rc != 0:
        return (None, f"rev-list could not enumerate {base}")

    branch_commits = branch_out.splitlines()
    base_commits = base_out.splitlines()
    if not branch_commits or not base_commits:
        return (False, None)

    base_by_id = {}
    for commit in base_commits:
        patch_id, err = _verbatim_patch_id(commit)
        if err:
            return (None, err)
        base_by_id.setdefault(patch_id, []).append(commit)

    for commit in branch_commits:
        patch_id, err = _verbatim_patch_id(commit)
        if err:
            return (None, err)
        candidates = base_by_id.get(patch_id, [])
        match = None
        for candidate in candidates:
            same, err = _same_patch_postimage(commit, candidate)
            if err:
                return (None, err)
            if same:
                match = candidate
                break
        if match is None:
            return (False, None)
        candidates.remove(match)
    return (True, None)


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


def fetched_branch_refs(ref):
    """Return every distinct local/remote tip named by a branch argument.

    A local branch can be either behind its fetched remote tip or ahead with
    unpushed work.  Replacing one with the other hides one of those two failure
    modes.  When both exist and differ, containment must be proven for both.
    The source labels are used only to make the two answers distinguishable.
    """
    if ref.startswith("refs/remotes/origin/"):
        name = ref[len("refs/remotes/origin/"):]
    elif ref.startswith("origin/"):
        name = ref[len("origin/"):]
    elif ref.startswith("refs/heads/"):
        name = ref[len("refs/heads/"):]
    elif ref.startswith("refs/"):
        return [(ref, None)]
    else:
        name = ref

    local_ref = "refs/heads/" + name
    remote_ref = "refs/remotes/origin/" + name
    local_rc, local_oid = _git("rev-parse", "--verify", "--quiet",
                               local_ref + "^{commit}")
    remote_rc, remote_oid = _git("rev-parse", "--verify", "--quiet",
                                 remote_ref + "^{commit}")
    if local_rc == 0 and remote_rc == 0 and local_oid != remote_oid:
        return [(local_ref, "local"), (remote_ref, "origin")]
    if remote_rc == 0:
        return [(remote_ref, "origin")]
    if local_rc == 0:
        #! A successful fetch with no origin ref cannot distinguish a genuinely
        #! local-only branch from a branch deleted after later work was pushed.
        #! Trusting the local tip can therefore certify the stale merge-time
        #! commit while the deleted remote once held stranded work.  Report the
        #! observable local tip and an UNKNOWN origin tip.  A caller who
        #! deliberately wants only the local ref can use --no-fetch with its
        #! full refs/heads/... name.
        return [(local_ref, "local"), (remote_ref, "origin")]
    return [(ref, None)]


def non_origin_remote_ref(ref):
    """Name an unrefreshable remote-tracking ref, or return None."""
    if ref.startswith("refs/remotes/origin/") or ref.startswith("origin/"):
        return None
    if ref.startswith("refs/remotes/"):
        return ref
    rc, full = _git("rev-parse", "--symbolic-full-name", "--verify", ref)
    if (rc == 0 and full.startswith("refs/remotes/")
            and not full.startswith("refs/remotes/origin/")):
        return full
    return None


def contained(branch, base):
    """(is_contained, commits_ahead, note_or_error).

    ``is_contained`` is True when ``base`` already has this branch's work --
    either because every commit is an ancestor, or because the content landed
    by another route (squash, rebase).  None means the question could not be
    answered, which is a finding, never a pass.
    """
    graft_error = active_graft_error()
    if graft_error:
        return (None, None, graft_error)

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
    if rc != 1:
        return (None, None,
                f"merge-base could not compare {branch} with {base}")

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
    if mb_rc not in (0, 1):
        return (None, None,
                f"merge-base could not find a common history for "
                f"{base} and {branch}")
    if mb_rc == 0 and mb:
        #! Disable rename folding so a move contributes both the deleted and
        #! added path.  Comparing only the destination can certify a base that
        #! copied the file but never removed the source.  NUL delimiters keep
        #! unusual but valid path names exact.
        rc, names = _git("diff", *RAW_DIFF_FLAGS, "--name-only",
                         "--no-renames", "-z", mb, branch)
        if rc != 0:
            return (None, None,
                    f"git diff could not enumerate paths changed by {branch}")
        paths = [n for n in names.split("\0") if n]
        if not paths:
            rc, _ = _git("diff", *RAW_DIFF_FLAGS, "--quiet", mb, branch)
            if rc == 0:
                return (True, ahead,
                        f"the branch has no net tree change ({ahead} "
                        f"commit(s) not ancestors)")
            if rc != 1:
                return (None, None,
                        f"git diff could not verify the empty path set for "
                        f"{branch}")
            return (None, None,
                    f"git diff reported content for {branch} after path "
                    f"enumeration reported none")
        if paths:
            #! Names came from git, not from a pathspec language.  A real file
            #! beginning with `:(exclude)` must not turn itself into an exclude
            #! rule and make a missing change compare equal.
            rc, _ = _git("--literal-pathspecs", "diff", *RAW_DIFF_FLAGS,
                         "--quiet", base, branch, "--", *paths)
            if rc == 0:
                return (True, ahead,
                        f"every path this branch touched is identical in "
                        f"{base} ({ahead} commit(s) not ancestors -- squash "
                        f"or rebase merge)")
            if rc != 1:
                return (None, None,
                        f"git diff could not compare {branch} with {base}")

    #! Rebase keeps one commit per change, so patch IDs still match.  Plain
    #! `git cherry` is not proof: its patch IDs ignore whitespace, which can
    #! equate different HDL or software content.  Measure every unique linear
    #! commit with `git patch-id --verbatim` instead, then require the candidate
    #! commits' touched-path postimages to match exactly.  Even verbatim patch
    #! IDs omit hunk line numbers, so the postimage check prevents the same edit
    #! to a different repeated location from becoming a false pass.  Merge
    #! commits remain excluded because patch IDs omit resolution content.
    rc, merge_count = _git("rev-list", "--min-parents=2", "--count",
                           f"{base}..{branch}")
    if rc != 0 or not merge_count.isdigit():
        return (None, None,
                f"could not determine whether {branch} contains merge commits")
    if int(merge_count) == 0:
        equivalent, err = _linear_patches_contained(branch, base)
        if equivalent is None:
            return (None, None, err)
        if equivalent:
            return (True, ahead,
                    f"every commit has a whitespace-exact equivalent in "
                    f"{base} ({ahead} not ancestors -- rebase merge)")

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
        rc2, names = _git("diff", *RAW_DIFF_FLAGS, "--name-only",
                          "--no-renames", "-z", base, branch)
        if rc2 != 0:
            return (None, None,
                    f"git diff could not enumerate paths differing between "
                    f"{branch} and {base}")
        differing = [n for n in names.split("\0") if n][:6]
    return (False, ahead, ("paths differing: " + ", ".join(differing))
            if differing else None)


def merged_pr_heads(limit, base):
    """([(number, branch, head_oid, cross_repository)], error).

    Scoped to PRs that actually targeted ``base``.  Sweeping every merged PR
    asks about branches that were never meant to be in this integration
    branch at all, and answers "diverged" for all of them -- noise that would
    bury the one real finding.

    GitHub's head OID is the head that was merged, not the branch tip after the
    merge.  The sweep checks a same-repository live branch only when its
    first-parent history still contains that OID.  That continuity proof keeps
    a fork or a deleted and recreated same-name branch from standing in for the
    merged branch.  A missing or discontinuous tip is UNKNOWN.
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
             "--json", "number,headRefName,headRefOid,isCrossRepository",
             "--search", "sort:updated-desc"],
            capture_output=True, text=True)
    except FileNotFoundError:
        #! distinct from "stranded": a tool we cannot run is not a finding
        return (None, "gh is not installed, so merged PRs cannot be listed")
    if p.returncode != 0:
        return (None, "gh could not list merged PRs (authenticated?): "
                      + (p.stderr or "").strip()[:200])
    try:
        return ([(d["number"], d["headRefName"], d["headRefOid"],
                  d["isCrossRepository"])
                 for d in json.loads(p.stdout)], None)
    except (ValueError, KeyError) as exc:
        return (None, f"could not parse gh output: {exc}")


def continuous_merged_pr_tip(head_oid, live_ref):
    """Return an error unless ``live_ref`` continues the merged PR branch."""
    if not (len(head_oid) in (40, 64)
            and all(c in "0123456789abcdefABCDEF" for c in head_oid)):
        return "GitHub returned an invalid merged head object ID"
    rc, _ = _git("rev-parse", "--verify", "--quiet", live_ref + "^{commit}")
    if rc != 0:
        return f"the live branch ref is missing: {live_ref}"
    rc, history = _git("rev-list", "--first-parent", live_ref)
    if rc != 0:
        return f"could not inspect first-parent continuity for {live_ref}"
    if head_oid.lower() not in {oid.lower() for oid in history.splitlines()}:
        return (f"{live_ref} is not a first-parent continuation of merged "
                f"head {head_oid}; the branch may have been replaced")
    return None


# --- self-test ---------------------------------------------------------------
# The cases below call contained() FOR REAL against controlled Git histories.
# An earlier cut had a table that re-implemented the predicate and
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
    if rc != 0:
        print("  FAIL selftest needs a repository with one commit")
        return 1

    ok, ahead, note = contained(head, head)
    case("self-containment", (ok, ahead), (True, 0),
         "a commit is contained in itself")

    saved_git = globals()["_git"]
    globals()["_git"] = lambda *args: (
        (128, "") if args[:2] == ("merge-base", "--is-ancestor")
        else saved_git(*args))
    try:
        ok, ahead, note = contained(head, head)
        case("ancestor-plumbing-error", (ok, ahead), (None, None),
             "a failed ancestry command is UNKNOWN, never not-ancestor")
    finally:
        globals()["_git"] = saved_git

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

            # These assertions used to rely on HEAD and HEAD~1 in the caller's
            # repository.  At a merge result, second-parent commits make that
            # range larger than one and the self-test falsely failed.  Keep the
            # one-commit relationship inside the controlled linear fixture.
            rc, tip = _git("rev-parse", "work")
            rc2, parent = _git("rev-parse", "work~1")
            ok, ahead, note = contained(tip, parent)
            case("stranded-count", (rc, rc2, ok, ahead),
                 (0, 0, False, 1),
                 "a linear child is one commit ahead of its parent")

            ok, ahead, note = contained(parent, tip)
            case("contained-backwards", (ok, ahead), (True, 0),
                 "...and the parent is contained in the child")

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

            rc, out = run(["--no-fetch", "--base", "base", "work~1"])
            case("e2e-revision-branch", rc, RC_CANNOT_RUN,
                 "a revision expression cannot hide the branch tip")
            rc, out = run(["--no-fetch", "--base", "work~1", "work"])
            case("e2e-revision-base", rc, RC_CANNOT_RUN,
                 "a revision expression cannot replace the exact base")

            rc, out = run(["--no-fetch", "--base", "base", "--base",
                           "work", "work"])
            case("e2e-duplicate-base", rc, RC_CANNOT_RUN,
                 "a repeated base option is refused")

            rc, out = run(["--no-fetch", "--no-fetch", "--base", "base",
                           "work"])
            case("e2e-duplicate-no-fetch", rc, RC_CANNOT_RUN,
                 "a repeated no-fetch option is refused")

            rc, out = run(["--no-fetch", "--merged-prs", "1", "work"])
            case("e2e-sweep-operand", rc, RC_CANNOT_RUN,
                 "a merged sweep cannot silently ignore a branch operand")

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
                    [(86, "work", base_oid, False)], None)
                try:
                    rc, out = run(["--no-fetch", "--base", "base",
                                   "--merged-prs", "1"])
                    case("merged-live-tip-rc", rc, RC_FINDING,
                         "the merged sweep ignores the frozen head OID")
                    case("merged-live-tip-word", "STRANDED" in out, True,
                         "...and assesses origin/work instead")
                finally:
                    globals()["merged_pr_heads"] = saved_merged_pr_heads

                globals()["merged_pr_heads"] = lambda _limit, _base: (
                    [(90, "work", base_oid, True)], None)
                try:
                    rc, out = run(["--no-fetch", "--base", "base",
                                   "--merged-prs", "1"])
                    case("merged-fork-rc", rc, RC_FINDING,
                         "a fork head cannot borrow origin's same-name ref")
                    case("merged-fork-word", "UNKNOWN" in out, True,
                         "...and the unrefreshable live tip is UNKNOWN")
                finally:
                    globals()["merged_pr_heads"] = saved_merged_pr_heads

                rc, work_tip = _git("rev-parse", "refs/remotes/origin/work")
                _git("update-ref", "refs/remotes/origin/reused", base_oid)
                globals()["merged_pr_heads"] = lambda _limit, _base: (
                    [(91, "reused", work_tip, False)], None)
                try:
                    rc2, out = run(["--no-fetch", "--base", "base",
                                    "--merged-prs", "1"])
                    case("merged-reused-rc", (rc, rc2),
                         (0, RC_FINDING),
                         "a recreated same-name branch cannot false-pass")
                    case("merged-reused-word", "UNKNOWN" in out, True,
                         "...and failed continuity is UNKNOWN")
                finally:
                    globals()["merged_pr_heads"] = saved_merged_pr_heads

                # The opposite divergence matters too: a local commit that is
                # not pushed must not disappear merely because origin is
                # refreshed and already contained.
                _git("checkout", "-qb", "local-ahead", "base")
                _git("push", "-q", "origin", "local-ahead")
                open("local-only", "w").write("not pushed")
                _git("add", "local-only")
                _git("commit", "-qm", "local-only")
                rc, local_ahead = _git(
                    "rev-list", "--count", "origin/base..local-ahead")
                rc2, remote_ahead = _git(
                    "rev-list", "--count", "origin/base..origin/local-ahead")
                case("local-ahead-fixture",
                     (rc, local_ahead, rc2, remote_ahead),
                     (0, "1", 0, "0"),
                     "only the local tip carries the unpushed commit")
                rc, out = run(["--base", "base", "local-ahead"])
                case("local-ahead-rc", rc, RC_FINDING,
                     "a fetched remote cannot hide unpushed local work")
                case("local-ahead-word",
                     "local-ahead (local)" in out and "STRANDED" in out,
                     True, "...and the local tip is named in the finding")
                rc, out = run(["--base", "base", "origin/local-ahead"])
                case("origin-spelling-local", rc, RC_FINDING,
                     "origin/name still checks an unpushed local tip")
                case("origin-spelling-label",
                     "origin/local-ahead (local)" in out and "STRANDED" in out,
                     True, "...and identifies the local source")

                # Normal mode refreshes origin only.  Accepting another
                # remote-tracking namespace would give a stale local cache the
                # authority of a fetch.  Reject both full and short spellings.
                _git("update-ref", "refs/remotes/upstream/work", "base")
                rc, out = run(["--base", "base",
                               "refs/remotes/upstream/work"])
                case("other-remote-full-rc", rc, RC_CANNOT_RUN,
                     "an unrefreshed full remote ref is refused")
                rc, out = run(["--base", "base", "upstream/work"])
                case("other-remote-short-rc", rc, RC_CANNOT_RUN,
                     "...and so is its short spelling")
                _git("update-ref", "refs/remotes/upstream/base", "base")
                rc, out = run(["--base", "refs/remotes/upstream/base",
                               "work"])
                case("other-remote-base-rc", rc, RC_CANNOT_RUN,
                     "an unrefreshed base ref is refused too")

                # After fetch --prune removes a deleted origin branch, a stale
                # local tip must not stand in for work that may have existed on
                # the remote.  Reproduce the incident shape in a separate repo:
                # H was merged, S was pushed later, then origin/feature vanished
                # while the checker's local feature remained at H.
                with tempfile.TemporaryDirectory() as deleted_parent:
                    checker = os.path.join(deleted_parent, "checker")
                    deleted_remote = os.path.join(deleted_parent, "remote.git")
                    writer = os.path.join(deleted_parent, "writer")
                    os.mkdir(checker)
                    os.chdir(checker)
                    _git("init", "-q", "-b", "base")
                    _git("config", "user.email", "s@s")
                    _git("config", "user.name", "s")
                    open("seed", "w").write("seed")
                    _git("add", "seed"); _git("commit", "-qm", "seed")
                    _git("checkout", "-qb", "feature")
                    open("merged", "w").write("H")
                    _git("add", "merged"); _git("commit", "-qm", "H")
                    _git("checkout", "-q", "base")
                    _git("merge", "-q", "--no-ff", "feature", "-m", "M")
                    _git("init", "--bare", "-q", deleted_remote)
                    _git("remote", "add", "origin", deleted_remote)
                    _git("push", "-q", "origin", "base", "feature")
                    _git("clone", "-q", deleted_remote, writer)
                    os.chdir(writer)
                    _git("config", "user.email", "s@s")
                    _git("config", "user.name", "s")
                    _git("checkout", "-q", "feature")
                    open("stranded", "w").write("S")
                    _git("add", "stranded"); _git("commit", "-qm", "S")
                    rc, stranded_oid = _git("rev-parse", "HEAD")
                    _git("push", "-q", "origin", "feature")
                    _git("push", "-q", "origin",
                         f"{stranded_oid}:refs/heads/evidence-S")
                    _git("push", "-q", "origin", "--delete", "feature")
                    os.chdir(checker)
                    rc, out = run(["--base", "origin/base", "feature"])
                    case("deleted-remote-rc", rc, RC_FINDING,
                         "a deleted remote tip cannot fall back to stale local")
                    case("deleted-remote-word", "UNKNOWN" in out, True,
                         "...and the missing origin tip is UNKNOWN")
                    case("deleted-remote-label", "feature (origin)" in out,
                         True, "...while the missing source is named")
                    os.chdir(td)

                # An incomplete history cannot prove ancestry or patch
                # equivalence.  Offline mode must refuse it, while normal mode
                # deepens the clone before answering.
                _git("--git-dir", remote, "symbolic-ref", "HEAD",
                     "refs/heads/work")
                with tempfile.TemporaryDirectory() as shallow_parent:
                    shallow_repo = os.path.join(shallow_parent, "repo")
                    _git("clone", "-q", "--depth", "1",
                         "--no-single-branch", "file://" + remote,
                         shallow_repo)
                    os.chdir(shallow_repo)
                    rc, out = run(["--no-fetch", "--base", "origin/base",
                                   "origin/work"])
                    case("shallow-offline-rc", rc, RC_CANNOT_RUN,
                         "offline mode refuses incomplete history")
                    rc, out = run(["--base", "origin/base", "origin/work"])
                    case("shallow-deepened-rc", rc, RC_FINDING,
                         "normal mode deepens before measuring containment")
                    os.chdir(td)

            # A short name shared by a branch and tag is not a stable input.
            # Git's normal precedence chooses the tag, which can hide a
            # stranded branch.  The checker must refuse the ambiguous name.
            _git("checkout", "-qb", "collision", "base")
            open("collision-work", "w").write("stranded")
            _git("add", "collision-work"); _git("commit", "-qm", "collision")
            _git("tag", "collision", "base")
            rc, out = run(["--no-fetch", "--base", "base", "collision"])
            case("ambiguous-ref-rc", rc, RC_FINDING,
                 "a tag and branch sharing one name cannot false-pass")
            case("ambiguous-ref-word", "UNKNOWN" in out, True,
                 "...and the ambiguity is reported as UNKNOWN")

            # Replacement refs rewrite ancestry for ordinary Git plumbing.
            # Make the base appear to descend from a stranded feature, then
            # prove the checker ignores that caller-local alternate history.
            _git("checkout", "-qb", "replace-feature", "base")
            open("replace-work", "w").write("stranded")
            _git("add", "replace-work"); _git("commit", "-qm", "replace work")
            rc, replace_feature = _git("rev-parse", "HEAD")
            _git("checkout", "-qb", "replace-base", "base")
            open("replace-unrelated", "w").write("base")
            _git("add", "replace-unrelated")
            _git("commit", "-qm", "replace base")
            rc2, replace_base = _git("rev-parse", "HEAD")
            replace_rc, _ = _git("replace", "--graft", replace_base,
                                  replace_feature)
            rc, out = run(["--no-fetch", "--base", "replace-base",
                           "replace-feature"])
            case("replacement-ref-fixture", (rc2, replace_rc), (0, 0),
                 "the fixture installs a replacement ancestry edge")
            case("replacement-ref-rc", rc, RC_FINDING,
                 "replacement ancestry cannot create containment")
            case("replacement-ref-path", "replace-work" in out, True,
                 "...and the raw stranded path is reported")
            _git("replace", "-d", replace_base)

            # Legacy info/grafts rewrites ancestry even when replacement refs
            # are disabled.  Refuse the repository rather than trusting an
            # alternate commit graph that cannot be disabled per invocation.
            graft_rc, graft_path = _git("rev-parse", "--git-path",
                                        "info/grafts")
            with open(graft_path, "w") as grafts:
                grafts.write(f"{replace_base} {replace_feature}\n")
            try:
                rc, out = run(["--no-fetch", "--base", "replace-base",
                               "replace-feature"])
                case("legacy-graft-fixture", graft_rc, 0,
                     "the fixture locates Git's active graft file")
                case("legacy-graft-rc", rc, RC_CANNOT_RUN,
                     "legacy graft ancestry is refused before a verdict")
                ok, ahead, note = contained("replace-feature", "replace-base")
                case("legacy-graft-direct", (ok, ahead), (None, None),
                     "the containment predicate cannot trust grafts either")
            finally:
                os.remove(graft_path)

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

            _git("checkout", "-qb", "net-zero", "base")
            open("temporary-change", "w").write("added then removed")
            _git("add", "temporary-change")
            _git("commit", "-qm", "add temporary path")
            os.remove("temporary-change")
            _git("add", "-A")
            _git("commit", "-qm", "remove temporary path")
            rc, out = run(["--no-fetch", "--base", "base", "net-zero"])
            case("net-zero-history-rc", rc, RC_OK,
                 "a branch with no net tree change is already contained")
            case("net-zero-history-word", "no net tree change" in out, True,
                 "...and the conservative proof is named")

            # A failed proof-producing path enumeration is UNKNOWN, not a
            # STRANDED verdict assembled from incomplete evidence.
            saved_git = globals()["_git"]
            globals()["_git"] = lambda *args: (
                (128, "") if args and args[0] == "diff"
                and "--name-only" in args else saved_git(*args))
            try:
                rc, out = run(["--no-fetch", "--base", "squash-base",
                               "squash-feature"])
                case("path-enumeration-error-rc", rc, RC_FINDING,
                     "a failed path measurement exits non-zero")
                case("path-enumeration-error-word", "UNKNOWN" in out, True,
                     "...and is UNKNOWN rather than STRANDED")
            finally:
                globals()["_git"] = saved_git

            saved_git = globals()["_git"]
            globals()["_git"] = lambda *args: (
                (128, "") if args and args[0] == "--literal-pathspecs"
                and "--quiet" in args else saved_git(*args))
            try:
                rc, out = run(["--no-fetch", "--base", "squash-base",
                               "squash-feature"])
                case("path-comparison-error-rc", rc, RC_FINDING,
                     "a failed path comparison exits non-zero")
                case("path-comparison-error-word", "UNKNOWN" in out, True,
                     "...and is UNKNOWN rather than STRANDED")
            finally:
                globals()["_git"] = saved_git

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

            # A filename is data, not a Git pathspec.  Without literal mode an
            # exclude-shaped name removes itself from the comparison.
            magic_name = ":(exclude)magic"
            _git("checkout", "-qb", "pathspec-feature", "base")
            open(magic_name, "w").write("stranded")
            _git("--literal-pathspecs", "add", "--", magic_name)
            _git("commit", "-qm", "pathspec")
            rc, out = run(["--no-fetch", "--base", "base",
                           "pathspec-feature"])
            case("literal-pathspec-name", rc, RC_FINDING,
                 "an exclude-shaped filename remains part of the comparison")

            # Verbatim patch-id equivalence is valid for a linear rebased
            # history even when the base later edits the same path.
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
            case("linear-patch-word",
                 "every commit has a whitespace-exact equivalent" in out,
                 True, "...through the patch-id fallback")

            # git cherry strips whitespace when it computes patch IDs.  These
            # two values are different content and must never compare equal.
            _git("checkout", "-qb", "whitespace-feature", "base")
            open("spacing.py", "w").write('value = "old"\n')
            _git("add", "spacing.py"); _git("commit", "-qm", "spacing seed")
            _git("checkout", "-qb", "whitespace-base", "HEAD~1")
            open("spacing.py", "w").write('value = "old"\n')
            _git("add", "spacing.py"); _git("commit", "-qm", "spacing seed")
            _git("checkout", "-q", "whitespace-feature")
            open("spacing.py", "w").write('value = "a b"\n')
            _git("commit", "-qam", "space is data")
            _git("checkout", "-q", "whitespace-base")
            open("spacing.py", "w").write('value = "ab"\n')
            _git("commit", "-qam", "different content")
            rc, cherry = _git("cherry", "whitespace-base",
                              "whitespace-feature")
            case("whitespace-fixture",
                 rc == 0 and bool(cherry)
                 and all(line.startswith("-") for line in cherry.splitlines()),
                 True, "git cherry equates different whitespace content")
            rc, out = run(["--no-fetch", "--base", "whitespace-base",
                           "whitespace-feature"])
            case("whitespace-exact-rc", rc, RC_FINDING,
                 "verbatim patch IDs refuse different content")
            case("whitespace-exact-path", "spacing.py" in out, True,
                 "...and the differing path is reported")

            # Verbatim patch IDs still omit hunk line numbers.  The same edit
            # to two repeated blocks therefore hashes alike, but the resulting
            # files differ and must not be certified as a replay.
            block = "a\nb\nc\nold\nd\ne\nf\n"
            separator = "".join(f"separator-{i}\n" for i in range(10))
            repeated = block + separator + block
            _git("checkout", "-qb", "hunk-feature", "base")
            open("repeated.txt", "w").write(repeated)
            _git("add", "repeated.txt"); _git("commit", "-qm", "hunk seed")
            _git("checkout", "-qb", "hunk-base", "HEAD~1")
            open("repeated.txt", "w").write(repeated)
            _git("add", "repeated.txt"); _git("commit", "-qm", "hunk seed")
            _git("checkout", "-q", "hunk-feature")
            open("repeated.txt", "w").write(repeated.replace("old", "new", 1))
            _git("commit", "-qam", "first block")
            rc, hunk_feature = _git("rev-parse", "HEAD")
            _git("checkout", "-q", "hunk-base")
            before, after = repeated.rsplit("old", 1)
            open("repeated.txt", "w").write(before + "new" + after)
            _git("commit", "-qam", "second block")
            rc2, hunk_base = _git("rev-parse", "HEAD")
            feature_id, feature_err = _verbatim_patch_id(hunk_feature)
            base_id, base_err = _verbatim_patch_id(hunk_base)
            case("hunk-position-fixture",
                 (rc, rc2, feature_err, base_err, feature_id == base_id),
                 (0, 0, None, None, True),
                 "verbatim patch IDs omit the different hunk positions")
            rc, out = run(["--no-fetch", "--base", "hunk-base",
                           "hunk-feature"])
            case("hunk-postimage-rc", rc, RC_FINDING,
                 "different repeated locations cannot false-pass")
            case("hunk-postimage-path", "repeated.txt" in out, True,
                 "...and the differing path is reported")

            # Diff configuration and attributes are untrusted inputs.  A
            # textconv that prints nothing can hide changed blobs from both
            # the path proof and patch fallback, while ignoreSubmodules=all can
            # hide a missing gitlink update.  Each fixture uses a separate repo
            # so its deliberately hostile configuration cannot leak onward.
            with tempfile.TemporaryDirectory() as config_parent:
                textconv_path = os.path.join(config_parent, "textconv-path")
                os.mkdir(textconv_path)
                os.chdir(textconv_path)
                _git("init", "-q", "-b", "root")
                _git("config", "user.email", "s@s")
                _git("config", "user.name", "s")
                open("f", "w").write("root\n")
                open(".gitattributes", "w").write("f diff=quiet\n")
                _git("add", "f", ".gitattributes")
                _git("commit", "-qm", "root")
                _git("checkout", "-qb", "feature")
                open("f", "w").write("stranded\n")
                _git("commit", "-qam", "feature")
                _git("checkout", "-qb", "base", "root")
                open("unrelated", "w").write("base")
                _git("add", "unrelated"); _git("commit", "-qm", "base")
                _git("config", "diff.quiet.textconv", "/bin/true")
                raw_rc, _ = _git("diff", *RAW_DIFF_FLAGS, "--quiet",
                                 "base", "feature", "--", "f")
                case("textconv-path-raw", raw_rc, 1,
                     "raw diff sees content hidden by textconv")
                rc, out = run(["--no-fetch", "--base", "base", "feature"])
                case("textconv-path-rc", rc, RC_FINDING,
                     "textconv cannot create path-equivalence containment")
                case("textconv-path-name", "f" in out, True,
                     "...and the raw differing path is reported")

                textconv_patch = os.path.join(config_parent, "textconv-patch")
                os.mkdir(textconv_patch)
                os.chdir(textconv_patch)
                _git("init", "-q", "-b", "root")
                _git("config", "user.email", "s@s")
                _git("config", "user.name", "s")
                open("f", "w").write("root\n")
                open(".gitattributes", "w").write("f diff=quiet\n")
                _git("add", "f", ".gitattributes")
                _git("commit", "-qm", "root")
                _git("checkout", "-qb", "feature")
                open("f", "w").write("stranded\n")
                open("g", "w").write("landed\n")
                _git("add", "f", "g"); _git("commit", "-qm", "first")
                rc, branch_first = _git("rev-parse", "HEAD")
                open("h", "w").write("landed\n")
                _git("add", "h"); _git("commit", "-qm", "second")
                _git("checkout", "-qb", "base", "root")
                open("g", "w").write("landed\n")
                _git("add", "g"); _git("commit", "-qm", "first replay")
                rc2, base_first = _git("rev-parse", "HEAD")
                open("h", "w").write("landed\n")
                _git("add", "h"); _git("commit", "-qm", "second replay")
                open("h", "w").write("superseded\n")
                _git("commit", "-qam", "later")
                _git("config", "diff.quiet.textconv", "/bin/true")
                branch_id, branch_err = _verbatim_patch_id(branch_first)
                base_id, base_err = _verbatim_patch_id(base_first)
                case("textconv-patch-raw",
                     (rc, rc2, branch_err, base_err, branch_id != base_id),
                     (0, 0, None, None, True),
                     "raw patch IDs include content hidden by textconv")
                rc, out = run(["--no-fetch", "--base", "base", "feature"])
                case("textconv-patch-rc", rc, RC_FINDING,
                     "textconv cannot create patch-equivalence containment")
                case("textconv-patch-name", "f" in out, True,
                     "...and the hidden file is reported")

                submodule_repo = os.path.join(config_parent, "submodule")
                os.mkdir(submodule_repo)
                os.chdir(submodule_repo)
                _git("init", "-q", "-b", "root")
                _git("config", "user.email", "s@s")
                _git("config", "user.name", "s")
                open("seed", "w").write("seed")
                _git("add", "seed"); _git("commit", "-qm", "root")
                rc, root_oid = _git("rev-parse", "HEAD")
                _git("checkout", "-qb", "feature")
                open("landed", "w").write("landed")
                _git("add", "landed")
                _git("update-index", "--add", "--cacheinfo",
                     f"160000,{root_oid},submodule-pin")
                _git("commit", "-qm", "feature")
                _git("checkout", "-qb", "base", "root")
                open("landed", "w").write("landed")
                _git("add", "landed"); _git("commit", "-qm", "partial")
                _git("config", "diff.ignoreSubmodules", "all")
                raw_rc, _ = _git("diff", *RAW_DIFF_FLAGS, "--quiet",
                                 "base", "feature", "--", "submodule-pin")
                case("submodule-pin-raw", (rc, raw_rc), (0, 1),
                     "raw diff includes a gitlink despite ignore configuration")
                rc, out = run(["--no-fetch", "--base", "base", "feature"])
                case("submodule-pin-rc", rc, RC_FINDING,
                     "an ignored submodule pin cannot false-pass")
                case("submodule-pin-name", "submodule-pin" in out, True,
                     "...and the missing gitlink path is reported")
                os.chdir(td)

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

    #! Reject unknown options rather than silently treating them as branches.
    #! `--bse 43a4c417 origin/foo` used to check TWO branches called
    #! "43a4c417" and "origin/foo" against the default base -- both contained,
    #! rc 0 -- where the same command spelled correctly reported 4 stranded.
    for a in args:
        if a.startswith("-") and a not in KNOWN_FLAGS:
            sys.stderr.write(f"unknown option: {a}\n{USAGE}\n")
            return RC_CANNOT_RUN

    for flag in ("--selftest", "--base", "--merged-prs", "--no-fetch"):
        if args.count(flag) > 1:
            sys.stderr.write(f"{flag} may be specified only once\n{USAGE}\n")
            return RC_CANNOT_RUN

    graft_error = active_graft_error()
    if graft_error:
        sys.stderr.write(graft_error + "\n")
        return RC_CANNOT_RUN

    if "--selftest" in args:
        if args != ["--selftest"]:
            sys.stderr.write(f"--selftest accepts no other arguments\n{USAGE}\n")
            return RC_CANNOT_RUN
        return selftest()

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

    if not exact_ref_syntax(base):
        sys.stderr.write(
            f"base must be an exact ref name or full object ID, not a "
            f"revision expression: {base}\n")
        return RC_CANNOT_RUN
    if "--merged-prs" not in args:
        for ref in (a for a in args if not a.startswith("-")):
            if not exact_ref_syntax(ref):
                sys.stderr.write(
                    f"branch must be an exact ref name or full object ID, "
                    f"not a revision expression: {ref}\n")
                return RC_CANNOT_RUN

    do_fetch = "--no-fetch" not in args
    args = [a for a in args if a != "--no-fetch"]
    rc, shallow = _git("rev-parse", "--is-shallow-repository")
    if rc != 0 or shallow not in ("true", "false"):
        sys.stderr.write(
            "could not determine whether the repository history is complete\n")
        return RC_CANNOT_RUN
    if shallow == "true" and not do_fetch:
        sys.stderr.write(
            "--no-fetch cannot answer from a shallow repository: history is "
            "incomplete\n")
        return RC_CANNOT_RUN
    if do_fetch:
        refs_to_refresh = [base]
        if "--merged-prs" not in args:
            refs_to_refresh.extend(a for a in args if not a.startswith("-"))
        for ref in refs_to_refresh:
            stale_remote = non_origin_remote_ref(ref)
            if stale_remote:
                sys.stderr.write(
                    f"cannot refresh {stale_remote}: normal mode fetches "
                    f"origin only. Use an origin ref, or use --no-fetch only "
                    f"when that other remote-tracking ref is known current.\n")
                return RC_CANNOT_RUN
        #! Answering from a stale remote-tracking ref is how this tool once
        #! reported `contained` for a branch that had work stranded on it.
        fetch_args = ["fetch", "--prune", "--quiet"]
        if shallow == "true":
            fetch_args.append("--unshallow")
        #! Do not trust a narrowed remote.origin.fetch configuration.  The
        #! command accepts any origin branch and must refresh every branch it
        #! may later resolve.
        fetch_args.extend(("origin",
                           "+refs/heads/*:refs/remotes/origin/*"))
        rc, _ = _git(*fetch_args)
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
        if args:
            sys.stderr.write(
                f"--merged-prs does not accept branch operands\n{USAGE}\n")
            return RC_CANNOT_RUN
        prs, err = merged_pr_heads(limit, base)
        if err:
            sys.stderr.write(err + "\n")
            return RC_CANNOT_RUN
        if not prs:
            sys.stderr.write(
                f"no merged PRs found targeting {base}. That is not a pass -- "
                f"check the base name.\n")
            return RC_CANNOT_RUN
        #! headRefOid is frozen at merge time and cannot reveal later pushes,
        #! but it proves that a current same-name ref is still the same branch.
        #! A fork, force-push, deletion or branch-name reuse becomes UNKNOWN
        #! instead of certifying an unrelated origin ref.
        targets = []
        for number, branch, head_oid, cross_repository in prs:
            label = f"#{number} {branch}"
            live_ref = f"refs/remotes/origin/{branch}"
            if cross_repository:
                pre_error = ("the merged head belongs to another repository; "
                             "origin cannot refresh or identify its live tip")
            else:
                pre_error = continuous_merged_pr_tip(head_oid, live_ref)
            targets.append((label, live_ref, pre_error))
    else:
        branches = [a for a in args if not a.startswith("-")]
        if not branches:
            rc, cur = _git("rev-parse", "--abbrev-ref", "HEAD")
            if rc != 0 or not cur or cur == "HEAD":
                sys.stderr.write(USAGE + "\n")
                return RC_CANNOT_RUN
            branches = [cur]
        targets = []
        for branch in branches:
            refs = (fetched_branch_refs(branch) if do_fetch
                    else [(branch, None)])
            for ref, source in refs:
                label = (f"{branch} ({source})" if len(refs) > 1 else branch)
                targets.append((label, ref, None))

    stranded = 0
    unknown = 0
    for label, ref, pre_error in targets:
        if pre_error:
            print(f"  UNKNOWN    {label}: {pre_error}")
            unknown += 1
            continue
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
        print(f"{stranded} branch tip(s) have work that {base} does not.")
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
