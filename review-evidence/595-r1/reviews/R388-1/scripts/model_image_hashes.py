#!/usr/bin/env python3
"""Hash the paired AEM descriptor image set and normalized config per tracked
configuration, using the builder in the tree given as argv[1]."""
import hashlib, json, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
assert Path(eb.__file__).resolve().is_relative_to(tree), eb.__file__
for name in ("endstation_arty_4x4", "endstation_arty_8ch", "endstation_arty_current",
             "endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    cfg = eb.load_config(tree / "configs" / f"{name}.yaml")
    norm = json.dumps(cfg, sort_keys=True, default=str).encode()
    print(f"{hashlib.sha256(norm).hexdigest()}  {name}/normalized_config.json")
    files = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    for fn in sorted(files):
        data = files[fn]
        data = data if isinstance(data, bytes) else str(data).encode()
        print(f"{hashlib.sha256(data).hexdigest()}  {name}/{fn}")
