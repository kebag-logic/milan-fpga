#!/usr/bin/env python3
"""Independent probes of the tsn-c-stack pin check (ctrl_build.py --stack-pin),
each on a fresh clone of the checkout's initialised stack. A recorder program
writes <probe>/ran when any configuration makes Git start it.

usage: python3 -I probes.py <superproject-root> <work-dir>
Prints one line per probe: name, expected, exit, RAN count, verdict line.
"""
import os, shutil, struct, hashlib, subprocess, sys
from pathlib import Path

ROOT, WORK = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
STACK = ROOT / "third_party/tsn-c-stack"
PIN = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--stage", "--", "third_party/tsn-c-stack"],
                     capture_output=True, text=True, check=True).stdout.split()[1]
CHECK = ROOT / "sw/firmware/ctrl/test/ctrl_build.py"
REC = '#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n'
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def g(d, *a, inp=None, check=True):
    r = subprocess.run(["git", "-c", "gc.auto=0", "-c", "maintenance.auto=false", "-C", str(d), *a], input=inp,
                       capture_output=True, env=ENV)
    if check and r.returncode:
        raise SystemExit(f"setup git {a} failed: {r.stderr.decode()}")
    return r.stdout.decode()


def fresh(own: Path) -> Path:
    shutil.rmtree(own, ignore_errors=True)
    own.mkdir(parents=True)
    (own / "recorder").write_text(REC)
    (own / "recorder").chmod(0o755)
    c = own / "clone"
    g(own, "clone", "--quiet", "--no-hardlinks", str(STACK), str(c))
    g(c, "-c", "advice.detachedHead=false", "checkout", "--quiet", PIN)
    return c


def edit(c):
    p = c / "src/adp.c"
    p.write_bytes(p.read_bytes() + b"\n")


def forged_src(c):
    """Write a src/ tree holding the edit (loose); return (pinned src oid, forged oid)."""
    blob = g(c, "hash-object", "-w", "--stdin", inp=(c / "src/adp.c").read_bytes()).strip()
    src = g(c, "rev-parse", f"{PIN}:src").strip()
    ents = []
    for e in filter(None, g(c, "ls-tree", "-z", src).split("\0")):
        meta, name = e.split("\t", 1)
        ents.append(f"{meta.rsplit(' ', 1)[0]} {blob}\t{name}" if name == "adp.c" else e)
    new = g(c, "mktree", "-z", inp=("\0".join(ents) + "\0").encode()).strip()
    return src, new


def run(c):
    r = subprocess.run([sys.executable, "-I", str(CHECK), "--stack-pin", str(c)], capture_output=True, text=True,
                       env=ENV, timeout=300)
    out = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, out[-1] if out else ""


def swap_in_pack(c, a, b):
    """Swap the idx entries (offset, crc) of objects a and b in the clone's single pack."""
    packdir = c / ".git/objects/pack"
    idx = next(packdir.glob("*.idx"))
    data = bytearray(idx.read_bytes())
    assert data[:8] == b"\xfftOc\x00\x00\x00\x02"
    n = struct.unpack(">I", data[8 + 255 * 4:8 + 256 * 4])[0]
    names = 8 + 256 * 4
    crcs, offs = names + 20 * n, names + 24 * n
    ids = [bytes(data[names + 20 * i:names + 20 * i + 20]).hex() for i in range(n)]
    i, j = ids.index(a), ids.index(b)
    for base, w in ((crcs, 4), (offs, 4)):
        x, y = data[base + w * i:base + w * i + w], data[base + w * j:base + w * j + w]
        data[base + w * i:base + w * i + w], data[base + w * j:base + w * j + w] = y, x
    data[-20:] = hashlib.sha1(bytes(data[:-20])).digest()
    idx.chmod(0o644)
    idx.write_bytes(bytes(data))


