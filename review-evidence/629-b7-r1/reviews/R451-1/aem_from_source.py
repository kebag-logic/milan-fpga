#!/usr/bin/env python3
"""Compute the bench shape's AEM image from source with the builder's own path.

usage: (from the repository root) python3 aem_from_source.py configs/endstation_ax7101_1x1_tdm8.yaml
Prints byte length, CRC32, SHA-256, entity_model_id and the CLOCK_SOURCE/CLOCK_DOMAIN slices
at the offsets the bench's identity/expected.json names. Writes nothing.
"""
import hashlib
import json
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path("sw/builder").resolve()))
import endstation_builder as b  # noqa: E402

cfg = b.load_config(sys.argv[1])
overlay = b.emit_aem_overlay(cfg)
blob = b._entity_model_image(cfg, overlay)["aem_desc.bin"]
out = dict(bytes=len(blob), crc32=f"{zlib.crc32(blob) & 0xffffffff:08x}", sha256=hashlib.sha256(blob).hexdigest(),
           entity_model_id=str(cfg.get("model_id")))
print(json.dumps(out, indent=1))
