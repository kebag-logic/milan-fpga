#!/usr/bin/env python3
"""The containment self-test's throwaway repositories: kept quiet, then removed.

Both halves of the self-test build Git histories in temporary directories and
remove them on the way out.  A hosted run failed on that removal (#438): every
arm had printed ok, then ``shutil.rmtree`` raised ``Directory not empty:
'pack'`` on a fixture's ``.git/objects/pack``, and the sweep printed the abort
meant for a checker whose verdicts are wrong.

The writer was Git's own housekeeping, which a command that writes to a
repository starts on its way out - here a commit, a merge or a fetch, and
``receive-pack`` after a push.  On Git 2.55, the version the hosted runner
carries, that is ``git maintenance run --auto --detach``: it returns at once
and works on in the background, its default geometric-repack task fires as
soon as two loose objects share ``objects/17``, and a traced self-test run
caught it writing ``.git/objects/pack`` after the ``git commit`` that started
it had returned.  One run of the self-test started seventy of them.  Git 2.43
starts ``git maintenance run --auto``, or ``git gc --auto`` from
``receive-pack``, and its ``gc --auto`` detaches by default.

So everything the self-test does with a temporary tree goes through here:

* ``quiet_git()`` hands ``QUIET_GIT`` to every Git the self-test starts, and
  ``init_quiet_bare()`` writes the one setting a push's ``receive-pack`` reads
  into the remote's own config, because Git starts that process without the
  environment's configuration;
* ``scratch()`` is the temporary directory, with a failed removal recorded
  instead of raised;
* ``verdict()`` turns the failure count and those records into the exit code.
  A failed arm is 1, as it always was.  A tree left behind after every arm
  passed is housekeeping, reported by path under its own exit code, and never
  called a verdict that cannot be trusted.

``scratch_cases()`` holds the arms that prove each of them.
"""

import contextlib
import errno
import io
import os
import re
import shutil
import tempfile
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from types import ModuleType

#: Every Git the self-test starts inherits these through ``GIT_CONFIG_*``.
#: Under default configuration each one alone stopped the cleanup race on Git
#: 2.43 and on 2.55; together they hold against a developer's own maintenance
#: and gc settings, because the environment outranks every configuration file.
#:
#: ``maintenance.auto=false``: no ``git maintenance run --auto`` is started
#: after a commit, merge or fetch; both versions check it before anything
#: else, and on 2.55 it is what stops the detached geometric repack.
#: ``gc.auto=0``: ``git gc --auto`` and the gc maintenance task find nothing to
#: do, and 2.55 also reads it as "no auto maintenance" when
#: ``maintenance.auto`` is unset.
#: ``gc.autoDetach=false``: whatever still runs finishes before the command
#: that started it returns; 2.43's ``gc --auto`` stays in the foreground, and
#: 2.55 falls back to it when ``maintenance.autoDetach`` is unset.
QUIET_GIT = (("maintenance.auto", "false"),
             ("gc.auto", "0"),
             ("gc.autoDetach", "false"))

#: A trace line recording that Git started maintenance or gc.
HOUSEKEEPING_RE = re.compile(r"run_command: .*\bgit (maintenance|gc)\b")


@contextlib.contextmanager
def quiet_git() -> Iterator[None]:
    """Hand ``QUIET_GIT`` to every Git started inside, then restore.

    The entries go after any ``GIT_CONFIG_COUNT`` the caller already passes,
    so that configuration still applies, and for these single-valued keys a
    later entry wins.
    """
    first = int(os.environ.get("GIT_CONFIG_COUNT") or 0)
    added = {"GIT_CONFIG_COUNT": str(first + len(QUIET_GIT))}
    for index, (key, value) in enumerate(QUIET_GIT, start=first):
        added[f"GIT_CONFIG_KEY_{index}"] = key
        added[f"GIT_CONFIG_VALUE_{index}"] = value
    saved = {name: os.environ.get(name) for name in added}
    os.environ.update(added)
    try:
        yield
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def init_quiet_bare(git: Callable[..., tuple[int, str]], path: str) -> None:
    """``git init --bare`` a remote whose ``receive-pack`` starts no housekeeping.

    Git runs ``receive-pack`` for a push to a local path with
    ``GIT_CONFIG_COUNT`` and ``GIT_CONFIG_PARAMETERS`` unset, like every
    repository-local variable on the far side of a transport, so
    ``QUIET_GIT`` never reaches it.  After a push ``receive-pack`` starts
    ``git gc --auto`` (2.43) or ``git maintenance run --auto --detach``
    (2.55) unless ``receive.autoGc`` is false in the remote's own config.
    """
    git("init", "--bare", "-q", path)
    git("--git-dir", path, "config", "receive.autoGc", "false")


