import copy,json,pathlib,sys
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1'); sys.path.insert(0,str(ROOT/'scripts'))
import ci_events as ci
world=ci.parse_world(ci.read_tree(ROOT)); assert not ci.check(world).findings
records=[]
for path,jid in ((ci.DOCS,'docs-check'),(ci.ELABORATE,'elaborate')):
 for label in ('drop-install-step','drop-install-command','drop-installer-selftest','verify-only','wrong-destination','move-install-after-builder','drop-require','skip-hit-verification','cache-fallback','skip-builder'):
  w=copy.deepcopy(world); steps=w[path]['jobs'][jid]['steps']; install=next(s for s in steps if s.get('name')=='Install and verify the pinned RV32 SDK'); builder=next(s for s in steps if 'sw/builder/test_builder.py' in s.get('run','')); cache=next(s for s in steps if s.get('name')=='Cache the pinned RV32 SDK')
  if label=='drop-install-step': steps.remove(install)
  elif label=='drop-install-command': install['run']='\n'.join(l for l in install['run'].splitlines() if 'ci_rv32_sdk.py ' not in l)
  elif label=='drop-installer-selftest': install['run']=install['run'].replace('python3 scripts/ci_rv32_sdk_selftest.py','true')
  elif label=='verify-only': install['run']=install['run'].replace('ci_rv32_sdk.py --destination','ci_rv32_sdk.py --verify-only --destination')
  elif label=='wrong-destination': install['run']=install['run'].replace('br-milan-rv32/host','unselected/host')
  elif label=='move-install-after-builder': steps.remove(install); steps.insert(steps.index(builder)+1,install)
  elif label=='drop-require': builder['run']=builder['run'].replace(' --require-rv32','')
  elif label=='skip-hit-verification': install['if']="${{ steps.cache.outputs.cache-hit != 'true' }}"
  elif label=='cache-fallback': cache['with']['restore-keys']='rv32-sdk-'
  elif label=='skip-builder': builder['if']=False
  findings=ci.check(w).findings; print(json.dumps({'workflow':path,'probe':label,'findings':findings})); assert findings,(path,label)
for label in ('drop-absent-step','drop-absent-call','drop-helper-selftest'):
 w=copy.deepcopy(world); steps=w[ci.DOCS]['jobs']['docs-check']['steps']; absent=next(s for s in steps if s.get('name')=='Compiler-absent firmware controls')
 if label=='drop-absent-step': steps.remove(absent)
 elif label=='drop-absent-call': absent['run']='\n'.join(l for l in absent['run'].splitlines() if ' --absent ' not in l)
 else: absent['run']=absent['run'].replace('python3 sw/builder/test_firmware_compiler.py --selftest','true')
 findings=ci.check(w).findings; print(json.dumps({'workflow':ci.DOCS,'probe':label,'findings':findings})); assert findings,label
print('23 independent in-memory workflow omission/adoption fault probes refused; pristine passes')
