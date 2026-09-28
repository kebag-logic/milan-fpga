#!/usr/bin/env python3
"""Hash the packed AEM descriptor image set for the five tracked configs.
Usage: aem_images.py <tree>. Prints '<sha256>  <config>/<name>' lines."""
import hashlib, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
for cfg_path in sorted((tree / "configs").glob("endstation_*.yaml")):
    cfg = eb.load_config(cfg_path)
    images = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    for name in sorted(images):
        data = images[name]
        data = data if isinstance(data, bytes) else str(data).encode()
        print(f"{hashlib.sha256(data).hexdigest()}  {cfg_path.stem}/{name}")
