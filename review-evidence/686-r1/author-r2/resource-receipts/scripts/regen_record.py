#!/usr/bin/env python3
"""Regenerate one resource-gate record from its receipts and compare it (issue #686).

usage: regen_record.py <repo> <receipt-dir> <endpoint> [--git <commit>] [--baseline <json>]

<repo> is a clone of the repository. Without --git it must be checked out at
the commit whose syn/ooc/pp_resource_baseline.json holds the record, with its
submodules initialised at their pins. With --git <commit>, every repository
file (the gate's own parsers, the baseline and each repo input) is read from
that commit's objects instead, a file inside a submodule from the submodule's
pinned commit, so the working tree may be at any commit. The script uses that
commit's own syn/ooc/pp_resource_gate.py parsers, so nothing here
re-implements a figure:
  figures  utilization() on baseline_utilization.rpt, timing() on the Design
           Timing Summary excerpt, census() on the CARRY4 rows of the census
           (the census counts nothing else);
  scopes   scopes() on baseline_hierarchy.rpt with that census;
  identity identity() on the executed script, the utilization report and
           clock.xdc;
  inputs   the digest recomputed from inputs.manifest.json, after every repo
           entry is re-hashed from the repository and every copied entry from
           its copy.
A route endpoint's route status is also read through routing(). Exit 0 when
the regenerated record equals the baseline's endpoint record and the route
(if any) is complete; 1 otherwise.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def main(modules: Path) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    parser.add_argument("receipts", type=Path)
    parser.add_argument("endpoint")
    parser.add_argument("--git", metavar="COMMIT")
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    repo, rdir, endpoint = args.repo.resolve(), args.receipts.resolve(), args.endpoint
    if args.git:
        links = {}
        for line in git(repo, "ls-tree", "-r", args.git).decode().splitlines():
            meta, path = line.split("\t", 1)
            mode, kind_, sha = meta.split()
            if mode == "160000":
                links[path] = sha

        def read(path: str) -> bytes:
            for link, sha in links.items():
                if path.startswith(link + "/"):
                    return git(repo / link, "show", f"{sha}:{path[len(link) + 1:]}")
            return git(repo, "show", f"{args.git}:{path}")

        for name in git(repo, "ls-tree", "--name-only", args.git, "syn/ooc/").decode().split():
            if name.endswith(".py"):
                (modules / Path(name).name).write_bytes(read(name))
        committed_text = read("syn/ooc/pp_resource_baseline.json").decode()
    else:
        def read(path: str) -> bytes:
            return (repo / path).read_bytes()

        for path in (repo / "syn/ooc").glob("*.py"):
            (modules / path.name).write_bytes(path.read_bytes())
        committed_text = (repo / "syn/ooc/pp_resource_baseline.json").read_text()
    if args.baseline:
        committed_text = args.baseline.read_text()
    sys.path.insert(0, str(modules))
    import pp_resource_gate as gate  # noqa: E402

    manifest = json.loads((rdir / "inputs.manifest.json").read_text())
    kind = manifest["kind"]
    problems = []
    digest = hashlib.sha256()
    for entry in manifest["files"]:
        if entry["role"] == "repo":
            data = read(entry["path"])
        else:
            raw = (rdir / entry["copy"]).read_bytes()
            data = gzip.decompress(raw) if entry["copy"].endswith(".gz") else raw
        sha = hashlib.sha256(data).hexdigest()
        if sha != entry["sha256"]:
            problems.append(f"input {entry.get('path', entry.get('copy'))}: sha256 {sha} != manifest {entry['sha256']}")
        digest.update(entry["name"].encode() + b"\0" + hashlib.sha256(data).digest())
    for generic in manifest["generics"]:
        digest.update(generic.encode() + b"\0")
    for image in manifest["images"]:
        digest.update(f"{image['name']}\0{image['sha256']}\0".encode())

    with tempfile.TemporaryDirectory() as scratch:
        work = Path(scratch)
        for path in rdir.iterdir():  # every receipt, decompressed, under its report name
            if path.is_file():
                data = path.read_bytes()
                name = path.name
                if name.endswith(".gz"):
                    data, name = gzip.decompress(data), name[:-3]
                (work / name).write_bytes(data)
        (work / "baseline_cells.tsv").write_bytes((work / "baseline_cells.carry4.tsv").read_bytes())
        script = (work / gate.SCRIPTS[kind]).read_text()
        report = (work / "baseline_utilization.rpt").read_text()
        figures = gate.utilization(report, kind)
        figures.update(gate.timing((work / "baseline_timing.summary.rpt").read_text()))
        carry = gate.census(work)
        figures["CARRY4"] = carry[""]
        regenerated = {"kind": kind, "identity": gate.identity(work, script, report),
                       "inputs_sha256": digest.hexdigest(), "figures": figures,
                       "scopes": gate.scopes(work, kind, carry)}
        unrouted = gate.routing(work, kind) if kind == "route" else []
    committed = json.loads(committed_text)["endpoints"][endpoint]["record"]
    receipt = json.loads((rdir / "record.json").read_text())
    for name, other in (("committed baseline", committed), ("receipt record.json", receipt)):
        if regenerated != other:
            keys = sorted(k for k in regenerated if regenerated[k] != other.get(k))
            problems.append(f"regenerated record differs from the {name} in {', '.join(keys)}")
    if kind == "route":
        problems += [f"route incomplete: {line}" for line in unrouted]
        print(f"route status: {'complete' if not unrouted else 'INCOMPLETE'}")
    print(f"{endpoint}: inputs_sha256 {regenerated['inputs_sha256']}")
    print(f"{endpoint}: " + ", ".join(f"{k} {v}" for k, v in figures.items()))
    for line in problems:
        print(f"[FAIL] {line}")
    print(f"{endpoint}: {'record EQUAL' if not problems else 'record NOT reproduced'}")
    return 1 if problems else 0


if __name__ == "__main__":
    scratch = Path(tempfile.mkdtemp(prefix="regen-gate-"))
    try:
        raise SystemExit(main(scratch))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
