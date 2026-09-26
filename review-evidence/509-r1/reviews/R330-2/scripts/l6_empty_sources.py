#!/usr/bin/env python3
"""Check the L6 row's 'empty source list' and 'INTERNAL/CRF only' claims.

Usage: l6_empty_sources.py <tree>. Loads arty_current with clocking edits in a
temporary copy of the YAML; the tracked input is never written.
"""
import json
import sys
import tempfile
from pathlib import Path

import yaml

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw" / "builder"))
import endstation_builder as builder  # noqa: E402

base = yaml.safe_load((tree / "configs" / "endstation_arty_current.yaml").read_text())
cases = {
    "tracked clocking keys": None,
    "empty list, default_source removed": lambda c: (c.update(media_clock_sources=[]), c.pop("default_source", None)),
    "empty list, default_source internal": lambda c: c.update(media_clock_sources=[], default_source="internal"),
    "gptp source requested": lambda c: c.update(media_clock_sources=["internal", "gptp"]),
}
out = {"tracked_clocking": {k: base["clocking"].get(k) for k in ("media_clock_sources", "default_source")}}
for label, edit in cases.items():
    raw = yaml.safe_load((tree / "configs" / "endstation_arty_current.yaml").read_text())
    if edit is not None:
        edit(raw["clocking"])
    with tempfile.TemporaryDirectory(prefix="l6-probe-") as tmp:
        path = Path(tmp) / "config.yaml"
        path.write_text(yaml.safe_dump(raw))
        try:
            builder.load_config(path)
            out[label] = "accepted"
        except Exception as exc:  # noqa: BLE001 - classify the failure type
            out[label] = f"{type(exc).__name__}: {str(exc)[:160]}"
print(json.dumps(out, indent=2))
