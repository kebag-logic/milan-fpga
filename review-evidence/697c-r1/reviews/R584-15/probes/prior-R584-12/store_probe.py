#!/usr/bin/env python3
"""R584-12 object-store and configuration probes of the #697 pin proof.

Usage: python3 -I store_probe.py <test-dir> <stack-checkout> <work-dir> [probe ...]

<test-dir> is a copy of sw/firmware/ctrl/test (the head's, or a mutant's); its
ctrl_build.stack_pin and ctrl_build.stack_gitlink are the code under test.
<stack-checkout> is an initialised tsn-c-stack submodule at the pin. Each probe
works in a fresh clone under <work-dir> whose objects are all loose, applies
one state, and prints one line: PROBE <name> ACCEPTED|REFUSED <detail> RAN=<n>,
where RAN counts the starts of a recorder program the state names.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

TEST, STACK, WORK = (Path(a).resolve() for a in sys.argv[1:4])
WANT = sys.argv[4:]
sys.path.insert(0, str(TEST))
import ctrl_build  # noqa: E402  (installs the proof's audit hook)

GIT = shutil.which("git")
ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "PATH": "/usr/bin:/bin",
       "GIT_NO_REPLACE_OBJECTS": "1"}
EDITED = "src/adp.c"


def g(d: Path, *args: str, stdin: bytes | None = None) -> bytes:
    r = subprocess.run([GIT, "-C", str(d), *args], input=stdin, capture_output=True, env=ENV, check=False)
    if r.returncode:
        raise SystemExit(f"setup failed: git {' '.join(args)}: {r.stderr.decode(errors='replace')}")
    return r.stdout


PIN = g(STACK, "rev-parse", "HEAD").decode().strip()


def loose_clone(name: str) -> Path:
    """A clone at the pin, every object loose in its own store."""
    d = WORK / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    c = d / "stack"
    g(d, "init", "--quiet", str(c))
    g(c, "-c", "fetch.unpackLimit=1000000", "fetch", "--quiet", "--no-tags", str(STACK), PIN)
    g(c, "-c", "advice.detachedHead=false", "checkout", "--quiet", PIN)
    assert not any((c / ".git/objects/pack").iterdir())
    return c


def obj_path(c: Path, oid: str) -> Path:
    return c / ".git/objects" / oid[:2] / oid[2:]


def write_obj(c: Path, kind: str, data: bytes) -> str:
    return g(c, "hash-object", "-t", kind, "-w", "--stdin", "--literally", stdin=data).decode().strip()


def forge(c: Path, victim: str, source: str) -> None:
    """The loose file of `victim` replaced by a new file holding `source`'s object."""
    p = obj_path(c, victim)
    new = p.with_name(p.name + ".new")
    new.write_bytes(obj_path(c, source).read_bytes())
    new.replace(p)


def edit(c: Path) -> bytes:
    f = c / EDITED
    f.write_bytes(f.read_bytes() + b"\n")
    return f.read_bytes()


def tree_with(c: Path, tree: str, name: str, oid: str) -> str:
    lines = []
    for e in filter(None, g(c, "ls-tree", "-z", tree).split(b"\0")):
        meta, ent = e.split(b"\t", 1)
        if ent.decode() == name:
            meta = meta.rsplit(b" ", 1)[0] + b" " + oid.encode()
        lines.append(meta + b"\t" + ent)
    return g(c, "mktree", "-z", stdin=b"\0".join(lines) + b"\0").decode().strip()


def edited_trees(c: Path) -> tuple[str, str, str, str]:
    """(pinned src tree, edited src tree, pinned root tree, edited root tree); the edit on disk."""
    blob = write_obj(c, "blob", edit(c))
    src = g(c, "rev-parse", f"{PIN}:src").decode().strip()
    nsrc = tree_with(c, src, "adp.c", blob)
    root = g(c, "rev-parse", f"{PIN}^{{tree}}").decode().strip()
    return src, nsrc, root, tree_with(c, root, "src", nsrc)


def recorder(d: Path, then: str = "exit 1") -> str:
    p = d / "recorder"
    p.write_text(f'#!/bin/sh\necho "$0 $*" >> "{d}/ran"\n{then}\n')
    p.chmod(0o755)
    return str(p)


