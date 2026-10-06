#!/usr/bin/env python3
"""Run all 17 FC model/firmware plants and the re-pointed composition plant.
Arguments: exact source checkout, disposable output directory.
"""
import sys
from pathlib import Path
root,work=map(lambda s:Path(s).resolve(),sys.argv[1:])
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_mutants
from ctrl_reuse import cut_reuse
reuse=work/'reuse'
cut_reuse(reuse)
all_arms=ctrl_mutants.MUTANTS
start=next(i for i,a in enumerate(all_arms) if a.name=='model-tag-stripped')
selected=all_arms[start:]+tuple(a for a in all_arms if a.name=='app-binds-pool-after-the-mailbox')
assert len(selected)==18
ctrl_mutants.MUTANTS=selected
print('Selected:', ', '.join(a.name for a in selected))
raise SystemExit(int(ctrl_mutants.campaign(work/'mutants',reuse)))
