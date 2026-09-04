#!/usr/bin/env python3
"""The self-test for ``check_merge_containment.py``: content equivalence.

The second half of ``merge_containment_selftest.py``, split off so that
neither module runs past the length a reviewer can hold.  Every case here asks
the same question: when the branch commits are NOT ancestors, did the work land
anyway?  Each one builds a history in which a cheaper comparison answers
wrongly -- a squash whose base moved on, a whitespace-only difference, the same
edit in a different repeated block, a diff configuration that hides a changed
blob -- and requires the shipped verdict to be the safe one.

``content_cases(fx)`` runs inside the other half's fixture repository, with its
working directory already at the fixture and its `_Fixture` carrying the module
under test.
"""

import os
import tempfile
from pathlib import Path

#! The fixture type and the managed-write helper are the other half's;
#! importing them keeps one definition of each. That module imports this one
#! only from inside a call, so this top-level import is not a cycle.
from merge_containment_selftest import _Fixture, _write


def content_cases(fx: _Fixture) -> None:
    """Run every content-equivalence case against the open fixture repo."""
    _ambiguous_and_graft_cases(fx)
    _squash_and_error_cases(fx)
    _rename_and_pathspec_cases(fx)
    _linear_rebase_cases(fx)
    _whitespace_cases(fx)
    _hunk_position_cases(fx)
    _hostile_diff_config_cases(fx)
    _merge_resolution_cases(fx)


def _hostile_diff_config_cases(fx):
    """Each hostile diff configuration gets a repository of its own."""
    # Diff configuration and attributes are untrusted inputs.  A textconv that
    # prints nothing can hide changed blobs from both the path proof and patch
    # fallback, while ignoreSubmodules=all can hide a missing gitlink update.
    # Each fixture uses a separate repo so its deliberately hostile
    # configuration cannot leak onward.
    with tempfile.TemporaryDirectory() as config_parent:
        _textconv_path_cases(fx, config_parent)
        _textconv_patch_cases(fx, config_parent)
        _submodule_pin_cases(fx, config_parent)
        os.chdir(fx.td)


def _ambiguous_and_graft_cases(fx):
    """A tag, a replacement ref and a legacy graft cannot rewrite ancestry."""
    mc = fx.mc
    case, run = fx.case, fx.run
    contained = mc.contained
    RC_FINDING = mc.RC_FINDING
    RC_CANNOT_RUN = mc.RC_CANNOT_RUN

    def _git(*args):
        return mc._git(*args)

    # A short branch name shared with a tag keeps its branch identity.
    # Git's normal precedence chooses the tag, which can otherwise
    # hide the stranded branch.
    _git("checkout", "-qb", "collision", "base")
    _write("collision-work", "stranded")
    _git("add", "collision-work"); _git("commit", "-qm", "collision")
    _git("tag", "collision", "base")
    rc, out = run(["--no-fetch", "--base", "base", "collision"])
    case("ambiguous-ref-rc", rc, RC_FINDING,
         "a tag and branch sharing one name cannot false-pass")
    case("ambiguous-ref-word", "STRANDED" in out, True,
         "...and the typed short name measures the branch")

    # Replacement refs rewrite ancestry for ordinary Git plumbing.
    # Make the base appear to descend from a stranded feature, then
    # prove the checker ignores that caller-local alternate history.
    _git("checkout", "-qb", "replace-feature", "base")
    _write("replace-work", "stranded")
    _git("add", "replace-work"); _git("commit", "-qm", "replace work")
    rc, replace_feature = _git("rev-parse", "HEAD")
    _git("checkout", "-qb", "replace-base", "base")
    _write("replace-unrelated", "base")
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