def ran(d: Path) -> int:
    f = d / "ran"
    return len(f.read_text().splitlines()) if f.exists() else 0


def verdict(name: str, call) -> None:
    try:
        said, out = "ACCEPTED", call()
    except ctrl_build.Refusal as exc:
        said, out = "REFUSED", str(exc)
    print(f"PROBE {name} {said} {out} RAN={ran(WORK / name)}", flush=True)


def check(name: str, c: Path) -> None:
    verdict(name, lambda: ctrl_build.stack_pin(c, PIN))


# --- probes ---------------------------------------------------------------------------------------------------

def p_clean(n):
    check(n, loose_clone(n))


def p_edit(n):
    c = loose_clone(n); edit(c); check(n, c)


def p_forged_src(n):
    c = loose_clone(n); src, nsrc, _, _ = edited_trees(c); forge(c, src, nsrc); check(n, c)


def p_forged_root(n):
    c = loose_clone(n); _, _, root, nroot = edited_trees(c); forge(c, root, nroot); check(n, c)


def p_forged_commit(n):
    c = loose_clone(n); _, _, root, nroot = edited_trees(c)
    body = g(c, "cat-file", "commit", PIN).replace(f"tree {root}\n".encode(), f"tree {nroot}\n".encode(), 1)
    forge(c, PIN, write_obj(c, "commit", body)); check(n, c)


def p_forged_blob(n):
    c = loose_clone(n); data = edit(c)
    forge(c, g(c, "rev-parse", f"{PIN}:{EDITED}").decode().strip(), write_obj(c, "blob", data)); check(n, c)


def p_forged_deep(n):
    """A tree two levels down (the deepest tree of the pin) forged to hold an edit of one of its files."""
    c = loose_clone(n)
    trees = [l.split(b"\t", 1) for l in g(c, "ls-tree", "-r", "-t", PIN).splitlines() if b" tree " in l]
    meta, path = max(trees, key=lambda t: t[1].count(b"/"))
    oid, path = meta.split()[2].decode(), path.decode()
    files = [l.split(b"\t", 1) for l in g(c, "ls-tree", oid).splitlines() if b" blob " in l]
    fmeta, fname = files[0]
    f = c / path / fname.decode()
    f.write_bytes(f.read_bytes() + b"\n")
    blob = write_obj(c, "blob", f.read_bytes())
    forge(c, oid, tree_with(c, oid, fname.decode(), blob))
    print(f"# {n}: forged tree {path} ({oid[:8]}), edited {path}/{fname.decode()}")
    check(n, c)


def p_tag_for_commit(n):
    """The pinned commit's object replaced by an annotated tag naming a commit whose tree holds the edit."""
    c = loose_clone(n); _, _, root, nroot = edited_trees(c)
    body = g(c, "cat-file", "commit", PIN).replace(f"tree {root}\n".encode(), f"tree {nroot}\n".encode(), 1)
    other = write_obj(c, "commit", body)
    tag = write_obj(c, "tag", f"object {other}\ntype commit\ntag t\ntagger p <p@invalid> 0 +0000\n\nt\n".encode())
    forge(c, PIN, tag); check(n, c)


def p_commit_for_tree(n):
    """The pinned src/ tree's object replaced by a commit whose tree is an src/ tree holding the edit (peeling)."""
    c = loose_clone(n); src, nsrc, _, _ = edited_trees(c)
    com = write_obj(c, "commit", f"tree {nsrc}\nauthor p <p@invalid> 0 +0000\ncommitter p <p@invalid> 0 +0000\n\nx\n"
                    .encode())
    forge(c, src, com); check(n, c)


def p_alternate_forged(n):
    """The src/ tree absent from the clone's own store and forged in a store its objects/info/alternates names."""
    c = loose_clone(n); src, nsrc, _, _ = edited_trees(c)
    other = WORK / n / "other-objects"
    (other / src[:2]).mkdir(parents=True)
    (other / src[:2] / src[2:]).write_bytes(obj_path(c, nsrc).read_bytes())
    obj_path(c, src).unlink()
    (c / ".git/objects/info/alternates").write_text(f"{other}\n")
    check(n, c)


