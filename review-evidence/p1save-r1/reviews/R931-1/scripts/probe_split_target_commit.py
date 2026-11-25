#!/usr/bin/env python3
"""R931-1: the split-target harness's own commit grade (target_grade.committed) over a finished commit run's journal and
its flash operations. Usage: probe_split_target_commit.py <checkout> <results dir> <work dir>"""
import re, sys, types
from pathlib import Path
root, res, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3])
sys.dont_write_bytecode = True
for p in ('tb/verilator/nvm_split_target', 'tb/verilator/ctrl_service_budget', 'scripts', 'sw/firmware/ctrl_nvm/test'):
    sys.path.insert(0, str(root / p))
import target_cases, target_grade                       # noqa: E402
bench, records, image = target_cases.shape_bench('endstation_ax7101_1x1_tdm8', work)
ops = [l.split() for l in (res / 'commit.log').read_text(errors='replace').splitlines() if l.startswith('FLASHOP ')]
flash = dict(erases=sum(o[2] == '216' for o in ops), programs=sum(o[2] == '2' for o in ops))
out = (res / 'commit.journal.out').read_bytes()
ctx = types.SimpleNamespace(pages=-(-image // 256), journal_out=out)
obs = types.SimpleNamespace(flash=flash)
marks = {l.split()[2]: int(l.split()[1]) / 1e5 for l in (res / 'commit.log').read_text(errors='replace').splitlines() if l.startswith('MARK ')}
print('marks, ms:', marks)
print('first erase(s), ms:', [round(int(o[1]) / 1e5, 1) for o in ops if o[2] == '216'])
print('flash:', flash, 'findings of target_grade.committed:', target_grade.committed(obs, ctx, bench) or 'none')
