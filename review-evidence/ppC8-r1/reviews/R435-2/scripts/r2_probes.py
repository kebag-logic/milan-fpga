#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-2 delta probes of the descriptor model lint (reviewer-owned).

usage: r2_probes.py TREE      TREE is a checkout/extraction of the processor
                              repository at the head under review.

Each probe edits a copy of hdl/aecp/desc/milan_min.json (bodies normalised to
literal bytes) and records whether build() packs it or which checks refuse it,
next to what the cited standard text requires. Nothing in TREE is written.
"""
import copy
import importlib.util
import json
import struct
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
DESC = TREE / "hdl/aecp/desc"
sys.path.insert(0, str(TREE / "tb/desc_store"))          # lint_mutations helpers only
import lint_mutations as mut                              # noqa: E402

_spec = importlib.util.spec_from_file_location("gen_desc_image_probe", DESC / "gen_desc_image.py")
gdi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gdi)
MIN = json.loads((DESC / "milan_min.json").read_text(encoding="utf-8"))
RECORDED = json.loads((DESC / "model_ids.json").read_text(encoding="utf-8"))["models"]


def normalised(model):
    out = copy.deepcopy(model)
    for row in out["descriptors"]:
        row["bytes"] = gdi.descriptor_bytes(row).hex()
        row["type"] = gdi._type_code(row["type"])
        for key in ("fields", "pad_to"):
            row.pop(key, None)
        if row["type"] != mut.ENTITY:
            row.pop("name_index", None)
    return out


def outcome(model, **kw):
    try:
        _, report = gdi.build(model, **kw)
        return "PACK", report
    except gdi.ImageError as exc:
        lines = str(exc).splitlines()
        checks = sorted({ln.split(":")[0] for ln in lines})
        return "REFUSE " + "; ".join(checks), "\n".join(lines)


RESULTS = []


def probe(name, expect, basis, model, **kw):
    got, text = outcome(model, **kw)
    ok = got == expect if expect == "PACK" else (got.startswith("REFUSE") and expect.split(" ", 1)[1] in got)
    RESULTS.append((name, expect, got, "as-expected" if ok else "UNEXPECTED", basis, text))


S_IN0, S_OUT0 = (mut.STREAM_INPUT, 0, 0), (mut.STREAM_OUTPUT, 0, 0)


def annex_c(model, at):
    """Re-lay one stream in Milan v1.2 Annex C Table C.1: formats at 136, no
    timing field, redundant_offset 136+8N, R = 0."""
    data = mut.body(model, *at)
    n = struct.unpack_from(">H", data, 84)[0]
    formats = data[138:138 + 8 * n]
    head = bytearray(data[:136])
    struct.pack_into(">H", head, 82, 136)
    struct.pack_into(">H", head, 132, 136 + 8 * n)
    struct.pack_into(">H", head, 134, 0)
    mut.store(model, at, bytes(head) + bytes(formats))


base = normalised(MIN)

# --- A. Annex C stream layout (Milan v1.2 §5.3.3.4 "may use ... for any of its Streams")
m = copy.deepcopy(base)
annex_c(m, S_OUT0)
probe("A1 output stream in Annex C Table C.1 layout (R=0)", "PACK",
      "Milan v1.2 §5.3.3.4 last paragraph + Annex C: permitted for any stream", m)
m = copy.deepcopy(base)
for at in ((mut.STREAM_INPUT, 0, 0), (mut.STREAM_INPUT, 1, 0), S_OUT0):
    annex_c(m, at)
probe("A2 every stream in Annex C layout (R=0)", "PACK",
      "Milan v1.2 §5.3.3.4 + Annex C", m)

# --- B. IDENTIFY CONTROL variants (IEEE 1722.1-2021 §7.3.5.2, Milan v1.2 §5.3.3.10)
CTL = (mut.CONTROL, 0, 0)
m = copy.deepcopy(base)
mut.put(m, CTL, 104 + 3, 255, 1)          # default 255
mut.put(m, CTL, 104 + 4, 255, 1)          # current 255 (identify on)
probe("B1 IDENTIFY default/current 255", "PACK", "§7.3.5.2 fixes min/max/step/unit only", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 111, 0x0001)              # string ref
mut.put(m, CTL, 98, 0x0005); mut.put(m, CTL, 100, 3)   # signal_type/index arbitrary
mut.put(m, CTL, 70, 1234, 4)              # block_latency
probe("B2 IDENTIFY with string ref, signal fields, latency", "PACK",
      "Milan §5.3.3.10 does not require block/control latency or signal_* valid", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 80, 0x8001)               # read-only flag + LINEAR_UINT8
probe("B3 IDENTIFY control_value_type with the read_only flag", "PACK",
      "§7.3.6.1: flags are not the value_type", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 106, 1, 1)
probe("B4 IDENTIFY step 1", "REFUSE L8 identify-format", "§7.3.5.2 step 255", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 109, 0x0100)              # multiplier 1
probe("B5 IDENTIFY unit multiplier 1", "REFUSE L8 identify-format", "§7.3.5.2 multiplier 0", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 80, 0x0000)               # LINEAR_INT8
probe("B6 IDENTIFY as CONTROL_LINEAR_INT8", "REFUSE L8 identify-format", "§7.3.5.2 UINT8", m)
m = copy.deepcopy(base)
mut.put(m, CTL, 94, 106)                  # values_offset moved
probe("B7 IDENTIFY values_offset 106", "REFUSE L8 identify-format", "§7.2.22 values_offset 104", m)
# a second, JACK-owned IDENTIFY in the right format packs (IEEE §7.3.5.2: child of a Jack)
m = copy.deepcopy(base)
jack = bytearray(78)
struct.pack_into(">HH", jack, 74, 1, 1)
mut.add(m, (mut.JACK_INPUT, 0, 0), bytes(jack), top=False)
mut.list_count(m, mut.JACK_INPUT, 1)
mut.add(m, (mut.CONTROL, 1, 0), mut.body(m, mut.CONTROL, 0), top=False)
probe("B8 a second IDENTIFY owned by a JACK", "PACK", "§7.3.5.2 child of a Jack", m)

# --- C. L12 extents and the 508 maximum
m = copy.deepcopy(base)
mut.add(m, (mut.CONTROL, 1, 0), bytes(mut.control(m))[:104] + bytes(404), top=True)
d = mut.body(m, mut.CONTROL, 1); struct.pack_into(">H", d, 80, 0x3FFE); struct.pack_into(">H", d, 96, 1)
mut.store(m, (mut.CONTROL, 1, 0), d)
probe("C1 a 508-octet vendor CONTROL", "PACK", "IEEE §7.2 max 508", m)
m = copy.deepcopy(base)
mut.add(m, (mut.CONTROL, 1, 0), bytes(mut.control(m))[:104] + bytes(405), top=True)
d = mut.body(m, mut.CONTROL, 1); struct.pack_into(">H", d, 80, 0x3FFE); struct.pack_into(">H", d, 96, 1)
mut.store(m, (mut.CONTROL, 1, 0), d)
probe("C2 a 509-octet vendor CONTROL", "REFUSE L12 descriptor-maximum", "IEEE §7.2 max 508", m)
m = copy.deepcopy(base)
mut.list_count(m, mut.JACK_INPUT, 0)
probe("C3 CONFIGURATION lists JACK_INPUT with count 0", "PACK",
      "§7.2.2: 74 + 4N with N pairs; a zero count is a count", m)
m = copy.deepcopy(base)
mut.put(m, (mut.AVB_INTERFACE, 0, 0), 76, 0x0007)    # interface_flags
probe("C4 AVB_INTERFACE interface_flags changed", "PACK", "no rule names it", m)
m = copy.deepcopy(base)
d = mut.body(m, mut.AUDIO_CLUSTER, 0) + bytes(2)
mut.store(m, (mut.AUDIO_CLUSTER, 0, 0), d)
probe("C5 AUDIO_CLUSTER 92 octets", "REFUSE L12 descriptor-extent", "§7.2.16: 90", m)

# --- D. digest exclusions (IEEE 1722.1-2021 §6.2.2.8) under the recorded id
def digest_probe(name, edit, expect):
    mm = copy.deepcopy(base)
    edit(mm)
    probe(name, expect, "§6.2.2.8", mm, model_ids=RECORDED)

digest_probe("D1 ENTITY available_index, association_id, firmware_version, serial_number",
             lambda mm: [mut.put(mm, (mut.ENTITY, 0, 0), o, 0x41, 1) for o in (39, 47, 116, 244)], "PACK")
digest_probe("D2 ENTITY entity_capabilities", lambda mm: mut.put(mm, (mut.ENTITY, 0, 0), 20, 0x12345678, 4),
             "REFUSE L9 model-digest")
digest_probe("D3 ENTITY vendor_name_string", lambda mm: mut.put(mm, (mut.ENTITY, 0, 0), 112, 7),
             "REFUSE L9 model-digest")
digest_probe("D4 IDENTIFY current 255", lambda mm: mut.put(mm, CTL, 108, 255, 1), "PACK")
digest_probe("D5 IDENTIFY default 255 (structural)", lambda mm: mut.put(mm, CTL, 107, 255, 1),
             "REFUSE L9 model-digest")
digest_probe("D6 IDENTIFY control_type changed to MUTE (structural CONTROL change)",
             lambda mm: mut.put(mm, CTL, 82, mut.MUTE, 8), "REFUSE L9 model-digest")
digest_probe("D7 AVB_INTERFACE mac + gPTP dataset", lambda mm: [mut.put(mm, (mut.AVB_INTERFACE, 0, 0), o, 0x55, 1)
                                                               for o in (70, 75, 78, 86, 87, 88, 90, 91, 92, 93, 94, 95)], "PACK")
digest_probe("D8 AVB_INTERFACE port_number", lambda mm: mut.put(mm, (mut.AVB_INTERFACE, 0, 0), 96, 5),
             "REFUSE L9 model-digest")
digest_probe("D9 CLOCK_DOMAIN clock_source_index", lambda mm: mut.put(mm, (mut.CLOCK_DOMAIN, 0, 0), 70, 1), "PACK")
digest_probe("D10 CLOCK_SOURCE flags + identifier", lambda mm: [mut.put(mm, (mut.CLOCK_SOURCE, 0, 0), 70, 3),
                                                                mut.put(mm, (mut.CLOCK_SOURCE, 0, 0), 74, 9, 8)], "PACK")
digest_probe("D11 CLOCK_SOURCE clock_source_location_index", lambda mm: mut.put(mm, (mut.CLOCK_SOURCE, 0, 0), 84, 1),
             "REFUSE L9 model-digest")
digest_probe("D12 STREAM_OUTPUT current_format (to a listed word)",
             lambda mm: None, "PACK")
digest_probe("D13 STREAM_INPUT buffer_length +1", lambda mm: mut.put(mm, S_IN0, 128,
             struct.unpack_from(">I", mut.body(mm, *S_IN0), 128)[0] + 1, 4), "REFUSE L9 model-digest")
digest_probe("D14 AUDIO_CLUSTER object_name", lambda mm: mut.put(mm, (mut.AUDIO_CLUSTER, 0, 0), 4, 0x41, 1), "PACK")
digest_probe("D15 AUDIO_CLUSTER localized_description", lambda mm: mut.put(mm, (mut.AUDIO_CLUSTER, 0, 0), 68, 3),
             "REFUSE L9 model-digest")

# --- E. waiver types and overlap (round-2 S2)
def waived(waivers):
    mm = copy.deepcopy(base)
    mut.input_port_without_clusters(mm)
    mm["lint_waivers"] = waivers
    return mm

W = {"rule": "L1", "check": "port-cluster-minimum", "configuration": 0,
     "type": "STREAM_PORT_INPUT", "first": 0, "last": 0, "reason": "kebag-logic/milan-fpga#584: probe"}
mm = waived([W])
got, text = outcome(mm)
RESULTS.append(("E0 base waived model (input port 0 has no cluster)", "info", got, "info", "-", text[-400:]))
for key, value in (("first", 0.0), ("first", True), ("configuration", "0"), ("configuration", False),
                   ("type", True), ("type", None), ("rule", 1), ("reason", ["x#1"]), ("last", 0.7)):
    w = dict(W); w[key] = value
    probe(f"E1 waiver {key}={value!r}", "REFUSE lint waiver 0", "S2 strict JSON types", waived([w]))
w = dict(W); w["type"] = 0x000E
probe("E2 waiver type as the numeric code 0x000E", "PACK", "type a name or a code", waived([w]))
probe("E3 the same waiver twice", "REFUSE lint waiver 1", "S2 overlap", waived([W, dict(W)]))
w2 = dict(W); w2["first"], w2["last"] = 0, 3
probe("E4 overlapping ranges 0..0 and 0..3", "REFUSE lint waiver 1", "S2 overlap", waived([W, w2]))
w3 = dict(W); w3["check"] = "cluster-channels"; w3["rule"] = "L7"; w3["type"] = "AUDIO_CLUSTER"
probe("E5 a second waiver of another check (stale, not an overlap)", "REFUSE lint waiver 1", "stale", waived([W, w3]))

# --- F. loaded by path: no sys.path change, a consumer's own model_rules/model_lint never used
import subprocess, tempfile, textwrap
with tempfile.TemporaryDirectory() as tmp:
    for name in ("model_rules", "model_lint"):
        Path(tmp, f"{name}.py").write_text("raise RuntimeError('consumer module shadowed the lint')\n")
    script = textwrap.dedent(f"""
        import sys, importlib.util, json
        sys.path.insert(0, {tmp!r})
        before = list(sys.path)
        spec = importlib.util.spec_from_file_location("gdi", {str(DESC / 'gen_desc_image.py')!r})
        g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
        g.build(json.load(open({str(DESC / 'milan_min.json')!r})))
        print("sys.path unchanged:", sys.path == before,
              "| model_rules/model_lint in sys.modules:", [n for n in ("model_rules", "model_lint") if n in sys.modules])
    """)
    proc = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True)
    RESULTS.append(("F1 by-path load beside shadowing consumer modules", "PACK, path unchanged",
                    (proc.stdout + proc.stderr).strip(), "as-expected" if proc.returncode == 0
                    and "unchanged: True" in proc.stdout and "[]" in proc.stdout else "UNEXPECTED", "S3", ""))

for name, expect, got, verdict, basis, text in RESULTS:
    print(f"{verdict:<12} {name}\n    expect: {expect}\n    got:    {got}\n    basis:  {basis}")
    if verdict == "UNEXPECTED" and text:
        print("    text:   " + text.replace("\n", "\n            ")[:1500])
print(f"\n{sum(r[3] == 'UNEXPECTED' for r in RESULTS)} unexpected of {len(RESULTS)}")
