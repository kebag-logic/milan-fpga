#!/usr/bin/env python3
"""Read-only source, interface, image and final tracked-byte integrity checks."""
import hashlib
import io
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
packet = pathlib.Path(__file__).resolve().parents[1]
root = pathlib.Path(sys.argv[1]).resolve()
head = "334e9fe64dfff5568be58a0dc9aeb302959b3b58"
tree = "fdb142e8ffb1a8f68158feaf00d486f6f5e3c3e2"
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == tree
entries = []
gitlinks = []
for record in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not record:
        continue
    meta, name = record.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    rel = name.decode()
    if kind == "commit":
        gitlinks.append({"path": rel, "oid": oid})
        continue
    p = root / rel
    data = os.readlink(p).encode() if mode == "120000" else p.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == oid, rel
    if mode != "120000":
        assert bool(p.stat().st_mode & stat.S_IXUSR) == (mode == "100755"), rel
    entries.append({"path": rel, "mode": mode, "blob": oid})
assert not gitlinks, "this donor has no nested submodules"
expected_index = sorted((e["mode"], e["blob"], e["path"]) for e in entries)
actual_index = []
for record in git("ls-files", "--stage", "-z").split(b"\0"):
    if not record:
        continue
    meta, name = record.split(b"\t", 1)
    mode, oid, stage = meta.decode().split()
    assert stage == "0"
    actual_index.append((mode, oid, name.decode()))
assert expected_index == sorted(actual_index)
assert not git("status", "--porcelain=v1", "--untracked-files=all").strip()
(packet / "receipts/source-integrity.json").write_text(json.dumps({"head": head, "tree": tree, "tracked_files": len(entries), "gitlinks": gitlinks, "index_matches_tree": True, "blobs_and_modes_match": True, "status_clean": True}, indent=2) + "\n")
print("PASS exact HEAD/tree,", len(entries), "tracked blobs and modes, index, clean status; no nested gitlinks")

headers = {}
for revision in ["b9ade3a63d1b2292d75eb9b1809647e6439542a0", "8f3c376d1e07d2f1417889ae2ac590c71b8cb910", head, "e4869fd0c42889b2ac806587cc5c78afb1c33461"]:
    text = git("show", revision + ":hdl/top/KL_gptp_engine.sv").decode()
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    header = re.search(r"module\s+KL_gptp_engine\b.*?\);", text, re.S).group()
    normalized = re.sub(r"\s+", "", header)
    headers[revision] = hashlib.sha256(normalized.encode()).hexdigest()
assert len(set(headers.values())) == 1
(packet / "receipts/interfaces.json").write_text(json.dumps(headers, indent=2) + "\n")
print("PASS parent pin/base/prior/current parameter and port token sequences identical")

work = packet / "scratch/source-checks"
work.mkdir(exist_ok=True)
generator = root / "hdl/ucode/gen_gptp_ucode.py"
images = [
    ("tb/verilator/engine/gptp_ucode.hex", ["--clk-hz", "2000000", "--cease-ms", "3000"]),
    ("tb/tsngen/gptp_ucode.hex", ["--clk-hz", "2000000"]),
    ("tb/verilator/ucpu/gptp_ucode.hex", []),
    ("syn/ooc/work/gptp_ucode.hex", []),
]
for i, (rel, args) in enumerate(images):
    dest = work / f"tracked-{i}.hex"
    subprocess.run([sys.executable, str(generator), *args, "-o", str(dest)], check=True, capture_output=True)
    assert dest.read_bytes() == (root / rel).read_bytes(), rel
    print("PASS regenerated", rel, hashlib.sha256(dest.read_bytes()).hexdigest())
for priority in [0, 248, 254, 255]:
    dest = work / f"priority-{priority}.hex"
    subprocess.run([sys.executable, str(generator), "--mac", "0x021122334455", "--p1", str(priority), "--clk-hz", "125000000", "-o", str(dest)], check=True, capture_output=True)
    words = [int(line, 16) for line in dest.read_text().splitlines()]
    assert len(words) == 1024
    assert ((words[1022] & 0xffffffff) << 32 | words[1023]) == 0x021122fffe334455
    assert ((words[1022] >> 32) & 1) == (priority < 255)
    print("PASS custom identity at priority1", priority, "and 125 MHz")
basegen = work / "basegen.py"
basegen.write_bytes(git("show", "b9ade3a63d1b2292d75eb9b1809647e6439542a0:hdl/ucode/gen_gptp_ucode.py"))
helper = packet / "scratch/public/author-r3/receipts/r3/scripts/romlayout.py"
for name, gen in [("base", basegen), ("head", generator)]:
    for seed, sync in [("0", "0"), ("0x200000", "0"), ("0", "0x10000")]:
        result = subprocess.run([sys.executable, str(helper), str(gen), seed, sync], env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True)
        assert result.returncode == 0 and "used " in result.stdout and "Traceback" not in result.stderr
        print("PASS layout", name, seed, sync, result.stdout.splitlines()[-1])

export = packet / "scratch/checked-source"
if not export.exists():
    export.mkdir()
    with tarfile.open(fileobj=io.BytesIO(git("archive", "HEAD"))) as archive:
        archive.extractall(export, filter="data")
print("PASS source checks; isolated archive ready for documentation and contract checks")
