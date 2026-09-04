#!/usr/bin/env python3
"""The self-test for ``check_merge_containment.py``: ref identity and remotes.

The cases here call the shipped ``contained()`` and ``main()`` FOR REAL against
controlled Git histories.  An earlier cut had a table that re-implemented the
predicate and never called it, so mutating the shipped code -- swapping the two
signals, hard-coding the count -- left every case printing ok.  The advertised
number had no coverage at all, which is the "test that cannot fail" this repo's
own review rounds keep finding.

``selftest(module)`` takes the module under test rather than importing it, for
two reasons.  The cases patch the very namespace ``main()`` and ``contained()``
resolve their helpers from -- the same reach the in-file ``globals()[...]``
assignments had while this lived in one file -- and neither file has to import
the other, so the entry point stays a script.  The content-equivalence half of
the suite is in ``merge_containment_selftest_content.py``.
"""

import contextlib
import io
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType


def _write(path, text, mode="w"):
    """Write ``text`` to ``path`` through a managed handle."""
    with open(path, mode) as handle:
        handle.write(text)


class _Fixture:
    """What a case needs: the module under test, the reporters, the repos."""

    def __init__(self, mc, case, run):
        self.mc = mc
        self.case = case
        self.run = run
        self.td = None            # the primary fixture repository
        self.remote = None        # its bare origin, while that block is open
        self.base_oid = None      # the object ID of its `base` branch


def selftest(module: ModuleType) -> int:
    """Run every case against `module`; 0 when they all pass, 1 otherwise."""
    bad = 0

    def case(name: str, got: object, want: object, why: str) -> None:
        """Report one comparison and, when it disagrees, count it against
        the suite's exit code - this is the only place a case fails."""
        nonlocal bad
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<26} {why}")
        if not ok:
            bad += 1
            print(f"       got {got!r}, expected {want!r}")

    # --- END TO END, through main() -----------------------------------------
    # Calling contained() directly leaves the whole verdict-aggregation path
    # uncovered: the exit code could be pinned to 0, STRANDED could be printed
    # and not counted, the advertised number could be printed as a literal 0,
    # and UNKNOWN could be made a pass -- SEVEN mutations, all silent.  `run`
    # drives the real tool and captures both the exit code and what it printed.
    def run(argv: Sequence[str]) -> tuple[int, str]:
        """Drive the shipped main() for real: its exit code, and everything
        it printed, so a verdict that is announced but not counted cannot
        pass for a verdict that is."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = module.main([sys.argv[0], *argv])
        return rc, buf.getvalue()

    fx = _Fixture(module, case, run)
    if not _direct_predicate_cases(fx):
        return 1

    #! Imported here, not at the top: the content half imports `_write` back
    #! out of this module, and no case ever runs outside this call.
    from merge_containment_selftest_content import content_cases

    with tempfile.TemporaryDirectory() as td:
        cwd = os.getcwd()
        fx.td = td
        try:
            os.chdir(td)
            _linear_history_cases(fx)
            _cli_option_cases(fx)
            _git_minimum_cases(fx)

            # Fetch updates origin/work but not the checked-out local work
            # branch.  The default path must assess the fetched tip, or the
            # exact incident this command guards becomes a quiet rc 0.
            _rc, fx.base_oid = module._git("rev-parse", "base")
            with tempfile.TemporaryDirectory() as remote:
                fx.remote = remote
                _fetched_tip_cases(fx)
                _deleted_ref_cases(fx)
                _remote_provenance_cases(fx)
                _merged_pr_identity_cases(fx)
                _merged_pr_timeline_cases(fx)
                _merged_pr_continuity_cases(fx)
                _unpushed_local_cases(fx)
                _deleted_origin_cases(fx)
            fx.remote = None
            content_cases(fx)
        finally:
            os.chdir(cwd)

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


def _direct_predicate_cases(fx):
    """Call contained() directly; False when the repository is unusable."""
    mc = fx.mc
    case = fx.case
    contained = mc.contained
    DEFAULT_BASE = mc.DEFAULT_BASE

    def _git(*args):
        return mc._git(*args)

    case("default-development-base", DEFAULT_BASE, "origin/dev",
         "the retired development branch name cannot return silently")

    rc, head = _git("rev-parse", "HEAD")
    if rc != 0:
        print("  FAIL selftest needs a repository with one commit")
        return False

    ok, ahead, note = contained(head, head)
    case("self-containment", (ok, ahead), (True, 0),
         "a commit is contained in itself")

    saved_git = mc._git
    mc._git = lambda *args: (
        (128, "") if args[:2] == ("merge-base", "--is-ancestor")
        else saved_git(*args))
    try:
        ok, ahead, note = contained(head, head)
        case("ancestor-plumbing-error", (ok, ahead), (None, None),
             "a failed ancestry command is UNKNOWN, never not-ancestor")
    finally:
        mc._git = saved_git

    ok, ahead, note = contained("refs/heads/definitely-not-a-branch", head)
    case("missing-ref", (ok, ahead), (None, None),
         "a ref that cannot be resolved is UNKNOWN, never contained")

    ok, ahead, note = contained(head, "refs/heads/definitely-not-a-base")
    case("missing-base", (ok, ahead), (None, None),
         "...and so is a base that cannot be resolved")
    return True


def _linear_history_cases(fx):
    """Build the linear fixture repository and measure it end to end."""
    mc = fx.mc
    case, run = fx.case, fx.run
    contained = mc.contained
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    _git("init", "-q", "-b", "base")
    _git("config", "user.email", "s@s")
    _git("config", "user.name", "s")
    _write("f", "1")
    _git("add", "-A"); _git("commit", "-qm", "c0")
    _git("checkout", "-qb", "work")
    #! THREE commits, so a count hard-coded to 1 -- the mutation the
    #! previous round named and that still survived -- cannot pass
    for i in range(3):
        _write(f"w{i}", str(i))
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


def _cli_option_cases(fx):
    """The refusals and the defaults of the command line itself."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_OK = mc.RC_OK
    RC_FINDING = mc.RC_FINDING
    RC_CANNOT_RUN = mc.RC_CANNOT_RUN

    def _git(*args):
        return mc._git(*args)

    #! Exercise main() without --base. origin/dev contains work while
    #! the retired name stops at base, so changing the production
    #! default path back to that name makes this case fail.
    _git("update-ref", "refs/remotes/origin/dev", "work")
    _git("update-ref", "refs/remotes/origin/main-push", "base")
    rc, out = run(["--no-fetch", "work"])
    case("default-base-e2e", rc, RC_OK,
         "the implicit CLI base is origin/dev")

    rc, base_oid = _git("rev-parse", "base")
    _git("checkout", "-qb", base_oid, "work")
    rc2, out = run(["--no-fetch", "--base", "base"])
    case("implicit-hex-branch-rc", (rc, rc2), (0, RC_FINDING),
         "the checked-out hex branch keeps its refs/heads identity")
    case("implicit-hex-branch-word", "STRANDED" in out, True,
         "...rather than becoming its contained object-name twin")
    _git("checkout", "-q", "refs/heads/work")

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


