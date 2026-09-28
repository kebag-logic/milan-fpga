#!/usr/bin/env python3
"""Build the five tracked configurations in the current tree and hash every artifact.

Usage (run from a repository root): artifact_inventory.py <outdir> <inventory.json>

For each configs/endstation_*.yaml this runs endstation_builder.build() into
<outdir>/<config stem>/ and also writes the descriptor-image set produced by
_entity_model_image() (aem_desc.bin/.json/.map, which runs the shipping-image
check), then records sha256 and size of every file, plus the tracked files the
build may rewrite. Nothing outside <outdir> is written except what build()
itself writes for srp.rtl_table configurations.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402

out = Path(sys.argv[1]).resolve()
inventory = {"head": None, "artifacts": {}}
head_file = ROOT / ".git"
for config in sorted((ROOT / "configs").glob("endstation_*.yaml")):
    target = out / config.stem
    target.mkdir(parents=True, exist_ok=True)
    result = eb.build(str(config), str(target))
    images = eb._entity_model_image(result["cfg"], result["overlay"])
    image_dir = target / "descriptor_image"
    image_dir.mkdir(exist_ok=True)
    for name, data in images.items():
        payload = data if isinstance(data, bytes) else (
            data.encode() if isinstance(data, str) else json.dumps(data, sort_keys=True).encode())
        (image_dir / name).write_bytes(payload)
for path in sorted(p for p in out.rglob("*") if p.is_file()):
    data = path.read_bytes()
    inventory["artifacts"][str(path.relative_to(out))] = {
        "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
for rel in ("hdl/common/csr/gen/lwsrp_csr_defaults.svh",):
    data = (ROOT / rel).read_bytes()
    inventory["artifacts"]["tracked:" + rel] = {
        "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
Path(sys.argv[2]).write_text(json.dumps(inventory, indent=1, sort_keys=True) + "\n")
print(f"{len(inventory['artifacts'])} artifacts hashed")
