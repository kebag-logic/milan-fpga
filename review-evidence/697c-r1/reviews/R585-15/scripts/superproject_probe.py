"""Independent probe of the superproject check (ctrl_build.stack_gitlink) at a tree, with the Git PATH names.

Each case builds a superproject whose index records the tree's tsn-c-stack gitlink, plants configuration, then
reads the gitlink as the proof does. A recorder program writes RAN lines; the verdict line says what the proof
said and how many times a planted program ran.

usage: python3 -B superproject_probe.py TREE WORK
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))
import ctrl_build  # noqa: E402

GITLINK = "third_party/tsn-c-stack"
PIN = ctrl_build.stack_gitlink(tree)


def g(cwd, *args, check=True):
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"setup failed: git {' '.join(args)}: {r.stderr}")
    return r.stdout


def recorder(d: Path) -> str:
    p = d / "recorder"
    p.write_text('#!/bin/sh\necho "RAN $0 $*" >> "%s/ran"\nexit 1\n' % d)
    p.chmod(0o755)
    return str(p)


def sparse(d: Path, keep_tree: bool) -> Path:
    """A superproject with a sparse index whose sparse directory third_party/ holds the gitlink; its tree removed
    unless keep_tree."""
    origin, top = d / "origin", d / "super"
    g(d, "init", "-q", str(origin))
    (origin / "kept").mkdir()
    (origin / "kept/file").write_text("kept\n")
    g(origin, "add", "kept/file")
    g(origin, "update-index", "--add", "--cacheinfo", f"160000,{PIN},{GITLINK}")
    g(origin, "-c", "user.name=p", "-c", "user.email=p@invalid", "commit", "-q", "-m", "p")
    g(d, "init", "-q", str(top))
    g(top, "-c", "fetch.unpackLimit=1000000", "fetch", "-q", "--no-tags", str(origin), "HEAD")
    g(top, "update-ref", "HEAD", "FETCH_HEAD")
    g(top, "sparse-checkout", "set", "--cone", "--sparse-index", "kept")
    g(top, "checkout", "-q")
    t = g(top, "rev-parse", "HEAD:third_party").strip()
    if not keep_tree:
        (top / ".git/objects" / t[:2] / t[2:]).unlink()
    return top


def plain(d: Path) -> Path:
    top = d / "super"
    g(d, "init", "-q", str(top))
    g(top, "update-index", "--add", "--cacheinfo", f"160000,{PIN},{GITLINK}")
    return top


def case(name, make, keys, files=None, append=""):
    d = work / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    rec = recorder(d)
    hooks = d / "hooks"
    hooks.mkdir()
    for h in ("post-index-change", "post-checkout", "reference-transaction", "pre-auto-gc"):
        (hooks / h).write_text(f'#!/bin/sh\n"{rec}" hook {h}\n')
        (hooks / h).chmod(0o755)
    top = make(d)
    sub = lambda s: s.replace("@REC@", rec).replace("@D@", str(d))
    for k, v in keys:
        g(top, "config", "--add", sub(k), sub(v))
    for rel, text in (files or {}).items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(sub(text))
    if append:
        with open(top / ".git/config", "a") as fh:
            fh.write(sub(append))
    try:
        said = "accepted " + ctrl_build.stack_gitlink(top)
    except ctrl_build.Refusal as exc:
        said = "REFUSED: " + str(exc)
    ran = (d / "ran").read_text().count("RAN") if (d / "ran").exists() else 0
    print(f"CASE {name}: RAN={ran} :: {said}", flush=True)


git = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
print(f"git: {shutil.which('git')} {git}; pin {PIN}", flush=True)
if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
OTHER = [("core.hooksPath", "@D@/hooks"), ("credential.helper", "@REC@"), ("core.askPass", "@REC@"),
         ("core.pager", "@REC@"), ("core.editor", "@REC@"), ("sequence.editor", "@REC@"), ("gpg.program", "@REC@"),
         ("core.alternateRefsCommand", "@REC@"), ("uploadpack.packObjectsHook", "@REC@"),
         ("filter.p.clean", "@REC@"), ("filter.p.smudge", "@REC@"), ("filter.p.process", "@REC@"),
         ("diff.p.textconv", "@REC@"), ("protocol.ext.allow", "always"), ("remote.origin.url", "ext::@REC@ %S"),
         ("core.gitProxy", "@REC@"), ("ssh.variant", "simple"), ("submodule.recurse", "true"),
         ("core.untrackedCache", "true"), ("index.sparse", "true"), ("maintenance.auto", "true"), ("gc.auto", "1"),
         ("gc.autoDetach", "false")]
ATTR = {"attributes": "* filter=p diff=p\n"}
OTHER_ATTR = OTHER + [("core.attributesFile", "@D@/attributes")]
for nm, mk in (("plain", plain), ("sparse_tree_missing", lambda d: sparse(d, False)),
               ("sparse_tree_present", lambda d: sparse(d, True))):
    case(f"{nm}_other_program_keys_no_promisor", mk, OTHER_ATTR, ATTR)
for nm, mk in (("plain", plain), ("sparse_tree_missing", lambda d: sparse(d, False))):
    case(f"{nm}_includeIf_gitdir_fsmonitor", mk, [("includeIf.gitdir:@D@/.path", "@D@/inc")],
         {"inc": "[core]\n\tfsmonitor = @REC@\n"})
    case(f"{nm}_includeIf_onbranch_promisor", mk, [("includeIf.onbranch:**.path", "@D@/inc")],
         {"inc": "[extensions]\n\tpartialClone = origin\n[remote \"origin\"]\n\turl = @D@/origin\n"
                 "\tpromisor = true\n\tuploadpack = @REC@\n"})
    case(f"{nm}_mixed_case_keys", mk, [("Remote.Origin.Promisor", "true"), ("EXTENSIONS.PartialClone", "Origin"),
                                       ("remote.Origin.url", "@D@/origin"), ("Remote.Origin.UploadPack", "@REC@")])
    case(f"{nm}_legacy_subsection_syntax", mk, [], None,
         "[remote.origin]\n\turl = @D@/origin\n\tpromisor = true\n\tuploadpack = @REC@\n"
         "[extensions]\n\tpartialClone = origin\n")
