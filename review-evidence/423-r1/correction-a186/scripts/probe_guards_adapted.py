"""Are the surviving guard mutants behaviourally distinct on real histories?

Builds two exact redundant-merge histories with raw plumbing:
  rename:    source renames a.txt -> b.txt; later tip re-adds a.txt (the
             deletion half of the source's work is reverted) + far ctl edit.
  gitlink:   source moves gitlink `sub` X -> Y; later tip resets it to X + far
             ctl edit; repository config sets diff.ignoreSubmodules=all.
  symlink:   ancestor has `p` as a symlink; source turns it into a regular
             file; tip keeps the source file plus a far extension.
Then runs the exact-head checker and a copy whose single guard is removed.
Correct verdict for rename/gitlink: UNKNOWN/1 (work not retained at tip).

Usage: probe_guards.py <clone> <workdir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

OLD = b"".join(b"line %02d\n" % i for i in range(40))
SRC = OLD.replace(b"line 05", b"source 05")
EXT = SRC.replace(b"line 35", b"later 35")
GIT = ("git", "-c", "user.name=F", "-c", "user.email=f@example.invalid")

MUTANTS = {
    "renames-folded": ('"--ignore-submodules=none", "--name-only", "--no-renames",',
                       '"--ignore-submodules=none", "--name-only",'),
    "submodules-default": ('"--ignore-submodules=none", "--name-only", "--no-renames",',
                           '"--name-only", "--no-renames",'),
    "ancestor-regular": ('for entry in (original, tip, branch)):', 'for entry in (tip, branch)):'),
}


def raw(cwd, *args, data=None):
    r = subprocess.run((*GIT, *args), input=data, capture_output=True, cwd=cwd)
    if r.returncode:
        raise SystemExit(f"fixture git {args!r}: {r.stderr!r}")
    return r.stdout.strip().decode()


def tree(cwd, entries):
    recs = b""
    for name, (mode, content) in entries.items():
        if mode == "160000":
            oid, kind = content, "commit"
        else:
            oid, kind = raw(cwd, "hash-object", "-w", "--stdin", data=content), "blob"
        recs += f"{mode} {kind} {oid}\t{name}".encode() + b"\0"
    return raw(cwd, "mktree", "-z", data=recs)


def commit(cwd, t, parents, msg):
    args = ["commit-tree", t, "-m", msg]
    for p in parents:
        args += ["-p", p]
    return raw(cwd, *args)


def history(cwd, o_entries, s_entries, tip_entries):
    """O; A (source edit); M redundant; C edits ctl; replays; later tip."""
    o = commit(cwd, tree(cwd, {**o_entries, "ctl": ("100644", OLD)}), [], "O")
    a_tree = tree(cwd, {**s_entries, "ctl": ("100644", OLD)})
    a = commit(cwd, a_tree, [o], "A")
    m = commit(cwd, a_tree, [o, a], "M redundant")
    c_tree = tree(cwd, {**s_entries, "ctl": ("100644", SRC)})
    c = commit(cwd, c_tree, [m], "C")
    ra = commit(cwd, a_tree, [o], "A'")
    rc = commit(cwd, c_tree, [ra], "C'")
    tip = commit(cwd, tree(cwd, {**tip_entries, "ctl": ("100644", EXT)}), [rc], "L")
    raw(cwd, "update-ref", "refs/heads/pr", c)
    raw(cwd, "update-ref", "refs/heads/main", tip)


def main():
    clone, work = Path(sys.argv[1]), Path(sys.argv[2])
    shutil.rmtree(work, ignore_errors=True)
    checkers = {"head": clone / "scripts" / "check_merge_containment.py"}
    for name, (before, after) in MUTANTS.items():
        d = work / "mutant" / name
        d.mkdir(parents=True)
        shutil.copy(clone / "scripts" / "check_merge_containment.py", d)
        shutil.copy(clone / "scripts" / "merge_containment_git.py", d)  # A186: new transport module
        text = (clone / "scripts" / "merge_containment_replay.py").read_text(encoding="utf-8")
        assert text.count(before) == 1, name
        (d / "merge_containment_replay.py").write_text(text.replace(before, after), encoding="utf-8")
        checkers[name] = d / "check_merge_containment.py"
    empty = None
    cases = {}
    fx = work / "rename"
    fx.mkdir(parents=True)
    raw(fx, "init", "-q", "-b", "main")
    history(fx, {"a.txt": ("100644", OLD)}, {"b.txt": ("100644", OLD)},
            {"a.txt": ("100644", OLD), "b.txt": ("100644", OLD)})
    cases["rename"] = fx
    fx = work / "gitlink"
    fx.mkdir(parents=True)
    raw(fx, "init", "-q", "-b", "main")
    empty = tree(fx, {})
    x = commit(fx, empty, [], "sub X")
    y = commit(fx, empty, [x], "sub Y")
    history(fx, {"sub": ("160000", x)}, {"sub": ("160000", y)}, {"sub": ("160000", x)})
    raw(fx, "config", "diff.ignoreSubmodules", "all")
    cases["gitlink"] = fx
    fx = work / "symlink"
    fx.mkdir(parents=True)
    raw(fx, "init", "-q", "-b", "main")
    history(fx, {"p": ("120000", b"target")}, {"p": ("100644", SRC)},
            {"p": ("100644", SRC + b"appended later\n")})
    cases["symlink"] = fx
    for case, fx in cases.items():
        for label, checker in checkers.items():
            r = subprocess.run((sys.executable, str(checker), "--no-fetch", "--base", "main", "pr"),
                               cwd=fx, capture_output=True, text=True)
            first = r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip()[-200:]
            print(f"{case:8} {label:18} rc={r.returncode} {first}")


if __name__ == "__main__":
    main()
