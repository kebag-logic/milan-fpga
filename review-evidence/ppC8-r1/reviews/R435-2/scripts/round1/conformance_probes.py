#!/usr/bin/env python3
"""Reviewer conformance probes of the model lint at a processor tree.

Each probe builds one model from milan_min.json (normalised as the gate does)
and prints what build() answers. No file of the tree is changed.

usage: conformance_probes.py <processor-tree>
"""
import copy
import struct
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/desc_store"))
sys.argv = sys.argv[:1]
import test_gen_desc_image as gate  # noqa: E402

mut = gate.mut
img = gate.gen_desc_image
lint = img.model_lint


def base():
    return gate.normalised(gate.MILAN_MIN)


def answer(model, **kw):
    try:
        _, report = img.build(model, **kw)
        tail = [ln for ln in report.splitlines() if ln.startswith(("  waiver", "lint waivers"))]
        return "PACKED " + " / ".join(tail)
    except img.ImageError as exc:
        return "REFUSED " + " || ".join(str(exc).splitlines())


def probe(title, model, **kw):
    print(f"- {title}: {answer(model, **kw)}")


def digest(model):
    return lint.lint(img._grouped_descriptors(model)).digest


print("## A. Clock sources (Milan v1.2 5.3.3.6; PR #142's L6 reading)")
m = base()
src = mut.body(m, mut.CLOCK_SOURCE, 1)            # the CRF input's INPUT_STREAM source
struct.pack_into(">HH", src, 82, mut.STREAM_INPUT, 0)   # one more at AAF input 0
mut.add(m, (mut.CLOCK_SOURCE, 2, 0), src)
mut.set_sources(m, [0, 1, 2])
probe("CRF input + one INPUT_STREAM source at the AAF input (INTERNAL 0, CRF 1, AAF 2)", m)

m = base()
mut._crf_input_becomes_aaf(m)                     # two AAF inputs, no CRF input
src = mut.body(m, mut.CLOCK_SOURCE, 1)
struct.pack_into(">HH", src, 82, mut.STREAM_INPUT, 0)
mut.add(m, (mut.CLOCK_SOURCE, 2, 0), src)
mut.set_sources(m, [0, 1, 2])
probe("no CRF input, two AAF inputs, one INPUT_STREAM source on each", m)

m = base()
src = mut.body(m, mut.CLOCK_SOURCE, 1)
mut.add(m, (mut.CLOCK_SOURCE, 2, 0), src)
mut.set_sources(m, [0, 1, 2])
probe("two INPUT_STREAM sources at the one CRF input ('exactly one')", m)

print("## B. L2 parent-order beyond multi-level types (IEEE 1722.1-2021 7.2)")
m = base()
mut.put(m, (mut.STREAM_PORT_INPUT, 0, 0), 14, 2)
mut.put(m, (mut.STREAM_PORT_OUTPUT, 0, 0), 14, 0)
probe("output port's clusters 0..1, input port's 2..3 (no CONTROL involved)", m)

print("## C. L5 interface index (Milan v1.2 5.3.3.5)")
m = base()
iface = mut.body(m, mut.AVB_INTERFACE, 0)
struct.pack_into(">H", iface, 96, 2)
mut.add(m, (mut.AVB_INTERFACE, 1, 0), iface)
probe("one configuration, two AVB_INTERFACEs (ports 1 and 2)", copy.deepcopy(m))
mut.second_configuration(m)
mut.drop(m, mut.AVB_INTERFACE, 1, 1)
counts = mut.body(m, mut.CONFIGURATION, 1)
for k in range(struct.unpack_from(">H", counts, 70)[0]):
    t, n = struct.unpack_from(">HH", counts, 74 + 4 * k)
    if t == mut.AVB_INTERFACE:
        struct.pack_into(">H", counts, 76 + 4 * k, n - 1)
mut.store(m, (mut.CONFIGURATION, 1, 0), counts)
probe("configuration 1 keeps only interface 0 (same port, same index 0)", m)

print("## D. Descriptor extent per 'shall have the format of [ATDECC 7.2.x]'")
for dtype, index, extra, name in ((mut.ENTITY, 0, 8, "ENTITY 312+8"),
                                  (mut.CLOCK_SOURCE, 0, 4, "CLOCK_SOURCE 86+4"),
                                  (mut.AUDIO_CLUSTER, 0, 4, "AUDIO_CLUSTER 90+4"),
                                  (mut.AVB_INTERFACE, 0, 2, "AVB_INTERFACE 102+2"),
                                  (mut.STREAM_PORT_INPUT, 0, 2, "STREAM_PORT_INPUT 20+2"),
                                  (mut.AUDIO_CLUSTER, 0, -4, "AUDIO_CLUSTER 90-4")):
    m = base()
    data = mut.body(m, dtype, index)
    data = data + bytes(extra) if extra > 0 else data[:extra]
    mut.store(m, (dtype, index, 0), data)
    probe(name, m)

