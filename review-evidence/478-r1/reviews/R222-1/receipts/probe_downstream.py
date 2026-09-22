#!/usr/bin/env python3
"""[R222] Loader acceptance versus downstream image support, and malformed input.

Usage: probe_downstream.py <scratch-root>

For variants of configs/endstation_arty_current.yaml whose only change is
clocking.audio_unit_rates_hz, report what _load_clocking, load_config and the
packed-image path (emit_aem_overlay + _entity_model_image) each do. Nothing
under <scratch-root> is written; variants go to a private temporary directory.
"""
import importlib.util
import struct
import sys
import tempfile
from pathlib import Path

import yaml

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "test_builder", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)
eb = tb.eb
base_yaml = tb.CONFIGS["arty_current"]
tmp = Path(tempfile.mkdtemp(prefix="r222-downstream-"))


def outcome(fn):
    try:
        return "ok", fn()
    except Exception as exc:  # the probe reports every exception class
        return f"{type(exc).__name__}", str(exc)[:140]


CASES = [
    ("shipping arty_current list", [48000, 96000, 192000]),
    ("three base rates reordered", [192000, 48000, 96000]),
    ("eight distinct (gate 36a loader boundary)",
     [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]),
    ("nine distinct", [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000, 22050]),
    ("nine duplicates of the current rate", [48000] * 9),
    ("two entries equal after int conversion", [48000, "48000"]),
    ("scalar instead of list", 48000),
    ("null", None),
    ("string", "48000"),
]
for label, rates in CASES:
    cfg = yaml.safe_load(base_yaml.read_text())
    cfg["clocking"]["audio_unit_rates_hz"] = rates
    path = tmp / "variant.yaml"
    path.write_text(yaml.safe_dump(cfg))
    raw = yaml.safe_load(path.read_text())
    lc = outcome(lambda: eb._load_clocking(raw, "probe")["audio_unit_rates_hz"])
    full = outcome(lambda: eb.load_config(str(path)))
    if full[0] == "ok":
        loaded = full[1]

        def image():
            blob = eb._entity_model_image(loaded, eb.emit_aem_overlay(loaded))["aem_desc.bin"]
            desc = tb.image_descriptor(blob, 0x0002)
            off, cnt = struct.unpack_from(">HH", desc, 140)
            return list(struct.unpack_from(f">{cnt}I", desc, off))
        img = outcome(image)
        full = ("ok", loaded["clocking"]["audio_unit_rates_hz"])
    else:
        img = ("not reached", "")
    print(f"{label}:\n  _load_clocking: {lc[0]} {lc[1]}\n  load_config:    {full[0]} {full[1]}"
          f"\n  packed image:   {img[0]} {img[1]}")
