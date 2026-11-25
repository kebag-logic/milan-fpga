#!/usr/bin/env python3
"""Probe a tree's scripts/mutant_stage.py for the two staging findings, with independent processes.

usage: python3 -I stage_probe.py TREE SCRATCH

Every holder is its own process. It takes a slot, writes its token there, waits until every holder
of the scenario holds one (or 20 s), then reports its resolved path, whether its slot still holds
exactly its token, and any exception or stderr. A "foreign" holder runs as a real other user: the
subordinate uid 100000, entered through a user namespace (unshare + setpriv), so ownership is real.
Prints one JSON line per scenario, never asserts: the same probe runs against the old and the new
helper, and the verdict column says what happened.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOLDER = r"""
import json, os, sys, time, traceback
from pathlib import Path
sys.path.insert(0, sys.argv[1])
token, prefix, parent, sync, count = sys.argv[2:7]
out = {"token": token}
try:
    import mutant_stage
    with mutant_stage.directory(prefix, parent or None) as held:
        out["path"] = os.path.realpath(held)
        Path(held, "owner").write_text(token)
        Path(sync, token).touch()
        deadline = time.monotonic() + 20
        while len(os.listdir(sync)) < int(count) and time.monotonic() < deadline:
            time.sleep(0.01)
        out.update(path=os.path.realpath(held), all_held=len(os.listdir(sync)) >= int(count),
                   kept=sorted(os.listdir(held)) == ["owner"] and Path(held, "owner").read_text() == token)
except Exception as exc:
    out["raised"] = f"{type(exc).__name__}: {exc}"
    Path(sync, token).touch()
