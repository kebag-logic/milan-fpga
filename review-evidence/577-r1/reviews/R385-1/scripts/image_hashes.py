#!/usr/bin/env python3
"""sha256 of _entity_model_image outputs for the five tracked shipping configs in <tree>."""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
assert Path(eb.__file__).resolve().is_relative_to(root)
for stem in ("arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"):
    cfg = eb.load_config(str(root / f"configs/endstation_{stem}.yaml"))
    out = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    for k in sorted(out):
        v = out[k] if isinstance(out[k], bytes) else out[k].encode()
        print(stem, k, len(v), hashlib.sha256(v).hexdigest())
