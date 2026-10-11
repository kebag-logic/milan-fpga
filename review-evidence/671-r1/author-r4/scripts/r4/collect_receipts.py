"""Preserve small text receipts and hash larger artifacts without copying them.

Usage: collect_receipts.py REPO SCRATCH OUTPUT
All inputs remain in scratch. Stored text uses relative role-based paths.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

repo, scratch, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
paths = sorted(set(scratch.glob("*.log"))
               | set(scratch.glob("builder/*.log"))
               | set(scratch.glob("verilator_suites/*.log"))
               | set(scratch.glob("fwunit/*.log"))
               | set(scratch.glob("fwunit/logs/*.log"))
               | set(scratch.glob("docsrep/*.log"))
               | set(scratch.glob("docs_resume/logs/*.log"))
               | set(scratch.glob("rtlfast/logs/*.log"))
               | set(scratch.glob("final_gates/*.log"))
               | set(scratch.glob("capture/driver-*.log"))
               | set(scratch.glob("capture/*/capture-*/measurement.json")))


def public_text(text: str) -> str:
    text = re.sub(r"PATH=\S+", "PATH=<suite-tools>", text)
    for source, label in ((str(repo), "<repo>"), (str(scratch.parent), "<scratch>"),
                          (str(Path.home()), "<home>")):
        text = text.replace(source, label)
    return text


rows = ["# Round 4 receipt manifest", "", "Original byte sizes and SHA-256 hashes.",
        "Stored receipts have local paths and environment path lists normalized.", "",
        "| Scratch-relative source | Bytes | SHA-256 | Stored receipt |",
        "|---|---:|---|---|"]
for path in paths:
    raw = path.read_bytes()
    if not raw:
        continue
    relative = path.relative_to(scratch).as_posix()
    name = relative.replace("/", "__")
    if len(raw) <= 190_000:
        normalized = public_text(raw.decode(errors="replace"))
        assert len(normalized.encode()) <= 200_000
        (output / name).write_text(normalized)
        stored = name
    else:
        stored = "hash and size only"
    rows.append(f"| `{relative}` | {len(raw)} | `{hashlib.sha256(raw).hexdigest()}` | {stored} |")
(output / "MANIFEST.md").write_text("\n".join(rows) + "\n")
print(f"Recorded {len(rows) - 7} nonempty receipts; no large artifacts copied")

artifacts = ["# Round 4 capture artifacts", "", "Build products remain in scratch; only their identities are retained here.", "", "| Arm / artifact | Bytes | SHA-256 |", "|---|---:|---|"]
for receipt in sorted(scratch.glob("capture/*/capture-*/measurement.json")):
    directory = receipt.parent
    source = json.loads((directory / "sources.json").read_text())
    products = [directory / "native/Vsim", directory / "software/bios/bios.bin",
                directory / "software/libmilan_baremetal/milan_baremetal.o"]
    products += [Path(name) for name in source["sources"] if Path(name).name.startswith("VexiiRiscvLitex_")]
    for path in products:
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        artifacts.append(f"| {directory.name} / `{path.name}` | {path.stat().st_size} | `{digest}` |")
(output / "CAPTURE-ARTIFACTS.md").write_text("\n".join(artifacts) + "\n")
