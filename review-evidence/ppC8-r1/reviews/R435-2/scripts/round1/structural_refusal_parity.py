#!/usr/bin/env python3
"""The packer's pre-existing structural refusals keep their text and order.

Runs a battery of layout-negative documents through the base packer
(gen_desc_image.py at 03c842a7) and the head packer, lint on and lint off, and
requires the same ImageError text from all three. Also packs every positive
the base accepts and requires byte-identical images with the lint off.

usage: structural_refusal_parity.py <base gen_desc_image.py> <head processor tree>
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load("gen_base", sys.argv[1])
tree = Path(sys.argv[2]).resolve()
head = load("gen_desc_image", tree / "hdl/aecp/desc/gen_desc_image.py")
example = json.loads((tree / "hdl/aecp/desc/example_milan_8.json").read_text())
milan = json.loads((tree / "hdl/aecp/desc/milan_min.json").read_text())


def first(doc, kind):
    rows = [r for r in doc["descriptors"] if r["type"] in kind]
    return rows


def variants(doc, label):
    out = []
    d = copy.deepcopy(doc); d["format"] = "x"; out.append((f"{label}: wrong format", d))
    d = copy.deepcopy(doc); d["version"] = 99; out.append((f"{label}: wrong version", d))
    d = copy.deepcopy(doc); d["descriptors"] = []; out.append((f"{label}: no descriptors", d))
    d = copy.deepcopy(doc); d["descriptors"].append(copy.deepcopy(d["descriptors"][-1]))
    out.append((f"{label}: duplicate of the last row", d))
    d = copy.deepcopy(doc); r = d["descriptors"][-1]; r["index"] = int(r.get("index", 0)) + 5
    out.append((f"{label}: last row's key index moved (body disagrees)", d))
    d = copy.deepcopy(doc); r = copy.deepcopy(d["descriptors"][-1]); r["configuration"] = 3
    d["descriptors"].append(r); out.append((f"{label}: row in configuration 3", d))
    d = copy.deepcopy(doc); r = d["descriptors"][0]; r["name_index"] = 70000
    out.append((f"{label}: invalid name_index", d))
    for lb in (64, 128):
        out.append((f"{label}: line_bytes {lb}", (copy.deepcopy(doc), lb)))
    d = copy.deepcopy(doc); d["descriptors"] = d["descriptors"][::-1]
    d["descriptors"].append(copy.deepcopy(d["descriptors"][0]))
    d["format"] = "x"
    out.append((f"{label}: two faults (format and a duplicate): first one wins", d))
    return out


def outcome(module, doc, lb, **kw):
    try:
        img, _ = module.build(copy.deepcopy(doc), lb, **kw)
        return ("PACK", img)
    except module.ImageError as exc:
        return ("REFUSE", str(exc))
    except Exception as exc:  # noqa: BLE001
        return ("CRASH", f"{type(exc).__name__}: {exc}")


bad = 0
cases = variants(example, "example_milan_8") + variants(milan, "milan_min")
cases += [("example_milan_8: positive", example), ("milan_min: positive", milan)]
for label, item in cases:
    doc, lb = item if isinstance(item, tuple) else (item, 576)
    b = outcome(base, doc, lb)
    off = outcome(head, doc, lb, lint=False)
    on = outcome(head, doc, lb)
    if b[0] == "REFUSE":
        same = b == off == on
        verdict = "SAME-TEXT" if same else "DIFFER"
    elif b[0] == "PACK":
        same = off == b
        verdict = "SAME-BYTES(lint off)" if same else "DIFFER"
    else:
        same, verdict = False, "BASE-CRASH"
    bad += not same
    shown = b[1] if b[0] != "PACK" else f"{len(b[1])} bytes"
    print(f"{verdict} | {label} | base {b[0]}: {str(shown)[:160]} | head lint-on {on[0]}")
print(f"cases {len(cases)}, differing {bad}")
sys.exit(1 if bad else 0)
