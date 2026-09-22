#!/usr/bin/env python3
"""Shipping-byte manifest of one checkout, for a base-versus-head comparison.

For each of the five tracked configs: the YAML bytes, the normalized
load_config result, the AEM overlay, every member of the packed entity-model
image (aem_desc.bin and its siblings), the AUDIO_UNIT words read back out of
the packed image, and every file build() writes into a private out directory.
After the five builds, the tracked-tree state of the checkout (build() may
rewrite tracked generated files) is recorded too. Paths are made relative so
two checkouts compare byte for byte.
Usage: 09_artifacts.py <checkout-root> <manifest.json>
"""
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/builder"))
import test_builder as tb  # noqa: E402

eb = tb.eb


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(obj) -> bytes:
    text = json.dumps(obj, sort_keys=True, default=str)
    return text.replace(str(root), "<ROOT>").encode()


manifest: dict = {}
with tempfile.TemporaryDirectory(prefix="r222-art-") as tmp:
    for name, path in tb.CONFIGS.items():
        row: dict = {"yaml": sha(path.read_bytes())}
        cfg = eb.load_config(str(path))
        row["load_config"] = sha(norm(cfg))
        row["audio_unit_rates_hz"] = cfg["clocking"]["audio_unit_rates_hz"]
        overlay = eb.emit_aem_overlay(cfg)
        row["overlay"] = sha(norm(overlay))
        image = eb._entity_model_image(cfg, overlay)
        row["image"] = {k: sha(v if isinstance(v, bytes) else norm(v))
                        for k, v in sorted(image.items())}
        desc = tb.image_descriptor(image["aem_desc.bin"], 0x0002)
        off, cnt = struct.unpack_from(">HH", desc, 140)
        row["audio_unit"] = {"current": struct.unpack_from(">I", desc, 136)[0],
                             "offset": off, "count": cnt,
                             "rates": list(struct.unpack_from(f">{cnt}I", desc, off))}
        out = Path(tmp) / name
        eb.build(str(path), str(out))
        row["build_outputs"] = {
            str(p.relative_to(out)): sha(p.read_bytes().replace(str(root).encode(), b"<ROOT>"))
            for p in sorted(out.rglob("*")) if p.is_file()}
        manifest[name] = row

status = subprocess.run(["git", "-C", str(root), "status", "--porcelain",
                         "--untracked-files=all"], capture_output=True, text=True).stdout
manifest["_tracked_tree_after_builds"] = {
    "status_lines": status.splitlines(),
    "diff_sha256": sha(subprocess.run(["git", "-C", str(root), "diff", "--binary"],
                                      capture_output=True).stdout),
}
Path(sys.argv[2]).write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
for name, row in manifest.items():
    if name.startswith("_"):
        continue
    print(f"{name}: rates {row['audio_unit_rates_hz']} image AU {row['audio_unit']} "
          f"aem_desc.bin {row['image']['aem_desc.bin'][:16]} outputs {len(row['build_outputs'])}")
print("tracked-tree status lines after builds:", len(status.splitlines()))