def _git_minimum_cases(fx):
    """Prove an old Git is refused by name, not through scattered UNKNOWNs.

    #351: Git 2.38 and older have no ``patch-id --verbatim``; the fallback
    then failed eight arms with "could not measure" and never said why.
    """
    real_git = shutil.which("git")
    #! Outside the fixture repository: an untracked directory inside it would
    #! ride along with a later `add -A` and change what the content cases see.
    with tempfile.TemporaryDirectory() as shim_home:
        _git_minimum_shim_cases(fx, Path(shim_home) / "git", real_git)


def _write_git_shim(shim, real_git, status):
    """A ``git`` that rejects ``--verbatim`` with ``status``, else passes through."""
    _write(shim, "#!/bin/sh\n"
                 "for a in \"$@\"; do\n"
                 "  if [ \"$a\" = --verbatim ]; then\n"
                 "    echo 'usage: git patch-id [--stable | --unstable]' >&2\n"
                 f"    exit {status}\n"
                 "  fi\n"
                 "done\n"
                 f"exec {shlex.quote(real_git)} \"$@\"\n")
    shim.chmod(0o755)


def _git_minimum_shim_cases(fx, shim, real_git):
    """The cases themselves, against a ``git`` shim rejecting ``--verbatim``."""
    mc = fx.mc
    case, run = fx.case, fx.run
    #! Resolved leniently so the parent, which has no probe, prints FAIL for
    #! these arms and still runs the rest of the suite.
    probe = getattr(mc, "verbatim_patch_id_error", None)
    minimum = getattr(mc, "MINIMUM_GIT", "")

    def refusal():
        return probe() if probe else "no probe"

    def named(message):
        return bool(minimum) and minimum in message and "unavailable" in message

    case("git-minimum-current", refusal(), None,
         "the Git running this self-test has patch-id --verbatim")
    old_path = os.environ.get("PATH")
    searched = os.defpath if old_path is None else old_path
    os.environ["PATH"] = f"{shim.parent}{os.pathsep}{searched}"
    real_selftest = mc._run_selftest
    try:
        _write_git_shim(shim, real_git, 129)
        message = refusal() or ""
        case("git-minimum-named", named(message), True,
             "a Git without --verbatim is refused naming the minimum")
        case("git-minimum-version", "git version" in message, True,
             "...and the version actually found")
        rc, out = run(["--no-fetch", "--base", "base", "work"])
        case("git-minimum-e2e-rc", rc, mc.RC_CANNOT_RUN,
             "...and main() cannot run instead of answering UNKNOWN")
        case("git-minimum-e2e-silent",
             "STRANDED" in out or "UNKNOWN" in out or "contained" in out,
             False, "...and prints no verdict at all")
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(err):
            mc.main([sys.argv[0], "--no-fetch", "--base", "base", "work"])
        case("git-minimum-e2e-stderr", named(err.getvalue()), True,
             "...and main() prints that refusal on stderr")
        #! The probe must precede the --selftest dispatch, or the field
        #! failure returns: run_all_suites.sh reaches eight scattered FAILs.
        mc._run_selftest = lambda: 99
        rc, _ = run(["--selftest"])
        case("git-minimum-selftest-rc", rc, mc.RC_CANNOT_RUN,
             "--selftest itself stops at the refusal before any arm runs")
        mc._run_selftest = real_selftest
        _write_git_shim(shim, real_git, 3)
        case("git-minimum-any-status", named(refusal() or ""), True,
             "a patch-id failing with another status is refused the same way")
    finally:
        mc._run_selftest = real_selftest
        if old_path is None:
            del os.environ["PATH"]
        else:
            os.environ["PATH"] = old_path
    rc, out = run(["--no-fetch", "--base", "base", "work"])
    case("git-minimum-restored", rc, mc.RC_FINDING,
         "the real Git measures the stranded fixture again")