def p_corrupt(n):
    """The src/ tree's loose file truncated (zlib stream cut)."""
    c = loose_clone(n); src = g(c, "rev-parse", f"{PIN}:src").decode().strip()
    p = obj_path(c, src); data = p.read_bytes(); p.unlink(); p.write_bytes(data[: len(data) // 2]); check(n, c)


def p_trailing(n):
    """The src/ tree's loose file holding its own object plus trailing bytes inside the stream's header length."""
    c = loose_clone(n); src = g(c, "rev-parse", f"{PIN}:src").decode().strip()
    p = obj_path(c, src); raw = zlib.decompress(p.read_bytes())
    p.unlink(); p.write_bytes(zlib.compress(raw + b"extra")); check(n, c)


def p_missing(n):
    c = loose_clone(n); src = g(c, "rev-parse", f"{PIN}:src").decode().strip()
    obj_path(c, src).unlink(); check(n, c)


def lazy(n, then: str, url_kind: str):
    """The src/ tree absent, the clone made a partial clone of a full copy whose fetch runs a program its own
    configuration names (remote.origin.uploadpack, or core.sshCommand)."""
    c = loose_clone(n); src = g(c, "rev-parse", f"{PIN}:src").decode().strip()
    full = WORK / n / "full"
    g(WORK / n, "clone", "--quiet", "--bare", "--no-hardlinks", str(STACK), str(full))
    obj_path(c, src).unlink()
    prog = recorder(WORK / n, then)
    g(c, "config", "core.repositoryformatversion", "1")
    g(c, "config", "extensions.partialClone", "origin")
    g(c, "config", "remote.origin.promisor", "true")
    if url_kind == "uploadpack":
        g(c, "config", "remote.origin.url", str(full))
        g(c, "config", "remote.origin.uploadpack", prog)
    else:
        g(c, "config", "remote.origin.url", f"ssh://example.invalid{full}")
        g(c, "config", "core.sshCommand", prog)
    check(n, c)


def p_lazy_uploadpack_fail(n):
    lazy(n, "exit 1", "uploadpack")


def p_lazy_uploadpack_serve(n):
    lazy(n, 'exec /usr/bin/git upload-pack "$@"', "uploadpack")


def p_lazy_ssh(n):
    lazy(n, "exit 1", "ssh")


def p_lazy_toctou(n):
    """As lazy_uploadpack_serve, the program also leaving a process that edits a core source after the proof
    has hashed it: the proof's acceptance does not describe the tree a build then reads."""
    stack = WORK / n / "stack"
    lazy(n, f'(sleep 3; echo "/* planted */" >> "{stack}/{EDITED}") >/dev/null 2>&1 &\n'
            'exec /usr/bin/git upload-pack "$@"', "uploadpack")
    import time
    time.sleep(5)
    print(f"# {n}: after the verdict, {EDITED} planted: {b'planted' in (stack / EDITED).read_bytes()}; "
          f"re-check: ", end="", flush=True)
    try:
        print("ACCEPTED", ctrl_build.stack_pin(stack, PIN))
    except ctrl_build.Refusal as exc:
        print("REFUSED", exc)


def p_super_fsmonitor(n):
    d = WORK / n
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    top = d / "superproject"
    g(d, "init", "--quiet", str(top))
    g(top, "update-index", "--add", "--cacheinfo", f"160000,{PIN},third_party/tsn-c-stack")
    g(top, "config", "core.fsmonitor", recorder(d))
    verdict(n, lambda: ctrl_build.stack_gitlink(top))


def p_stack_fsmonitor(n):
    c = loose_clone(n); g(c, "config", "core.fsmonitor", recorder(WORK / n)); edit(c); check(n, c)


def p_core_worktree(n):
    """The clone's own configuration naming another work tree (core.worktree), the edit on disk."""
    c = loose_clone(n); other = WORK / n / "other"
    shutil.copytree(c, other, ignore=shutil.ignore_patterns(".git")); edit(c)
    g(c, "config", "core.worktree", str(other)); check(n, c)


PROBES = {k[2:]: v for k, v in globals().items() if k.startswith("p_")}
for name in WANT or PROBES:
    PROBES[name](name)
