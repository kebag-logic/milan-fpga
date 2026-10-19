#!/usr/bin/env python3
"""Read-only source and published-packet audit. Run: python3 audit.py SOURCE_ROOT."""
import ast
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
HEAD = "2022d363fc622f6bbf4c312239fc3db741b4d29a"
TREE = "249bdbe6209bbc7ec17a816c26823ad97bb6d748"

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

def source_identity():
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert git("ls-files", "--stage", "-z") == b"".join(
        mode + b" " + oid + b" 0\t" + path + b"\0"
        for record in git("ls-tree", "-rz", HEAD).split(b"\0") if record
        for meta, path in [record.split(b"\t", 1)]
        for mode, kind, oid in [meta.split(b" ")]
    )
    n = 0
    links = []
    for record in git("ls-tree", "-rz", HEAD).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        f = ROOT / os.fsdecode(path)
        if mode == b"160000":
            links.append((os.fsdecode(path), oid.decode()))
            continue
        data = os.fsencode(os.readlink(f)) if mode == b"120000" else f.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), str(f)
        if mode != b"120000":
            assert bool(f.stat().st_mode & 0o111) == (mode == b"100755"), str(f)
        n += 1
    assert not links, links
    print(f"Source: {HEAD}; tree {TREE}; {n} tracked blobs, modes and index match; no submodule gitlinks.")

def evidence():
    rows = json.loads((PACKET / "evidence/MANIFEST.json").read_text())
    manifest = {r["file"]: r for r in rows}
    tree = {r["path"]: r for r in json.loads((PACKET / "public/evidence-tree.json").read_text())["tree"]}
    prefix = "review-evidence/gptp84-r1/"
    n = 0
    for f in sorted((PACKET / "evidence").rglob("*")):
        if not f.is_file():
            continue
        name = f.relative_to(PACKET / "evidence").as_posix()
        data = f.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert blob == tree[prefix + name]["sha"], name
        if name != "MANIFEST.json":
            assert hashlib.sha256(data).hexdigest() == manifest[name]["published_sha256"], name
        n += 1
    print(f"Published evidence: {n} fetched files match pinned Git blobs and applicable published SHA-256 entries.")
    for version in ["author-r2", "author-r3"]:
        index = (PACKET / "evidence" / version / "receipts/INDEX.md").read_text()
        entries = re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]+)` \|$", index, re.M)
        expected = {a[len(prefix + version + '/receipts/'):] for a, x in tree.items()
                    if a.startswith(prefix + version + '/receipts/') and x['type'] == 'blob'
                    and not a.endswith('/INDEX.md')}
        assert {a for a, _, _ in entries} == expected
        for name, size, digest in entries:
            m = manifest[version + '/receipts/' + name]
            assert m['original_sha256'].startswith(digest), name
            if not m['path_redacted']:
                assert int(size) == tree[prefix + version + '/receipts/' + name]['size'], name
        print(f"{version} receipt index: {len(entries)} entries exactly cover pinned receipt files; original digests match manifest; unredacted sizes match.")
    for name in ["packet-commit", "source-commit"]:
        v = json.loads((PACKET / "public" / (name + ".json")).read_text())["verification"]
        print(f"{name} signature status: verified={v['verified']}, reason={v['reason']} (no signature assurance claimed).")

def light_checks():
    scratch = PACKET / "scratch" / "images"
    scratch.mkdir(parents=True, exist_ok=True)
    tasks = [
        ("contract", ["make", "-j16", "contract"]),
        ("docs", ["make", "-j16", "docs"]),
        ("diagrams", ["make", "-j16", "diagrams-check"]),
    ]
    def run(task):
        name, cmd = task
        result = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (PACKET / (name + ".log")).write_bytes(result.stdout)
        (PACKET / (name + ".rc")).write_text(str(result.returncode) + "\n")
        assert result.returncode == 0, name
        return name + ": rc=0"
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run, tasks):
            print(result)
    recipes = [
        ("tb/verilator/engine/gptp_ucode.hex", ["--clk-hz", "2000000", "--cease-ms", "3000"]),
        ("tb/verilator/ucpu/gptp_ucode.hex", []),
        ("tb/tsngen/gptp_ucode.hex", ["--clk-hz", "2000000"]),
        ("syn/ooc/work/gptp_ucode.hex", []),
    ]
    for i, (tracked, args) in enumerate(recipes):
        out = scratch / f"{i}.hex"
        result = subprocess.check_output([sys.executable, str(ROOT / "hdl/ucode/gen_gptp_ucode.py"), *args, "-o", str(out)])
        assert b"1015 real (99.1%)" in result
        assert out.read_bytes() == (ROOT / tracked).read_bytes()
        print(f"ROM: {tracked}: 1015/1024 used, nine free, regenerated bytes match; sha256={hashlib.sha256(out.read_bytes()).hexdigest()}")
    old = git("show", "53ac2e9d:hdl/ucode/gen_gptp_ucode.py").decode()
    new = (ROOT / "hdl/ucode/gen_gptp_ucode.py").read_text()
    def executable(src):
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                node.body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
        return ast.dump(tree, include_attributes=False)
    assert executable(old) == executable(new)
    assert not git("diff", "53ac2e9d", HEAD, "--", "*.sv", "*.hex")
    print("Delta: generator executable AST, all RTL and all committed ROM images unchanged from 53ac2e9d.")

source_identity()
if "--identity-only" not in sys.argv[2:]:
    evidence()
    light_checks()
    source_identity()
