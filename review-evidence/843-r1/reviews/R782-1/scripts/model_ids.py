#!/usr/bin/env python3
"""Print each shipping config's resolved gptp.clock_accuracy and
entity_model_id as the builder of <checkout> derives them.

usage: model_ids.py <checkout>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

for name in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8",
             "endstation_arty_current", "endstation_arty_4x4",
             "endstation_arty_8ch"):
    cfg = eb.load_config(str(root / "configs" / f"{name}.yaml"))
    mid = cfg.get("entity_model_id") or cfg.get("adp", {}).get("entity_model_id")
    if mid is None:
        mid = eb.derive_model_id(eb.model_shape(cfg)) if hasattr(eb, "model_shape") else None
    print(f"{name}: clock_accuracy 0x{cfg['gptp']['clock_accuracy']:02X} "
          f"model_id {mid if isinstance(mid, str) else hex(mid) if mid is not None else None}")
