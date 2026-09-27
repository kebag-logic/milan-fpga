#!/usr/bin/env python3
"""R356-1: can a hand-written configuration drive AUDIO_UNIT, CLOCK_DOMAIN or
CONTROL to zero?  Each variant is a tracked configuration plus one edit that
tries to remove the IDENTIFY control, the AUDIO_UNIT or the CLOCK_DOMAIN.
For every variant: does the builder refuse it (ConfigError / other), and if
it loads, what do the census, the generated header and the descriptor model
(the bytes the processor serves) say?
Usage: probe_zero_reach.py <repo root at exact head> <scratch dir>
"""
import copy
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(sys.argv[1]).resolve()
SCR = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
sys.path.insert(0, str(ROOT / "avdecc"))
import endstation_builder as B  # noqa: E402
import gen_aem_store as G  # noqa: E402
import aem_assemble as A  # noqa: E402

BASE = yaml.safe_load((ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())


def v(fn):
    d = copy.deepcopy(BASE)
    fn(d)
    return d


VARIANTS = {
    "V0 unmodified copy": v(lambda d: None),
    "V1 top-level descriptors: {CONTROL: 0, AUDIO_UNIT: 0, CLOCK_DOMAIN: 0}":
        v(lambda d: d.__setitem__("descriptors",
                                  {"CONTROL": 0, "AUDIO_UNIT": 0, "CLOCK_DOMAIN": 0})),
    "V2 top-level descriptor_counts: {CONTROL: 0}":
        v(lambda d: d.__setitem__("descriptor_counts", {"CONTROL": 0})),
    "V3 top-level controls: []": v(lambda d: d.__setitem__("controls", [])),
    "V4 top-level audio_units: []": v(lambda d: d.__setitem__("audio_units", [])),
    "V5 entity.controls: []": v(lambda d: d["entity"].__setitem__("controls", [])),
    "V6 entity.identify: false": v(lambda d: d["entity"].__setitem__("identify", False)),
    "V7 names.control_identify: null":
        v(lambda d: d.setdefault("names", {}).__setitem__("control_identify", None)),
    "V8 names.control_identify: ''":
        v(lambda d: d.setdefault("names", {}).__setitem__("control_identify", "")),
    "V9 clocking.clock_domains: 0":
        v(lambda d: d["clocking"].__setitem__("clock_domains", 0)),
    "V10 board.features.identify: false":
        v(lambda d: d["board"].setdefault("features", {}).__setitem__("identify", False)),
    "V11 clocking.audio_unit_rates_hz: []":
        v(lambda d: d["clocking"].__setitem__("audio_unit_rates_hz", [])),
}

SCR.mkdir(parents=True, exist_ok=True)
for label, doc in VARIANTS.items():
    tag = label.split()[0]
    path = SCR / f"zero_{tag}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False))
    try:
        cfg = B.load_config(str(path))
        ovl = B.emit_aem_overlay(cfg)
        hdr = B.emit_adp_shape_svh(cfg, ovl)
        model = G.build_model(G.spec_from_overlay(ovl))
    except B.ConfigError as e:
        print(f"{label}\n    REFUSED ConfigError: {str(e)[:150]}")
        continue
    except Exception as e:  # noqa: BLE001
        print(f"{label}\n    FAILED {type(e).__name__}: {str(e)[:150]}")
        continue
    dc = ovl["descriptor_counts"]
    hv = {s: re.findall(rf"{s}\s*=\s*(\d+);", hdr) for s in
          ("AEM_N_AUDIO_UNIT_C", "AEM_N_CLKDOM_C", "AEM_N_CONTROL_C")}
    served = {}
    for t, _i, *_ in A._entity_descriptors(G.spec_from_overlay(ovl)):
        served[t] = served.get(t, 0) + 1
    print(f"{label}\n    LOADED census AU/CD/CTL="
          f"{dc['AUDIO_UNIT']}/{dc['CLOCK_DOMAIN']}/{dc['CONTROL']} header="
          f"{hv['AEM_N_AUDIO_UNIT_C']}/{hv['AEM_N_CLKDOM_C']}/{hv['AEM_N_CONTROL_C']} "
          f"constructor AU/CD/CTL={served.get(A.AUDIO_UNIT, 0)}/"
          f"{served.get(A.CLOCK_DOMAIN, 0)}/{served.get(A.CONTROL, 0)} "
          f"model={'ok' if model else 'empty'}")
