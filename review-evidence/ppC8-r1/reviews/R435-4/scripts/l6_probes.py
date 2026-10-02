#!/usr/bin/env python3
"""l6_probes.py <processor-root>

Probes the L6 lint at a processor tree, each model derived from
hdl/aecp/desc/milan_min.json with the gate's own mutation helpers:
  P1 the new positive case's model, rebuilt as the test builds it, decoded;
  P2 the same ten sources in another class order (AAF sources first, the
     CRF input's source last, INTERNAL in the middle);
  P3 216 sources pack, 217 are refused, and by which check;
  P4 no CRF input, one INPUT_STREAM source per AAF input (main's L6: only
     the single AAF input's source when no CRF input exists);
  P5 beside the CRF input, two sources at one AAF input (beyond main's
     "one per AAF input"; the lint sets no count there);
  P6 the domain-source-identity refusal's text."""
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/desc_store"))
sys.path.insert(0, str(root / "hdl/aecp/desc"))
import gen_desc_image as image                       # noqa: E402
import lint_mutations as mut                         # noqa: E402
import test_gen_desc_image as t                      # noqa: E402

KIND = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM"}


def verdict(model):
    try:
        report = image.build(model)[1]
        w = [ln for ln in report.splitlines() if "lint waivers applied" in ln]
        return "PACKS (" + (w[0].strip() if w else "?") + ")"
    except image.ImageError as exc:
        lines = str(exc).splitlines()
        return f"REFUSED {len(lines)} line(s): " + " | ".join(lines[:3])


def decode(model):
    g = image._grouped_descriptors(model)
    fam = {i: {0x02: "AAF", 0x04: "CRF"}.get(b[74] & 0x7F, hex(b[74]))
           for i, (b, _) in g[(0, 0x0005)].items()}
    dom = g[(0, 0x0024)][0][0]
    cnt = struct.unpack_from(">H", dom, 74)[0]
    lst = list(struct.unpack_from(f">{cnt}H", dom, 76))
    srcs = []
    for i, (b, _) in sorted(g[(0, 0x000A)].items()):
        st, lt, li = (struct.unpack_from(">H", b, o)[0] for o in (72, 82, 84))
        srcs.append(f"{i}:{KIND.get(st, st)}" + (f"@SI{li}({fam.get(li)})" if lt == 5 else ""))
    return f"domain count {cnt} list {lst}; sources " + ", ".join(srcs)


def ten_sources(order):
    """milan_min with STREAM_INPUT 0 and 2..8 AAF (1 is CRF); the sources
    given as a list of ('INTERNAL'|'CRF'|aaf stream) in CLOCK_SOURCE order."""
    model = t.normalised(t.MILAN_MIN)
    aaf = [0, *range(2, 9)]
    for stream in aaf[1:]:
        mut.add(model, (mut.STREAM_INPUT, stream, 0), mut.body(model, mut.STREAM_INPUT, 0))
    mut.put(model, (mut.ENTITY, 0, 0), 28, len(aaf) + 1)
    internal = mut.body(model, mut.CLOCK_SOURCE, 0)
    crf = mut.body(model, mut.CLOCK_SOURCE, 1)
    model["descriptors"] = [r for r in model["descriptors"] if r["type"] != mut.CLOCK_SOURCE]
    mut.set_count(model, mut.CLOCK_SOURCE, 0)
    for i, what in enumerate(order):
        if what == "INTERNAL":
            data = internal
        else:
            data = bytearray(crf)
            if what != "CRF":
                struct.pack_into(">H", data, 84, what)
        mut.add(model, (mut.CLOCK_SOURCE, i, 0), data)
    mut.set_sources(model, list(range(len(order))))
    return model


def main():
    g0 = image._grouped_descriptors(t.normalised(t.MILAN_MIN))
    print("milan_min CLOCK_SOURCE 0/1 type@72:",
          [struct.unpack_from(">H", g0[(0, 0x000A)][i][0], 72)[0] for i in (0, 1)],
          "location@84:", [struct.unpack_from(">H", g0[(0, 0x000A)][i][0], 84)[0] for i in (0, 1)])

    # P1: rebuild exactly as the test does
    model = t.normalised(t.MILAN_MIN)
    aaf = [0, *range(2, 9)]
    for stream in aaf[1:]:
        mut.add(model, (mut.STREAM_INPUT, stream, 0), mut.body(model, mut.STREAM_INPUT, 0))
    mut.put(model, (mut.ENTITY, 0, 0), 28, len(aaf) + 1)
    for k, stream in enumerate(aaf):
        source = mut.body(model, mut.CLOCK_SOURCE, 1)
        struct.pack_into(">H", source, 84, stream)
        mut.add(model, (mut.CLOCK_SOURCE, 2 + k, 0), source)
    mut.set_sources(model, list(range(2 + len(aaf))))
    print("P1 test model:", decode(model))
    print("P1 verdict, lint on:", verdict(model))
    print("P1b same through ten_sources():",
          verdict(ten_sources(["INTERNAL", "CRF", *aaf])), decode(ten_sources(["INTERNAL", "CRF", *aaf])))

    # P2: another class order
    order = [8, 7, 6, "INTERNAL", 5, 4, 3, 2, 0, "CRF"]
    m2 = ten_sources(order)
    print("P2 permuted order:", decode(m2))
    print("P2 verdict:", verdict(m2))

    # P3: 216 and 217 sources (INTERNAL, CRF, AAF 0, 2..8, then INTERNAL copies)
    for n in (216, 217):
        m3 = ten_sources(["INTERNAL", "CRF", *aaf] + ["INTERNAL"] * (n - 10))
        dom = mut.body(m3, mut.CLOCK_DOMAIN, 0)
        print(f"P3 {n} sources, CLOCK_DOMAIN {len(dom)} octets:", verdict(m3))

    # P4: no CRF input, one INPUT_STREAM source per AAF input
    m4 = ten_sources(["INTERNAL", "CRF", *aaf])
    crf_si = mut.body(m4, mut.STREAM_INPUT, 1)
    aaf_si = mut.body(m4, mut.STREAM_INPUT, 0)
    struct.pack_into(">H", aaf_si, 2, 1)
    mut.store(m4, (mut.STREAM_INPUT, 1, 0), aaf_si)
    print("P4 STREAM_INPUT 1 was CRF:", crf_si[74] & 0x7F == 0x04, "now:", decode(m4))
    print("P4 verdict:", verdict(m4))

    # P5: beside CRF, two sources at AAF input 0
    m5 = ten_sources(["INTERNAL", "CRF", 0, 0])
    print("P5", decode(m5), "->", verdict(m5))

    # P6: identity refusal text
    m6 = t.normalised(t.MILAN_MIN)
    mut.set_sources(m6, [1, 0])
    print("P6", verdict(m6))


main()
