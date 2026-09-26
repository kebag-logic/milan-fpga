#!/usr/bin/env python3
"""Check the generator's input sketch and the F07.4 bytes 0-3 sentence.

Usage: sketch_and_f074.py <tree> [<tree> ...]

For each exported processor tree:
1. Lift the JSON sketch out of gen_desc_image.py's INPUT FORMAT docstring
   (drop // comments, the bare `...` list token and the `...` after a hex
   prefix; string placeholders stay literal) and run the generator's own _grouped_descriptors() on it: this is
   the body/key rule. build() is also run, to report which rule (if any) still
   refuses the sketch.
2. Pack example_milan_8.json and walk the produced image's header and index
   map: for every row and every member i, bytes 0-3 at elem_off + i*stride
   must be (descriptor_type, first + i), where `first` is the running count of
   earlier rows of the same (cfg, type). That is the F07.4 sentence, checked
   on the bytes the store would serve rather than on the generator's source.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path


def load(tree):
    spec = importlib.util.spec_from_file_location(
        f"gen_{abs(hash(str(tree)))}", tree / "hdl/aecp/desc/gen_desc_image.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sketch_model(mod):
    doc = mod.__doc__
    start = doc.index("{", doc.index("INPUT FORMAT"))
    end = doc.index("\n}\n", start) + 2
    text = re.sub(r"//[^\n]*", "", doc[start:end])
    text = text.replace(', ...', '')
    # Only a hex prefix loses its trailing ellipsis; a "string": "..." name
    # placeholder is kept literally (its bytes are 2E 2E 2E), so a sketch
    # that relied on the name's first bytes for descriptor_index is caught.
    text = re.sub(r'"([0-9a-fA-F]+)\.\.\."', r'"\1"', text)
    return json.loads(text)


def walk(img):
    u16 = lambda o: int.from_bytes(img[o:o + 2], "big")
    u32 = lambda o: int.from_bytes(img[o:o + 4], "big")
    n_entries, index_off = u16(0x08), u32(0x0C)
    seen, checked, bad = {}, 0, []
    for e in range(n_entries):
        row = index_off + 16 * e
        cfg, typ, count = u16(row), u16(row + 2), u16(row + 4)
        elem_off, stride = u32(row + 8), u16(row + 14)
        first = seen.get((cfg, typ), 0)
        for i in range(count):
            at = elem_off + i * stride
            got = (u16(at), u16(at + 2))
            checked += 1
            if got != (typ, first + i):
                bad.append((cfg, typ, first + i, got))
        seen[(cfg, typ)] = first + count
    return n_entries, checked, bad


def main():
    rc = 0
    for arg in sys.argv[1:]:
        tree = Path(arg).resolve()
        mod = load(tree)
        model = sketch_model(mod)
        print(f"== {arg}")
        print("sketch descriptors:",
              [(d["type"], d.get("index"), "fields" if "fields" in d else "bytes")
               for d in model["descriptors"]])
        for d in model["descriptors"]:
            body = mod.descriptor_bytes(d)
            print(f"  {d['type']}: body[0:4]={body[:4].hex()} len={len(body)}")
        try:
            mod._grouped_descriptors(model)
            print("sketch body/key rule (_grouped_descriptors): ACCEPTED")
        except mod.ImageError as exc:
            print(f"sketch body/key rule (_grouped_descriptors): REFUSED: {exc}")
        try:
            mod.build(model)
            print("sketch build(): ACCEPTED")
        except mod.ImageError as exc:
            print(f"sketch build(): REFUSED: {exc}")
        ex = json.loads((tree / "hdl/aecp/desc/example_milan_8.json").read_text())
        img, _ = mod.build(ex)
        rows, checked, bad = walk(img)
        print(f"example_milan_8 image: {rows} index rows, {checked} descriptors "
              f"walked, {len(bad)} with bytes 0-3 != key {bad[:5]}")
        rc |= 1 if bad else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
