#!/usr/bin/env python3
"""Complete only ungraded NVM mutants in a frozen partition, using the repository grader."""
import argparse,json,pathlib,sys
from concurrent.futures import ThreadPoolExecutor
ap=argparse.ArgumentParser()
ap.add_argument("repo",type=pathlib.Path);ap.add_argument("work",type=pathlib.Path);ap.add_argument("plan",type=pathlib.Path)
ap.add_argument("--part",type=int,required=True);ap.add_argument("--jobs",type=int,default=4)
a=ap.parse_args();repo=a.repo.resolve();work=a.work.resolve();work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/"sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as gate
import fw_gtest,nvm_mutants
plan=json.loads(a.plan.read_text()); names=plan["parts"][a.part]
by_name={m.name:m for m in nvm_mutants.MUTANTS}; chosen=[by_name[name] for name in names]
shapes={}
for m in chosen:
    stem=m.shape or gate.SELF_TEST_SHAPE
    if stem not in shapes:shapes[stem]=gate.prepare(repo/"configs"/(stem+".yaml"),work/"shapes"/stem)
shared=fw_gtest.Build(jobs=1)
listing={stem:gate.build(shape,work/"listing"/stem,fw_gtest.Build(jobs=a.jobs,cache=shared.cache)) for stem,shape in shapes.items()}
held={stem:gate.suite_tests(listing[stem],shape) for stem,shape in shapes.items()}
with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    verdicts=list(pool.map(lambda m:gate.plant_and_grade(m,shapes[m.shape or gate.SELF_TEST_SHAPE],
          held[m.shape or gate.SELF_TEST_SHAPE],work/"mutants",shared),chosen))
bad=[v for v in verdicts if v]
for row in bad:print(row)
print("PART",a.part,"caught",len(chosen)-len(bad),"of",len(chosen))
assert not bad
