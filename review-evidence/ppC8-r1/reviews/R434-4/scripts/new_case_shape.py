#!/usr/bin/env python3
"""Dump the model the round-4 positive case packs: its CLOCK_SOURCEs
(index, type, location type, location index), each STREAM_INPUT's format
family, the CLOCK_DOMAIN list, and the lint report. Usage: new_case_shape.py <clone>"""
import struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / "tb/desc_store"))
import test_gen_desc_image as t
mut = t.mut
seen = {}
case = t.ConformingModelTest("test_a_source_per_aaf_input_beside_crf")
case.packs = lambda model: seen.setdefault("model", model)
case.test_a_source_per_aaf_input_beside_crf()
model = seen["model"]
TYPES = {0x0000: "INTERNAL", 0x0001: "EXTERNAL", 0x0002: "INPUT_STREAM"}
rows = sorted((r for r in model["descriptors"] if r["type"] == mut.CLOCK_SOURCE), key=lambda r: r["index"])
for r in rows:
    b = bytes.fromhex(r["bytes"])
    st, lt, li = (struct.unpack_from(">H", b, o)[0] for o in (72, 82, 84))
    print(f"CLOCK_SOURCE {r['index']}: {TYPES.get(st, hex(st))} location_type {lt:#06x} location_index {li}")
for r in sorted((r for r in model["descriptors"] if r["type"] == mut.STREAM_INPUT), key=lambda r: r["index"]):
    b = bytes.fromhex(r["bytes"])
    fmt = b[74:82].hex()   # current_format (IEEE 1722.1-2021 §7.2.6, offset 74)
    print(f"STREAM_INPUT {r['index']}: current_format {fmt} ({'CRF' if fmt.startswith("04") else 'AAF' if fmt.startswith('02') else '?'})")
dom = bytes.fromhex(next(r for r in model["descriptors"] if r["type"] == mut.CLOCK_DOMAIN)["bytes"])
n = struct.unpack_from(">H", dom, 74)[0]
print("CLOCK_DOMAIN 0 clock_sources:", list(struct.unpack_from(f">{n}H", dom, 76)), "length", len(dom))
print(t.gen_desc_image.build(model)[1].splitlines()[-12:])
