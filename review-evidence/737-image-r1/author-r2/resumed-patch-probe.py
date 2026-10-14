#!/usr/bin/env python3
"""Reproduce the pinned CPU patch versus whole-file privacy allowance conflict."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tree", type=Path, required=True)
parser.add_argument("--cache", type=Path, required=True)
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.tree / "ci/image"))
import privacy

pins = json.loads((args.tree / "ci/image/sources.lock.json").read_text())
row = next(item for item in pins["sources"] if item["tool"] == "VexiiRiscv")
archive = args.cache / row["filename"]
with archive.open("rb") as stream:
    assert hashlib.file_digest(stream, "sha256").hexdigest() == row["sha256"]
assert archive.stat().st_size == row["size"]
relative = "src/main/scala/vexiiriscv/soc/litex/Soc.scala"
with tarfile.open(archive) as stream:
    member = next(item for item in stream if item.name.endswith("/" + relative))
    original = stream.extractfile(member).read()
patch = args.tree / "sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch"
with tempfile.TemporaryDirectory(dir=args.scratch, prefix="patch-conflict-") as work:
    target = Path(work) / "pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv" / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(original)
    result = subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(patch.resolve())],
                            cwd=work, capture_output=True, check=True)
    patched = target.read_bytes()
assert original != patched
policy = privacy.Policy()
original_sha = hashlib.sha256(original).hexdigest()
patched_sha = hashlib.sha256(patched).hexdigest()
proof = {original_sha: {"tool": row["tool"], "pin": row["version"],
                       "source_sha256": row["sha256"], "member_sha256": original_sha}}
allowed = []
privacy.check_file(io.BytesIO(original), "opt/cpu/Soc.scala", policy, proof, allowed)
assert len(allowed) == 1
try:
    privacy.check_file(io.BytesIO(patched), "opt/cpu/Soc.scala", policy, proof, [])
except ValueError:
    refused = True
else:
    refused = False
assert refused
paths = next(pattern for name, pattern, _ in policy.rules if name == "absolute-user-path")
assert len(list(paths.finditer(original))) == len(list(paths.finditer(patched))) == 3
report = {
    "meaning": "Reproduced scope conflict; this is not image acceptance",
    "source_pin": row["version"], "source_archive_sha256": row["sha256"],
    "source_file": relative, "original_sha256": original_sha,
    "patch": patch.relative_to(args.tree).as_posix(),
    "patch_sha256": hashlib.sha256(patch.read_bytes()).hexdigest(), "patch_rc": result.returncode,
    "patched_sha256": patched_sha,
    "original_path_lines": [i for i, line in enumerate(original.splitlines(), 1) if paths.search(line)],
    "patched_path_lines": [i for i, line in enumerate(patched.splitlines(), 1) if paths.search(line)],
    "unchanged_upstream_allowed": True, "workflow_patched_copy_refused": refused,
    "protected_strings": "Redacted; only counts, locations and content hashes are recorded"
}
print(json.dumps(report, indent=2, sort_keys=True))
