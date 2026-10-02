#!/usr/bin/env python3
"""Round-3 reviewer probes of the model lint (no file written).
Usage: probe_r3.py <repo-root> [<round-2-repo-root>]

A  Annex C (Milan v1.2 Table C.1) built here, independently of the gate's
   lint_mutations.annex_c: R = 0, 1, 8 positives; inconsistent layouts refused.
B  identify-format: r / u flag positives, a value-type bit refused.
C  the 508-octet boundary.
D  the digest, octet by octet, against this reviewer's own table of
   IEEE 1722.1-2021 6.2.2.8 (every octet of a descriptor is flipped; the set of
   octets that keep the digest must equal the clause's fields exactly).
E  milan_min's digest: model_ids.json, this head and the round-2 head."""
import importlib.util
import json
import pathlib
import struct
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/desc_store"))
sys.argv = sys.argv[:1] + sys.argv[2:]
import test_gen_desc_image as t      # noqa: E402
import lint_mutations as mut          # noqa: E402
g = t.gen_desc_image
SO, SI = mut.STREAM_OUTPUT, mut.STREAM_INPUT
bad = 0


def run(name, model, expect, needle=None, **kw):
    """Pack; compare with `expect` ('PACK' or 'REFUSE'), and when refused that
    some refusal line contains `needle`."""
    global bad
    try:
        g.build(model, **kw)
        got, lines = "PACK", []
    except g.ImageError as e:
        got, lines = "REFUSE", [l.split(" (Milan")[0].split(" (IEEE")[0] for l in str(e).splitlines()]
    ok = got == expect and (needle is None or any(needle in l for l in lines))
    bad += not ok
    print(f"[{'ok' if ok else 'UNEXPECTED'}] {name}: {got} {lines}")


def annex(model, at, streams=(), timing=False, redundant=None, extra=b""):
    """Re-lay a Table 7-8 stream in Annex C Table C.1 by hand: drop `timing`
    (136..137), formats_offset 136, redundant_offset 136 + 8N, R, the formats,
    then R two-octet indices."""
    data = bytes(mut.body(model, *at))
    n = struct.unpack_from(">H", data, 84)[0]
    assert struct.unpack_from(">H", data, 82)[0] == 138
    head = bytearray(data[:136])
    struct.pack_into(">H", head, 82, 136)
    struct.pack_into(">H", head, 132, 136 + 8 * n if redundant is None else redundant)
    struct.pack_into(">H", head, 134, len(streams))
    keep = data[136:138] if timing else b""
    mut.store(model, at, bytes(head) + keep + data[138:138 + 8 * n]
              + b"".join(struct.pack(">H", s) for s in streams) + extra)


M = lambda: t.normalised(t.MILAN_MIN)

print("== A: L4 stream-layout, Milan v1.2 Annex C Table C.1 and IEEE 1722.1-2021 Table 7-8")
m = M(); run("A0 milan_min (Table 7-8 everywhere)", m, "PACK")
m = M()
for at in ((SI, 0, 0), (SI, 1, 0), (SO, 0, 0)):
    annex(m, at)
