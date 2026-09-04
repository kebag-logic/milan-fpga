#!/usr/bin/env python3
"""Did the merge actually take the branch?

    python3 scripts/check_merge_containment.py [--base <ref>] <branch>...
    python3 scripts/check_merge_containment.py --merged-prs [N]
    python3 scripts/check_merge_containment.py --selftest
    python3 scripts/check_merge_containment.py --no-fetch ...   (skip Git fetch)

WHY THIS EXISTS
---------------
A pull request merged before review activity stops can leave later work
behind: the merge takes the commit the branch had at the time, and everything
pushed after it stays on the branch.  Nothing reports this.  ``gh pr view``
says ``MERGED`` and CI is green, while the issue and board can be closed
manually even though commits remain on a branch nobody is watching.

It has happened twice here: **#77** (merged after a positive round, while
later review still produced two blocking rounds; re-landed as #85) and **#86**
(merged with a round running; three commits stranded, tracked as #87 and
re-landed as #89).  Both were found by a reviewer checking by hand, which is
why this is a command.

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
from pathlib import Path

USAGE = __doc__.split("WHY THIS EXISTS")[0].strip()

#! rc 0 contained · rc 1 something is stranded or unknown · rc 2 cannot run
RC_OK, RC_FINDING, RC_CANNOT_RUN = 0, 1, 2
DEFAULT_BASE = "origin/dev"
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


def active_graft_error() -> str | None:
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


def is_full_oid(ref: str) -> bool:
    """True when ``ref`` has a complete SHA-1 or SHA-256 spelling."""
    return (len(ref) in (40, 64)
            and all(c in "0123456789abcdefABCDEF" for c in ref))


def exact_ref_syntax(ref: str) -> bool:
    """True for a ref name or full object ID, never a revision expression."""
    if is_full_oid(ref):
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


def refreshed_origin_ref(ref: str) -> str:
    """Prefer the fetched origin tip when ``ref`` names a branch.

    ``git fetch origin`` refreshes ``refs/remotes/origin/*``; it deliberately
    does not move a checked-out local branch.  Checking that local ref after a
    fetch therefore gives exactly the stale answer this command exists to
    prevent.  Full non-branch refs remain exact, and callers using
    ``--no-fetch`` do not call this helper.
    """
    if is_full_oid(ref):
        return ref
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
    #! Normal mode has just fetched origin, so an origin-qualified answer is
    #! authoritative even when that ref is now missing.  Falling back to an
    #! explicit but stale refs/heads base can certify work against a branch
    #! that origin deleted.  Deliberate local-only checks use --no-fetch.
    return remote_ref


def configured_remote_name(ref: str) -> tuple[str | None, str | None]:
    """Return the longest configured remote prefix in a shorthand ref."""
    if "/" not in ref:
        return (None, None)
    rc, configured = _git("remote")
    if rc != 0:
        return (None, "could not identify configured remotes")
    matches = [name for name in configured.splitlines()
               if ref.startswith(name + "/")]
    if len(matches) > 1:
        matches.sort(key=len, reverse=True)
        return (None, f"{ref!r} matches multiple configured remotes: "
                + ", ".join(matches))
    return (matches[0] if matches else None, None)


def offline_ref(ref: str) -> tuple[str | None, str | None]:
    """Resolve a local-only branch spelling without falling through to tags."""
    if is_full_oid(ref) or ref.startswith("refs/"):
        return (ref, None)

    local_ref = "refs/heads/" + ref
    remote_ref = "refs/remotes/" + ref
    remote_name, remote_error = configured_remote_name(ref)
    if remote_error:
        return (None, remote_error + f" for {ref!r}")
    if remote_name:
        #! --no-fetch is the deliberate route for another remote.  Its
        #! shorthand keeps that remote identity even when a slash-named local
        #! branch also exists or the tracking ref is missing.  Remote names
        #! may themselves contain slashes, so match the full configured name.
        return (remote_ref, None)
    if ref.startswith("origin/"):
        return (remote_ref, None)
    local_rc, _ = _git("rev-parse", "--verify", "--quiet",
                       local_ref + "^{commit}")
    remote_rc, _ = _git("rev-parse", "--verify", "--quiet",
                        remote_ref + "^{commit}")
    if local_rc == 0 and remote_rc == 0:
        return (None, f"{ref!r} names both {local_ref} and {remote_ref}; "
                f"name the full ref")
    if remote_rc == 0:
        return (remote_ref, None)
    #! A short operand denotes a branch, never a tag.  Keep a missing local
    #! branch fully qualified so a same-named tag cannot turn UNKNOWN into a
    #! false contained result.
    return (local_ref, None)


def fetched_branch_refs(ref: str) -> list[tuple[str, str | None]]:
    """Return every distinct local/remote tip named by a branch argument.

    A local branch can be either behind its fetched remote tip or ahead with
    unpushed work.  Replacing one with the other hides one of those two failure
    modes.  When both exist and differ, containment must be proven for both.
    The source labels are used only to make the two answers distinguishable.
    """
    if is_full_oid(ref):
        return [(ref, None)]
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
    #! Fetch completed, so an absent branch stays absent.  Returning the
    #! caller's short spelling here lets Git resolve a tag in its place and
    #! certify a deleted remote branch as contained.
    return [(remote_ref, "origin")]


def non_origin_remote_ref(ref: str) -> str | None:
    """Name an unrefreshable remote-tracking ref, or return None."""
    if is_full_oid(ref):
        return None
    #! These spellings explicitly select the namespace refreshed by the
    #! origin fetch below.  A pathological configured remote named
    #! origin/team may share its tracking path, but fetching origin overwrites
    #! that path with origin's authoritative team/... branch before use.
    if ref.startswith("refs/remotes/origin/") or ref.startswith("origin/"):
        return None
    if ref.startswith("refs/"):
        if not ref.startswith("refs/remotes/"):
            return None
        shorthand = ref[len("refs/remotes/"):]
    else:
        shorthand = ref
    remote_name, remote_error = configured_remote_name(shorthand)
    if remote_error:
        #! We cannot prove that a remote-like shorthand is refreshable by the
        #! origin-only fetch, so refuse it instead of changing type.
        return ref
    if remote_name and remote_name != "origin":
        return (ref if ref.startswith("refs/remotes/")
                else "refs/remotes/" + ref)
    if (ref.startswith("refs/remotes/origin/")
            or ref.startswith("origin/")):
        return None
    if ref.startswith("refs/remotes/"):
        return ref
    #! Resolve the remote namespace directly before asking Git to resolve the
    #! caller's shorthand.  When refs/heads/upstream/work and
    #! refs/remotes/upstream/work both exist, symbolic-full-name rejects the
    #! ambiguous spelling.  Treating that failure as "not a remote" lets the
    #! normal path silently measure origin/upstream/work instead.
    rc, _ = _git("rev-parse", "--verify", "--quiet",
                 "refs/remotes/" + ref + "^{commit}")
    if rc == 0:
        return "refs/remotes/" + ref
    rc, full = _git("rev-parse", "--symbolic-full-name", "--verify", ref)
    if (rc == 0 and full.startswith("refs/remotes/")
            and not full.startswith("refs/remotes/origin/")):
        return full
    return None


def _unreadable_ref_error(branch, base):
    """Explain a ref that cannot be resolved or is ambiguous, or return None."""
    for ref in (branch, base):
        rc, _ = _git("rev-parse", "--verify", "--quiet", ref + "^{commit}")
        if rc != 0:
            return f"no such ref: {ref}"
        #! An ambiguous name (a tag AND a branch called the same thing) is
        #! resolved silently by git's own precedence -- the tag wins, and a
        #! stranded branch reads as contained. git says so on stderr, which
        #! _git discards, so ask explicitly instead of trusting the default.
        hits = ([] if is_full_oid(ref) or ref.startswith("refs/") else
                [k for k in ("refs/heads/", "refs/remotes/", "refs/tags/")
                 if _git("rev-parse", "--verify", "--quiet", k + ref)[0] == 0])
        if len(hits) > 1:
            return (f"{ref!r} is ambiguous ({', '.join(h + ref for h in hits)})"
                    f" -- name the full ref")
    return None


def _commits_ahead(branch, base):
    """(count, None), or (None, error) when the count cannot be measured."""
    rc, out = _git("rev-list", "--count", f"{base}..{branch}")
    if rc != 0:
        return (None, f"rev-list failed for {base}..{branch}")
    #! empty is NOT zero -- rev-list always prints a number when it succeeds,
    #! so nothing means the plumbing failed and the answer is unknown
    if not out.isdigit():
        return (None,
                f"rev-list printed {out!r} rather than a count; treating as "
                f"UNKNOWN rather than as zero")
    return (int(out), None)


def _path_scoped_verdict(branch, base, merge_base, ahead):
    """A contained/UNKNOWN triple from the touched-path proof, or None.

    None means the paths still differ, which is not yet a verdict: the patch-id
    fallback gets its turn before anything is called stranded.
    """
    #! Disable rename folding so a move contributes both the deleted and
    #! added path.  Comparing only the destination can certify a base that
    #! copied the file but never removed the source.  NUL delimiters keep
    #! unusual but valid path names exact.
    rc, names = _git("diff", *RAW_DIFF_FLAGS, "--name-only",
                     "--no-renames", "-z", merge_base, branch)
    if rc != 0:
        return (None, None,
                f"git diff could not enumerate paths changed by {branch}")
    paths = [n for n in names.split("\0") if n]
    if not paths:
        rc, _ = _git("diff", *RAW_DIFF_FLAGS, "--quiet", merge_base, branch)
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
    return None


def _patch_id_verdict(branch, base, ahead):
    """A contained/UNKNOWN triple from whitespace-exact patch IDs, or None."""
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
    return None


def _differing_paths(branch, base):
    """(first few paths that differ, None), or ([], error) when unmeasurable."""
    rc, names = _git("diff", *RAW_DIFF_FLAGS, "--name-only",
                     "--no-renames", "-z", base, branch)
    if rc != 0:
        return ([],
                f"git diff could not enumerate paths differing between "
                f"{branch} and {base}")
    return ([n for n in names.split("\0") if n][:6], None)


def contained(branch: str,
              base: str) -> tuple[bool | None, int | None, str | None]:
    """(is_contained, commits_ahead, note_or_error).

    ``is_contained`` is True when ``base`` already has this branch's work --
    either because every commit is an ancestor, or because the content landed
    by another route (squash, rebase).  None means the question could not be
    answered, which is a finding, never a pass.
    """
    graft_error = active_graft_error()
    if graft_error:
        return (None, None, graft_error)

    ref_error = _unreadable_ref_error(branch, base)
    if ref_error:
        return (None, None, ref_error)

    rc, _ = _git("merge-base", "--is-ancestor", branch, base)
    if rc == 0:
        return (True, 0, None)
    if rc != 1:
        return (None, None,
                f"merge-base could not compare {branch} with {base}")

    ahead, count_error = _commits_ahead(branch, base)
    if count_error:
        return (None, None, count_error)

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
    have_merge_base = mb_rc == 0 and bool(mb)
    if have_merge_base:
        verdict = _path_scoped_verdict(branch, base, mb, ahead)
        if verdict is not None:
            return verdict

    verdict = _patch_id_verdict(branch, base, ahead)
    if verdict is not None:
        return verdict

    #! NAME THE PATHS. "3 commits not in base" does not tell anyone whether
    #! this is real, and there is one case that reads STRANDED without being
    #! so: a multi-commit squash whose paths were later edited on base. No
    #! patch-id matches (the squash collapsed them) and the paths no longer
    #! agree (the later edit), so neither arm above can prove it landed. That
    #! is a false ALARM rather than a false pass -- the safe direction -- and
    #! naming the paths is what lets a reader settle it in one look instead of
    #! learning to ignore the check.
    differing = []
    if have_merge_base:
        differing, enumeration_error = _differing_paths(branch, base)
        if enumeration_error:
            return (None, None, enumeration_error)
    return (False, ahead, ("paths differing: " + ", ".join(differing))
            if differing else None)


def post_merge_ref_event_error(number: int,
                               merged_at: str | None) -> str | None:
    """Report a durable GitHub event that breaks branch-tip continuity."""
    import json
    if not isinstance(merged_at, str) or not merged_at:
        return "GitHub returned no merge timestamp for the pull request"
    try:
        p = subprocess.run(
            ["gh", "api", "--paginate", "--slurp",
             f"repos/{{owner}}/{{repo}}/issues/{number}/timeline?per_page=100"],
            capture_output=True, text=True)
    except FileNotFoundError:
        return "gh is not installed, so branch history events are unknown"
    if p.returncode != 0:
        return ("gh could not read pull-request timeline events: "
                + (p.stderr or "").strip()[:200])
    try:
        pages = json.loads(p.stdout)
        if not isinstance(pages, list):
            raise ValueError("timeline response is not a page list")
        events = []
        for page in pages:
            if not isinstance(page, list):
                raise ValueError("timeline page is not an event list")
            events.extend(page)
    except (ValueError, TypeError) as exc:
        return f"could not parse pull-request timeline events: {exc}"

    continuity_events = {
        "head_ref_deleted", "head_ref_restored", "head_ref_force_pushed"
    }
    for event in events:
        if not isinstance(event, dict) or event.get("event") not in continuity_events:
            continue
        created_at = event.get("created_at")
        if not isinstance(created_at, str) or not created_at:
            return (f"GitHub returned an undated {event.get('event')} event "
                    f"for PR #{number}")
        if created_at >= merged_at:
            return (f"GitHub records {event['event']} at {created_at}, on or "
                    f"after the PR merged; the current same-name ref cannot "
                    f"prove branch continuity")
    return None


def merged_pr_heads(
        limit: int, base: str
) -> tuple[list[tuple[int, str, str, bool, str | None]] | None, str | None]:
    """([(number, branch, head_oid, cross_repository, ref_error)], error).

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
    #! remote. Passing "origin/dev" here silently matched nothing, so the
    #! sweep printed an empty list and exited 0 -- a pass by vacancy.
    if base.startswith("refs/remotes/origin/"):
        base_name = base[len("refs/remotes/origin/"):]
    elif base.startswith("origin/"):
        base_name = base[len("origin/"):]
    elif base.startswith("refs/heads/"):
        base_name = base[len("refs/heads/"):]
    else:
        base_name = base
    #! gh cannot order by mergedAt.  Fetch a complete candidate set, refuse a
    #! truncated result, then sort locally.  Limiting an updated-desc query
    #! first lets a comment on an old PR displace the newest merge.
    candidate_limit = max(limit + 1, 1001)
    try:
        p = subprocess.run(
            ["gh", "pr", "list", "--state", "merged", "--base", base_name,
             "--limit", str(candidate_limit),
             "--json",
             "number,headRefName,headRefOid,isCrossRepository,mergedAt"],
            capture_output=True, text=True)
    except FileNotFoundError:
        #! distinct from "stranded": a tool we cannot run is not a finding
        return (None, "gh is not installed, so merged PRs cannot be listed")
    if p.returncode != 0:
        return (None, "gh could not list merged PRs (authenticated?): "
                      + (p.stderr or "").strip()[:200])
    try:
        candidates = json.loads(p.stdout)
        if not isinstance(candidates, list):
            raise ValueError("gh output is not a pull-request list")
        if len(candidates) == candidate_limit:
            return (None, f"more than {candidate_limit - 1} merged PRs target "
                    f"{base_name}; refusing a possibly truncated sweep")
        candidates.sort(key=lambda d: d["mergedAt"], reverse=True)
        rows = []
        for d in candidates[:limit]:
            ref_error = (None if d["isCrossRepository"] else
                         post_merge_ref_event_error(d["number"], d["mergedAt"]))
            rows.append((d["number"], d["headRefName"], d["headRefOid"],
                         d["isCrossRepository"], ref_error))
        return (rows, None)
    except (ValueError, KeyError, TypeError) as exc:
        return (None, f"could not parse gh output: {exc}")


def continuous_merged_pr_tip(head_oid: str, live_ref: str) -> str | None:
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


KNOWN_FLAGS = {"--selftest", "--base", "--merged-prs", "--no-fetch"}


def _run_selftest():
    """Run the self-test, which lives in two modules beside this one.

    It is handed THIS module rather than importing it: the cases patch the
    namespace ``main()`` and ``contained()`` resolve their helpers from, which
    is this module's own, and importing by name would build a second copy of
    it whose globals no patch here would reach.
    """
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    from merge_containment_selftest import selftest
    return selftest(sys.modules[__name__])


def _option_error(args):
    """The refusal text for a malformed option list, or None."""
    #! Reject unknown options rather than silently treating them as branches.
    #! `--bse 43a4c417 origin/foo` used to check TWO branches called
    #! "43a4c417" and "origin/foo" against the default base -- both contained,
    #! rc 0 -- where the same command spelled correctly reported 4 stranded.
    for a in args:
        if a.startswith("-") and a not in KNOWN_FLAGS:
            return f"unknown option: {a}\n{USAGE}\n"

    for flag in ("--selftest", "--base", "--merged-prs", "--no-fetch"):
        if args.count(flag) > 1:
            return f"{flag} may be specified only once\n{USAGE}\n"
    return None


def _take_base(args):
    """Consume `--base <ref>` out of `args`: (base, None) or (None, refusal)."""
    if "--base" not in args:
        return (DEFAULT_BASE, None)
    i = args.index("--base")
    if i + 1 >= len(args) or args[i + 1].startswith("-"):
        #! `--base --no-fetch origin/x` used to set base to "--no-fetch"
        #! AND consume the flag, so the fetch ran despite being asked not
        #! to, and the run failed for the wrong reason
        return (None, f"--base needs a ref\n{USAGE}\n")
    base = args[i + 1]
    del args[i:i + 2]
    return (base, None)


def _revision_expression_error(args, base):
    """Refuse a revision expression wherever an exact ref is required."""
    if not exact_ref_syntax(base):
        return (f"base must be an exact ref name or full object ID, not a "
                f"revision expression: {base}\n")
    if "--merged-prs" not in args:
        for ref in (a for a in args if not a.startswith("-")):
            if not exact_ref_syntax(ref):
                return (f"branch must be an exact ref name or full object ID, "
                        f"not a revision expression: {ref}\n")
    return None


def _offline_refs(args, base):
    """Pin every operand to the local namespace: (base, args, error)."""
    base, ref_error = offline_ref(base)
    if ref_error:
        return (None, None, ref_error + "\n")
    if "--merged-prs" in args:
        return (base, args, None)
    normalized = []
    for arg in args:
        if arg.startswith("-"):
            normalized.append(arg)
            continue
        ref, ref_error = offline_ref(arg)
        if ref_error:
            return (None, None, ref_error + "\n")
        normalized.append(ref)
    return (base, normalized, None)


def _fetch_origin(args, base, shallow):
    """Refresh origin, returning the refreshed base or (None, refusal)."""
    refs_to_refresh = [base]
    if "--merged-prs" not in args:
        refs_to_refresh.extend(a for a in args if not a.startswith("-"))
    for ref in refs_to_refresh:
        stale_remote = non_origin_remote_ref(ref)
        if stale_remote:
            return (None,
                    f"cannot refresh {stale_remote}: normal mode fetches "
                    f"origin only. Use an origin ref, or use --no-fetch only "
                    f"when that other remote-tracking ref is known current.\n")
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
        return (None,
                "could not fetch origin. Re-run with --no-fetch only if you "
                "are certain the refs are current: a stale ref reports "
                "'contained' for stranded work.\n")
    return (refreshed_origin_ref(base), None)


def _merged_pr_targets(args, base):
    """The live tips of the merged PRs to assess: (targets, None) or refusal."""
    i = args.index("--merged-prs")
    limit = 20
    if i + 1 < len(args) and args[i + 1].isdigit():
        limit = int(args[i + 1])
        del args[i + 1]
    del args[i]
    if args:
        return (None,
                f"--merged-prs does not accept branch operands\n{USAGE}\n")
    prs, err = merged_pr_heads(limit, base)
    if err:
        return (None, err + "\n")
    if not prs:
        return (None,
                f"no merged PRs found targeting {base}. That is not a pass -- "
                f"check the base name.\n")
    #! headRefOid is frozen at merge time and cannot reveal later pushes,
    #! but it proves that a current same-name ref is still the same branch.
    #! A fork, force-push, deletion or branch-name reuse becomes UNKNOWN
    #! instead of certifying an unrelated origin ref.
    targets = []
    for (number, branch, head_oid, cross_repository,
         ref_event_error) in prs:
        label = f"#{number} {branch}"
        live_ref = f"refs/remotes/origin/{branch}"
        if cross_repository:
            pre_error = ("the merged head belongs to another repository; "
                         "origin cannot refresh or identify its live tip")
        elif ref_event_error:
            pre_error = ref_event_error
        else:
            pre_error = continuous_merged_pr_tip(head_oid, live_ref)
        targets.append((label, live_ref, pre_error))
    return (targets, None)


def _branch_targets(args, do_fetch):
    """The tips named by the branch operands: (targets, None) or refusal."""
    branches = [a for a in args if not a.startswith("-")]
    if not branches:
        rc, cur = _git("rev-parse", "--abbrev-ref", "HEAD")
        if rc != 0 or not cur or cur == "HEAD":
            return (None, USAGE + "\n")
        #! Git has already told us this is a branch.  Preserve that type:
        #! a legal 40-hex branch name must not become an object ID merely
        #! because the no-operand route removed its refs/heads/ namespace.
        branches = ["refs/heads/" + cur]
    targets = []
    for branch in branches:
        refs = (fetched_branch_refs(branch) if do_fetch
                else [(branch, None)])
        for ref, source in refs:
            label = (f"{branch} ({source})" if len(refs) > 1 else branch)
            targets.append((label, ref, None))
    return (targets, None)


def _report(targets, base):
    """Print one verdict per target and return the process exit status."""
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


def main(argv: list[str]) -> int:
    """Parse the option list, then answer for branches or for a merged-PR sweep.

    Every refusal returns RC_CANNOT_RUN and none of them is a pass: the
    three exit codes exist so a caller can tell "the work is contained" from
    "the question was never answered".
    """
    args = argv[1:]

    refusal = _option_error(args)
    if refusal:
        sys.stderr.write(refusal)
        return RC_CANNOT_RUN

    graft_error = active_graft_error()
    if graft_error:
        sys.stderr.write(graft_error + "\n")
        return RC_CANNOT_RUN

    if "--selftest" in args:
        if args != ["--selftest"]:
            sys.stderr.write(f"--selftest accepts no other arguments\n{USAGE}\n")
            return RC_CANNOT_RUN
        return _run_selftest()

    base, refusal = _take_base(args)
    if refusal:
        sys.stderr.write(refusal)
        return RC_CANNOT_RUN

    refusal = _revision_expression_error(args, base)
    if refusal:
        sys.stderr.write(refusal)
        return RC_CANNOT_RUN

    do_fetch = "--no-fetch" not in args
    args = [a for a in args if a != "--no-fetch"]
    if not do_fetch:
        base, args, refusal = _offline_refs(args, base)
        if refusal:
            sys.stderr.write(refusal)
            return RC_CANNOT_RUN

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
        base, refusal = _fetch_origin(args, base, shallow)
        if refusal:
            sys.stderr.write(refusal)
            return RC_CANNOT_RUN

    if "--merged-prs" in args:
        targets, refusal = _merged_pr_targets(args, base)
    else:
        targets, refusal = _branch_targets(args, do_fetch)
    if refusal:
        sys.stderr.write(refusal)
        return RC_CANNOT_RUN

    return _report(targets, base)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
