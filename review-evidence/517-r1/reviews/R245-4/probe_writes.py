#!/usr/bin/env python3
"""Reviewer write-set probe for the eleven pooled milan_dp legs (#517 R245-4).

Two independent observers:
  * a file-operation trace per leg (strace -f, every write-capable open,
    create, mkdir, rename, unlink, link, truncate, chmod, utime and chdir,
    with resolved fd paths), from which the leg's set of WRITTEN paths is
    derived; transient files created and deleted inside the leg still appear;
  * a whole-tree metadata snapshot of the repository (every file AND
    directory, ignored and untracked included: mtime_ns, ctime_ns, size,
    inode), taken before and after a phase; a directory entry created and
    removed again still moves its parent's mtime.

Subcommands (each fits one foreground command):
  snapshot NAME            write snapshots/NAME.json
  diff A B                 list every path whose metadata differs
  run TAG CAP LEG...       run legs (<= CAP at once) from the suite dir with a
                           shared TMPDIR, each under strace; results/TAG-*.json
  pc                       planted positive controls through the same trace
                           parser (tracked same-byte rewrite, real root-mode
                           builder rewrite, two writers of one private path)
  analyze TAG...           per-leg write sets and pairwise intersections
Paths: REPO, OUT from the environment (defaults: cwd, ./probe-out).
"""

import json
import os
import re
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

REPO = Path(os.environ.get("REPO", os.getcwd())).resolve()
OUT = Path(os.environ.get("OUT", "probe-out")).resolve()
SUITE = REPO / "tb/verilator/milan_dp"
TMP = OUT / "tmp-common"
TRACE = ("openat,open,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,"
         "unlinkat,rmdir,link,linkat,symlink,symlinkat,truncate,ftruncate,"
         "chmod,fchmodat,utimensat,utime,utimes,chdir,fchdir,mknod,mknodat")
WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
LINE = re.compile(r"^(\d+)\s+(\w+)\((.*)\)\s+=\s+(-?\d+)(<[^>]*>)?")
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')


def snapshot(name: str) -> None:
    meta = {}
    for root, dirs, files in os.walk(REPO):
        for entry in dirs + files:
            p = os.path.join(root, entry)
            st = os.lstat(p)
            meta[os.path.relpath(p, REPO)] = [st.st_mtime_ns, st.st_ctime_ns,
                                              st.st_size, st.st_ino]
    st = os.lstat(REPO)
    meta["."] = [st.st_mtime_ns, st.st_ctime_ns, st.st_size, st.st_ino]
    (OUT / "snapshots").mkdir(parents=True, exist_ok=True)
    (OUT / "snapshots" / f"{name}.json").write_text(json.dumps(meta))
    print(f"snapshot {name}: {len(meta)} entries")


def diff(a: str, b: str) -> int:
    ma = json.loads((OUT / "snapshots" / f"{a}.json").read_text())
    mb = json.loads((OUT / "snapshots" / f"{b}.json").read_text())
    changed = sorted(p for p in set(ma) | set(mb) if ma.get(p) != mb.get(p))
    for p in changed:
        print(f"CHANGED {p}: {ma.get(p)} -> {mb.get(p)}")
    print(f"diff {a} {b}: {len(changed)} changed of {len(mb)}")
    return len(changed)


def parse(trace: Path, cwd: Path) -> dict:
    """Return written paths and every mutating call, resolved to absolute."""
    written, calls, chdirs, fails = set(), [], [], []
    for raw in trace.read_text(errors="replace").splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        pid, call, args, ret, fdpath = m.groups()
        strs = STR.findall(args)
        ok = int(ret) >= 0
        if call in ("chdir", "fchdir"):
            chdirs.append(raw)
            continue
        # *at calls: every path string is relative to the dirfd before it,
        # which -y prints as AT_FDCWD</cwd> or N</dir>
        bases = [Path(b) for b in re.findall(r"(?:AT_FDCWD|\b\d+)<([^>]*)>", args)]
        if call in ("openat", "open", "creat"):
            if call != "creat" and not any(f in args for f in WRITE_FLAGS):
                continue
        if call == "ftruncate":
            paths = bases[:1]
        elif call == "symlinkat":                 # target is not written
            paths = [bases[0] / strs[1]] if bases and len(strs) > 1 else []
        elif call == "symlink":
            paths = [Path(strs[1])] if len(strs) > 1 else []
        elif call.endswith("at") or call == "renameat2":
            paths = [b / s for b, s in zip(bases, strs)]
        else:
            paths = [Path(s) for s in strs[:2]] if call in ("rename", "link") else [Path(s) for s in strs[:1]]
        if call in ("openat", "open", "creat") and ok and fdpath:
            paths = [Path(fdpath[1:-1])]
        paths = [p if p.is_absolute() else cwd / p for p in paths]
        if not ok:
            fails.append(raw)
            continue
        for p in paths:
            path = os.path.normpath(str(p))
            if path.startswith(("/dev/", "/proc/")) or path.startswith("pipe:"):
                continue
            written.add(path)
            calls.append(f"{call} {path}")
    return {"written": sorted(written), "calls": calls, "chdirs": chdirs,
            "failed_mutations": fails}


def classify(paths: list[str]) -> dict:
    repo = [p for p in paths if p == str(REPO) or p.startswith(str(REPO) + "/")]
    tmp = [p for p in paths if p.startswith(str(TMP) + "/")]
    other = [p for p in paths if p not in repo and p not in tmp]
    return {"repo": repo, "tmpdir": tmp, "other": other}


