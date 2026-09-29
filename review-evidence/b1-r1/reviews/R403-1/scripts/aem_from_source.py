#!/usr/bin/env python3
"""Regenerate the shipping AEM image (aem_desc.bin) from the checkout's config
through the builder's own entry points, and print its length, CRC32 and
SHA-256, so the identity gate's AEM values can be bound to source.

usage: aem_from_source.py <repo-checkout> [config-name]
Writes nothing into the checkout (python -B recommended).
"""
import hashlib
import sys
import zlib
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
name = sys.argv[2] if len(sys.argv) > 2 else "endstation_ax7101_1x1_tdm8"
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

cfg = eb.load_config(str(repo / "configs" / (name + ".yaml")))
overlay = eb.emit_aem_overlay(cfg)
blob = eb._entity_model_image(cfg, overlay)["aem_desc.bin"]
print(f"{name} aem_desc.bin len={len(blob)} crc32={zlib.crc32(blob) & 0xffffffff:08x} "
      f"sha256={hashlib.sha256(blob).hexdigest()}")
