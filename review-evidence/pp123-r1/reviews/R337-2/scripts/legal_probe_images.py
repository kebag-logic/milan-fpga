#!/usr/bin/env python3
"""Pack the PR test file's eight legal models with each tree's generator.

Usage: legal_probe_images.py MODEL_TREE TREE [TREE ...]

The legal models (4 key spellings x 2 body forms) come from MODEL_TREE's
tb/desc_store/test_gen_desc_image.py BodyKeyTest.model(). Each TREE's
generator packs them; the script prints each image's sha256 per tree, whether
all trees agree, and walks every image's index map to confirm bytes 0-3 of
every descriptor equal its (type, index) key (the F07.4 sentence).
"""
import hashlib
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sketch_and_f074 import walk  # noqa: E402  (reuses the index-map walker)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


model_tree = Path(sys.argv[1]).resolve()
trees = [Path(a).resolve() for a in sys.argv[2:]]
tests = load("pr_tests", model_tree / "tb/desc_store/test_gen_desc_image.py")
case = tests.BodyKeyTest()
digests, rc = {}, 0
for i, tree in enumerate(trees):
    gen = load(f"gen{i}", tree / "hdl/aecp/desc/gen_desc_image.py")
    for form in ("fields", "bytes"):
        for key, typ in tests.BodyKeyTest.KEYS:
            img, _ = gen.build(case.model(form, key, typ))
            rows, checked, bad = walk(img)
            label = f"{form}/{key!r}"
            digests.setdefault(label, []).append(hashlib.sha256(img).hexdigest())
            print(f"{tree.name:10} {label:22} {digests[label][-1]}  rows={rows} "
                  f"walked={checked} bytes0-3!=key={len(bad)}")
            rc |= 1 if bad else 0
agree = all(len(set(v)) == 1 for v in digests.values())
print(f"{len(digests)} legal images x {len(trees)} trees: "
      f"{'ALL IDENTICAL' if agree else 'DIFFER'}")
sys.exit(rc | (not agree))
