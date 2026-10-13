"""Run one bounded slice of the unchanged NVM campaign, with the full naming check."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as gate

index, work = int(sys.argv[1]), Path(sys.argv[2])
table = gate.nvm_mutants.MUTANTS
selected = table[index::3]
shapes = {}
for m in table:
    stem = m.shape or gate.SELF_TEST_SHAPE
    if stem not in shapes:
        shapes[stem] = gate.prepare(gate.ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
shared = gate.fw_gtest.Build(jobs=1)
listing = {stem: gate.build(shape, work / "listing" / stem, gate.fw_gtest.Build(jobs=4, cache=shared.cache))
           for stem, shape in shapes.items()}
held = {stem: gate.suite_tests(listing[stem], shape) for stem, shape in shapes.items()}
found = [f"no defect names {n}" for n in gate.nvm_mutants.unnamed_checks(sorted(held[gate.SELF_TEST_SHAPE]))]
print(f"full campaign names all {len(held[gate.SELF_TEST_SHAPE])} checks: {not found}", flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:
    verdicts = pool.map(lambda m: gate.plant_and_grade(m, shapes[m.shape or gate.SELF_TEST_SHAPE],
                                                     held[m.shape or gate.SELF_TEST_SHAPE], work / "mutants", shared),
                        selected)
    found += [v for v in verdicts if v]
for line in found:
    print("FINDING:", line)
(work / "population.json").write_text(json.dumps([m.name for m in selected], indent=2) + "\n")
print(f"NVM slice {index + 1}/3: {len(selected)} defects; {len(found)} findings", flush=True)
raise SystemExit(bool(found))