def _fetched_tip_cases(fx):
    """A fetch decides the tip, and a full object ID keeps its identity."""
    mc = fx.mc
    case, run = fx.case, fx.run
    remote, base_oid = fx.remote, fx.base_oid
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

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

    # A full object ID is immutable evidence, not a branch name.
    # Git permits a branch whose name is the same 40 hex digits;
    # neither the branch nor base operand may be substituted with
    # that ref after fetch.
    rc, stranded_oid = _git(
        "rev-parse", "refs/remotes/origin/work")
    _git("--git-dir", remote, "update-ref",
         f"refs/heads/{stranded_oid}", base_oid)
    _git("--git-dir", remote, "update-ref",
         f"refs/heads/{base_oid}", stranded_oid)
    rc2, out = run(["--base", "base", stranded_oid])
    case("full-oid-branch-rc", (rc, rc2), (0, RC_FINDING),
         "a hex-named origin branch cannot replace an object ID")
    case("full-oid-branch-word", "STRANDED" in out, True,
         "...and the immutable stranded object is measured")
    rc, out = run(["--base", base_oid, "work"])
    case("full-oid-base-rc", rc, RC_FINDING,
         "a hex-named origin branch cannot replace the base OID")
    case("full-oid-base-word", "STRANDED" in out, True,
         "...and the immutable base object is measured")
    _git("update-ref", "refs/heads/" + stranded_oid, base_oid)
    _git("tag", stranded_oid, base_oid)
    rc, out = run(["--no-fetch", "--base", base_oid,
                   stranded_oid])
    case("full-oid-local-collision-branch-rc", rc, RC_FINDING,
         "local branch and tag names cannot obscure a branch OID")
    case("full-oid-local-collision-branch-word",
         "STRANDED" in out, True,
         "...and the immutable branch object remains measured")
    _git("update-ref", "refs/heads/" + base_oid, stranded_oid)
    _git("tag", base_oid, stranded_oid)
    rc, out = run(["--no-fetch", "--base", base_oid,
                   stranded_oid])
    case("full-oid-local-collision-base-rc", rc, RC_FINDING,
         "local branch and tag names cannot obscure a base OID")
    case("full-oid-local-collision-base-word",
         "STRANDED" in out, True,
         "...and the immutable base object remains measured")


