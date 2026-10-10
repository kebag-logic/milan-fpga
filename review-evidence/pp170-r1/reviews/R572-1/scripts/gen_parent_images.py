#!/usr/bin/env python3
"""Regenerate the parent's descriptor images (aem_desc.bin) for the two shapes.

Usage: gen_parent_images.py <parent checkout with processor+gptp present> <outdir>
Uses the parent's own builder helpers (load_config, emit_aem_overlay,
_entity_model_image), i.e. the same path the parent build uses.
"""
import hashlib, importlib.util, sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("eb", root / "sw/builder/endstation_builder.py")
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)
for shape, cfgname in (("1x1", "endstation_ax7101_1x1_tdm8.yaml"), ("8x8", "endstation_ax7101_8x8.yaml")):
    cfg = eb.load_config(str(root / "configs" / cfgname))
    files = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    blob = files["aem_desc.bin"]
    (out / f"{shape}.img.bin").write_bytes(blob)
    n_names = (blob[10] << 8) | blob[11]
    print(shape, cfgname, len(blob), hashlib.sha256(blob).hexdigest(), "n_names", n_names)
