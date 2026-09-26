#!/usr/bin/env python3
"""Pack the new test's eight legal models with the base and the head generator.

Usage: legal_models.py <base-tree> <head-tree>
Prints "sha256 form key" per model and exits 1 unless base == head for all.
"""
import hashlib
import importlib.util
import sys
from pathlib import Path

BASE, HEAD = (Path(a).resolve() for a in sys.argv[1:3])


def load(path, tag):
    spec = importlib.util.spec_from_file_location(tag, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


test = load(HEAD / "tb/desc_store/test_gen_desc_image.py", "t")
base = load(BASE / "hdl/aecp/desc/gen_desc_image.py", "gb")
head = load(HEAD / "hdl/aecp/desc/gen_desc_image.py", "gh")
case = test.BodyKeyTest()
bad = 0
for form in ("fields", "bytes"):
    for key, typ in test.BodyKeyTest.KEYS:
        m = case.model(form, key, typ)
        bi, bm = base.build(m)
        hi, hm = head.build(m)
        same = (bi, bm) == (hi, hm)
        bad += not same
        print(hashlib.sha256(hi).hexdigest(), form, repr(key),
              "base==head" if same else "DIFFERS")
sys.exit(1 if bad else 0)
