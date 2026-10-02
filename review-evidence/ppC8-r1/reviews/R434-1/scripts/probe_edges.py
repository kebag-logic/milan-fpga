#!/usr/bin/env python3
"""Reviewer edge-case probes of the model lint. Usage: probe_edges.py <repo-root>"""
import sys, pathlib, struct, copy, traceback
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/desc_store")); sys.argv = [sys.argv[0]]
import test_gen_desc_image as t, lint_mutations as mut
g = t.gen_desc_image
def run(name, model, **kw):
    try:
        _, rep = g.build(model, **kw); res = "ACCEPTED"
        tail = [l for l in rep.splitlines() if "waiver" in l or "semantic lint" in l]
        print(f"[{name}] ACCEPTED {tail}")
    except g.ImageError as e:
        print(f"[{name}] IMAGEERROR {[l.split(' (')[0] for l in str(e).splitlines()]}")
    except Exception as e:
        print(f"[{name}] CRASH {type(e).__name__}: {e}")
M = lambda: t.normalised(t.MILAN_MIN)

# E1: no CRF input, two AAF inputs, one INPUT_STREAM source per AAF input (PR #142 allowance)
m = M(); mut.set_formats(m, (mut.STREAM_INPUT,1,0), [mut.BASE_IN], 0x0205022002006000)
src = mut.body(m, mut.CLOCK_SOURCE, 1); struct.pack_into(">H", src, 84, 0)
mut.add(m, (mut.CLOCK_SOURCE, 2, 0), src); mut.set_sources(m, [0,1,2])
run("E1 no-CRF, AAF inputs 0 and 1 each with an INPUT_STREAM source", m)
# E1b: same but only one source (control)
m = M(); mut.set_formats(m, (mut.STREAM_INPUT,1,0), [mut.BASE_IN], 0x0205022002006000)
run("E1b no-CRF, one INPUT_STREAM source at AAF input 1", m)
# E2: CRF input present plus an INPUT_STREAM source at the AAF input (PR #142 / #634 shape)
m = M(); src = mut.body(m, mut.CLOCK_SOURCE, 1); struct.pack_into(">H", src, 84, 0)
mut.add(m, (mut.CLOCK_SOURCE, 2, 0), src); mut.set_sources(m, [0,1,2])
run("E2 CRF input + INPUT_STREAM source at AAF input 0", m)
# E3: empty document
run("E3 empty descriptor list", {"format":"kl-aem-image","version":1,"descriptors":[]})
# E4: malformed model_ids key
run("E4 model_ids key not hex", M(), model_ids={"zz": "00"})
# E5: waiver numeric oddities
w = dict(t.WAIVER); m = M(); mut.input_port_without_clusters(m); m["lint_waivers"]=[dict(w, first=0.7, last=0.2)]
run("E5 waiver first=0.7 last=0.2 (floats)", m)
m = M(); mut.input_port_without_clusters(m); m["lint_waivers"]=[dict(w, first=True, last=False)]
run("E5b waiver first=True last=False", m)
# E6: waiver of STREAM_PORT_INPUT cannot excuse STREAM_PORT_OUTPUT 0 (same check, same index)
m = M(); mut.input_port_without_clusters(m)
o = mut.body(m, mut.STREAM_PORT_OUTPUT, 0); struct.pack_into(">H", o, 12, 0); mut.store(m, (mut.STREAM_PORT_OUTPUT,0,0), o)
m["lint_waivers"]=[w]; run("E6 input-port waiver, output port 0 also cluster-less", m)
# E7: a waiver for a whole type without range on a per-descriptor check
m = M(); mut.input_port_without_clusters(m)
m["lint_waivers"]=[{k:v for k,v in w.items() if k not in ("first","last")}]
run("E7 rangeless waiver on per-descriptor check", m)
# E8: reason that only *contains* an issue ref token inside other text
m = M(); mut.input_port_without_clusters(m); m["lint_waivers"]=[dict(w, reason="see a#1")]
run("E8 reason 'see a#1'", m)
# E9: lint_waivers not a list / waiver with lint off
m = M(); m["lint_waivers"] = {"x":1}; run("E9 lint_waivers is an object", m)
# E10: CONTROL owned by a JACK_INPUT (IEEE 7.2.7 number_of_controls/base_control): top-level count
m = M(); jack = bytearray(74); struct.pack_into(">HH", jack, 0, 0x0007, 0)
struct.pack_into(">HH", jack, 70, 1, 1)  # jack_flags? see layout note
# JACK layout: 68 loc desc, 70 jack_flags, 72 jack_type, 74 number_of_controls, 76 base_control
jack = bytearray(78); struct.pack_into(">HH", jack, 0, 0x0007, 0); struct.pack_into(">HHHH", jack, 68, 0xFFFF, 0, 0x0008, 1); struct.pack_into(">HH", jack, 74, 1, 1)
m["descriptors"].append({"configuration":0,"type":0x0007,"index":0,"bytes":bytes(jack).hex()})
cfgd = mut.body(m, mut.CONFIGURATION, 0); n = struct.unpack_from(">H", cfgd, 70)[0]
cfgd = cfgd + struct.pack(">HH", 0x0007, 1); struct.pack_into(">H", cfgd, 70, n+1); mut.store(m, (mut.CONFIGURATION,0,0), cfgd)
ctl = mut.body(m, mut.CONTROL, 0); struct.pack_into(">HHQ", ctl, 0, 0x001A, 1, 0); struct.pack_into(">Q", ctl, 82, 0x90E0F00000000002)
m["descriptors"].append({"configuration":0,"type":0x001A,"index":1,"bytes":bytes(ctl).hex()})
run("E10 JACK_INPUT owning CONTROL 1, descriptor_counts CONTROL 1 (top level only)", m)
# E11: current_format carrying the ut bit and listed verbatim
m = M(); s = mut.body(m, mut.STREAM_INPUT, 0); struct.pack_into(">Q", s, 74, 0x0215022002006000); mut.store(m,(mut.STREAM_INPUT,0,0),s)
run("E11 current_format with ut bit (equal to list entry)", m)
# E12: duplicate static mapping across two output AUDIO_MAPs
m = M(); amap = mut.body(m, mut.AUDIO_MAP, 0); a2 = bytearray(amap); struct.pack_into(">HH", a2, 0, 0x0017, 1)
m["descriptors"].append({"configuration":0,"type":0x0017,"index":1,"bytes":bytes(a2).hex()})
o = mut.body(m, mut.STREAM_PORT_OUTPUT, 0); struct.pack_into(">H", o, 16, 2); mut.store(m, (mut.STREAM_PORT_OUTPUT,0,0), o)
run("E12 AUDIO_MAP 1 repeats AUDIO_MAP 0's mappings", m)
# E13: CRF input listing the Milan word plus a 44.1 kHz CRF word, current at 44.1 kHz
m = M(); mut.set_formats(m, (mut.STREAM_INPUT,1,0), [mut.CRF, 0x041060010000AC44], 0x041060010000AC44)
run("E13 CRF input [BB80, AC44], current_format AC44", m)
# E14: CRF output stream beside the AAF output, listing only a non-Milan CRF word -> control (refused)
m = M(); mut.set_formats(m, (mut.STREAM_INPUT,1,0), [0x041060010000AC44], 0x041060010000AC44)
run("E14 CRF input [AC44] only (control)", m)
