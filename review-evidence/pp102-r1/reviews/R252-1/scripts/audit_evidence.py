#!/usr/bin/env python3
"""Verify published execution receipts, inventories and source preservation."""
import json
import re
from collect import BASE, CHECKOUT, HEAD, OUT, capture

manager=OUT/'evidence/source/manager'
before=capture('raw/base-tree.raw',['git','--no-replace-objects','ls-tree','-rz',BASE])
after=capture('raw/review-head-tree.raw',['git','--no-replace-objects','ls-tree','-rz',HEAD])
def entries(raw):
    result={}
    for item in raw.split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1)
            mode,kind,oid=meta.decode().split()
            result[path.decode()]={'mode':mode,'kind':kind,'blob':oid}
    return result
a,b=entries(before),entries(after)
assert a.keys()==b.keys()
changed=[p for p in a if a[p]!=b[p]]
assert changed==['tb/pp_top/Makefile'],changed
assert a[changed[0]]['mode']==b[changed[0]]['mode']=='100644'
identity=json.loads((OUT/'raw/prebuild-integrity.json').read_text())
current={r['path']:r for r in identity['files']}
for name in ['initial-integrity.json','source-final-integrity.json','validation-final-integrity.json']:
    v=json.loads((manager/name).read_text())
    assert v['head']==HEAD and v['tree']==identity['tree'] and v['index_verified']
    assert len(v['records'])==len(b)==224
    assert {r['path'] for r in v['records']}==set(b)
    for r in v['records']:
        mine=current[r['path']]
        assert r['mode']==mine['mode'] and r['blob']==mine['git_blob'] and r['sha256']==mine['sha256'],r

commands=json.loads((manager/'full-native.json').read_text())
results=json.loads((manager/'full-native/results.json').read_text())
assert commands['head']==results['head']==HEAD and commands['base']==results['base']==BASE
assert len(commands['commands'])==len(results['results'])==9
for i,(c,r) in enumerate(zip(commands['commands'],results['results']),1):
    assert c==r['command'] and r['exit_code']==0
    assert (manager/f'full-native/{i:02d}.log').exists()

suites=(manager/'full-native/04.log').read_text()
rows=re.findall(r'^PASS (\S+) \((\d+) checks: (\d+) PASS, (\d+) FAIL\)$',suites,re.M)
inventory=sorted(p.split('/')[1] for p in b if p.startswith('tb/') and p.endswith('/Makefile'))
assert sorted(x[0] for x in rows)==inventory and len(rows)==30
assert all(n==p and int(f)==0 and int(n)>0 for _,n,p,f in rows)
assert sum(int(n) for _,n,_,_ in rows)==14943
assert 'suites: 14943 checks total, 0 failing' in suites
assert not re.search(r'^(SKIP|FAIL|UNREADABLE)',suites,re.M)
lint=(manager/'full-native/03.log').read_text()
assert len(re.findall(r'^LINT OK ',lint,re.M))==37
ys=(manager/'full-native/07.log').read_text()
ys_tops=re.findall(r'^YOSYS OK  (\S+)$',ys,re.M)
ys_recipe=(CHECKOUT/'syn/yosys/run.sh').read_text()
top_names=re.search(r'tops=\((.*?)\)',ys_recipe,re.S).group(1).split()
assert ys_tops==top_names and len(ys_tops)==32
assert 'YOSYS XILINX OK  KL_aecp_engine' in ys and 'YOSYS FAIL' not in ys
assert 'select -assert-count 1 c:amap_stage_r* t:RAMB36E1 %i; select -assert-count 6 t:RAMB36E1' in ys_recipe
figures=(manager/'full-native/08.log').read_text()
assert '42 Verilator builds: 1 baseline + 12 arms + 18 mutations + 6 models + 5 matrix' in figures
assert 'baseline: 122 checks, 122 PASS, 0 FAIL' in figures
assert 'all measured figures agree with the tree' in figures
assert 'NOT measured (waived' in figures
for path in ['syn/yosys/run.sh','tb/nvm_port/Makefile','tb/common/verilator_harness.hpp']:
    capture('source/'+path,['git','--no-replace-objects','show',HEAD+':'+path])
result={'head':HEAD,'base':BASE,'only_changed_path':changed[0],
        'unchanged_entries':223,'all_entry_modes_preserved':True,'gitlinks':[],
        'published_source_and_validation_manifests_match':224,
        'manager_commands_exit_zero':9,'manager_suites':rows,
        'manager_suite_checks':14943,'manager_failing_suites':0,
        'manager_lint_modules':37,'manager_yosys_elaboration_tops':ys_tops,
        'manager_yosys_xilinx_engine':True,'manager_figures_builds':42,
        'no_full_banks_rerun_by_reviewer':True}
(OUT/'raw/evidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['manager_suites','manager_yosys_elaboration_tops']},indent=2))
