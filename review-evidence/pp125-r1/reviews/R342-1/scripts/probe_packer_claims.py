#!/usr/bin/env python3
"""Probe every packer enforcement statement in 07 section 3.1 at one checkout.

Usage: probe_packer_claims.py <processor-checkout> <out.tsv>

Each row pairs an accepted control with one invalid change.  "refuse" rows
must be refused while their control packs; "accept" rows document a semantic
check the packer does not implement: the mutated input packs and its mutated
descriptor bytes survive in the image unchanged.  Exit 0 only when every row
behaves as the documentation states.  Read-only on the checkout.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(
    "gen_desc_image", root / "hdl/aecp/desc/gen_desc_image.py")
gdi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gdi)
BASE = json.loads((root / "hdl/aecp/desc/example_milan_8.json").read_text())


def base():
    return copy.deepcopy(BASE)


def find(m, typ, idx=0, cfg=0):
    for d in m["descriptors"]:
        if d["type"] == typ and d.get("index", 0) == idx \
                and d.get("configuration", 0) == cfg:
            return d
    raise KeyError(typ)


def set_field(d, name, value):
    for f in d["fields"]:
        if f["name"] == name:
            f["value"] = value
            return
    raise KeyError(name)


def packs(m, line_bytes=576):
    try:
        img, _ = gdi.build(m, line_bytes)
        return True, img, ""
    except gdi.ImageError as exc:
        return False, None, str(exc)


def au(m, offset=144, count=2, rates=(48000, 96000)):
    """Rewrite AUDIO_UNIT[0] rate fields; its length follows the words given."""
    d = find(m, "AUDIO_UNIT")
    d.pop("pad_to", None)
    d["fields"] = [f for f in d["fields"]
                   if not f["name"].startswith("sampling_rate_")]
    set_field(d, "sampling_rates_offset", offset)
    set_field(d, "sampling_rates_count", count)
    d["fields"] += [{"name": f"sampling_rate_{i}", "size": 4, "value": r}
                    for i, r in enumerate(rates)]
    return m


def clock_domain(m, sources):
    """CLOCK_DOMAIN[0] with the given clock_sources list, plus enough
    CLOCK_SOURCE descriptors that every listed index exists."""
    d = find(m, "CLOCK_DOMAIN")
    d.pop("pad_to", None)
    d["fields"] = [f for f in d["fields"]
                   if not f["name"].startswith("clock_source_")
                   or f["name"] == "clock_source_index"]
    set_field(d, "clock_sources_count", len(sources))
    d["fields"] += [{"name": f"clock_source_{i}", "size": 2, "value": s}
                    for i, s in enumerate(sources)]
    src0 = find(m, "CLOCK_SOURCE")
    for i in range(1, max(sources) + 1):
        extra = copy.deepcopy(src0)
        extra["index"] = i
        set_field(extra, "descriptor_index", i)
        extra.pop("name_index", None)
        m["descriptors"].append(extra)
    # the example names CLOCK_SOURCE[0]; a named run must stay contiguous, so
    # unname the whole run instead of growing the name table
    for d2 in m["descriptors"]:
        if d2["type"] == "CLOCK_SOURCE":
            d2.pop("name_index", None)
            for f in d2["fields"]:
                if f["name"] == "object_name":
                    f.pop("string", None)
    return m


def body_of(m, typ, idx=0, cfg=0):
    return gdi.descriptor_bytes(find(m, typ, idx, cfg))


rows = []


def row(rule, expect, control, mutant, note, survive=None):
    c_ok, _, c_err = packs(control[0], *control[1:])
    m_ok, m_img, m_err = packs(mutant[0], *mutant[1:])
    if expect == "refuse":
        good = c_ok and not m_ok
        detail = m_err
    else:
        good = c_ok and m_ok
        detail = "packed"
        if good and survive is not None:
            s = survive(mutant[0])
            good = m_img.find(s) >= 0
            detail = f"packed; mutated {len(s)}-byte body found in image: {good}"
    rows.append((rule, expect, "accepted" if c_ok else "REFUSED:" + c_err,
                 "accepted" if m_ok else "refused", detail, note,
                 "OK" if good else "MISMATCH"))


# ---- statements the text says the packer ENFORCES at 493e5e4b ------------
cfg_gap = base()
for d in list(cfg_gap["descriptors"]):
    if d["type"] == "AVB_INTERFACE":
        e = copy.deepcopy(d); e["configuration"] = 2; e.pop("name_index", None)
        for f in e["fields"]:
            if f["name"] == "object_name":
                f.pop("string", None)
        cfg_gap["descriptors"].append(e)
row("configuration index gap", "refuse", (base(),), (cfg_gap,),
    "descriptor in cfg 2 with no cfg 1")

idx_gap = base(); d = find(idx_gap, "CLOCK_SOURCE"); d["index"] = 1
set_field(d, "descriptor_index", 1)
row("per-type index gap (L2)", "refuse", (base(),), (idx_gap,),
    "CLOCK_SOURCE indices [1] instead of [0]")

dup = base(); dup["descriptors"].append(copy.deepcopy(find(dup, "AVB_INTERFACE")))
row("duplicate directory key", "refuse", (base(),), (dup,),
    "second AVB_INTERFACE index 0")

nb = base(); d = find(nb, "ENTITY")
for f in d["fields"]:
    if f["name"] == "entity_name":
        f["string"] = "X" + str(f.get("string", ""))[1:]
row("name binding", "refuse", (base(),), (nb,),
    "ENTITY inline entity_name differs from name-table entry")

def opaque(n):
    m = base(); m["descriptors"].append(
        {"configuration": 0, "type": "0x1234", "index": 0,
         "bytes": "12340000" + "00" * (n - 4)})
    return m
row("line-buffer bound", "refuse", (opaque(576),), (opaque(577),),
    "opaque descriptor 576 B control, 577 B mutant, --line-bytes 576")

for form in ("fields", "bytes"):
    for what in ("type", "index"):
        def mk(bad, form=form, what=what):
            m = base(); d = find(m, "AVB_INTERFACE")
            if form == "bytes":
                body = bytearray(gdi.descriptor_bytes(d))
                if bad:
                    if what == "type":
                        body[0:2] = (0x000A).to_bytes(2, "big")
                    else:
                        body[2:4] = (1).to_bytes(2, "big")
                d.clear(); d.update({"configuration": 0, "type": "AVB_INTERFACE",
                                     "index": 0, "name_index": 6,
                                     "bytes": body.hex()})
            elif bad:
                set_field(d, "descriptor_type" if what == "type" else "descriptor_index",
                          "0x000A" if what == "type" else 1)
            return m
        row(f"body/key {what} ({form} input)", "refuse", (mk(False),), (mk(True),),
            f"AVB_INTERFACE body {what} disagrees with directory key")

# ---- statements the text says the packer does NOT enforce ----------------
ctl = lambda: au(base(), 144, 8, [48000] * 8)
for label, mut in (
        ("L10 offset 143", lambda: au(base(), 143, 2, (48000, 96000))),
        ("L10 count 9 (180 B)", lambda: au(base(), 144, 9, [48000] * 9)),
        ("L10 count 2, one word (length 148)", lambda: au(base(), 144, 2, (48000,))),
        ("L10 count 1, two words (length 152)", lambda: au(base(), 144, 1, (48000, 96000)))):
    row(label, "accept", (ctl(),), (mut(),),
        "AUDIO_UNIT semantic rule; control offset/count/length 144/8/176",
        survive=lambda m: body_of(m, "AUDIO_UNIT"))

row("L6 clock_sources [1,0]", "accept", (clock_domain(base(), [0, 1]),),
    (clock_domain(base(), [1, 0]),), "non-identity list shape",
    survive=lambda m: body_of(m, "CLOCK_DOMAIN"))

# ---- context rows for the ownership judgement (no packer check claimed) ---
def spi(clusters):
    m = base()
    body = ((0x000E).to_bytes(2, "big") + (0).to_bytes(2, "big")
            + bytes(8) + clusters.to_bytes(2, "big") + bytes(6))
    m["descriptors"].append({"configuration": 0, "type": "STREAM_PORT_INPUT",
                             "index": 0, "bytes": body.hex()})
    return m
row("L1/F07.2 STREAM_PORT_INPUT number_of_clusters 0", "accept", (spi(1),), (spi(0),),
    "Milan 5.3.3.8 minimum; packing is not a waiver",
    survive=lambda m: body_of(m, "STREAM_PORT_INPUT"))

zid = base(); set_field(find(zid, "ENTITY"), "entity_model_id", 0)
row("L9 entity_model_id 0", "accept", (base(),), (zid,),
    "integrator guide 6 obligation; tracked by #38",
    survive=lambda m: body_of(m, "ENTITY"))
oid = base(); set_field(find(oid, "ENTITY"), "entity_model_id", (1 << 64) - 1)
row("L9 entity_model_id all-ones", "accept", (base(),), (oid,),
    "integrator guide 6 obligation; tracked by #38",
    survive=lambda m: body_of(m, "ENTITY"))

bl = base(); d = find(bl, "STREAM_INPUT")
names = [f["name"] for f in d["fields"]]
if "buffer_length" in names:
    set_field(d, "buffer_length", 2125999)
    row("L4 STREAM_INPUT buffer_length 2125999", "accept", (base(),), (bl,),
        "no processor L4 check; parent-owned semantic",
        survive=lambda m: body_of(m, "STREAM_INPUT"))

with out.open("w") as fh:
    fh.write("rule\texpect\tcontrol\tmutant\tdetail\tnote\tverdict\n")
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")
print(out.read_text(), end="")
sys.exit(0 if all(r[-1] == "OK" for r in rows) else 1)
