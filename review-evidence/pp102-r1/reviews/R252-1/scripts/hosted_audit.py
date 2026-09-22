#!/usr/bin/env python3
"""Check job conclusions against executed steps and raw checkout identities."""
import json
import re
from collect import HEAD,OUT

runs=json.loads((OUT/'public/hosted-current-runs.json').read_text())
records=[]
for run in runs['workflow_runs']:
    assert run['head_sha']==HEAD and run['status']=='completed' and run['conclusion']=='success'
    ident=HEAD if run['event']=='push' else 'e66e6eb9271ff045d9061449423331d47472ab12'
    jobs=json.loads((OUT/f'public/hosted-{run["id"]}-jobs.json').read_text())['jobs']
    assert {j['name'] for j in jobs}=={'docs-gates','suites','portability'}
    for job in jobs:
        assert job['status']=='completed' and job['conclusion']=='success' and job['head_sha']==HEAD
        log=(OUT/f'public/hosted-{run["id"]}-{job["name"]}.raw.log').read_text()
        assert re.search(r'\[command\]/usr/bin/git log -1 --format=%H\n[^\n]+ '+ident+r'\n',log)
        skipped=[s['name'] for s in job['steps'] if s['conclusion']=='skipped']
        assert skipped==(['Build Verilator v5.050'] if job['name']=='suites' else [])
        if job['name']=='suites':
            assert 'Verilator 5.050' in log
            assert 'PASS pp_top (1411 checks: 1411 PASS, 0 FAIL)' in log
            assert 'suites: 14943 checks total, 0 failing' in log
            assert 'all measured figures agree with the tree' in log
        elif job['name']=='docs-gates':
            assert 'links: 807 checked, OK' in log and 'wavedrom: 18 blocks checked, OK' in log
        else:
            assert len(re.findall(r'YOSYS OK  \S+',log))==32
            assert 'YOSYS XILINX OK  KL_aecp_engine' in log
        records.append({'run':run['id'],'event':run['event'],'job':job['id'],'name':job['name'],
                        'run_head':HEAD,'actual_checkout':ident,'conclusion':'success',
                        'skipped_steps':skipped,'html_url':job['html_url']})
(OUT/'raw/hosted-audit.json').write_text(json.dumps(records,indent=2)+'\n')
print('Six completed hosted jobs verified, including actual checkout identities; only cached tool rebuilds skipped.')
