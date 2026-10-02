#!/usr/bin/env python3
"""For every mutation of tb/desc_store/lint_mutations.py, list every check the
lint refuses it with, so a reader can see whether each negative case fails for
its named check only.

usage: probe_mutation_exclusivity.py <processor-tree>
Prints one line per mutation: ONLY|EXTRA, the named check, the full set.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/desc_store"))
sys.argv = sys.argv[:1]
import test_gen_desc_image as gate  # noqa: E402

mut = gate.mut
only = extra = 0
for m in mut.MUTATIONS:
    model = gate.normalised(gate.MILAN_MIN)
    m.edit(model)
    checks = {"adp": m.adp or None,
              "model_ids": gate.RECORDED if m.recorded else None}
    lines = gate.refusal(model, **checks)
    found = sorted({ln.split(":")[0] for ln in lines})
    named = f"{gate.gen_desc_image.model_lint.CHECKS[m.check][0]} {m.check}"
    tag = "ONLY " if found == [named] else "EXTRA"
    only += tag == "ONLY "
    extra += tag == "EXTRA"
    print(f"{tag} | {m.name} | {named} | {'; '.join(found)}")
print(f"mutations {len(mut.MUTATIONS)}: only-named {only}, with-extra {extra}; "
      f"distinct checks {len({m.check for m in mut.MUTATIONS})} of "
      f"{len(gate.gen_desc_image.model_lint.CHECKS)}")