def _deleted_ref_cases(fx):
    """No tag may stand in for a branch the remote no longer has."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    _git("push", "-q", "origin",
         "refs/remotes/origin/work:refs/heads/deleted-tag")
    _git("tag", "origin/deleted-tag", "base")
    _git("tag", "deleted-tag", "base")
    _git("push", "-q", "origin", "--delete", "deleted-tag")
    rc, out = run(["--base", "base", "origin/deleted-tag"])
    case("deleted-tag-remote-rc", rc, RC_FINDING,
         "a tag cannot stand in for a deleted origin branch")
    case("deleted-tag-remote-word", "UNKNOWN" in out, True,
         "...and the qualified missing branch is UNKNOWN")
    rc, out = run(["--base", "base", "deleted-tag"])
    case("deleted-tag-short-rc", rc, RC_FINDING,
         "a short tag cannot stand in for a missing branch")
    case("deleted-tag-short-word", "UNKNOWN" in out, True,
         "...and the fetched namespace remains authoritative")
    _git("tag", "offline-tag-only", "base")
    rc, out = run(["--no-fetch", "--base", "base",
                   "offline-tag-only"])
    case("offline-tag-branch-rc", rc, RC_FINDING,
         "an offline short branch cannot fall through to a tag")
    case("offline-tag-branch-word", "UNKNOWN" in out, True,
         "...and the missing local branch remains UNKNOWN")
    _git("tag", "offline-base-tag-only",
         "refs/remotes/origin/work")
    rc, out = run(["--no-fetch", "--base",
                   "offline-base-tag-only", "base"])
    case("offline-tag-base-rc", rc, RC_FINDING,
         "an offline short base cannot fall through to a tag")
    case("offline-tag-base-word", "UNKNOWN" in out, True,
         "...and the missing local base remains UNKNOWN")
    _git("push", "-q", "origin", "base:refs/heads/deleted-base")
    _git("tag", "deleted-base", "refs/remotes/origin/work")
    _git("push", "-q", "origin", "--delete", "deleted-base")
    rc, out = run(["--base", "deleted-base", "origin/work"])
    case("deleted-tag-base-rc", rc, RC_FINDING,
         "a tag cannot stand in for a deleted base branch")
    case("deleted-tag-base-word", "UNKNOWN" in out, True,
         "...and the missing fetched base is UNKNOWN")
    _git("branch", "stale-base", "refs/remotes/origin/work")
    rc, out = run(["--base", "refs/heads/stale-base",
                   "origin/work"])
    case("deleted-explicit-base-rc", rc, RC_FINDING,
         "a stale explicit local base cannot replace origin")
    case("deleted-explicit-base-word", "UNKNOWN" in out, True,
         "...and normal mode keeps the missing origin base")


def _remote_provenance_cases(fx):
    """A non-origin remote shorthand keeps the identity it was typed with."""
    mc = fx.mc
    case, run = fx.case, fx.run
    remote = fx.remote
    RC_FINDING = mc.RC_FINDING
    RC_CANNOT_RUN = mc.RC_CANNOT_RUN

    def _git(*args):
        return mc._git(*args)

    _git("remote", "add", "upstream", remote)
    _git("update-ref", "refs/remotes/upstream/work",
         "refs/remotes/origin/work")
    _git("branch", "upstream/work", "base")
    rc, out = run(["--base", "base", "upstream/work"])
    case("ambiguous-remote-normal-rc", rc, RC_CANNOT_RUN,
         "an ambiguous non-origin remote shorthand is refused")
    rc, out = run(["--no-fetch", "--base", "base",
                   "upstream/work"])
    case("ambiguous-remote-offline-rc", rc, RC_FINDING,
         "...and offline mode keeps the remote shorthand typed")
    case("ambiguous-remote-offline-word", "STRANDED" in out, True,
         "...so a same-spelled local branch cannot replace it")
    _git("update-ref", "-d", "refs/remotes/upstream/work")
    _git("--git-dir", remote, "update-ref",
         "refs/heads/upstream/work", "refs/heads/base")
    rc, out = run(["--base", "base", "upstream/work"])
    case("missing-remote-tracking-rc", rc, RC_CANNOT_RUN,
         "a configured remote shorthand stays non-origin even "
         "when its tracking ref is missing")
    rc, out = run(["--no-fetch", "--base", "base",
                   "upstream/work"])
    case("missing-remote-offline-rc", rc, RC_FINDING,
         "offline remote shorthand keeps its missing identity")
    case("missing-remote-offline-word", "UNKNOWN" in out, True,
         "...instead of falling back to a slash-named branch")
    rc, out = run(["--base", "upstream/work", "base"])
    case("missing-remote-base-rc", rc, RC_CANNOT_RUN,
         "a missing configured remote base is refused before fetch")
    rc, out = run(["--no-fetch", "--base", "upstream/work",
                   "base"])
    case("missing-remote-base-offline-rc", rc, RC_FINDING,
         "offline mode keeps a missing remote base typed")
    case("missing-remote-base-offline-word", "UNKNOWN" in out,
         True, "...rather than using a slash-named local base")

    _git("remote", "add", "corp/upstream", remote)
    _git("update-ref", "refs/remotes/corp/upstream/work",
         "refs/remotes/origin/work")
    _git("branch", "corp/upstream/work", "base")
    _git("update-ref", "-d",
         "refs/remotes/corp/upstream/work")
    _git("--git-dir", remote, "update-ref",
         "refs/heads/corp/upstream/work", "refs/heads/base")
    rc, out = run(["--base", "base", "corp/upstream/work"])
    case("slash-remote-normal-rc", rc, RC_CANNOT_RUN,
         "a slash-bearing configured remote stays non-origin")
    rc, out = run(["--no-fetch", "--base", "base",
                   "corp/upstream/work"])
    case("slash-remote-offline-rc", rc, RC_FINDING,
         "offline slash-bearing remote shorthand stays typed")
    case("slash-remote-offline-word", "UNKNOWN" in out, True,
         "...instead of using a same-spelled local branch")
    rc, out = run(["--base", "corp/upstream/work", "base"])
    case("slash-remote-base-rc", rc, RC_CANNOT_RUN,
         "a slash-bearing remote base is refused before fetch")
    rc, out = run(["--no-fetch", "--base",
                   "corp/upstream/work", "base"])
    case("slash-remote-base-offline-rc", rc, RC_FINDING,
         "offline slash-bearing remote base stays typed")
    case("slash-remote-base-offline-word", "UNKNOWN" in out, True,
         "...instead of using a same-spelled local base")
    # git remote add rejects overlapping names, but a repository
    # config can still contain them.  Such a ref has no unique
    # remote provenance and must be refused.
    _git("config", "remote.corp.url", remote)
    _git("config", "remote.corp.fetch",
         "+refs/heads/*:refs/remotes/corp/*")
    rc, out = run(["--no-fetch", "--base", "base",
                   "corp/upstream/work"])
    case("overlapping-remote-prefix-rc", rc, RC_CANNOT_RUN,
         "overlapping configured remote prefixes are ambiguous")
    _git("config", "remote.origin/team.url", remote)
    _git("config", "remote.origin/team.fetch",
         "+refs/heads/*:refs/remotes/origin/team/*")
    rc, out = run(["--base", "refs/remotes/origin/base",
                   "refs/remotes/origin/work"])
    case("explicit-origin-overlap-rc", rc, RC_FINDING,
         "an explicit origin ref stays refreshable despite a "
         "configured prefix collision")
    case("explicit-origin-overlap-word", "STRANDED" in out, True,
         "...and the fetched origin branch is measured")


def _merged_pr_identity_cases(fx):
    """The merged sweep assesses the live tip, not the frozen head OID."""
    mc = fx.mc
    case, run = fx.case, fx.run
    base_oid = fx.base_oid
    continuous_merged_pr_tip = mc.continuous_merged_pr_tip
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # A merged PR's head OID is frozen at merge time.  The live
    # branch tip is the only ref that can expose later pushes.
    saved_merged_pr_heads = mc.merged_pr_heads
    mc.merged_pr_heads = lambda _limit, _base: (
        [(86, "work", base_oid, False, None)], None)
    try:
        rc, out = run(["--no-fetch", "--base", "base",
                       "--merged-prs", "1"])
        case("merged-live-tip-rc", rc, RC_FINDING,
             "the merged sweep ignores the frozen head OID")
        case("merged-live-tip-word", "STRANDED" in out, True,
             "...and assesses origin/work instead")
    finally:
        mc.merged_pr_heads = saved_merged_pr_heads

    _git("update-ref", "refs/remotes/origin/recreated-exact",
         base_oid)
    continuity = continuous_merged_pr_tip(
        base_oid, "refs/remotes/origin/recreated-exact")
    mc.merged_pr_heads = lambda _limit, _base: (
        [(92, "recreated-exact", base_oid, False,
          "GitHub records head_ref_deleted after merge")], None)
    try:
        rc, out = run(["--no-fetch", "--base", "base",
                       "--merged-prs", "1"])
        case("merged-recreated-lineage", continuity, None,
             "lineage alone cannot see exact-head recreation")
        case("merged-recreated-event", rc, RC_FINDING,
             "a durable deletion event prevents false success")
        case("merged-recreated-word", "UNKNOWN" in out, True,
             "...and the lost ref identity is UNKNOWN")
    finally:
        mc.merged_pr_heads = saved_merged_pr_heads


def _merged_pr_timeline_cases(fx):
    """The GitHub timeline and candidate-list parsers, over faked replies."""
    mc = fx.mc
    case = fx.case
    post_merge_ref_event_error = mc.post_merge_ref_event_error

    def merged_pr_heads(*args) -> tuple:
        """Resolve the shipped helper at call time, as the module itself does."""
        return mc.merged_pr_heads(*args)

    saved_subprocess_run = subprocess.run

    class TimelineResult:
        returncode = 0
        stderr = ""
        stdout = ('[[{"event":"head_ref_deleted",'
                  '"created_at":"2026-08-17T12:00:00Z"}]]')

    subprocess.run = lambda *a, **k: TimelineResult()
    try:
        timeline_error = post_merge_ref_event_error(
            92, "2026-08-17T11:00:00Z")
        case("timeline-delete-parser",
             "head_ref_deleted" in (timeline_error or ""), True,
             "the GitHub timeline parser preserves deletion proof")
    finally:
        subprocess.run = saved_subprocess_run

    class MergedListResult:
        returncode = 0
        stderr = ""

        def __init__(self, stdout):
            self.stdout = stdout

    merged_list_calls = []
    unsorted_prs = (
        '[{"number":1,"headRefName":"one",'
        '"headRefOid":"1111111111111111111111111111111111111111",'
        '"isCrossRepository":true,'
        '"mergedAt":"2026-01-01T00:00:00Z"},'
        '{"number":2,"headRefName":"two",'
        '"headRefOid":"2222222222222222222222222222222222222222",'
        '"isCrossRepository":true,'
        '"mergedAt":"2026-03-01T00:00:00Z"},'
        '{"number":3,"headRefName":"three",'
        '"headRefOid":"3333333333333333333333333333333333333333",'
        '"isCrossRepository":true,'
        '"mergedAt":"2026-02-01T00:00:00Z"}]')

    def fake_merged_list(argv: Sequence[str],
                         **_kwargs: object) -> MergedListResult:
        """Stand in for subprocess.run with the deliberately out-of-order
        candidate list, and keep the argv so the case can also prove WHAT
        the sweep asked GitHub for."""
        merged_list_calls.append(argv)
        return MergedListResult(unsorted_prs)

    subprocess.run = fake_merged_list
    try:
        ordered_prs, list_error = merged_pr_heads(2, "base")
        case("merged-list-order",
             (list_error, [row[0] for row in ordered_prs]),
             (None, [2, 3]),
             "the sweep selects PRs by merge time")
        call = merged_list_calls[0]
        case("merged-list-complete-query",
             ("--search" not in call,
              call[call.index("--limit") + 1]),
             (True, "1001"),
             "...after requesting a bounded complete candidate set")

        one_candidate = (
            '{"number":1,"headRefName":"one",'
            '"headRefOid":'
            '"1111111111111111111111111111111111111111",'
            '"isCrossRepository":true,'
            '"mergedAt":"2026-01-01T00:00:00Z"}')
        repeated = ",".join(
            one_candidate for _index in range(1001))
        subprocess.run = lambda *a, **k: MergedListResult(
            "[" + repeated + "]")
        truncated_prs, truncated_error = merged_pr_heads(2, "base")
        case("merged-list-truncation",
             (truncated_prs,
              "truncated" in (truncated_error or "")),
             (None, True),
             "...and possible candidate truncation is not a pass")
    finally:
        subprocess.run = saved_subprocess_run


def _merged_pr_continuity_cases(fx):
    """A fork or a recreated same-name branch becomes UNKNOWN."""
    mc = fx.mc
    case, run = fx.case, fx.run
    base_oid = fx.base_oid
    RC_FINDING = mc.RC_FINDING
    #! Re-taken here rather than passed in: the identity cases above
    #! have already restored it, so this is the shipped function.
    saved_merged_pr_heads = mc.merged_pr_heads

    def _git(*args):
        return mc._git(*args)

    mc.merged_pr_heads = lambda _limit, _base: (
        [(90, "work", base_oid, True, None)], None)
    try:
        rc, out = run(["--no-fetch", "--base", "base",
                       "--merged-prs", "1"])
        case("merged-fork-rc", rc, RC_FINDING,
             "a fork head cannot borrow origin's same-name ref")
        case("merged-fork-word", "UNKNOWN" in out, True,
             "...and the unrefreshable live tip is UNKNOWN")
    finally:
        mc.merged_pr_heads = saved_merged_pr_heads

    rc, work_tip = _git("rev-parse", "refs/remotes/origin/work")
    _git("update-ref", "refs/remotes/origin/reused", base_oid)
    mc.merged_pr_heads = lambda _limit, _base: (
        [(91, "reused", work_tip, False, None)], None)
    try:
        rc2, out = run(["--no-fetch", "--base", "base",
                        "--merged-prs", "1"])
        case("merged-reused-rc", (rc, rc2),
             (0, RC_FINDING),
             "a recreated same-name branch cannot false-pass")
        case("merged-reused-word", "UNKNOWN" in out, True,
             "...and failed continuity is UNKNOWN")
    finally:
        mc.merged_pr_heads = saved_merged_pr_heads


def _unpushed_local_cases(fx):
    """A fetched remote cannot hide an unpushed local commit."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_FINDING = mc.RC_FINDING
    RC_CANNOT_RUN = mc.RC_CANNOT_RUN

    def _git(*args):
        return mc._git(*args)

    # The opposite divergence matters too: a local commit that is
    # not pushed must not disappear merely because origin is
    # refreshed and already contained.
    _git("checkout", "-qb", "local-ahead", "base")
    _git("push", "-q", "origin", "local-ahead")
    _write("local-only", "not pushed")
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


