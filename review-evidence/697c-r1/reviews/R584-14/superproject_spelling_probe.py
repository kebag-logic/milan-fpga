# Reviewer probe (R584-14): does the superproject key check (ctrl_build.superproject_configured) refuse every
# spelling of a promisor remote and its transport that Git itself honours?
#
# Usage: python3 -I superproject_spelling_probe.py <clone-root> <work-dir>
# The Git the probe runs is the first `git` on PATH (the pin proof's own rule, ctrl_build.GIT).
# It builds the head's own sparse-superproject scene (ctrl_pin_store.sparse_superproject: a sparse index whose
# sparse directory holding the gitlink lacks its tree), then writes the remote's keys straight into the
# superproject's own config file in one of several spellings, and reads the gitlink with the head's
# ctrl_build.stack_gitlink. It prints, per case, the verdict and RAN=<number of recorder lines>.
# Nothing in the clone is written; every file is under <work-dir>.
import shutil
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402
from ctrl_build import Refusal, stack_gitlink  # noqa: E402
from ctrl_pin_env import Scene, answer  # noqa: E402
import ctrl_pin_store  # noqa: E402

PIN = answer(root, "ls-files", "--stage", "--", "third_party/tsn-c-stack").split()[1]


def scene_for(name: str) -> Scene:
    own = work / name
    if own.exists():
        shutil.rmtree(own)
    own.mkdir(parents=True)
    return Scene(root / "third_party/tsn-c-stack", PIN, own)


def case(name: str, body: str | None, check: bool = True) -> None:
    """`body`: text appended to the superproject's .git/config ({origin}, {server} substituted); None: the
    head's own control keys, set with git config."""
    s = scene_for(name)
    if body is None:
        ctrl_pin_store.sparse_superproject(s, lambda origin: (*ctrl_pin_store.partial("origin", str(origin)),
                                                             ("remote.origin.partialCloneFilter", "tree:0"),
                                                             ("remote.origin.uploadpack", ctrl_pin_store.served(s))))
    else:
        ctrl_pin_store.sparse_superproject(s, lambda origin: ())
        server = ctrl_pin_store.served(s)
        # An ext:: transport program: it records that it ran (as the head's RECORDER and SERVER do), then serves
        # the origin with the upload-pack of the Git under test, so a Git that fetched through it gets the tree.
        upload = Path(ctrl_build.GIT).parent / "git-upload-pack"
        ext = s.own / "extserver"
        ext.write_text(f'#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexec {upload} {s.own / "origin"}\n',
                       encoding="utf-8")
        ext.chmod(0o755)
        with open(s.own / "superproject/.git/config", "a", encoding="utf-8") as f:
            f.write(body.format(origin=s.own / "origin", server=server, ext=ext))
    listed = answer(s.own / "superproject", "config", "--list", "--show-scope", "--local")
    saved = ctrl_build.superproject_configured
    if not check:
        ctrl_build.superproject_configured = lambda r: None
    try:
        verdict = f"ACCEPTED gitlink {stack_gitlink(s.own / 'superproject')}"
    except Refusal as exc:
        verdict = f"REFUSED: {exc}"
    finally:
        ctrl_build.superproject_configured = saved
    ran = sum(len(p.read_text().splitlines()) for p in s.own.rglob("ran"))
    remote_keys = [line.split("\t", 1)[1] for line in listed.splitlines() if "remote" in line or "extensions" in line]
    print(f"{name}: check={'on' if check else 'OFF'} keys={remote_keys} -> {verdict} RAN={ran}", flush=True)


print(f"git: {ctrl_build.GIT} {answer(root, 'version').strip()}", flush=True)
case("S0-head-control", None)
case("S1-head-control-check-removed", None, check=False)
case("S2-empty-subsection", '[remote ""]\n\turl = {origin}\n\tpromisor = true\n\tuploadpack = {server}\n')
case("S3-no-subsection-promisor", '[remote]\n\tpromisor = true\n[remote ""]\n\turl = {origin}\n\tuploadpack = {server}\n')
case("S4-empty-subsection-with-extension",
     '[core]\n\trepositoryformatversion = 1\n[extensions]\n\tpartialclone = \n'
     '[remote ""]\n\turl = {origin}\n\tpromisor = true\n\tuploadpack = {server}\n')
case("S5-named-remote-control", '[remote "origin"]\n\turl = {origin}\n\tpromisor = true\n\tuploadpack = {server}\n')
# Git names the promisor remote of a subsection-less remote.promisor (or remote.partialCloneFilter) "", and fetches
# from "" as a URL; an empty url.<base>.insteadOf rewrites "" to <base>.
case("S6-no-subsection-promisor-url-rewrite-ext",
     '[remote]\n\tpromisor = true\n[url "ext::{ext}"]\n\tinsteadOf =\n[protocol "ext"]\n\tallow = always\n')
case("S7-no-subsection-filter-url-rewrite-ext",
     '[remote]\n\tpartialCloneFilter = tree:0\n[url "ext::{ext}"]\n\tinsteadOf =\n[protocol "ext"]\n\tallow = always\n')
case("S8-no-subsection-promisor-url-rewrite-file", '[remote]\n\tpromisor = true\n[url "{origin}"]\n\tinsteadOf =\n')
case("S9-empty-subsection-promisor-url-rewrite-ext",
     '[remote ""]\n\tpromisor = true\n[url "ext::{ext}"]\n\tinsteadOf =\n[protocol "ext"]\n\tallow = always\n')
