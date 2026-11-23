#!/usr/bin/env python3
"""Focused core plants on disposable copies, concurrently; no checkout mutation."""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(sys.argv[1]).resolve(); P=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'sw/firmware/ctrl/test'))
import gptp_mutants as g
names={'steps-left-on-the-local-clock','multiple-responses-cleared-at-completion'}
rows=[None]+[m for m in g.MUTANTS if m.name in names]
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(lambda m:g.run_one(P/'scratch/plants',m),rows))
for name,passed,log in results:
    (P/('plant-'+name+'.log')).write_text(log+'\n')
    print(name, 'PASS' if passed else 'FAIL')
sys.exit(not all(ok for _,ok,_ in results))