def _squash_and_error_cases(fx):
    """The squash and net-zero proofs, and the failures that are UNKNOWN."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_OK = mc.RC_OK
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # A multi-commit squash remains contained after unrelated work
    # advances the base, because only branch-touched paths matter.
    _git("checkout", "-qb", "squash-feature", "base")
    _write("sq0", "0")
    _git("add", "sq0"); _git("commit", "-qm", "sq0")
    _write("sq1", "1")
    _git("add", "sq1"); _git("commit", "-qm", "sq1")
    _git("checkout", "-qb", "squash-base", "base")
    _git("merge", "-q", "--squash", "squash-feature")
    _git("commit", "-qm", "squash")
    _write("unrelated", "later")
    _git("add", "unrelated"); _git("commit", "-qm", "later")
    rc, out = run(["--no-fetch", "--base", "squash-base",
                   "squash-feature"])
    case("squash-base-advanced", rc, RC_OK,
         "unrelated base work does not hide a squash merge")
    case("squash-path-equivalence",
         "every path this branch touched" in out, True,
         "...through the path-scoped content check")

    _git("checkout", "-qb", "net-zero", "base")
    _write("temporary-change", "added then removed")
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
    saved_git = mc._git
    mc._git = lambda *args: (
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
        mc._git = saved_git

    saved_git = mc._git
    mc._git = lambda *args: (
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
        mc._git = saved_git


def _rename_and_pathspec_cases(fx):
    """A copy is not a rename, and a filename is data, not a pathspec."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # A copied destination is not equivalent to a rename because the
    # source path still exists.  Rename folding must not hide it.
    _git("checkout", "-qb", "rename-feature", "base")
    _git("mv", "f", "renamed")
    _git("commit", "-qm", "rename")
    _git("checkout", "-qb", "rename-base", "base")
    _write("renamed", "1")
    _git("add", "renamed"); _git("commit", "-qm", "copy")
    rc, out = run(["--no-fetch", "--base", "rename-base",
                   "rename-feature"])
    case("rename-source-remains", rc, RC_FINDING,
         "a copied destination cannot hide a missing deletion")

    # A filename is data, not a Git pathspec.  Without literal mode an
    # exclude-shaped name removes itself from the comparison.
    magic_name = ":(exclude)magic"
    _git("checkout", "-qb", "pathspec-feature", "base")
    _write(magic_name, "stranded")
    _git("--literal-pathspecs", "add", "--", magic_name)
    _git("commit", "-qm", "pathspec")
    rc, out = run(["--no-fetch", "--base", "base",
                   "pathspec-feature"])
    case("literal-pathspec-name", rc, RC_FINDING,
         "an exclude-shaped filename remains part of the comparison")


def _linear_rebase_cases(fx):
    """A linear rebase is contained through the patch-id fallback."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_OK = mc.RC_OK

    def _git(*args):
        return mc._git(*args)

    # Verbatim patch-id equivalence is valid for a linear rebased
    # history even when the base later edits the same path.
    _git("checkout", "-qb", "linear-feature", "base")
    _write("linear", "landed\n")
    _git("add", "linear"); _git("commit", "-qm", "linear")
    rc, linear_commit = _git("rev-parse", "HEAD")
    _git("checkout", "-qb", "linear-base", "base")
    _write("advance", "first")
    _git("add", "advance"); _git("commit", "-qm", "advance")
    _git("cherry-pick", linear_commit)
    _write("linear", "superseded\n", "a")
    _git("add", "linear"); _git("commit", "-qm", "supersede")
    rc, out = run(["--no-fetch", "--base", "linear-base",
                   "linear-feature"])
    case("linear-patch-fallback", rc, RC_OK,
         "patch equivalence handles a linear rebase")
    case("linear-patch-word",
         "every commit has a whitespace-exact equivalent" in out,
         True, "...through the patch-id fallback")


def _whitespace_cases(fx):
    """Whitespace is content: git cherry's patch IDs are not proof."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # git cherry strips whitespace when it computes patch IDs.  These
    # two values are different content and must never compare equal.
    _git("checkout", "-qb", "whitespace-feature", "base")
    _write("spacing.py", 'value = "old"\n')
    _git("add", "spacing.py"); _git("commit", "-qm", "spacing seed")
    _git("checkout", "-qb", "whitespace-base", "HEAD~1")
    _write("spacing.py", 'value = "old"\n')
    _git("add", "spacing.py"); _git("commit", "-qm", "spacing seed")
    _git("checkout", "-q", "whitespace-feature")
    _write("spacing.py", 'value = "a b"\n')
    _git("commit", "-qam", "space is data")
    _git("checkout", "-q", "whitespace-base")
    _write("spacing.py", 'value = "ab"\n')
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


def _hunk_position_cases(fx):
    """The same edit in a different repeated block is not a replay."""
    mc = fx.mc
    case, run = fx.case, fx.run
    _verbatim_patch_id = mc._verbatim_patch_id
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # Verbatim patch IDs still omit hunk line numbers.  The same edit
    # to two repeated blocks therefore hashes alike, but the resulting
    # files differ and must not be certified as a replay.
    block = "a\nb\nc\nold\nd\ne\nf\n"
    separator = "".join(f"separator-{i}\n" for i in range(10))
    repeated = block + separator + block
    _git("checkout", "-qb", "hunk-feature", "base")
    _write("repeated.txt", repeated)
    _git("add", "repeated.txt"); _git("commit", "-qm", "hunk seed")
    _git("checkout", "-qb", "hunk-base", "HEAD~1")
    _write("repeated.txt", repeated)
    _git("add", "repeated.txt"); _git("commit", "-qm", "hunk seed")
    _git("checkout", "-q", "hunk-feature")
    _write("repeated.txt", repeated.replace("old", "new", 1))
    _git("commit", "-qam", "first block")
    rc, hunk_feature = _git("rev-parse", "HEAD")
    _git("checkout", "-q", "hunk-base")
    before, after = repeated.rsplit("old", 1)
    _write("repeated.txt", before + "new" + after)
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


