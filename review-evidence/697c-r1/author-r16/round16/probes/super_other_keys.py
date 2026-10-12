"""Scratch (round 16): the superproject's keys the pin check does not judge, each naming a recorder where it names a
program, in two superprojects whose index records the pin: one plain, one whose sparse index lacks the tree that
holds the gitlink (no promisor remote). The gitlink is read as the pin proof reads it (ctrl_build.stack_gitlink);
prints its verdict and how many times a recorder ran.

usage: python3 -I -B super_other_keys.py <superproject checkout> <scratch dir>
"""
import shutil
import sys
from pathlib import Path

top, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(top / "sw/firmware/ctrl/test"), str(top / "sw/firmware/gtest")]
import ctrl_build  # noqa: E402
from ctrl_pin_env import GITLINK, Scene, answer  # noqa: E402
from ctrl_pin_store import sparse_superproject, superproject  # noqa: E402

RECORDER = '#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n'


def keys(own: Path) -> tuple[tuple[str, str], ...]:
    """Every key the stack's controls name a program by, and others Git starts one for, none of them refused here."""
    rec = own / "recorder"
    hooks = own / "hooks"
    hooks.mkdir(exist_ok=True)
    for hook in ("post-checkout", "post-index-change", "reference-transaction", "pre-auto-gc", "post-merge"):
        (hooks / hook).write_text(RECORDER, encoding="utf-8")
        (hooks / hook).chmod(0o755)
    (own / "attributes").write_text("* filter=pc diff=pc merge=pc\n", encoding="utf-8")
    return (("core.hooksPath", str(hooks)), ("credential.helper", str(rec)), ("core.askPass", str(rec)),
            ("core.pager", str(rec)), ("core.editor", str(rec)), ("sequence.editor", str(rec)),
            ("diff.pc.textconv", str(rec)), ("diff.external", str(rec)), ("merge.pc.driver", str(rec)),
            ("filter.pc.clean", str(rec)), ("filter.pc.smudge", str(rec)), ("filter.pc.process", str(rec)),
            ("core.attributesFile", str(own / "attributes")), ("gpg.program", str(rec)),
            ("core.alternateRefsCommand", str(rec)), ("uploadpack.packObjectsHook", str(rec)),
            ("core.gitProxy", str(rec)), ("protocol.ext.allow", "always"), ("remote.origin.url", f"ext::{rec} %S"),
            ("remote.origin.vcs", "pc"), ("url.ext::.insteadOf", "file://"), ("submodule.recurse", "true"),
            ("core.untrackedCache", "true"), ("core.splitIndex", "true"), ("index.skipHash", "true"),
            ("gc.auto", "1"), ("maintenance.auto", "true"), ("include.path", str(own / "included")))


for shape in ("plain", "sparse"):
    own = scratch / shape
    if own.exists():
        shutil.rmtree(own)
    own.mkdir(parents=True)
    (own / "recorder").write_text(RECORDER, encoding="utf-8")
    (own / "recorder").chmod(0o755)
    (own / "included").write_text("[core]\n\tpager = " + str(own / "recorder") + "\n", encoding="utf-8")
    scene = Scene(top / "third_party/tsn-c-stack", ctrl_build.stack_gitlink(top), own)
    if shape == "plain":
        superproject(scene, keys(own))
    else:
        sparse_superproject(scene, lambda _: ())
        for key, value in keys(own):
            answer(own / "superproject", "config", key, value)
    try:
        said = f"gitlink {ctrl_build.stack_gitlink(own / 'superproject')}"
    except ctrl_build.Refusal as exc:
        said = f"REFUSED {exc}"
    ran = sorted(own.rglob("ran"))
    count = sum(len(r.read_text(encoding="utf-8").splitlines()) for r in ran)
    listed = answer(own / "superproject", "config", "--list", "--local").count("\n")
    print(f"{shape}: {listed} keys in its own configuration; {said}; RAN={count}")
print("git", answer(top, "version").split()[-1])
