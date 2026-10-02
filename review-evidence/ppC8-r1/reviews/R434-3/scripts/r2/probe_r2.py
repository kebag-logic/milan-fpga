#!/usr/bin/env python3
"""Round-2 reviewer probes of the model lint at the exact head (no file written).
Usage: probe_r2.py <repo-root>"""
import copy, struct, sys, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/desc_store")); sys.argv = [sys.argv[0]]
import test_gen_desc_image as t, lint_mutations as mut
g = t.gen_desc_image
def run(name, model, **kw):
    try:
        _, rep = g.build(model, **kw)
        print(f"[{name}] ACCEPTED {[l for l in rep.splitlines() if 'waiver' in l]}")
    except g.ImageError as e:
        print(f"[{name}] REFUSED {[l.split(' (')[0] for l in str(e).splitlines()]}")
M = lambda: t.normalised(t.MILAN_MIN)

# A1: Milan v1.2 Annex C Table C.1 layout on STREAM_OUTPUT 0 (formats at 136, no timing
# field, 136 + 8N octets, R = 0), which 07 §3.2's Δ note calls a permitted normative layout.
m = M(); s = mut.body(m, mut.STREAM_OUTPUT, 0)
n = struct.unpack_from(">H", s, 84)[0]; fm = s[138:138 + 8 * n]
c = bytearray(s[:136]); struct.pack_into(">H", c, 82, 136); struct.pack_into(">H", c, 132, 136 + 8 * n)
mut.store(m, (mut.STREAM_OUTPUT, 0, 0), bytes(c) + fm)
run("A1 STREAM_OUTPUT 0 in Milan Annex C layout (formats at 136, no timing)", m)
# A1b: control, the same stream in Table 7-8 layout (the head model)
run("A1b control: milan_min unchanged", M())
# A2: a 508-octet non-subset descriptor (a MUTE CONTROL) packs; 509 is refused
for size in (506, 507, 508, 509):
    m = M(); body = bytearray(mut.control(m)) + bytes(size - 113)
    mut.add(m, (mut.CONTROL, 1, 0), bytes(body[:size]))
    run(f"A2 a {size}-octet MUTE CONTROL", m)
# A3: identify-format, each arm alone, on CONTROL 0 (the primary IDENTIFY)
for what, off, val, size in (("maximum 1", 105, 1, 1), ("minimum 1", 104, 1, 1), ("step 1", 106, 1, 1),
                             ("unit code 1", 110, 1, 1), ("values_offset 105", 94, 105, 2),
                             ("number_of_values 2", 96, 2, 2), ("control_value_type UINT16", 80, 3, 2),
                             ("control_value_type UINT8 with the r flag", 80, 0x8001, 2)):
    m = M(); mut.put(m, (mut.CONTROL, 0, 0), off, val, size); run(f"A3 IDENTIFY {what}", m)
m = M(); mut.store(m, (mut.CONTROL, 0, 0), mut.body(m, mut.CONTROL, 0) + bytes(9))
run("A3 IDENTIFY 122 octets (two values' room)", m)
# A4: overlapping waivers whose ranges share only some descriptors (0..1 and 1..1)
m = M(); mut.input_port_without_clusters(m); m["lint_waivers"] = [dict(t.WAIVER), dict(t.WAIVER, first=0, last=0, reason="o/r#2: again")]
run("A4a identical-scope waivers", m)
m = M(); mut.second_configuration(m)
m["lint_waivers"] = []
# two cluster-less input ports in one config: build by adding a second input port
m = M(); mut.input_port_without_clusters(m)
p = mut.body(m, mut.STREAM_PORT_INPUT, 0); mut.add(m, (mut.STREAM_PORT_INPUT, 1, 0), p, top=False)
mut.put(m, (mut.AUDIO_UNIT, 0, 0), 72, 2)
m["lint_waivers"] = [dict(t.WAIVER, first=0, last=1), dict(t.WAIVER, first=1, last=1, reason="o/r#2: partial")]
run("A4b waivers 0..1 then 1..1 (partial overlap)", m)
m["lint_waivers"] = [dict(t.WAIVER, first=0, last=1)]
run("A4c control: one waiver 0..1", m)
# A5: L5, a port that first appears in configuration 1
m = M(); mut.second_configuration(m); mut.second_interface(m, 1)
run("A5 configuration 1 adds port 2 at AVB_INTERFACE 1", m)
# A6: digest exclusions the gate does not pin: CLOCK_DOMAIN clock_source_index, ENTITY current_configuration
m = M(); mut.second_configuration(m); rec = {"0x020000FFFE00C801": t.digest(m)}
mut.put(m, (mut.CLOCK_DOMAIN, 0, 0), 70, 1); mut.put(m, (mut.ENTITY, 0, 0), 310, 1)
run("A6 clock_source_index 1 and current_configuration 1 under the two-configuration record", m, model_ids=rec)
# A7: CONTROLs owned by an AVB_INTERFACE, a CONTROL_BLOCK and a PTP_INSTANCE are not top-level
m = M(); mut.add(m, (mut.CONTROL, 1, 0), mut.control(m), top=False); mut.own_controls(m, (mut.AVB_INTERFACE, 0), 98, 1)
run("A7a AVB_INTERFACE 0 owns CONTROL 1", m)
m = M(); cb = bytearray(74); struct.pack_into(">HH", cb, 70, 1, 1); mut.add(m, (0x0025, 0, 0), cb); mut.list_count(m, 0x0025, 1)
mut.add(m, (mut.CONTROL, 1, 0), mut.control(m), top=False); run("A7b CONTROL_BLOCK 0 owns CONTROL 1", m)
m = M(); pi = bytearray(90); struct.pack_into(">HH", pi, 82, 1, 1); mut.add(m, (0x0027, 0, 0), pi); mut.list_count(m, 0x0027, 1)
mut.add(m, (mut.CONTROL, 1, 0), mut.control(m), top=False); run("A7c PTP_INSTANCE 0 owns CONTROL 1", m)