print("## E. N cap and rate cap at the boundary (positive side)")
m = base()
mut.set_formats(m, (mut.STREAM_INPUT, 0, 0), [mut.BASE_IN] * 46, 0x0205022002006000)
probe("STREAM_INPUT with 46 formats (506 octets)", m)
m = base()
mut.set_rates(m, [48000, 96000, 192000, 44100, 88200, 176400, 32000, 24000])
probe("AUDIO_UNIT with 8 rates", m)

print("## F. Model digest against IEEE 1722.1-2021 6.2.2.8")


def selector_control(options, current=0):
    """A configuration-level CONTROL_SELECTOR_UINT8 (0x000B) of len(options) options."""
    data = bytearray(104)
    struct.pack_into(">HH", data, 0, mut.CONTROL, 1)
    struct.pack_into(">H", data, 80, 0x000B)
    struct.pack_into(">Q", data, 82, 0x90E0F00000000099)
    struct.pack_into(">HH", data, 94, 104, len(options))
    return bytes(data) + bytes([current, options[0]] + options) + b"\x00\x00"


m = base()
mut.add(m, (mut.CONTROL, 1, 0), selector_control([1, 2, 3]))
d0 = digest(m)
m2 = copy.deepcopy(m)
mut.store(m2, (mut.CONTROL, 1, 0), selector_control([1, 2, 7]))
d1 = digest(m2)
m3 = copy.deepcopy(m)
mut.store(m3, (mut.CONTROL, 1, 0), selector_control([1, 2, 3], current=2))
d2 = digest(m3)
print(f"- selector option[2] 3 -> 7 (a structural field 6.2.2.8 does not exclude): "
      f"digest {'UNCHANGED' if d0 == d1 else 'changed'}")
print(f"- selector current 0 -> 2 (excluded by 6.2.2.8): digest "
      f"{'UNCHANGED' if d0 == d2 else 'changed'}")
m4 = copy.deepcopy(m)
data = mut.body(m4, mut.CONTROL, 0)
value_type = struct.unpack_from(">H", data, 80)[0]
offset = struct.unpack_from(">H", data, 94)[0]
data[offset + 1] ^= 0x01              # IDENTIFY linear maximum[0], a structural field
mut.store(m4, (mut.CONTROL, 0, 0), data)
print(f"- IDENTIFY (value type 0x{value_type:04X}) maximum[0] changed: digest "
      f"{'UNCHANGED' if digest(m4) == d0 else 'changed'}")

print("## G. Waiver input edges")
w = dict(gate.WAIVER)
m = base()
mut.input_port_without_clusters(m)
for title, waiver in (("configuration true", dict(w, configuration=True)),
                      ("first/last 0.9 floats", dict(w, first=0.2, last=0.9)),
                      ("reason a list", dict(w, reason=["x/y#1"])),
                      ("first -1", dict(w, first=-1)),
                      ("type as code 14", dict(w, type=14))):
    mm = copy.deepcopy(m)
    mm["lint_waivers"] = [waiver]
    probe(title, mm)
mm = copy.deepcopy(m)
mm["lint_waivers"] = [w, dict(w)]
probe("the same waiver twice", mm)
mm = copy.deepcopy(m)
mm["lint_waivers"] = [dict(w, rule="L1", check="port-cluster-minimum", type="STREAM_PORT_OUTPUT")]
mut.put(mm, (mut.STREAM_PORT_OUTPUT, 0, 0), 12, 0)
probe("input port waived by type STREAM_PORT_OUTPUT only (output port also cluster-less)", mm)

print("## H. Refusal text: rule, check, descriptor, clause on every lint line")
m = base()
mut.store(m, (mut.CLOCK_SOURCE, 0, 0), mut.body(m, mut.CLOCK_SOURCE, 0)[:80])
probe("CLOCK_SOURCE 0 cut to 80 bytes", m)
m = base()
m["lint_waivers"] = {"rule": "L1"}
probe("lint_waivers not a list", m)

print("## I. IEEE 1722.1-2021 7.2: 'The maximum length of a descriptor shall be 508 octets'")
m = base()
amap = bytearray(mut.body(m, mut.AUDIO_MAP, 0)[:8])
struct.pack_into(">HH", amap, 4, 8, 64)
amap += b"".join(struct.pack(">HHHH", 0, k, 0, 0) for k in range(64))
mut.store(m, (mut.AUDIO_MAP, 0, 0), bytes(amap))
probe(f"AUDIO_MAP 0 with 64 distinct mappings ({len(amap)} octets)", m)