@contextlib.contextmanager
def scratch(leftovers: list[str],
            remove: Callable[[str], None] = shutil.rmtree) -> Iterator[str]:
    """A temporary directory whose failed removal is recorded, not raised.

    ``tempfile.TemporaryDirectory`` raises from its exit, and that exception
    replaced the verdict of a self-test whose every arm had passed (#438).
    Only the removal is caught, and only an ``OSError``: an exception from the
    body still propagates.
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        try:
            remove(path)
        except OSError as exc:
            leftovers.append(f"{path}: {exc}")


def verdict(failures: int, leftovers: Sequence[str],
            rc_cleanup_failed: int) -> int:
    """Print the suite's last word and return the exit code it stands for.

    A failed arm is 1 whatever else happened: it is the result the sweep must
    abort on.  A tree left behind after every arm passed gets its own code
    and its own words, because nothing any arm measured is in doubt.
    """
    for leftover in leftovers:
        print(f"  CLEANUP  could not remove {leftover}")
    if failures:
        print(f"selftest: {failures} FAILURE(S)")
        return 1
    if leftovers:
        print(f"selftest: PASS, but {len(leftovers)} temporary tree(s) could "
              f"not be removed: housekeeping, and every arm passed")
        return rc_cleanup_failed
    print("selftest: PASS")
    return 0


def scratch_cases(mc: ModuleType, case: Callable[[str, object, object, str], None],
                  leftovers: list[str]) -> None:
    """Prove the three pieces above before any fixture relies on them."""
    _quiet_git_cases(mc, case, leftovers)
    _cleanup_verdict_cases(case, mc.RC_CLEANUP_FAILED)


def _quiet_git_cases(mc, case, leftovers):
    """A commit, a push and a fetch start no housekeeping on either side."""
    def _git(*args):
        return mc._git(*args)

    with scratch(leftovers) as home:
        repo, bare = str(Path(home) / "repo"), str(Path(home) / "bare.git")
        trace = Path(home) / "trace"
        init_quiet_bare(_git, bare)
        _git("init", "-q", "-b", "base", repo)
        _git("-C", repo, "config", "user.email", "s@s")
        _git("-C", repo, "config", "user.name", "s")
        _git("-C", repo, "remote", "add", "origin", bare)
        saved_trace = os.environ.get("GIT_TRACE")
        #! GIT_TRACE is not one of the variables Git removes for another
        #! repository, so the push's receive-pack writes here too.
        os.environ["GIT_TRACE"] = str(trace)
        try:
            _git("-C", repo, "commit", "-q", "--allow-empty", "-m", "quiet")
            _git("-C", repo, "push", "-q", "origin", "base")
            _git("-C", repo, "fetch", "-q", "origin")
        finally:
            if saved_trace is None:
                os.environ.pop("GIT_TRACE", None)
            else:
                os.environ["GIT_TRACE"] = saved_trace
        lines = (trace.read_text(errors="replace").splitlines()
                 if trace.exists() else [])

    traced = ["commit", "receive-pack", "fetch"]
    case("quiet-git-traced",
         [name for name in traced
          if any(f"built-in: git {name}" in line for line in lines)],
         traced, "the trace saw the commit, the push's receive-pack, the fetch")
    case("quiet-git-no-housekeeping",
         [line for line in lines if HOUSEKEEPING_RE.search(line)], [],
         "...and none of them started maintenance or gc (#438)")


def _cleanup_verdict_cases(case, rc_cleanup_failed):
    """A leftover tree is reported as one, and never outranks a failed arm."""
    planted = []

    def refilled(path: str) -> None:
        """Fail the way the hosted run did, leaving the tree behind."""
        raise OSError(errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY), "pack")

    with scratch(planted, remove=refilled) as kept:
        pass
    shutil.rmtree(kept)
    case("cleanup-recorded", [entry.startswith(kept) for entry in planted],
         [True], "a failed removal is recorded with its path, not raised")

    raised = None
    try:
        with scratch(planted, remove=refilled) as kept:
            raise LookupError("planted arm failure")
    except LookupError as exc:
        raised = str(exc)
    shutil.rmtree(kept)
    case("cleanup-keeps-arm-error", (raised, len(planted)),
         ("planted arm failure", 2),
         "...and an arm's own exception still propagates past it")

    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = verdict(0, planted, rc_cleanup_failed)
    words = out.getvalue()
    case("cleanup-verdict-rc", rc, rc_cleanup_failed,
         "every arm passed, a tree was left: the cleanup exit code")
    case("cleanup-verdict-words",
         ("could not be removed" in words, "FAILURE" in words,
          "trusted" in words), (True, False, False),
         "...worded as housekeeping, never as a failed or untrusted check")
    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = verdict(1, planted, rc_cleanup_failed)
    case("cleanup-under-failure",
         (rc, "selftest: 1 FAILURE(S)" in out.getvalue()), (1, True),
         "a failed arm is still exit 1, the status the sweep aborts on")
