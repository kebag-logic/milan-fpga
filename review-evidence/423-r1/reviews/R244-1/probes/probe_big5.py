"""Probe: filename transport under a locale whose codec does not round-trip.

Builds, with raw plumbing and fixed bytes, one exact redundant-merge history:
  source touches LOSSY (b"\\xa1\\xfe.txt") and ctl; both replayed exactly on
  main; a later main commit reverts LOSSY's change and extends ctl far away.
The correct verdict is UNKNOWN/1 (LOSSY's change is not retained at the tip).

Usage: probe_big5.py build <dir>       (build fixture, any locale)
       probe_big5.py run <dir> <checker>  (run checker from <dir>, print rc)
"""
import subprocess
import sys
from pathlib import Path

LOSSY = b"\xa1\xfe.txt"
OLD = b"".join(b"line %02d\n" % i for i in range(40))
SRC = OLD.replace(b"line 05", b"source 05")
EXT = SRC.replace(b"line 35", b"later 35")
ENV_GIT = ("-c", "user.name=F", "-c", "user.email=f@example.invalid")


def raw(*args, data=None, cwd=None):
    r = subprocess.run(("git", *ENV_GIT, *args), input=data, capture_output=True, cwd=cwd)
    if r.returncode:
        raise SystemExit(f"fixture git {args!r}: {r.stderr!r}")
    return r.stdout.strip()


def tree(entries, cwd):
    recs = b""
    for name, content in entries.items():
        oid = raw("hash-object", "-w", "--stdin", data=content, cwd=cwd)
        recs += b"100644 blob " + oid + b"\t" + name + b"\0"
    return raw("mktree", "-z", data=recs, cwd=cwd).decode()


def commit(t, parents, msg, cwd):
    args = ["commit-tree", t, "-m", msg]
    for p in parents:
        args += ["-p", p]
    return raw(*args, cwd=cwd).decode()


def build(d):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    raw("init", "-q", "-b", "main", cwd=d)
    o = commit(tree({LOSSY: OLD, b"ctl": OLD}, d), [], "O", d)
    a_tree = tree({LOSSY: SRC, b"ctl": OLD}, d)
    a = commit(a_tree, [o], "A edits lossy-named file", d)
    m = commit(a_tree, [o, a], "M redundant merge", d)
    c_tree = tree({LOSSY: SRC, b"ctl": SRC}, d)
    c = commit(c_tree, [m], "C edits ctl", d)
    ra = commit(a_tree, [o], "A' replay", d)
    rc = commit(c_tree, [ra], "C' replay", d)
    # later tip: LOSSY reverted to OLD, ctl extended far from C's hunk
    tip = commit(tree({LOSSY: OLD, b"ctl": EXT}, d), [rc], "L reverts lossy + far ext", d)
    raw("update-ref", "refs/heads/pr", c, cwd=d)
    raw("update-ref", "refs/heads/main", tip, cwd=d)
    print("built", d, "pr", c, "main", tip)


def run(d, checker):
    r = subprocess.run((sys.executable, checker, "--no-fetch", "--base", "main", "pr"),
                       cwd=d, capture_output=True)
    sys.stdout.buffer.write(r.stdout + r.stderr)
    print(f"rc={r.returncode} fsenc={sys.getfilesystemencoding()}")


if __name__ == "__main__":
    {"build": lambda: build(sys.argv[2]), "run": lambda: run(sys.argv[2], sys.argv[3])}[sys.argv[1]]()
