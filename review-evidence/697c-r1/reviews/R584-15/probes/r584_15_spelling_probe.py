# Reviewer probe (R584-15): further spellings of a promisor remote in the superproject's own configuration, beyond
# R584-14's superproject_spelling_probe.py: letter case, Git's legacy dotted subsection, a dotted named subsection, a
# value-less boolean, an included file, a conditional include, the work tree's own file, and an empty-subsection
# filter. Each case builds the head's own sparse-superproject scene (ctrl_pin_store.sparse_superproject: a sparse
# index whose sparse directory holding the gitlink lacks its tree), appends the case's text to a configuration file,
# and reads the gitlink with the head's ctrl_build.stack_gitlink. The remote is reached through an ext:: program
# that records it ran and then serves the origin, so a Git that fetched through it would be given the tree.
# Usage: python3 -I r584_15_spelling_probe.py <clone-root> <work-dir>
# The Git is the first `git` on PATH (the pin proof's own rule, ctrl_build.GIT). Prints per case the verdict and
# RAN=<recorder lines>. Nothing in the clone is written; every file is under <work-dir>.
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
EXT = '[protocol "ext"]\n\tallow = always\n'


def case(name: str, body: str, where: str = "config", check: bool = True) -> None:
    """`body` ({ext}, {inc} substituted) appended to the superproject's .git/<where>; `where` "included" writes it
    to a file the superproject's config includes (include.path), "onbranch" to one it includes on its branch."""
    own = work / name
    if own.exists():
        shutil.rmtree(own)
    own.mkdir(parents=True)
    s = Scene(root / "third_party/tsn-c-stack", PIN, own)
    ctrl_pin_store.sparse_superproject(s, lambda origin: ())
    upload = Path(ctrl_build.GIT).parent / "git-upload-pack"
    ext = own / "extserver"
    ext.write_text(f'#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexec {upload} {own / "origin"}\n',
                   encoding="utf-8")
    ext.chmod(0o755)
    top = own / "superproject"
    text = body.format(ext=ext)
    if where == "config" or where == "config.worktree":
        with open(top / ".git" / where, "a", encoding="utf-8") as f:
            f.write(text)
    else:
        inc = own / "included"
        inc.write_text(text, encoding="utf-8")
        branch = answer(top, "symbolic-ref", "--short", "HEAD").strip()
        header = "[include]\n" if where == "included" else f'[includeIf "onbranch:{branch}"]\n'
        with open(top / ".git/config", "a", encoding="utf-8") as f:
            f.write(f"{header}\tpath = {inc}\n")
    saved = ctrl_build.superproject_configured
    if not check:
        ctrl_build.superproject_configured = lambda r: None
    try:
        verdict = f"ACCEPTED gitlink {stack_gitlink(top)}"
    except Refusal as exc:
        verdict = f"REFUSED: {exc}"
    finally:
        ctrl_build.superproject_configured = saved
    ran = sum(len(p.read_text().splitlines()) for p in own.rglob("ran"))
    print(f"{name}: where={where} check={'on' if check else 'OFF'} -> {verdict} RAN={ran}", flush=True)


ROUTE = '[url "ext::{ext}"]\n\tinsteadOf =\n' + EXT
print(f"git: {ctrl_build.GIT} {answer(root, 'version').strip()}", flush=True)
case("E0-route-only-no-promisor", ROUTE)
case("E1-upper-case-section-variable", "[Remote]\n\tPromisor = true\n" + ROUTE)
case("E1x-upper-case-check-removed", "[Remote]\n\tPromisor = true\n" + ROUTE, check=False)
case("E2-legacy-dotted-subsection", "[remote.x]\n\tpromisor = true\n\turl = ext::{ext}\n" + EXT)
case("E3-dotted-named-subsection", '[remote "a.b"]\n\tpromisor = true\n\turl = ext::{ext}\n' + EXT)
case("E4-valueless-boolean", '[remote "x"]\n\tpromisor\n\turl = ext::{ext}\n' + EXT)
case("E5-included-file", "[remote]\n\tpromisor = true\n" + ROUTE, where="included")
case("E6-conditional-include-onbranch", "[remote]\n\tpromisor = true\n" + ROUTE, where="onbranch")
case("E7-worktree-file", "[remote]\n\tpromisor = true\n" + ROUTE, where="config.worktree")
case("E8-empty-subsection-filter", '[remote ""]\n\tpartialCloneFilter = blob:none\n' + ROUTE)
case("E9-partialclone-extension-v0", "[extensions]\n\tpartialClone = x\n" + '[remote "x"]\n\turl = ext::{ext}\n' + EXT)
