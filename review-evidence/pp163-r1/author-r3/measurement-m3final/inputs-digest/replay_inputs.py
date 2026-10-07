"""Replay pp_resource_gate.inputs() from inputs-components.json.

Usage: python3 replay_inputs.py inputs-components.json baseline_images.json
It chains name NUL component for every file in order, then each generic NUL,
then each image name NUL sha256 NUL sorted by name, and prints the digest.
Recompute any component yourself: sha256 of the file at this head, or of the
published inputs/ file (the generated top is published in its normalized form,
comments removed and roots replaced as the gate does).
"""
import hashlib, json, sys
from pathlib import Path
c = json.loads(Path(sys.argv[1]).read_text())
images = json.loads(Path(sys.argv[2]).read_text())
d = hashlib.sha256()
for row in c["files"]:
    d.update(row["name"].encode() + b"\0" + bytes.fromhex(row["component_sha256"]))
for g in c["generics"]:
    d.update(g.encode() + b"\0")
for im in sorted(images, key=lambda r: Path(r["path"]).name):
    d.update(f"{Path(im['path']).name}\0{im['sha256']}\0".encode())
print(d.hexdigest(), "match" if d.hexdigest() == c["recorded_inputs_sha256"] else "MISMATCH")
