from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parent
rows=[json.loads(line) for line in (p/'gates.jsonl').read_text().splitlines()]
latest={row['name']:row for row in rows}
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
small=['pp-srcs','docs-git','docs-no-git','em-dash','doc-style','toc','doc-paths','module-matrix','xvlog','rtl-lists','cpp-idiom','py-idiom','port-contracts','naming','test-evidence','test-evidence-selftest','rtl-lint','diff-check']
required=[*[name+'-final' for name in small],'builder-sdk-candidate','builder-absent-candidate','pp-shadow',*[f'dp-{i:02d}' for i in range(1,37)],'milan-dp-render','nvm-cosim','gsi-mutants','behave',*[f'yosys-{i}' for i in range(4)]]
for name in required:
 assert name in latest,('missing',name)
 r=latest[name]
 assert r['rc']==0,(name,r['rc'])
 assert r['head']==head,(name,r['head'],head)
assert not subprocess.check_output(['git','status','--porcelain'],text=True)
for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 assert not subprocess.check_output(['git','-C',sub,'status','--porcelain'],text=True),sub
sdk=[json.loads(line) for line in (p/'full-builder-sdk-candidate-argv.jsonl').read_text().splitlines()]
assert sdk
for r in sdk:
 assert r['requested'][1:]==r['executed'][1:]
 assert r['executed'][0]=='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
absent=[json.loads(line) for line in (p/'full-builder-absent-argv.jsonl').read_text().splitlines()]
assert len({r['requested'][0] for r in absent})==3
assert all(r['executed'] is None for r in absent)
commits=subprocess.check_output(['git','rev-list','--first-parent','35f0695815c202392b6b4806bb9f59dd110687ed..HEAD'],text=True).splitlines()
for commit in commits:
 body=subprocess.check_output(['git','show','-s','--format=%B',commit],text=True)
 assert len(body.strip().splitlines())==1,(commit,body)
inventory=json.loads((p/'yosys-inventory.json').read_text())
tops={top for shard in inventory for top in shard['tops']}
results=list((p/'yosys-results').glob('top-*.result'))
assert len(results)==len(tops)==54
for result_path in results:
 fields=dict(line.split('=',1) for line in result_path.read_text().splitlines())
 assert fields['name'] in tops and fields['status']=='PASS' and fields['mode']=='full',fields
for name in ['gate-tap-purity.result','gate-tied-input.result']:
 fields=dict(line.split('=',1) for line in (p/'yosys-results'/name).read_text().splitlines())
 assert fields['status']=='PASS',fields
result=dict(head=head,yosys_full_tops=54,required_commands=len(required),all_rc_zero=True,all_at_final_head=True,clean_superproject=True,clean_required_submodules=True,sdk_mapped_invocations=len(sdk),compiler_absent_candidates=3,one_line_round2_commits=commits)
(p/'completion-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
