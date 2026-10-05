#!/usr/bin/env python3
"""Run gate 36b and the 8x8 waiver build path of sw/builder/test_builder.py in a given checkout.

Usage: run_gate36b.py <checkout-root>
Prints PASS/FAIL per function; rc 0 only when every listed function passes.
"""
import os, sys, traceback, importlib
root = os.path.abspath(sys.argv[1])
os.chdir(root)
sys.path.insert(0, os.path.join(root, "sw", "builder"))
tb = importlib.import_module("test_builder")
names = ["test_shipping_image_contract", "test_soc_shipping_image_contract",
         "test_shipping_image_contract_presence"]
rc = 0
for n in names:
    try:
        getattr(tb, n)()
        print(f"RESULT PASS {n}", flush=True)
    except BaseException as exc:  # noqa: BLE001 - a probe reports every failure
        rc = 1
        print(f"RESULT FAIL {n}: {type(exc).__name__}: {str(exc)[:300]}", flush=True)
# The 8x8 config must still pack with its declared waiver, and the waiver must be reported.
try:
    eb = tb.eb
    cfg = eb.load_config(os.path.join(root, "configs", "endstation_ax7101_8x8.yaml"))
    out = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    rep = out.get("aem_desc.map", "")
    rep = rep.decode() if isinstance(rep, bytes) else str(rep)
    waived = [l for l in rep.splitlines() if "waive" in l.lower()]
    assert waived, "8x8 layout report lists no waiver"
    print("RESULT PASS 8x8-image-with-waiver:", waived[:3], flush=True)
except BaseException as exc:  # noqa: BLE001
    rc = 1
    print(f"RESULT FAIL 8x8-image-with-waiver: {type(exc).__name__}: {str(exc)[:400]}", flush=True)
sys.exit(rc)
