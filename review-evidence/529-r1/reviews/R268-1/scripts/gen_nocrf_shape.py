#!/usr/bin/env python3
"""Emit a disposable arty_4x4 shape header with clocking.crf_sink = false.

Usage: gen_nocrf_shape.py <checkout> <outdir>
Writes <outdir>/gen/adp_shape_defaults.svh through the checkout's own
builder emitter (the same call gen_divergent_shape.py makes), so the header
is what the builder would ship for a shape without the CRF Media Clock Input.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

cfg = eb.load_config(str(root / "configs" / "endstation_arty_4x4.yaml"))
cfg["clocking"]["crf_sink"] = False
cfg["clocking"]["media_clock_sources"] = [
    s for s in cfg["clocking"]["media_clock_sources"] if s != "crf"]
svh = eb.emit_adp_shape_svh(cfg, eb.emit_aem_overlay(cfg))
(out / "gen").mkdir(parents=True, exist_ok=True)
(out / "gen" / "adp_shape_defaults.svh").write_text(svh)
for line in svh.splitlines():
    if "ADP_LISTENER_SINK_C" in line or "ADP_TALKER_SRC_C" in line:
        print(line.strip())
