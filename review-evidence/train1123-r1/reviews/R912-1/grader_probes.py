#!/usr/bin/env python3
"""Disposable in-memory probes of the composition's grading amendment."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
folder = root/'tb/verilator/ctrl_service_budget'
sys.path.insert(0,str(folder))
path = folder/'kept_grade.py'
source = path.read_text()
packet=Path(__file__).resolve().parent
def module(text):
    spec=importlib.util.spec_from_file_location('review_probe',path)
    mod=importlib.util.module_from_spec(spec)
    exec(compile(text,str(path),'exec'),mod.__dict__)
    return mod

cases = {
 'margin-removed': ('KEPT_MARGIN_PERCENT = 5','KEPT_MARGIN_PERCENT = 0'),
 'margin-too-wide': ('KEPT_MARGIN_PERCENT = 5','KEPT_MARGIN_PERCENT = 7'),
 'margin-too-narrow': ('KEPT_MARGIN_PERCENT = 5','KEPT_MARGIN_PERCENT = 3'),
 'strict-edge': ('return kept * 100 <= bound *','return kept * 100 < bound *'),
 'bound-build-rejected': ("BOUND_OWED_BUILDS = ('build-one',)", 'BOUND_OWED_BUILDS = ()'),
 'whole-build-waived': ("BOUND_OWED_BUILDS = ('build-one',)", "BOUND_OWED_BUILDS = ('build-one', 'build')"),
 'kept-build-waived': ("name == kept_window.BOUND and o['kind']", "name in OWED_KINDS and o['kind']"),
 'bound-line-not-owed': ('"a build-one pass of ",','"a wrong-build-one pass of ",'),
 'bound-slice-not-owed': ('"a tier-2 slice of THE TRANSMIT\'s build of ")}', '"a wrong-tier-2 slice of THE TRANSMIT\'s build of ")}'),
 'kept-line-owed': ('OWED_KINDS = {kept_window.NAME: (', 'OWED_KINDS = {kept_window.NAME: ("a build-one pass of ", '),
 'kept-slice-owed': ('OWED_KINDS = {kept_window.NAME: (', 'OWED_KINDS = {kept_window.NAME: ("a tier-2 slice of THE TRANSMIT\'s build of ", '),
}
rows=[]
baseline=module(source)
checks=baseline.selftest()
rows.append(dict(probe='baseline',passed=all(ok for _,ok,_ in checks),checks=len(checks)))
for name,(old,new) in cases.items():
    assert source.count(old)==1,(name,source.count(old))
    mod=module(source.replace(old,new))
    checks=mod.selftest()
    caught=[what for what,ok,_ in checks if not ok]
    direct=[]
    for kept,bound,expected in [(104000,100000,True),(106000,100000,False),
                                (105000,100000,True),(105001,100000,False)]:
        if mod.kept_within(kept,bound) != expected:
            direct.append(f'{kept}/{bound}: expected {expected}')
    rows.append(dict(probe=name,passed=bool(caught or direct),caught_by=caught,direct_checks=direct))
# Direct values from the amendment and its stated boundary controls.
for kept,bound,expected in [(142582,142137,True),(104000,100000,True),(106000,100000,False),
                            (105000,100000,True),(105001,100000,False),(149243,142137,True),
                            (149244,142137,False)]:
    rows.append(dict(probe=f'cycles {kept}/{bound}',passed=baseline.kept_within(kept,bound)==expected,
                     expected=expected,line=baseline.kept_line('review',kept,bound)))
print(json.dumps(rows,indent=2))
assert all(r['passed'] for r in rows)
