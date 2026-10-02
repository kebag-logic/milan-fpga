#!/usr/bin/env python3
"""Behavioural probes of L6 at a tree, built from milan_min with the gate's
own mutation helpers. Usage: l6_probes.py <clean clone>

Each probe prints PACKS (lint on, report line "lint waivers applied: 0") or
REFUSED with the refusal's lines that name a rule.
"""
import struct
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "tb/desc_store"))
sys.dont_write_bytecode = True
import test_gen_desc_image as t  # noqa: E402  (the gate module: MILAN_MIN, normalised, gen_desc_image)
mut = t.mut


def d1_model(aaf_count: int, order=None, per_aaf: int = 1, crf: bool = True):
    """milan_min plus AAF inputs; one CLOCK_DOMAIN over INTERNAL, the CRF
    input's source and per_aaf INPUT_STREAM sources per AAF input. `order`
    permutes the CLOCK_SOURCE descriptor indices (the list stays 0..n-1)."""
    model = t.normalised(t.MILAN_MIN)
    aaf = [0, *range(2, 2 + aaf_count - 1)]
    for stream in aaf[1:]:
        mut.add(model, (mut.STREAM_INPUT, stream, 0), mut.body(model, mut.STREAM_INPUT, 0))
    mut.put(model, (mut.ENTITY, 0, 0), 28, len(aaf) + 1)
    internal = mut.body(model, mut.CLOCK_SOURCE, 0)
    crf_src = mut.body(model, mut.CLOCK_SOURCE, 1)
    sources = [internal, crf_src]
    for stream in aaf:
        for _ in range(per_aaf):
            s = bytearray(crf_src)
            struct.pack_into(">H", s, 84, stream)
            sources.append(s)
    if not crf:
        # STREAM_INPUT 1 becomes an AAF input (copy of input 0); drop the CRF source
        mut.store(model, (mut.STREAM_INPUT, 1, 0), bytes(struct.pack(">HH", mut.STREAM_INPUT, 1))
                  + bytes(mut.body(model, mut.STREAM_INPUT, 0)[4:]))
        sources.pop(1)
    order = order or list(range(len(sources)))
    model["descriptors"] = [r for r in model["descriptors"] if r["type"] != mut.CLOCK_SOURCE]
    for new_index, which in enumerate(order):
        mut.add(model, (mut.CLOCK_SOURCE, new_index, 0), sources[which], top=False)
    cfg = mut.body(model, mut.CONFIGURATION, 0)
    for k in range(struct.unpack_from(">H", cfg, 70)[0]):
        if struct.unpack_from(">H", cfg, 74 + 4 * k)[0] == mut.CLOCK_SOURCE:
            struct.pack_into(">H", cfg, 76 + 4 * k, len(sources))
    mut.store(model, (mut.CONFIGURATION, 0, 0), cfg)
    mut.set_sources(model, list(range(len(sources))))
    return model


def report(name: str, model) -> None:
    try:
        rep = t.gen_desc_image.build(model)[1]
        ok = "lint waivers applied: 0" in rep
        print(f"{name}: {'PACKS' if ok else 'PACKS-WITHOUT-LINT-LINE'}")
    except t.gen_desc_image.ImageError as exc:
        lines = [ln.strip() for ln in str(exc).splitlines() if ln.strip()]
        print(f"{name}: REFUSED")
        for ln in lines[:6]:
            print(f"    {ln}")


report("control: milan_min", t.normalised(t.MILAN_MIN))
report("D1 order, 8 AAF inputs, 10 sources (the new case's shape)", d1_model(8))
report("D1 order, 1 AAF input, 3 sources", d1_model(1))
report("order: AAF sources first, then CRF, then INTERNAL", d1_model(3, order=[2, 3, 4, 1, 0]))
report("order: CRF first, INTERNAL last", d1_model(3, order=[1, 2, 3, 4, 0]))
report("order: AAF interleaved reverse", d1_model(3, order=[4, 0, 3, 1, 2]))
report("two INPUT_STREAM sources at each AAF input beside CRF", d1_model(2, per_aaf=2))
report("no CRF input, a source at each of two AAF inputs", d1_model(2, crf=False))
report("no CRF input, one AAF source (control)", d1_model(1, crf=False))
report("214 AAF inputs: 216 sources (508-octet CLOCK_DOMAIN)", d1_model(214))
report("215 AAF inputs: 217 sources (510-octet CLOCK_DOMAIN)", d1_model(215))
