#!/usr/bin/env python3
"""Independently verify source scope and the downloaded public native evidence."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();public=out/'public'
sys.path.insert(0,str(root/'scripts'))
from suite_tally import scan,log_reports_failure
HEAD='5874895eb817ed41c0f8be4eb427ad3315c29844'
ORIGINAL='7ab1c8d0ad073fbc1977c455dea89b7b318d4e52'
BASE='483a133ed08867ea0d300d2b4a027b5b48a4282f'
def git(*argv):return subprocess.check_output(['git','-C',str(root),*argv],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
def load(path):return json.loads(path.read_text())
base_make=git('show',BASE+':tb/verilator/milan_dp/Makefile').decode()
tail=base_make[base_make.index('\t./obj_dir/Vmilan_dp_sim',base_make.index('\nrun:')):]
legs=[x.strip() for x in tail.splitlines() if x.startswith('\t./obj_')][:10]
now_make=(root/'tb/verilator/milan_dp/Makefile').read_text()
stripped=now_make.replace('# Ordinary simulations only; never derived from the make jobserver.\nSIM_JOBS ?= 2\n','')
start=stripped.index('\t@exec python3 sim_pool.py');stop=stripped.index('\t@echo "---- #386',start)
old_start=base_make.index('\t./obj_dir/Vmilan_dp_sim',base_make.index('\nrun:'));old_stop=base_make.index('\t@echo "---- #386',old_start)
assert stripped[:start]+base_make[old_start:old_stop]+stripped[stop:]==base_make
scope={'head':HEAD,'base':BASE,'changed_paths':git('diff','--name-only',BASE,HEAD).decode().splitlines(),'makefile_outside_bounded_tail_identical':True,'benchmark_artifacts':[]}
for name in ['Makefile','sim_pool.py','test_sim_pool.py','sim_nxn.cpp','README.md']:
    path='tb/verilator/milan_dp/'+name;a=git('show',ORIGINAL+':'+path);b=git('show',HEAD+':'+path);assert a==b
    scope['benchmark_artifacts'].append(dict(path=path,blob=git('rev-parse',HEAD+':'+path).decode().strip(),sha256=hashlib.sha256(b).hexdigest()))
cpp_base=git('show',BASE+':tb/verilator/milan_dp/sim_nxn.cpp').decode()
cpp_now=(root/'tb/verilator/milan_dp/sim_nxn.cpp').read_text()
assert cpp_base.replace('// The builder writes into <outdir>/<config-stem>/; no --write-rtl and no\n    // --write-fragment, so it touches nothing tracked.','// Images use <outdir>/<config-stem>/, but the builder also rewrites the\n    // tracked per-config shape header. The ordinary runner serializes these legs.')==cpp_now
scope['cpp_comment_only']=True
budgets=[x for x in git('ls-tree','-r','--name-only',HEAD).decode().splitlines() if x.endswith('.budget')]
assert len(budgets)==13
for path in budgets:assert git('show',BASE+':'+path)==git('show',HEAD+':'+path)
scope['unchanged_budgets']=budgets
for path in ['scripts/run_all_suites.sh','scripts/suite_tally.py','scripts/suite_shards.py','.github/workflows/rtl.yml','tb/verilator/milan_dp/render_mutants.py','tb/verilator/milan_dp/test_render_phase_observation.py','tb/verilator/milan_dp/sim_main.cpp','tb/verilator/milan_dp/sim_prune.cpp','tb/verilator/milan_dp/sim_aclk.cpp','sw/builder/endstation_builder.py']:
    assert git('show',BASE+':'+path)==git('show',HEAD+':'+path)
(out/'source-scope-proof.json').write_text(json.dumps(scope,indent=2)+'\n')

runrows=[];all_bodies=[];phase_sets=[];named_render=[]
for name in ['cold-sequential','cold-pooled','warm-sequential','warm-pooled']:
    directory=public/'author/runs'/name;identity=load(directory/'identity.json');summary=load(directory/'summary.json')
    assert identity['head']==ORIGINAL and identity['version'].startswith('Verilator 5.050 ')
    assert load(directory/'exit.json')==dict(make=0,verdict=0,tally=0,clean=True,same_head=True)
    assert summary['exit']==0
    before=load(directory/'inputs-before.json');after=load(directory/'inputs-after.json');assert all(after.get(k)==v for k,v in before.items())
    for header in (directory/'headers-before').iterdir():
        data=header.read_bytes();assert data==(directory/'headers-after'/header.name).read_bytes()
        assert data==git('show',ORIGINAL+':configs/generated/'+header.stem+'/gen/adp_shape_defaults.svh')
    whole=(directory/'milan_dp.log').read_bytes();tally=scan(whole.decode());assert tally[:2]==(9324,0) and len(tally[2])==13 and not tally[3]
    assert not log_reports_failure(whole.decode())[1]
    bodies=[];counts=[]
    for i,exe in enumerate(legs,1):
        body=(directory/'legs'/f'{i:02d}-{Path(exe).name}.log').read_bytes()
        assert whole.count((exe+'\n').encode()+body)==1,exe
        bodies.append(body);counts.append(scan(body.decode())[0])
    all_bodies.append(bodies)
    render=whole.decode().split('python3 render_mutants.py\n',1)[1]
    phases=[{k:v for k,v in json.loads(line[13:]).items() if k not in ('t_s','elapsed_s','idle_s')} for line in render.splitlines() if line.startswith('RENDER-PHASE ')]
    assert len(phases)==23;phase_sets.append(phases)
    named_render.append([line for line in render.splitlines() if line.startswith('[PASS]')]);assert len(named_render[-1])==6
    peak=group_peak=rss_peak=tree_peak=overlap=0;seen={exe:set() for exe in legs};samples=0
    with (directory/'samples.jsonl').open() as f:
        for line in f:
            sample=json.loads(line);samples+=1
            live=[p for p in sample['procs'] if p['state']!='Z']
            ordinary=[p for p in live if p['argv'] and p['argv'][0] in legs]
            grouped=[p for p in ordinary if p['argv'][0] in legs[1:6]]
            peak=max(peak,len(ordinary));group_peak=max(group_peak,len(grouped))
            rss_peak=max(rss_peak,sum(p['rss_kb'] for p in ordinary));tree_peak=max(tree_peak,sum(p['rss_kb'] for p in live))
            overlap+=bool(grouped and len(ordinary)>len(grouped))
            for p in ordinary:
                assert p['argv']==[p['argv'][0]]
                seen[p['argv'][0]].add(p['pid'])
    assert all(len(p)==1 for p in seen.values())
    assert peak==(1 if name.endswith('sequential') else 2) and group_peak==1
    runrows.append(dict(name=name,head=ORIGINAL,whole_seconds=summary['wall_s'],checks=tally[0],failures=tally[1],tallies=len(tally[2]),per_leg_checks=counts,phase_records=len(phases),sample_count=samples,peak_ordinary=peak,peak_group=group_peak,overlap_samples=overlap,peak_ordinary_rss_kib=rss_peak,peak_aggregate_rss_kib=tree_peak,max_single_rss_kib=summary['max_single_rss_kb']))
assert all(x==all_bodies[0] for x in all_bodies)
assert all(x==phase_sets[0] for x in phase_sets)
assert all(x==named_render[0] for x in named_render)
for temp in ('cold','warm'):
    a=public/'author/runs'/f'{temp}-sequential';b=public/'author/runs'/f'{temp}-pooled'
    assert load(a/'inputs-after.json')==load(b/'inputs-after.json')
    assert load(a/'executables.json')==load(b/'executables.json')
    ai=load(a/'identity.json');bi=load(b/'identity.json')
    for key in ('head','tree','tool','tool_sha256','tool_files','version','command','mode','affinity','limits','cgroup','submodules'):assert ai[key]==bi[key],key
    assert {k:v for k,v in ai['environment'].items() if k!='SIM_JOBS'}=={k:v for k,v in bi['environment'].items() if k!='SIM_JOBS'}
    at=load(a/'summary.json')['wall_s'];bt=load(b/'summary.json')['wall_s']
    assert round((at-bt)/at*100,3)==(3.257 if temp=='cold' else 4.448)

manager=public/'corrected-source2/manager';bank=[]
for path,count in [('manager-builder/results.json',50),('full-native/results.json',5)]:
    ledger=load(manager/path);assert ledger['head']==HEAD and ledger['base']==BASE
    assert len(ledger['results'])==count and all(x['exit_code']==0 for x in ledger['results'])
    bank.append(dict(ledger=path,commands=count,all_exit_zero=True))
whole=(manager/'full-suite-logs/milan_dp.log').read_bytes();tally=scan(whole.decode());assert tally[:2]==(9324,0) and len(tally[2])==13 and not tally[3]
for exe,body in zip(legs,all_bodies[0]):assert whole.count((exe+'\n').encode()+body)==1,exe
render=whole.decode().split('python3 render_mutants.py\n',1)[1]
phases=[{k:v for k,v in json.loads(line[13:]).items() if k not in ('t_s','elapsed_s','idle_s')} for line in render.splitlines() if line.startswith('RENDER-PHASE ')]
assert phases==phase_sets[0]
assert [line for line in render.splitlines() if line.startswith('[PASS]')]==named_render[0]
receipt=dict(source_head=HEAD,original_benchmark_head=ORIGINAL,runs=runrows,ordinary_bodies_equal_across_all_four_runs_and_corrected_manager=True,render_named_outcomes=named_render[0],corrected_manager_banks=bank,corrected_manager_tally=tally[:2],corrected_manager_render_phase_semantics_equal=True)
(out/'public-evidence-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