def probes():
    P = []

    def add(name, expect):
        def deco(f):
            P.append((name, expect, f))
            return f
        return deco

    @add("Q0 clean clone", "accept")
    def _(own):
        return fresh(own)

    @add("Q1 forged src/ tree inside a pack (idx entries swapped), edit on disk", "refuse:forged or corrupt object: the pinned src/ tree")
    def _(own):
        c = fresh(own); edit(c)
        src, new = forged_src(c)
        g(c, "update-ref", "refs/probe/keep", new)
        g(c, "repack", "-a", "-d", "-q"); g(c, "prune-packed")
        swap_in_pack(c, src, new)
        g(c, "update-ref", "-d", "refs/probe/keep")
        raw = subprocess.run(["git", "-C", str(c), "cat-file", "tree", src], capture_output=True, env=ENV).stdout
        (own / "note").write_text(f"setup check: Git now serves src {src[:8]} as an object hashing to "
                                  f"{hashlib.sha1(b'tree %d' % len(raw) + bytes(1) + raw).hexdigest()[:8]}\n")
        return c

    @add("Q2 forged src/ tree in an alternates store, clone's own store emptied, edit on disk", "refuse:forged or corrupt object: the pinned src/ tree")
    def _(own):
        c = fresh(own); edit(c)
        g(c, "repack", "-a", "-d", "-q")
        alt = own / "altstore"
        # make every object loose in a separate store
        tmp = own / "tmp"; g(own, "init", "-q", "--bare", str(tmp))
        g(tmp, "-c", "fetch.unpackLimit=1000000", "fetch", "-q", "--no-tags", str(c), f"{PIN}:refs/heads/p")
        shutil.copytree(tmp / "objects", alt)
        src, new = forged_src(c)
        newbytes = (c / ".git/objects" / new[:2] / new[2:]).read_bytes()
        victim = alt / src[:2] / src[2:]
        victim.chmod(0o644); victim.unlink(); victim.write_bytes(newbytes)
        for e in (c / ".git/objects").iterdir():
            if e.name != "info":
                shutil.rmtree(e) if e.is_dir() else e.unlink()
        (c / ".git/objects/info").mkdir(exist_ok=True)
        (c / ".git/objects/info/alternates").write_text(str(alt) + "\n")
        return c

    def cfg(own, c, text):
        with open(c / ".git/config", "a") as f:
            f.write(text.replace("@REC@", str(own / "recorder")))

    @add("Q3a [Core] FSMonitor (mixed case), edit on disk", "refuse:core.fsmonitor (local)")
    def _(own):
        c = fresh(own); edit(c); cfg(own, c, "[Core]\n\tFSMonitor = @REC@\n"); return c

    @add("Q3b [core \"x\"] fsmonitor (subsection)", "refuse:core.x.fsmonitor (local)")
    def _(own):
        c = fresh(own); cfg(own, c, '[core "x"]\n\tfsmonitor = @REC@\n'); return c

    @add("Q3c includeIf gitdir: to a file naming core.fsmonitor, edit on disk", "refuse:core.fsmonitor (local)")
    def _(own):
        c = fresh(own); edit(c)
        (own / "inc").write_text(f"[core]\n\tfsmonitor = {own / 'recorder'}\n")
        cfg(own, c, f'[includeIf "gitdir:{c}/"]\n\tpath = {own / "inc"}\n'); return c

    @add("Q3d valueless boolean [core] fsmonitor (builtin daemon), edit on disk", "refuse:core.fsmonitor (local)")
    def _(own):
        c = fresh(own); edit(c); cfg(own, c, "[core]\n\tfsmonitor\n"); return c

    @add("Q3e url.<base>.insteadOf rewriting the remote", "refuse:insteadof (local)")
    def _(own):
        c = fresh(own); cfg(own, c, '[url "ext::sh -c x"]\n\tinsteadOf = /\n'); return c

    @add("Q3f value with an embedded newline in an allowlisted key", "accept")
    def _(own):
        c = fresh(own); cfg(own, c, '[branch "x"]\n\tmerge = "a\\nlocal\\ncore.fsmonitor"\n'); return c

    @add("Q4 pinned src/ tree object missing, no configuration", "refuse:cannot read")
    def _(own):
        c = fresh(own)
        g(c, "repack", "-a", "-d", "-q")
        tmp = own / "loose"; g(own, "init", "-q", str(tmp))
        g(tmp, "-c", "fetch.unpackLimit=1000000", "fetch", "-q", "--no-tags", str(c), f"{PIN}:refs/heads/p")
        g(tmp, "-c", "advice.detachedHead=false", "checkout", "-q", PIN)
        src = g(tmp, "rev-parse", f"{PIN}:src").strip()
        (tmp / ".git/objects" / src[:2] / src[2:]).unlink()
        return tmp

    @add("Q5 core.worktree naming a pristine pinned checkout, the edit in the gated directory", "refuse:is not its own checkout")
    def _(own):
        c = fresh(own); edit(c)
        other = own / "pristine"; g(own, "clone", "-q", "--no-hardlinks", str(STACK), str(other))
        g(other, "-c", "advice.detachedHead=false", "checkout", "-q", PIN)
        g(c, "config", "core.worktree", str(other)); return c

    @add("Q6 shallow clone (--depth 1) at the pin", "accept")
    def _(own):
        own.mkdir(parents=True, exist_ok=True)
        s = own / "shallow"
        shutil.rmtree(s, ignore_errors=True)
        g(own, "-c", "protocol.file.allow=always", "clone", "-q", "--depth", "1", "--no-single-branch",
          f"file://{STACK}", str(s))
        g(s, "fetch", "-q", "--depth", "1", "origin", PIN)
        g(s, "-c", "advice.detachedHead=false", "checkout", "-q", PIN); return s

    @add("Q7 linked worktree of a clone, at the pin", "accept")
    def _(own):
        c = fresh(own); w = own / "wt"
        g(c, "worktree", "add", "-q", "--detach", str(w), PIN); return w

    @add("Q8 linked worktree of a clone, at the pin, edit on disk", "refuse:src/adp.c")
    def _(own):
        c = fresh(own); w = own / "wt"
        g(c, "worktree", "add", "-q", "--detach", str(w), PIN); edit(w); return w

    @add("Q9 forged pinned commit inside a pack (idx entries swapped), edit on disk", "refuse:forged or corrupt object: the pinned commit")
    def _(own):
        c = fresh(own); edit(c)
        src, new = forged_src(c)
        root = g(c, "rev-parse", f"{PIN}^{{tree}}").strip()
        ents = [(e.split("\t")[0].rsplit(" ", 1)[0] + f" {new}\tsrc") if e.endswith("\tsrc") else e
                for e in filter(None, g(c, "ls-tree", "-z", root).split("\0"))]
        nroot = g(c, "mktree", "-z", inp=("\0".join(ents) + "\0").encode()).strip()
        body = g(c, "cat-file", "commit", PIN).replace(f"tree {root}\n", f"tree {nroot}\n", 1)
        ncommit = g(c, "hash-object", "-t", "commit", "-w", "--stdin", inp=body.encode()).strip()
        g(c, "update-ref", "refs/probe/keep", ncommit)
        g(c, "repack", "-a", "-d", "-q"); g(c, "prune-packed")
        swap_in_pack(c, PIN, ncommit)
        g(c, "update-ref", "-d", "refs/probe/keep")
        raw = subprocess.run(["git", "-C", str(c), "cat-file", "commit", PIN], capture_output=True, env=ENV).stdout
        (own / "note").write_text(f"setup check: Git now serves the pin as an object hashing to "
                                  f"{hashlib.sha1(b'commit %d' % len(raw) + bytes(1) + raw).hexdigest()[:8]}\n")
        return c

    return P


only = set(sys.argv[3:])
bad = 0
for name, expect, make in probes():
    if only and name.split()[0] not in only:
        continue
    own = WORK / name.split()[0]
    shutil.rmtree(own, ignore_errors=True)
    try:
        c = make(own)
        rc, last = run(c)
    except SystemExit as exc:
        rc, last = -1, f"SETUP: {exc}"
    ran = len((own / "ran").read_text().splitlines()) if (own / "ran").exists() else 0
    if expect == "accept":
        ok = rc == 0 and ran == 0
    else:
        ok = rc == 2 and expect.split(":", 1)[1] in last and ran == 0
    bad += not ok
    note = (own / "note").read_text().strip() if (own / "note").exists() else ""
    print(f"[{'as-expected' if ok else 'UNEXPECTED'}] {name} | expect {expect} | exit {rc} | RAN={ran} | {last}"
          + (f" | {note}" if note else ""), flush=True)
print(f"PROBES: {bad} unexpected")
