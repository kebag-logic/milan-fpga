#!/usr/bin/env python3
"""R357-1 probe: can a hand-written configuration reach a zero
AUDIO_UNIT / CLOCK_DOMAIN / CONTROL count?

Usage: probe_zero_counts.py <tree-root> <scratch-dir>

Loads the builder from <tree-root>, writes hand-edited variants of the
AX 1x1 configuration under <scratch-dir>, and records for each variant
whether load_config refuses it and, if accepted, the overlay census, the
generated AEM_N_* header values, and the descriptor directory counts.
Writes nothing inside <tree-root>.
"""
import copy
import importlib.util
import re
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw/builder"))
sys.path.insert(0, str(root / "scripts"))
spec = importlib.util.spec_from_file_location(
    "endstation_builder", root / "sw/builder/endstation_builder.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
import check_entity_shape as G  # noqa: E402

base_path = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
base = yaml.safe_load(base_path.read_text())

def variant(label, edit):
    doc = copy.deepcopy(base)
    edit(doc)
    return label, doc

def set_top(key, value):
    return lambda d: d.__setitem__(key, value)

def set_names(value):
    return lambda d: d.__setitem__("names", value)

def set_entity(key, value):
    return lambda d: d["entity"].__setitem__(key, value)

VARIANTS = [
    variant("baseline (unedited)", lambda d: None),
    variant("top-level descriptor_counts all zero",
            set_top("descriptor_counts",
                    {"AUDIO_UNIT": 0, "CLOCK_DOMAIN": 0, "CONTROL": 0})),
    variant("top-level controls: []", set_top("controls", [])),
    variant("top-level audio_units: []", set_top("audio_units", [])),
    variant("top-level clock_domains: []", set_top("clock_domains", [])),
    variant("names.control_identify: null", set_names({"control_identify": None})),
    variant("names.control_identify: ''", set_names({"control_identify": ""})),
    variant("names.controls: []", set_names({"controls": []})),
    variant("entity.controls: []", set_entity("controls", [])),
    variant("entity.identify: false", set_entity("identify", False)),
]

UNITS = (("AUDIO_UNIT", 0x0002, "AEM_N_AUDIO_UNIT_C"),
         ("CLOCK_DOMAIN", 0x0024, "AEM_N_CLKDOM_C"),
         ("CONTROL", 0x001A, "AEM_N_CONTROL_C"))

rows = []
for i, (label, doc) in enumerate(VARIANTS):
    path = scratch / f"variant_{i}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False))
    try:
        cfg = B.load_config(str(path))
    except B.ConfigError as exc:
        rows.append(f"{label}: REFUSED ConfigError: {str(exc)[:160]}")
        continue
    except Exception as exc:  # anything else is a probe result too
        rows.append(f"{label}: REFUSED {type(exc).__name__}: {str(exc)[:160]}")
        continue
    ovl = B.emit_aem_overlay(cfg)
    hdr = B.emit_adp_shape_svh(cfg, ovl)
    rom = G.rom_descriptor_counts(B.emit_aem_rom_svh(cfg, ovl))
    parts = []
    for kind, dtype, sym in UNITS:
        hv = re.findall(rf"localparam\s+int\s+{sym}\s*=\s*(\d+)\s*;", hdr)
        parts.append(f"{kind}: census={ovl['descriptor_counts'][kind]} "
                     f"header={hv} dir={rom.get(dtype, 0)}")
    rows.append(f"{label}: ACCEPTED; " + "; ".join(parts))

for r in rows:
    print(r)