print(json.dumps(out))
"""
FOREIGN = ["unshare", "--map-root-user", "--map-users=1:100000:1", "--map-groups=1:100000:1",
           "setpriv", "--reuid=1", "--regid=1", "--clear-groups"]


def as_foreign(*argv: str) -> None:
    subprocess.run([*FOREIGN, *argv], check=False)


def holders(tree: Path, specs: list[dict], sync: Path) -> list[dict]:
    sync.mkdir()
    os.chmod(sync, 0o1777)
    procs = []
    for n, spec in enumerate(specs):
        env = {"PATH": os.environ["PATH"], "TMPDIR": spec["tmpdir"], "HOME": "/nonexistent"}
        argv = [sys.executable, "-I", "-c", HOLDER, str(tree / "scripts"), f"h{n}", spec["prefix"],
                str(spec.get("parent", "")), str(sync), str(len(specs))]
        if spec.get("foreign"):
            argv = [*FOREIGN, *argv]
        procs.append(subprocess.Popen(argv, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    out = []
    for proc in procs:
        o, e = proc.communicate(timeout=120)
        rep = json.loads(o) if o.strip() else {"raised": f"exit {proc.returncode}"}
        rep["stderr"] = e.strip()
        out.append(rep)
    shutil.rmtree(sync)
    return out


def isolation(reports: list[dict]) -> str:
    paths = [r.get("path") for r in reports if r.get("path")]
    raised = "; ".join(r["raised"] for r in reports if "raised" in r)
    if len(set(paths)) < len(paths):
        return "COLLISION (one physical slot handed to two live holders)" + (f"; the victim raised {raised}" if raised else "")
    if raised:
        return "RAISED " + raised
    if not all(r["kept"] for r in reports):
        return "COLLISION (a live holder's file was erased)"
    return "isolated"


def root_verdict(report: dict, root: Path) -> str:
    if "raised" in report:
        return "RAISED " + report["raised"]
    inside = report["path"].startswith(os.path.realpath(root) + "/") or report["path"].startswith(str(root) + "/")
    return ("ACCEPTED (staged inside the planted root)" if inside
            else "REFUSED (staged elsewhere)" + (f"; stderr: {report['stderr']}" if report["stderr"] else ""))


def main() -> int:
    tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scratch.mkdir(parents=True)
    os.chmod(scratch, 0o755)
    uid = os.getuid()

    def emit(name: str, verdict: str, reports: list[dict]) -> None:
        print(json.dumps({"scenario": name, "verdict": verdict,
                          "holders": [{k: v for k, v in r.items() if k != "token"} for r in reports]}), flush=True)

    t1 = scratch / "t1"; t1.mkdir(mode=0o700)
    t2 = scratch / "t2"; t2.mkdir(mode=0o700)
    reps = holders(tree, [{"prefix": "race-", "tmpdir": str(t1)} for _ in range(6)], scratch / "s")
    emit("six holders race for one slot, one TMPDIR", isolation(reps), reps)

    parent = scratch / "parent"; parent.mkdir()
    reps = holders(tree, [{"prefix": "split-mutants-", "parent": parent, "tmpdir": str(t1)},
                          {"prefix": "split-mutants-", "parent": parent, "tmpdir": str(t2)}], scratch / "s")
    emit("in-tree, same parent, two TMPDIRs (R924-1-F1)", isolation(reps), reps)

    alias = scratch / "t1-alias"; alias.symlink_to(t1)
    reps = holders(tree, [{"prefix": "alias-", "tmpdir": str(t1)}, {"prefix": "alias-", "tmpdir": str(alias)}],
                   scratch / "s")
    emit("TMPDIR and a symbolic link to it (R923-1-F1)", isolation(reps), reps)

    palias = scratch / "parent-alias"; palias.symlink_to(parent)
    reps = holders(tree, [{"prefix": "palias-", "parent": parent, "tmpdir": str(t1)},
                          {"prefix": "palias-", "parent": palias, "tmpdir": str(t1)}], scratch / "s")
    emit("in-tree parent and a symbolic link to it", isolation(reps), reps)

    shared = scratch / "shared-parent"; shared.mkdir(); os.chmod(shared, 0o1777)
    ft = scratch / "foreign-tmp"; ft.mkdir(); os.chmod(ft, 0o1777)
    reps = holders(tree, [{"prefix": "split-mutants-", "parent": shared, "tmpdir": str(t1)},
                          {"prefix": "split-mutants-", "parent": shared, "tmpdir": str(ft), "foreign": True}],
                   scratch / "s")
    emit("in-tree, two real users, one shared parent", isolation(reps), reps)
    as_foreign("rm", "-rf", *[str(p) for p in [*shared.iterdir(), *ft.iterdir()] if p.lstat().st_uid != uid])

    def root_case(name: str, plant) -> None:
        case = scratch / ("root-" + name.split()[0]); case.mkdir(mode=0o700)
        root = case / f"milan-mutant-stage-{uid}"
        plant(case, root)
        rep, = holders(tree, [{"prefix": "probe-", "tmpdir": str(case)}], scratch / "s")
        emit(name, root_verdict(rep, root), [rep])

    def symlink(case: Path, root: Path) -> None:
        (case / "chosen-elsewhere").mkdir(); os.chmod(case / "chosen-elsewhere", 0o777)
        root.symlink_to(case / "chosen-elsewhere")

    def writable(case: Path, root: Path) -> None:
        root.mkdir(); os.chmod(root, 0o777)

    def foreign(case: Path, root: Path) -> None:
        os.chmod(case, 0o1777)
        as_foreign("mkdir", "-m", "0777", str(root))

    def locksfile(case: Path, root: Path) -> None:
        root.mkdir(); (root / "locks").write_text("")

    root_case("symlinked root", symlink)
    root_case("world-writable root", writable)
    root_case("foreign-owned root (real uid 100000, mode 0777)", foreign)
    root_case("locks-is-a-file root", locksfile)
    base = scratch / "open-base"; base.mkdir(); os.chmod(base, 0o777)
    rep, = holders(tree, [{"prefix": "probe-", "tmpdir": str(base)}], scratch / "s")
    emit("TMPDIR writable by others, not sticky", root_verdict(rep, base / f"milan-mutant-stage-{uid}"), [rep])
    as_foreign("rm", "-rf", *[str(p) for p in scratch.rglob("*") if p.lstat().st_uid == 100000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
