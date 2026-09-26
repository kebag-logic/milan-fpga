#!/usr/bin/env python3
"""Check the generator docstring's INPUT FORMAT sketch against the body/key rule.

Usage: sketch_probe.py <tree> [<tree> ...]

For each exported tree, the sketch between "INPUT FORMAT" and the first line
starting "The assembled body" is lifted from the module docstring, its // comments
and bare `...` list elements are removed, and a `...` suffix inside a hex string
is dropped. Each sketch descriptor is then assembled by the tree's own
descriptor_bytes(), and offsets 0-3 are compared with the normalised directory
key. The whole sketch is then passed to _grouped_descriptors(), the one place
build() enforces the rule, without the later name-binding and layout checks
(the sketch's ENTITY is schematic about name offsets). Exit 0 only if every
sketch descriptor satisfies the rule and _grouped_descriptors() accepts the
sketch, for every tree given.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path


def load(tree: Path, tag: str):
    spec = importlib.util.spec_from_file_location(tag, tree / "hdl/aecp/desc/gen_desc_image.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sketch(doc: str) -> dict:
    block = doc.split("INPUT FORMAT", 1)[1].split("The assembled body", 1)[0]
    block = block[block.index("{"):block.rindex("}") + 1]
    block = re.sub(r"//[^\n]*", "", block)
    block = re.sub(r",\s*\.\.\.\s*\]", "]", block)
    block = re.sub(r'"([0-9a-fA-F]+)\.\.\."', r'"\1"', block)
    return json.loads(block)


bad = 0
for n, arg in enumerate(sys.argv[1:]):
    tree = Path(arg).resolve()
    gen = load(tree, f"g{n}")
    model = sketch(gen.__doc__)
    print(f"== {tree.name}: sketch has {len(model['descriptors'])} descriptors")
    for desc in model["descriptors"]:
        typ = gen._type_code(desc["type"])
        idx = gen._u(desc.get("index", 0))
        body = gen.descriptor_bytes(desc)
        head = (int.from_bytes(body[0:2], "big"), int.from_bytes(body[2:4], "big"))
        ok = head == (typ, idx)
        bad += not ok
        names = [f.get("name") for f in desc.get("fields", [])][:3]
        print(f"   key type 0x{typ:04X} index {idx}; body bytes 0-3 {body[:4].hex()} "
              f"-> type 0x{head[0]:04X} index {head[1]}; first fields {names}: "
              f"{'AGREES' if ok else 'DISAGREES'}")
    try:
        groups = gen._grouped_descriptors(model)
        print(f"   _grouped_descriptors(sketch): accepted, keys {sorted(groups)}")
    except gen.ImageError as exc:
        bad += 1
        print(f"   _grouped_descriptors(sketch): ImageError: {exc}")
print("RESULT:", "every sketch agrees and is accepted" if not bad else f"{bad} disagreement(s)")
sys.exit(1 if bad else 0)