def launch(tag: str, argv: list[str], cwd: Path, env: dict) -> tuple:
    cap = OUT / "captures" / f"{tag}.log"
    tr = OUT / "traces" / f"{tag}.strace"
    cap.parent.mkdir(parents=True, exist_ok=True)
    tr.parent.mkdir(parents=True, exist_ok=True)
    full = ["strace", "-f", "-qq", "-y", "-s", "4096", "-o", str(tr), "-e",
            f"trace={TRACE}"] + argv
    fh = cap.open("wb")
    proc = subprocess.Popen(full, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            stdout=fh, stderr=subprocess.STDOUT)
    return proc, fh, cap, tr, time.monotonic()


def finish(tag, proc, fh, cap, tr, t0, cwd) -> dict:
    rc = proc.wait()
    fh.close()
    res = {"tag": tag, "exit": rc, "seconds": round(time.monotonic() - t0, 3),
           "capture": str(cap.relative_to(OUT)),
           "capture_sha256": subprocess.run(["sha256sum", str(cap)], capture_output=True,
                                            text=True).stdout.split()[0]}
    res.update(parse(tr, cwd))
    res["classified"] = classify(res["written"])
    (OUT / "results").mkdir(parents=True, exist_ok=True)
    (OUT / "results" / f"{tag}.json").write_text(json.dumps(res, indent=1))
    return res


def run(tag: str, cap: int, legs: list[str]) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(TMP))
    env.pop("MILAN_COUNTER_FRAME_OUT", None)
    pending, live = list(legs), []
    while pending or live:
        while pending and len(live) < cap:
            leg = pending.pop(0)
            name = f"{tag}-{leg.split('/')[1]}"
            live.append((name,) + launch(name, [f"./{leg}"], SUITE, env))
        name, proc, fh, capf, tr, t0 = live[0]
        for item in live:
            if item[1].poll() is not None:
                name, proc, fh, capf, tr, t0 = item
                break
        else:
            time.sleep(0.5)
            continue
        live.remove((name, proc, fh, capf, tr, t0))
        r = finish(name, proc, fh, capf, tr, t0, SUITE)
        c = r["classified"]
        print(f"{name}: exit={r['exit']} {r['seconds']}s repo={len(c['repo'])} "
              f"tmpdir={len(c['tmpdir'])} other={len(c['other'])} chdir={len(r['chdirs'])}",
              flush=True)


def pc() -> None:
    """Planted positive controls, through launch/finish/parse unchanged."""
    TMP.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(TMP))
    hdr = REPO / "configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh"
    keep = hdr.read_bytes(), os.stat(hdr).st_mtime_ns
    rows = []
    # PC1: a same-byte rewrite of a tracked header from the suite directory
    rows.append(finish("pc1-samebyte", *launch("pc1-samebyte", [
        "python3", "-c", "import sys;p=sys.argv[1];b=open(p,'rb').read();open(p,'wb').write(b)",
        str(hdr)], SUITE, env), SUITE))
    # PC2: the real builder invoked from the repository root (the write path
    # the round-4 premise described), into a private -o directory
    rows.append(finish("pc2-rootbuilder", *launch("pc2-rootbuilder", [
        "python3", "sw/builder/endstation_builder.py", "configs/endstation_arty_4x4.yaml",
        "-o", str(OUT / "pc2-out")], REPO, env), REPO))
    # PC3/PC4: two writers of one private path, for the intersection check
    for t in ("pc3-shared-a", "pc4-shared-b"):
        rows.append(finish(t, *launch(t, ["sh", "-c", f"echo {t} > \"$TMPDIR/shared.txt\""],
                                      SUITE, env), SUITE))
    if hdr.read_bytes() != keep[0]:
        hdr.write_bytes(keep[0])
        print("PC restored header bytes")
    os.utime(hdr, ns=(keep[1], keep[1]))
    for r in rows:
        c = r["classified"]
        print(f"{r['tag']}: exit={r['exit']} repo={c['repo']} tmpdir={c['tmpdir']}")


def analyze(tags: list[str]) -> None:
    res = []
    for t in tags:
        res += [json.loads(p.read_text()) for p in sorted((OUT / "results").glob(f"{t}-*.json"))]
    summary = {}
    for r in res:
        c = r["classified"]
        files = [p for p in r["written"] if not any(q.startswith(p + "/") for q in r["written"])]
        summary[r["tag"]] = {"exit": r["exit"], "seconds": r["seconds"],
                             "repo_writes": c["repo"], "other_writes": c["other"],
                             "tmpdir_leaf_paths": [p for p in files if p in c["tmpdir"]],
                             "chdirs": len(r["chdirs"])}
    shared = []
    for a, b in combinations(res, 2):
        inter = sorted((set(a["written"]) & set(b["written"])) - {str(TMP)})
        if inter:
            shared.append({"a": a["tag"], "b": b["tag"], "paths": inter})
    out = {"legs": summary, "shared_written_paths": shared}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "snapshot":
        snapshot(args[0])
    elif cmd == "diff":
        sys.exit(0 if diff(args[0], args[1]) == 0 else 3)
    elif cmd == "run":
        run(args[0], int(args[1]), args[2:])
    elif cmd == "pc":
        pc()
    elif cmd == "analyze":
        analyze(args)
    elif cmd == "reparse":                        # re-derive results from kept traces
        for tag in args:
            res = json.loads((OUT / "results" / f"{tag}.json").read_text())
            cwd = REPO if tag.startswith("pc2") else SUITE
            res.update(parse(OUT / "traces" / f"{tag}.strace", cwd))
            res["classified"] = classify(res["written"])
            (OUT / "results" / f"{tag}.json").write_text(json.dumps(res, indent=1))
            c = res["classified"]
            print(f"{tag}: exit={res['exit']} repo={len(c['repo'])} tmpdir={len(c['tmpdir'])} "
                  f"other={len(c['other'])} chdir={len(res['chdirs'])}")
