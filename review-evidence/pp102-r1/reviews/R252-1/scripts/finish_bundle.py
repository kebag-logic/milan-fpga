#!/usr/bin/env python3
"""Finalize reviewer-owned evidence and validate every delivered manifest entry."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
from datetime import datetime, timezone
from collect import HEAD, BASE, OUT
from integrity import verify

verify('final')
parser=json.loads((OUT/'raw/parser-results.json').read_text())
assert parser['head']==HEAD and all(c['pass'] for c in parser['controls'])
build=json.loads((OUT/'raw/pp-top-full.stdout.log.command.json').read_text())
assert build['exit']==0
assert (OUT/'raw/build-tally.txt').read_text().splitlines()==['1391 0','20 0']
native=json.loads((OUT/'raw/evidence-audit.json').read_text())
assert native['manager_commands_exit_zero']==9 and native['manager_suite_checks']==14943
hosted=json.loads((OUT/'raw/hosted-audit.json').read_text())
assert len(hosted)==6 and all(j['conclusion']=='success' for j in hosted)
tool=json.loads((OUT/'raw/tool-identity.json').read_text())
for row in tool:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']

evidence={
 'Conformance':['raw/source.diff','raw/parser-results.json','source/tb/pp_top/Makefile','public/donor-issue-102.json'],
 'RTL':['raw/evidence-audit.json','source/hdl/top/protocol_processor_top.sv','source/hdl/srp/KL_srp_domain.sv','raw/pp-top-full.stdout.log'],
 'Robustness':['controls/Makefile.remove-Wall','controls/Makefile.remove-Wextra','source/tb/pp_top/fixture_guards.py','source/tb/pp_top/test_fixture_guards.py','raw/pp-top-full.stdout.log'],
 'Tests':['raw/build-tally.txt','raw/pp-top-full.stdout.log.command.json','raw/tool-identity.json','raw/evidence-audit.json','raw/hosted-audit.json','source/tb/pp_top/sim_main.cpp'],
 'Docs':['raw/source.diff','source/docs/architecture/01_overview.md','source/docs/architecture/10_srp_engine.md','source/tb/pp_top/README.md','public/pr103.json','evidence/source/manager/full-native/05.log'],
}
ledger={
 'reviewer':'R252','round':'R252-1','head':HEAD,'base':BASE,
 'tree':'0547903adc17449dfb4f0c2610a23e6adb4ff6a2',
 'verdict':'POSITIVE','scope':'issue102/PR103 exact-head internal source review',
 'authored_by_reviewer':True,'open_findings':[],
 'lenses':[{'lens':k,'covering_round':'R252-1','exact_head':HEAD,'severity':'PASS','state':'CLEAN',
            'open_blocker_major_minor':[],'evidence':v} for k,v in evidence.items()],
 'external_R253':'PENDING, not waived','merge_ready':False,
 'manager_remaining':['external positive and complete review closure','current-main candidate validation and decision','merge authorization/execution','post-merge containment and evidence'],
 'historical_PR13_6_continuity':'UNKNOWN','historical_PR13_9':'negative-review baseline retained',
 'parent_pin_adopted':False,'restored_PTOF_400_403_70_completed':False,
 'author_extra_parent_selftest':'FAILED exit 2: uninitialized submodules; required focused controls passed separately',
 'terminal':'R252-1 FINISHED', 'created_utc':datetime.now(timezone.utc).isoformat(),
}
(OUT/'LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
report=(OUT/'REPORT.md').read_text()
assert report.startswith('[R252] POSITIVE - exact head '+HEAD+'\n')
assert report.rstrip().endswith('R252-1 FINISHED')
for row in ledger['lenses']:
    for rel in row['evidence']: assert (OUT/rel).exists(),rel
for target in re.findall(r'\]\(([^)]+)\)',report):
    if target.startswith(('https://','http://')): continue
    if target in ('MANIFEST.json','MANIFEST.sha256'): continue
    assert (OUT/target).exists(),target
for cache in OUT.rglob('__pycache__'):
    assert OUT in cache.parents
    shutil.rmtree(cache)
items=[]
for p in sorted(OUT.rglob('*')):
    if p.is_dir(): continue
    assert p.is_file() and not p.is_symlink(),p
    rel=p.relative_to(OUT).as_posix()
    if rel in ('MANIFEST.json','MANIFEST.sha256'): continue
    b=p.read_bytes()
    items.append({'path':rel,'kind':'regular','mode':oct(stat.S_IMODE(p.stat().st_mode)),
                  'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'reviewer':'R252','round':'R252-1','head':HEAD,'created_utc':datetime.now(timezone.utc).isoformat(),
          'excludes':['MANIFEST.json','MANIFEST.sha256'],'files':items}
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
hashes=[f'{x["sha256"]}  {x["path"]}' for x in items]
hashes.append(hashlib.sha256((OUT/'MANIFEST.json').read_bytes()).hexdigest()+'  MANIFEST.json')
(OUT/'MANIFEST.sha256').write_text('\n'.join(hashes)+'\n')
for entry in items:
    p=OUT/entry['path']; b=p.read_bytes()
    assert hashlib.sha256(b).hexdigest()==entry['sha256'] and len(b)==entry['bytes']
    assert oct(stat.S_IMODE(p.stat().st_mode))==entry['mode']
print('Packet manifest verified:',len(items),'artifacts plus MANIFEST.json; total bytes',sum(x['bytes'] for x in items))
print('Reviewer ledger: 5 CLEAN lenses, exact head',HEAD)
