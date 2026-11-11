#!/usr/bin/env python3
"""digest_diag.py <lane> <export-a> <export-b>: compare two route exports input by input, with the resource gate's
own located() and inputs() normalisation, and say where their input digests part. Prints the receipt to stdout;
exit 0 when the two differ only inside the exporter's /* */ hierarchy comment (or not at all), else 1."""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402


def load(directory: Path) -> dict:
    script = (directory / "baseline_integrated.tcl").read_text()
    files, roots = gate.located(directory, script, "all-fabric")
    texts, sums = {}, {}
    for path in files:
        data = path.read_bytes()
        if str(path).startswith(roots[0] + "/"):
            text = re.sub(r"//[^\n]*", "", data.decode(errors="replace"))
            for index, root in enumerate(roots):
                text = text.replace(root, f"$ROOT{index}")
            texts[path.name] = text
            data = text.encode()
        sums.setdefault(path.name, []).append(hashlib.sha256(data).hexdigest())
    generics = [re.sub(r'"[^"]*/([^/"]+)"', r'"\1"', g) for g in gate.GENERICS.findall(script)]
    images = {Path(i["path"]).name: i["sha256"] for i in json.loads((directory / "baseline_images.json").read_text())}
    return {"script": script, "texts": texts, "sums": sums, "generics": generics, "images": images,
            "digest": gate.inputs(directory, script), "files": len(files)}


def main() -> int:
    a, b = load(Path(sys.argv[2])), load(Path(sys.argv[3]))
    print(f"gate inputs() digest, export A: {a['digest']}")
    print(f"gate inputs() digest, export B: {b['digest']}")
    print(f"files read: A {a['files']}, B {b['files']}")
    names = sorted(set(a["sums"]) | set(b["sums"]))
    differ = [n for n in names if a["sums"].get(n) != b["sums"].get(n)]
    print(f"files whose normalised sha256 differs: {differ or 'none'}")
    print(f"generics equal: {a['generics'] == b['generics']} ({len(a['generics'])} generics)")
    print(f"baseline_images.json entries equal: {a['images'] == b['images']} ({len(a['images'])} images)")
    ok = a["generics"] == b["generics"] and a["images"] == b["images"]
    for name in differ:
        if name not in a["texts"] or name not in b["texts"]:
            print(f"{name}: not a generated file, so a real input difference")
            ok = False
            continue
        la, lb = a["texts"][name].splitlines(), b["texts"][name].splitlines()
        opens = [i for i, line in enumerate(la) if line.strip() == "/*"]
        closes = [i for i, line in enumerate(la) if line.strip() == "*/"]
        lo, hi = opens[0], closes[0]
        print(f"{name}: first /* */ block is lines {lo + 1}-{hi + 1} of export A")
        moved = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
            if tag != "equal":
                moved.append((i1, i2, j1, j2))
                inside = lo <= i1 and i2 <= hi + 1 and lo <= j1 and j2 <= hi + 1
                print(f"  {tag} A {i1 + 1}-{i2} B {j1 + 1}-{j2} inside the block: {inside}")
                ok &= inside
        exact = sorted(la[lo:hi + 1]) == sorted(lb[lo:hi + 1])
        print(f"  the block holds byte-identical lines in both, only reordered: {exact}")
        # A leaf that moves into or out of the last place of its parent trades the tree glyph for the other one.
        def glyphless(lines: list[str]) -> list[str]:
            return sorted(line.replace("└──", "├──") for line in lines)
        same_multiset = glyphless(la[lo:hi + 1]) == glyphless(lb[lo:hi + 1])
        print(f"  ... with the last-child and middle-child tree glyphs treated alike: {same_multiset}")
        outside = la[:lo] + la[hi + 1:] == lb[:lo] + lb[hi + 1:]
        print(f"  outside the block the file is identical: {outside}")
        ok &= same_multiset and outside
    print("VERDICT: " + ("the synthesis inputs are identical; the digests part only in the exporter's hierarchy "
                         "comment" if ok else "a real input difference"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