run("A1 every stream Annex C, R=0", m, "PACK")
m = M(); annex(m, (SO, 0, 0), (0,)); run("A2 Annex C output, R=1 naming itself (pairing not linted)", m, "PACK")
m = M(); mut.second_interface(m)
out = mut.body(m, SO, 0); struct.pack_into(">H", out, 126, 1); mut.add(m, (SO, 1, 0), out)
mut.put(m, (mut.ENTITY, 0, 0), 24, 2)
annex(m, (SO, 0, 0), (1,)); annex(m, (SO, 1, 0), (0,))
run("A3 redundant pair of outputs on two interfaces, R=1 each", m, "PACK")
m = M(); annex(m, (SO, 0, 0), tuple(range(1, 9))); run("A4 Annex C R=8", m, "PACK")
m = M(); annex(m, (SO, 0, 0), tuple(range(1, 10))); run("A5 Annex C R=9", m, "REFUSE", "number_of_redundant_streams 9, above 8")
m = M(); mut.set_formats(m, (SI, 0, 0), [mut.BASE_IN] * 44); annex(m, (SI, 0, 0), tuple(range(8)))
run("A6 Annex C N=44 R=8 (504 octets)", m, "PACK")
m = M(); mut.set_formats(m, (SI, 0, 0), [mut.BASE_IN] * 45); annex(m, (SI, 0, 0), tuple(range(8)))
run("A7 Annex C N=45 R=8 (512 octets, past 508)", m, "REFUSE", "508")
m = M(); mut.set_formats(m, (SI, 0, 0), [mut.BASE_IN] * 46); annex(m, (SI, 0, 0))
run("A8 Annex C N=46 R=0 (504 octets)", m, "PACK")
m = M(); annex(m, (SO, 0, 0), timing=True); run("A9 formats_offset 136 but timing kept (list really at 138)", m, "REFUSE", "stream-layout")
m = M(); annex(m, (SO, 0, 0), redundant=146); run("A10 Annex C, Table 7-8's redundant_offset", m, "REFUSE", "redundant_offset 146, not 144")
m = M(); annex(m, (SO, 0, 0), extra=bytes(2)); run("A11 Annex C, R=0 but a 2-octet tail", m, "REFUSE", "stream-layout")
m = M(); annex(m, (SO, 0, 0), (1, 2)); mut.put(m, (SO, 0, 0), 134, 1); run("A12 Annex C, R=1 but two indices", m, "REFUSE", "stream-layout")
m = M(); d = bytearray(mut.body(m, SO, 0)); struct.pack_into(">H", d, 134, 1); mut.store(m, (SO, 0, 0), bytes(d) + bytes(2))
run("A13 Table 7-8 R=1 with a consistent tail", m, "REFUSE", "in the Table 7-8 layout")
m = M(); d = bytearray(mut.body(m, SO, 0)); struct.pack_into(">H", d, 132, 144); mut.store(m, (SO, 0, 0), bytes(d))
run("A14 Table 7-8 with Annex C's redundant_offset", m, "REFUSE", "redundant_offset 144, not 146")
m = M(); d = bytearray(mut.body(m, SO, 0)); struct.pack_into(">H", d, 82, 137); mut.store(m, (SO, 0, 0), bytes(d))
run("A15 formats_offset 137", m, "REFUSE", "formats_offset 137, not 138 (Table 7-8) or 136 (Annex C)")
m = M(); annex(m, (SI, 0, 0)); mut.put(m, (SI, 0, 0), 74, 0x0102030405060708, 8)
run("A16 Annex C input, current_format outside its list (the list is read at 136)", m, "REFUSE", "current-format")
m = M(); d = bytearray(mut.body(m, SO, 0)); struct.pack_into(">H", d, 134, 9); mut.store(m, (SO, 0, 0), bytes(d) + bytes(18))
run("A17 Table 7-8 R=9 (both arms)", m, "REFUSE", "above 8")

print("== B: identify-format value type flags (IEEE 1722.1-2021 7.3.6.1)")
for vt, expect in ((0x8001, "PACK"), (0x4001, "PACK"), (0xC001, "PACK"), (0x2001, "REFUSE"), (0x0002, "REFUSE")):
    m = M(); mut.put(m, (mut.CONTROL, 0, 0), 80, vt)
    run(f"B control_value_type 0x{vt:04X}", m, expect, None if expect == "PACK" else "identify-format")

print("== C: 508-octet maximum (IEEE 1722.1-2021 7.2)")
for size, expect in ((507, "PACK"), (508, "PACK"), (509, "REFUSE")):
    m = M(); mut.add(m, (mut.CONTROL, 1, 0), mut.control(m) + bytes(size - 113))
    run(f"C a {size}-octet CONTROL", m, expect, None if expect == "PACK" else "508")

print("== D: digest octet partition against 6.2.2.8 (reviewer's own field table)")
NAME = [(4, 68)]
FIX = {  # type: (length, excluded spans per 6.2.2.8, offsets from the 7.2 tables)
    0x0000: (312, [(4, 20), (36, 48), (40, 48), (48, 112), (116, 180), (180, 244), (244, 308), (310, 312)]),
    0x0001: (78, NAME),
    0x0002: (148, NAME + [(136, 140)]),
    0x0005: (146, NAME + [(74, 82)]), 0x0006: (144, NAME + [(74, 82)]),
    0x0007: (78, NAME), 0x0008: (78, NAME),
    0x0009: (102, NAME + [(70, 76)] + [(78, 86), (86, 87), (87, 88), (88, 90), (90, 91), (91, 92),
                                        (92, 93), (93, 94), (94, 95), (95, 96)]),
    0x000A: (86, NAME + [(70, 72), (74, 82)]),
    0x000B: (108, NAME + [(92, 100)]),
    0x000E: (20, []), 0x000F: (20, []), 0x0010: (20, []), 0x0013: (20, []),
    0x0014: (90, NAME),
    0x0015: (121, NAME + [(85, 89), (93, 97), (101, 103), (107, 111), (115, 117)]),
    0x0016: (104, NAME + [(84, 92), (96, 100)]),
    0x0017: (16, []), 0x001E: (14, []), 0x000C: (76, []), 0x000D: (86, []),
    0x001B: (96, NAME + [(84, 86), (86, 88), (88, 90)]),
    0x0024: (80, NAME + [(70, 72)]),
    0x0025: (82, NAME), 0x0026: (90, NAME), 0x0027: (90, NAME), 0x0028: (90, NAME),
}


def valued(dtype, vt, n, length, type_at=80, off_at=94, cnt_at=96, start=104):
    d = bytearray(start + length)
    struct.pack_into(">H", d, 0, dtype); struct.pack_into(">H", d, type_at, vt)
    struct.pack_into(">H", d, off_at, start)
    if cnt_at is not None:
        struct.pack_into(">H", d, cnt_at, n)
    return d


