#!/usr/bin/env python3
"""For each named mutation of milan_min.json, list every check the lint refuses
with. Usage: probe_mutation_checks.py <repo-root>"""
import sys, json, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/desc_store"))
sys.argv = [sys.argv[0]]
import test_gen_desc_image as t
import lint_mutations as mut
only = extra = 0
for m in mut.MUTATIONS:
    model = t.normalised(t.MILAN_MIN); m.edit(model)
    checks = {"adp": m.adp or None, "model_ids": t.RECORDED if m.recorded else None}
    try:
        t.gen_desc_image.build(model, **checks); lines = ["<ACCEPTED>"]
    except t.gen_desc_image.ImageError as e:
        lines = str(e).splitlines()
    got = sorted({l.split(":")[0] for l in lines})
    named = f"{t.gen_desc_image.model_lint.CHECKS[m.check][0]} {m.check}"
    tag = "ONLY" if got == [named] else ("EXTRA" if named in got else "MISSING")
    only += tag == "ONLY"; extra += tag == "EXTRA"
    print(f"{tag:7} {m.name!r:55} named={named} got={got}")
print(f"SUMMARY mutations={len(mut.MUTATIONS)} only={only} extra={extra}")
