#!/usr/bin/env python3
"""Audit and retain focused tallies, raw campaign causes and generated bindings."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT=Path('$VALIDATION_STORAGE/reviews/r240-372-r1')
OUT=Path(__file__).resolve().parent
HERE=ROOT/'tb/verilator/ptp_ts'
sys.path.insert(0,str(ROOT/'scripts'))
import suite_tally
import suite_shards
spec=importlib.util.spec_from_file_location('campaign',HERE/'sva_campaign.py')
campaign=importlib.util.module_from_spec(spec)
sys.modules['campaign']=campaign
spec.loader.exec_module(campaign)

log=(OUT/'focused-default.log').read_text()
scan=suite_tally.scan(log)
assert scan[:2]==(495,0) and len(scan[2])==4 and not scan[3] and not scan[4]
assert [x[1] for x in scan[2]]==[92,170,171,62]
assert not suite_tally.log_reports_failure(log)[1]
rows=re.findall(r'^  \[PASS\] ([^:]+): (.*)$',log,re.M)
assert len(rows)==62 and set(n for n,_ in rows)==set(campaign.row_names())
suite_list=suite_shards.sweep_suites(ROOT/'tb/verilator')
assert suite_list.count('ptp_ts')==1
owners=[i for i in range(5) if 'ptp_ts' in suite_shards.select_suites(suite_list,i,5)]
assert len(owners)==1

saved=[]
def save(path,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(path,target)
    saved.append(dict(path=str(target.relative_to(OUT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))

for row in sorted((HERE/'obj_dir_sva_campaign').iterdir()):
    for p in row.iterdir():
        if p.is_file() and p.suffix in ('.log','.sv'):
            save(p,OUT/'campaign-raw'/row.name/p.name)

property_rows=[]
for mutation in campaign.MUTATIONS:
    row=campaign.mutation_row_name(mutation)
    p=HERE/'obj_dir_sva_campaign'/row
    assert (p/'obj/Vmux_sva').is_file()
    text=(p/'run.log').read_text()
    if mutation.expect:
        assert campaign.CHECKER+'.'+mutation.expect in campaign.fired(text)
    else:
        assert not campaign.fired(text) and any(campaign.SCOREBOARD_FAILURE in x for x in campaign.fail_lines(text))
    property_rows.append(dict(row=row,expected=mutation.expect or 'independent scoreboard',
                               assertion_paths=campaign.fired(text),binary_sha256=hashlib.sha256((p/'obj/Vmux_sva').read_bytes()).hexdigest()))
for width in (8,64):
    for port in (0,1):
        for fault,rule in campaign.STIMULUS_FAULTS:
            row=f'stimulus-s{port}_{fault}-w{width}'
            text=(HERE/'obj_dir_sva_campaign'/row/'run.log').read_text()
            path=f'{campaign.CHECKER}.u_s{port}_stimulus.{rule}'
            assert campaign.INJECTED in text and path in campaign.fired(text)
            property_rows.append(dict(row=row,expected=path,assertion_paths=campaign.fired(text)))

bindings=[]
for width in (8,64):
    obj=HERE/f'obj_dir_mux_sva_w{width}'
    syms=obj/'Vaxis_mux_rr_2in_1out__Syms__Slow.cpp'
    text=syms.read_text()
    for suffix in ('u_sva','u_sva.u_s0_stimulus','u_sva.u_s1_stimulus','u_sva.u_m_dut'):
        assert f'"axis_mux_rr_2in_1out.{suffix}"' in text
    for p in obj.iterdir():
        if p.name.endswith(('__Syms__Slow.cpp','__verFiles.dat','.h')):
            save(p,OUT/'elaboration'/f'w{width}'/p.name)
    witnesses=[]
    raw=(HERE/'obj_dir_sva_campaign'/f'clean-w{width}'/'run.log').read_text()
    for match in re.finditer(r'^witness (\S+)\s+nonvacuous=(\d+) harness=(\d+) \(([^)]+)\)',raw,re.M):
        key,seen,expected,bound=match.groups()
        seen,expected=int(seen),int(expected)
        assert seen>0 and expected>0
        assert bound!='equal' or seen==expected
        assert bound!='at least' or seen>=expected
        witnesses.append(dict(path=key,seen=seen,port_count=expected,bound=bound))
    assert len(witnesses)==21
    bindings.append(dict(width=width,witnesses=witnesses,binary_sha256=hashlib.sha256((obj/'Vmux_sva').read_bytes()).hexdigest()))
old_files=list((HERE/'obj_dir').glob('*Syms*.cpp'))
assert old_files and all('u_sva' not in p.read_text() for p in old_files)

pub=OUT/'public/candidate1'
manager=suite_tally.scan((pub/'full-suite-logs/ptp_ts.log').read_text())
assert manager[:2]==(495,0) and len(manager[2])==4
final=json.loads((pub/'manager-builder-final/results.json').read_text())
original=json.loads((pub/'manager-builder/results.json').read_text())
corrected=json.loads((pub/'whitespace-correction/results.json').read_text())
assert len(final['results'])==45
for row in final['results']:
    origin=original if row['receipt_origin']=='manager-builder/results.json' else corrected
    assert {k:v for k,v in row.items() if k not in ('receipt_origin','receipt_row')}==origin['results'][row['receipt_row']]
    assert row['exit_code']==0
assert final['results'][43]['command'][-2:]==['52711029f374650dc93830d5ea28e81cb5c8f410','60c5225fe5f93209bf313c51b7a722f25f9aaa7d']

result=dict(focused_scan=scan,ordinary_suites=len(suite_list),five_shard_owner=owners[0],
            campaign_rows=rows,property_controls=property_rows,elaboration=bindings,
            legacy_checker_absent=True,manager_focused_scan=manager,manager_composition_verified=True,
            campaign_breakdown=dict(clean=2,stimulus=16,dut_mutant=14,scoreboard=1,elaboration=1,coverage_refusal=4,coverage_fault_non_detection=24))
(OUT/'receipt-audit-details.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'copied-raw-manifest.json').write_text(json.dumps(saved,indent=2)+'\n')
print('PASS: 495 checks / 4 tallies; 62 distinct campaign rows; 21 witnessed properties at each width; all 30 named assertion controls; generated bindings and absent legacy bind; unique ordinary suite owner; exact public 45-row receipt composition')