VAL = [  # (what, body, excluded spans beyond object_name) per Tables 7-122..7-126 and 6.2.2.8
    ("CONTROL LINEAR_UINT8 N=1", valued(0x1A, 0x0001, 1, 9), [(108, 109)]),
    ("CONTROL LINEAR_INT16 N=2", valued(0x1A, 0x0002, 2, 28), [(112, 114), (126, 128)]),
    ("CONTROL LINEAR_INT8 N=1", valued(0x1A, 0x0000, 1, 9), []),
    ("CONTROL SELECTOR_UINT16 N=2", valued(0x1A, 0x000D, 2, 12), [(104, 106)]),
    ("CONTROL SELECTOR_STRING N=2", valued(0x1A, 0x0014, 2, 10), [(104, 106)]),
    ("CONTROL ARRAY_UINT8 N=3", valued(0x1A, 0x0016, 3, 11), [(112, 115)]),
    ("CONTROL ARRAY_FLOAT N=2", valued(0x1A, 0x001D, 2, 28), [(124, 132)]),
    ("CONTROL UTF8", valued(0x1A, 0x001F, 1, 20), [(104, 124)]),
    ("CONTROL SAMPLE_RATE", valued(0x1A, 0x0022, 1, 4), [(104, 108)]),
    ("CONTROL VENDOR", valued(0x1A, 0x3FFE, 1, 12), [(104, 116)]),
    ("CONTROL BODE N=1", valued(0x1A, 0x0020, 1, 60), [(152, 164)]),
    ("MIXER LINEAR_UINT8", valued(0x1C, 0x0001, 1, 9, 80, 86, None, 88), [(92, 93)]),
    ("MIXER SELECTOR_UINT8 N=1 (not named for MIXER)", valued(0x1C, 0x000B, 1, 5, 80, 86, None, 88), []),
    ("MATRIX ARRAY_UINT8 N=2", valued(0x1D, 0x0016, 2, 10, 80, 94, 96, 102), [(110, 112)]),
    ("MATRIX UTF8 (CONTROL only)", valued(0x1D, 0x001F, 1, 8, 80, 94, 96, 102), []),
    ("SIGNAL_TRANSCODER SELECTOR_UINT8 N=2", valued(0x23, 0x000B, 2, 6, 80, 82, 84, 100), [(100, 101)]),
]
digest = g.model_lint.model_digest


def partition(body):
    dtype = struct.unpack_from(">H", body, 0)[0]
    ref = digest({0: {dtype: {0: bytes(body)}}})
    keep = set()
    for k in range(len(body)):
        e = bytearray(body); e[k] ^= 0x5A
        if struct.unpack_from(">H", e, 0)[0] != dtype:
            continue
        if digest({0: {dtype: {0: bytes(e)}}}) == ref:
            keep.add(k)
    return keep


def expect(spans):
    return {k for a, b in spans for k in range(a, b)}


cases = [(f"type 0x{dt:04X} ({g.model_lint.type_name(dt)}) {n} octets",
          bytearray(struct.pack(">H", dt) + bytes(n - 2)), spans) for dt, (n, spans) in sorted(FIX.items())]
cases += [(w, b, NAME + s if struct.unpack_from(">H", b, 0)[0] in (0x1A, 0x1C, 0x1D, 0x23) else s) for w, b, s in VAL]
for what, body, spans in cases:
    got, want = partition(body), expect(spans)
    ok = got == want
    bad += not ok
    extra, missing = sorted(got - want), sorted(want - got)
    print(f"[{'ok' if ok else 'UNEXPECTED'}] D {what}: {len(got)} octets keep the digest"
          + ("" if ok else f"; kept but not in the clause {extra[:12]}; in the clause but moved {missing[:12]}"))

print("== E: milan_min digest")
rec = json.loads((root / "hdl/aecp/desc/model_ids.json").read_text())
head = g.build(M())[1]
hd = [l for l in head.splitlines() if "model digest" in l][0].split()[3]
print("    model_ids.json:", json.dumps(rec.get("models", rec))[:160])
print("    head report digest:", hd)
if sys.argv[1:]:
    r2 = pathlib.Path(sys.argv[1]).resolve() / "hdl/aecp/desc/gen_desc_image.py"
    spec = importlib.util.spec_from_file_location("gen_desc_image_r2", r2)
    g2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g2)
    r2d = [l for l in g2.build(t.normalised(t.MILAN_MIN))[1].splitlines() if "model digest" in l][0].split()[3]
    print("    round-2 head report digest:", r2d, "equal" if r2d == hd else "DIFFERENT")
    bad += r2d != hd
bad += hd not in json.dumps(rec)
print(f"unexpected: {bad}")
sys.exit(1 if bad else 0)
