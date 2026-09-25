#!/usr/bin/env python3
"""Print entity_model_id and stream_outputs per shipped config for one tree."""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
for cfg_path in sorted((root / "configs").glob("endstation_*.yaml")):
    cfg = eb.load_config(cfg_path)
    ovl = eb.emit_aem_overlay(cfg)
    ovl = json.loads(ovl) if isinstance(ovl, str) else ovl
    print(cfg_path.stem, ovl["entity"]["entity_model_id"],
          len(ovl["stream_outputs"]))
