# Standalone bounded validation helper; run from a disposable candidate checkout.
import os
import concurrent.futures
import json
from pathlib import Path
import sys

repo = Path.cwd()
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as gate

first, last = map(int, sys.argv[1:])
work = Path(os.environ["VALIDATION_WORK"]).resolve() / f"nvm-batch-{first}-{last}"
mutants = gate.nvm_mutants.MUTANTS[first-1:last]
shapes = {stem: gate.prepare(gate.ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
          for stem in {m.shape or gate.SELF_TEST_SHAPE for m in gate.nvm_mutants.MUTANTS}}
shared = gate.fw_gtest.Build(jobs=1)
listing = {stem: gate.build(shape, work / "listing" / stem,
                           gate.fw_gtest.Build(jobs=4, cache=shared.cache))
           for stem, shape in shapes.items()}
held = {stem: gate.suite_tests(listing[stem], shape) for stem, shape in shapes.items()}
missing = gate.nvm_mutants.unnamed_checks(sorted(held[gate.SELF_TEST_SHAPE]))
assert not missing, missing

def grade(mutant):
    stem = mutant.shape or gate.SELF_TEST_SHAPE
    result = gate.plant_and_grade(mutant, shapes[stem], held[stem], work / "mutants", shared)
    record = dict(name=mutant.name, kills=mutant.kills, finding=result)
    (work / (mutant.name + ".json")).write_text(json.dumps(record) + "\n")
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    findings = [f for f in pool.map(grade, mutants) if f]
print(f"Batch {first}-{last}: {len(mutants)-len(findings)}/{len(mutants)} caught", flush=True)
for finding in findings:
    print(finding, flush=True)
sys.exit(bool(findings))
