#!/usr/bin/env python3
"""Compare local rebuilt images with exact-head published size evidence."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parent
expected = json.loads((packet / "public-evidence/ROUND8-SIZES.json").read_text())
ours = json.loads((packet / "receipts/srp-images-size.json").read_text())
comparisons = []
for actual, reference in zip(ours, expected["srp_images"], strict=True):
    for key in ("shape", "interfaces", "sections", "static_storage", "ram_span", "ram_sections"):
        assert actual[key] == reference[key], (key, actual[key], reference[key])
    elf = next(a for a in actual["artifacts"] if a["name"] == "ctrl_app.elf")
    assert elf == next(a for a in reference["artifacts"] if a["name"] == "ctrl_app.elf")
    comparisons.append({"shape": actual["shape"], "interfaces": actual["interfaces"],
                        "sections_storage_span_and_elf_match": True, "elf_sha256": elf["sha256"]})
f3 = []
for reference in expected["f3_artifacts"]:
    if not reference["path"].endswith(".elf"):
        continue
    path = packet / "scratch" / reference["path"].removeprefix("$SCRATCH/")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == reference["sha256"]
    f3.append({"path": reference["path"], "sha256": digest, "equal": True})
runtime = json.loads((packet / "scratch/runtime/provenance.json").read_text())
def normalize(path):
    return path.replace(str(packet / "scratch/runtime"), "$RUNTIME").replace(str(Path.home()), "$USER_HOME")
reference_files = {a["path"]: a for a in expected["runtime"]["files"]}
verified = []
different_archives = []
for item in runtime["files"]:
    key = normalize(item["path"])
    reference = reference_files[key]
    if key.endswith(".a"):
        different_archives.append({"path": key, "local_sha256": item["sha256"],
                                   "published_sha256": reference["sha256"]})
        continue
    assert item["sha256"] == reference["sha256"] and item["size"] == reference["size"], key
    verified.append(key)
public_runtime = json.dumps(runtime, indent=2).replace(str(packet), "$PACKET").replace(str(Path.home()), "$USER_HOME")
(packet / "receipts/runtime-provenance.json").write_text(public_runtime + "\n")
print(json.dumps({"srp": comparisons, "f3": f3, "verified_runtime_inputs": verified,
                  "archive_digests": different_archives,
                  "limits": "Archive container bytes differ; linked ELF bytes and all measured sections match. Link maps include local paths."}, indent=2))