def _textconv_path_cases(fx, config_parent):
    """A silent textconv cannot make the touched-path proof succeed."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RAW_DIFF_FLAGS = mc.RAW_DIFF_FLAGS
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    textconv_path = Path(config_parent) / "textconv-path"
    textconv_path.mkdir()
    os.chdir(textconv_path)
    _git("init", "-q", "-b", "root")
    _git("config", "user.email", "s@s")
    _git("config", "user.name", "s")
    _write("f", "root\n")
    _write(".gitattributes", "f diff=quiet\n")
    _git("add", "f", ".gitattributes")
    _git("commit", "-qm", "root")
    _git("checkout", "-qb", "feature")
    _write("f", "stranded\n")
    _git("commit", "-qam", "feature")
    _git("checkout", "-qb", "base", "root")
    _write("unrelated", "base")
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


def _textconv_patch_cases(fx, config_parent):
    """...nor the patch-id fallback, whose IDs are taken raw."""
    mc = fx.mc
    case, run = fx.case, fx.run
    _verbatim_patch_id = mc._verbatim_patch_id
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    textconv_patch = Path(config_parent) / "textconv-patch"
    textconv_patch.mkdir()
    os.chdir(textconv_patch)
    _git("init", "-q", "-b", "root")
    _git("config", "user.email", "s@s")
    _git("config", "user.name", "s")
    _write("f", "root\n")
    _write(".gitattributes", "f diff=quiet\n")
    _git("add", "f", ".gitattributes")
    _git("commit", "-qm", "root")
    _git("checkout", "-qb", "feature")
    _write("f", "stranded\n")
    _write("g", "landed\n")
    _git("add", "f", "g"); _git("commit", "-qm", "first")
    rc, branch_first = _git("rev-parse", "HEAD")
    _write("h", "landed\n")
    _git("add", "h"); _git("commit", "-qm", "second")
    _git("checkout", "-qb", "base", "root")
    _write("g", "landed\n")
    _git("add", "g"); _git("commit", "-qm", "first replay")
    rc2, base_first = _git("rev-parse", "HEAD")
    _write("h", "landed\n")
    _git("add", "h"); _git("commit", "-qm", "second replay")
    _write("h", "superseded\n")
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


def _submodule_pin_cases(fx, config_parent):
    """An ignored gitlink is still a missing change."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RAW_DIFF_FLAGS = mc.RAW_DIFF_FLAGS
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    submodule_repo = Path(config_parent) / "submodule"
    submodule_repo.mkdir()
    os.chdir(submodule_repo)
    _git("init", "-q", "-b", "root")
    _git("config", "user.email", "s@s")
    _git("config", "user.name", "s")
    _write("seed", "seed")
    _git("add", "seed"); _git("commit", "-qm", "root")
    rc, root_oid = _git("rev-parse", "HEAD")
    _git("checkout", "-qb", "feature")
    _write("landed", "landed")
    _git("add", "landed")
    _git("update-index", "--add", "--cacheinfo",
         f"160000,{root_oid},submodule-pin")
    _git("commit", "-qm", "feature")
    _git("checkout", "-qb", "base", "root")
    _write("landed", "landed")
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


def _merge_resolution_cases(fx):
    """A merge commit's unique resolution cannot vanish from the fallback."""
    mc = fx.mc
    case, run = fx.case, fx.run
    RC_FINDING = mc.RC_FINDING

    def _git(*args):
        return mc._git(*args)

    # git cherry intentionally omits merge commits.  An equivalent
    # normal commit must not hide unique merge-resolution content.
    _git("checkout", "-qb", "merge-side", "base")
    _write("side", "side")
    _git("add", "side"); _git("commit", "-qm", "side")
    _git("checkout", "-qb", "merge-feature", "base")
    _write("normal", "normal")
    _git("add", "normal"); _git("commit", "-qm", "normal")
    _git("checkout", "-qb", "merge-replayed", "merge-side")
    _write("normal", "normal")
    _git("add", "normal"); _git("commit", "-qm", "replayed")
    _git("checkout", "-q", "merge-feature")
    _git("merge", "-q", "--no-ff", "--no-commit", "merge-side")
    _write("resolution", "unique")
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
