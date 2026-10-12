#!/usr/bin/env python3
"""Probe the pin proof (ctrl_build.stack_pin of a tree) against state inside its stated threat model.

usage: forge_probe.py <tree root> <work dir>
Each case builds a fresh scratch clone of the tree's tsn-c-stack submodule at its gitlink, with every
object loose, spoils it, and calls the tree's own stack_pin(clone, pin):
  F0 control: an edit of src/adp.c alone (must be refused)
  F1 the src/ tree's loose object overwritten with a tree holding the edit's blob, plus the edit on disk
  F2 the pinned commit's loose object overwritten with a commit whose root tree holds the edit, plus the edit
  F3 the repository's own core.fsmonitor naming a recorder (the clone's .git/config, and the superproject's
     index read by stack_gitlink is not involved: the pin is passed explicitly), unmodified clone
Prints, for each, ACCEPTED/REFUSED with the proof's words and `git fsck` on the clone.
The tree's modules are imported unmodified; nothing outside <work dir> is written.
"""
import os
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_build  # noqa: E402

pin = ctrl_build.stack_gitlink(root)
ENV = {"PATH": os.environ["PATH"], "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "HOME": str(work)}


def g(repo, *args, data=None):
    r = subprocess.run(["git", "-C", str(repo), *args], input=data, capture_output=True, env=ENV)
    if r.returncode:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.decode()}")
    return r.stdout


def fresh(name):
    clone = work / name
    if clone.exists():
        shutil.rmtree(clone)
    g(work, "clone", "--quiet", "--no-hardlinks", str(ctrl_build.STACK), str(clone))
    g(clone, "-c", "advice.detachedHead=false", "checkout", "--quiet", pin)
    packs = clone / ".git/objects/pack"
    for pack in sorted(packs.glob("*.pack")):
        moved = work / (name + "-" + pack.name)
        shutil.move(pack, moved)
        pack.with_suffix(".idx").unlink()
        g(clone, "unpack-objects", "-q", data=moved.read_bytes())
        moved.unlink()
    alt = clone / ".git/objects/info/alternates"
    if alt.exists():
        alt.unlink()
    return clone


def loose(clone, oid):
    return clone / ".git/objects" / oid[:2] / oid[2:]


def overwrite(clone, victim, source):
    """Make reading `victim` yield `source`'s content (a loose object holding another object's bytes)."""
    path = loose(clone, victim)
    os.chmod(path, 0o644)
    path.write_bytes(loose(clone, source).read_bytes())


def edit(clone):
    target = clone / "src/adp.c"
    target.write_bytes(target.read_bytes() + b"/* probe edit */\n")
    return g(clone, "hash-object", "-w", "src/adp.c").decode().strip()


def edited_tree(clone, tree, blob):
    listing = g(clone, "ls-tree", tree).decode()
    lines = [ln if not ln.endswith("\tadp.c") else ln.split(" ")[0] + " blob " + blob + "\tadp.c"
             for ln in listing.splitlines()]
    return g(clone, "mktree", data=("\n".join(lines) + "\n").encode()).decode().strip()


def verdict(clone):
    try:
        return "ACCEPTED " + ctrl_build.stack_pin(clone, pin)
    except ctrl_build.Refusal as exc:
        return "REFUSED " + str(exc)


def fsck(clone):
    r = subprocess.run(["git", "-C", str(clone), "fsck", "--full"], capture_output=True, env=ENV)
    return f"fsck rc={r.returncode} {(r.stderr + r.stdout).decode().strip().splitlines()[:1]}"


work.mkdir(parents=True, exist_ok=True)
print(f"pin {pin}")

c = fresh("f0")
edit(c)
print("F0 edit only:", verdict(c), "|", fsck(c))

c = fresh("f1")
blob = edit(c)
src = g(c, "rev-parse", f"{pin}:src").decode().strip()
forged = edited_tree(c, src, blob)
overwrite(c, src, forged)
print("F1 forged src/ tree:", verdict(c), "|", fsck(c))

c = fresh("f2")
blob = edit(c)
src = g(c, "rev-parse", f"{pin}:src").decode().strip()
top = g(c, "rev-parse", f"{pin}^{{tree}}").decode().strip()
new_src = edited_tree(c, src, blob)
listing = g(c, "ls-tree", top).decode().splitlines()
listing = [ln if not ln.endswith("\tsrc") else f"040000 tree {new_src}\tsrc" for ln in listing]
new_top = g(c, "mktree", data=("\n".join(listing) + "\n").encode()).decode().strip()
body = g(c, "cat-file", "commit", pin).decode().replace(f"tree {top}", f"tree {new_top}", 1)
new_commit = g(c, "hash-object", "-t", "commit", "-w", "--stdin", data=body.encode()).decode().strip()
overwrite(c, pin, new_commit)
print("F2 forged pinned commit:", verdict(c), "|", fsck(c))

c = fresh("f3")
record = work / "fsmonitor-ran"
if record.exists():
    record.unlink()
hook = work / "recorder.sh"
hook.write_text(f"#!/bin/sh\necho ran >> {record}\nexit 1\n")
hook.chmod(0o755)
g(c, "config", "core.fsmonitor", str(hook))
print("F3 clone's own core.fsmonitor:", verdict(c), "| program ran:",
      record.read_text().count("ran") if record.exists() else 0, "time(s)")
