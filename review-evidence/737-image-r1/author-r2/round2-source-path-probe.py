#!/usr/bin/env python3
"""Verify pinned upstream members and report absolute user paths without disclosing them."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--lock", type=Path, required=True)
parser.add_argument("--cache", type=Path, required=True)
args = parser.parse_args()
pins = json.loads(args.lock.read_text())
cases = (
    ("VexiiRiscv", "src/main/scala/vexiiriscv/soc/litex/Soc.scala"),
    ("SpinalHDL", "lib/src/main/scala/spinal/lib/eda/altera/QuartusFlow.scala"),
    ("NaxSoftware", "riscv-arch-test/rv32i_m/B/andn-01.elf"),
)
report = []
for tool, suffix in cases:
    row = next(item for item in pins["sources"] if item["tool"] == tool)
    path = args.cache / row["filename"]
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    assert actual == row["sha256"] and path.stat().st_size == row["size"]
    with tarfile.open(path) as archive:
        member = next(item for item in archive if item.name.endswith("/" + suffix))
        data = archive.extractfile(member).read()
    matches = list(re.finditer(rb"/(?:home|Users)/[^\x00\s\"']+", data))
    assert matches, suffix
    report.append({
        "tool": tool, "revision": row["version"], "source_url": row["url"],
        "archive_sha256": actual, "archive_size": row["size"], "member": suffix,
        "member_sha256": hashlib.sha256(data).hexdigest(), "member_size": len(data),
        "absolute_user_path_count": len(matches), "byte_offsets": [m.start() for m in matches],
        "source_lines": [data[:m.start()].count(b"\n") + 1 for m in matches] if suffix.endswith(".scala") else [],
        "matched_values": "REDACTED",
    })
print(json.dumps({"status": "scope conflict reproduced", "cases": report}, indent=2))
