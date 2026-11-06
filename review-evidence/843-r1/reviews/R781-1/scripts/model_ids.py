#!/usr/bin/env python3
"""Print each config's derived entity_model_id at one checkout.
usage: model_ids.py <repo>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
for p in sorted((root / "configs").glob("endstation_*.yaml")):
    try:
        c = eb.load_config(str(p))
        r = eb.emit_aem_overlay(c)
        mid = c.get("entity", {}).get("entity_model_id") or r.get("entity_model_id") if isinstance(r, dict) else None
        print(p.name, hex(mid) if isinstance(mid, int) else mid, "clock_accuracy", hex(c["gptp"]["clock_accuracy"]))
    except Exception as e:
        print(p.name, "ERR", type(e).__name__, str(e)[:120])