def _deleted_origin_cases(fx):
    """A pruned origin branch and a shallow clone are both UNKNOWN."""
    mc = fx.mc
    case, run = fx.case, fx.run
    td, remote = fx.td, fx.remote
    RC_FINDING = mc.RC_FINDING
    RC_CANNOT_RUN = mc.RC_CANNOT_RUN

    def _git(*args):
        return mc._git(*args)

    # After fetch --prune removes a deleted origin branch, a stale
    # local tip must not stand in for work that may have existed on
    # the remote.  Reproduce the incident shape in a separate repo:
    # H was merged, S was pushed later, then origin/feature vanished
    # while the checker's local feature remained at H.
    with tempfile.TemporaryDirectory() as deleted_parent:
        #! str, not Path: all three go straight into git's argv.
        parent = Path(deleted_parent)
        checker = str(parent / "checker")
        deleted_remote = str(parent / "remote.git")
        writer = str(parent / "writer")
        os.mkdir(checker)
        os.chdir(checker)
        _git("init", "-q", "-b", "base")
        _git("config", "user.email", "s@s")
        _git("config", "user.name", "s")
        _write("seed", "seed")
        _git("add", "seed"); _git("commit", "-qm", "seed")
        _git("checkout", "-qb", "feature")
        _write("merged", "H")
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
        _write("stranded", "S")
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
        #! str, for the same reason: `git clone` is handed this word.
        shallow_repo = str(Path(shallow_parent) / "repo")
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
