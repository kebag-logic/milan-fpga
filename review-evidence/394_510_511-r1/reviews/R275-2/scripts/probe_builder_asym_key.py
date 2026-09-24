#!/usr/bin/env python3
"""Disposable probe: does the builder refuse a gptp asymmetry key?

Control: the shipped configuration loads through load_config() unchanged.
Arms: the same raw document with one asymmetry-shaped key planted in its
gptp section is (a) passed to _load_gptp() and (b) written to a scratch YAML
and loaded end to end through load_config(). Each arm must raise ConfigError
naming the planted key. Read-only against the checkout; run with python3 -B.
Usage: probe_builder_asym_key.py <parent-checkout> <config-relpath> <scratch-dir>
"""
import copy
import sys
from pathlib import Path

import yaml

repo = Path(sys.argv[1]).resolve()
cfg_rel = sys.argv[2]
scratch = Path(sys.argv[3]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

src = repo / cfg_rel
ok = True
try:
    cfg = eb.load_config(str(src))
    print(f"CONTROL load_config: gptp ingress={cfg['gptp']['ingress_latency_ns']} "
          f"egress={cfg['gptp']['egress_latency_ns']} keys={sorted(cfg['gptp'])}")
except Exception as exc:
    print(f"CONTROL FAILED: {type(exc).__name__}: {exc}")
    ok = False

raw = eb._load_document(str(src))
try:
    eb._load_gptp(copy.deepcopy(raw))
    print("CONTROL _load_gptp(raw): loaded")
except Exception as exc:
    print(f"CONTROL _load_gptp(raw) FAILED: {type(exc).__name__}: {exc}")
    ok = False

for key, val in (("delay_asymmetry_ns", 0), ("delayAsymmetry", 5),
                 ("delay_asymmetry", -12), ("asymmetry_ns", 1)):
    doc = copy.deepcopy(raw)
    doc["gptp"][key] = val
    try:
        eb._load_gptp(doc)
        print(f"ARM _load_gptp {key}={val}: ACCEPTED (unexpected)")
        ok = False
    except eb.ConfigError as exc:
        named = key in str(exc)
        print(f"ARM _load_gptp {key}={val}: ConfigError, names key={named}: {exc}")
        ok = ok and named
    out = scratch / f"planted_{key}.yaml"
    out.write_text(yaml.safe_dump(doc, sort_keys=False))
    try:
        eb.load_config(str(out))
        print(f"ARM load_config {key}={val}: ACCEPTED (unexpected)")
        ok = False
    except eb.ConfigError as exc:
        named = key in str(exc)
        print(f"ARM load_config {key}={val}: ConfigError, names key={named}")
        ok = ok and named
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
