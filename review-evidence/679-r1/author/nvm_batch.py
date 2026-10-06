import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path("sw/firmware/ctrl_nvm/test").resolve()))
import test_ctrl_nvm as t
start, stop = map(int, sys.argv[1:3])
work=Path(sys.argv[3]).resolve()
all_mutants=t.nvm_mutants.MUTANTS
selected=all_mutants[start:stop]
assert len(selected)==stop-start and stop<=len(all_mutants)
print(f"Original inventory {len(all_mutants)}; batch [{start}:{stop}]")
stems={m.shape or t.SELF_TEST_SHAPE for m in all_mutants}
shapes={stem:t.prepare(t.ROOT/"configs"/f"{stem}.yaml", work/"shapes"/stem) for stem in stems}
shared=t.fw_gtest.Build(jobs=1)
listing={stem:t.build(shapes[stem], work/"listing"/stem, t.fw_gtest.Build(jobs=4,cache=shared.cache)) for stem in stems}
held={stem:t.suite_tests(listing[stem],shapes[stem]) for stem in stems}
missing=t.nvm_mutants.unnamed_checks(sorted(held[t.SELF_TEST_SHAPE]))
assert not missing, missing
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda m:t.plant_and_grade(m,shapes[m.shape or t.SELF_TEST_SHAPE],held[m.shape or t.SELF_TEST_SHAPE],work/"mutants",shared),selected))
for result in results:
    if result: print(result)
assert not any(results), results
print(f"BATCH PASS [{start}:{stop}] / {len(all_mutants)}")
