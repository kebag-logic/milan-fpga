import collections, concurrent.futures, hashlib, json, os, pathlib, re, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
source=(root/'scripts/ci_events.py').read_text()
logs=out/'receipts/cli';logs.mkdir(exist_ok=True)
mutdir=out/'disposable/mutants';mutdir.mkdir(exist_ok=True)
def once(old,new):
 if old.startswith('c.item('):
  start=source.index('def check_carrier_script(');end=source.index('\ndef check_carrier_steps(',start)
  region=source[start:end];assert region.count(old)==1,(old,region.count(old))
  return source[:start]+region.replace(old,new)+source[end:]
 assert source.count(old)==1,(old,source.count(old))
 return source.replace(old,new)
comparison='c.item(tuple(lines) == canonical, path,'
exprs={
 'accept-truncation':'tuple(lines) == canonical[:len(lines)]',
 'accept-extension':'tuple(lines[:len(canonical)]) == canonical',
 'only-line-count':'len(lines) == len(canonical)',
 'unordered-lines':'sorted(lines) == sorted(canonical)',
 'ignore-comments':'tuple(l for l in lines if not l.startswith("#")) == tuple(l for l in canonical if not l.startswith("#"))',
 'ignore-interior-swallow':'tuple(l.removesuffix(" || true") if n < len(lines)-1 else l for n,l in enumerate(lines)) == canonical',
}
mutants={name:once(comparison,'c.item('+expr+', path,') for name,expr in exprs.items()}
mutants.update({
 'disconnect-seven':once('or (path, jid) in RTL_STEP_LISTS','or False'),
 'disconnect-sha':once('and entry.get("id") == PIN_STEP_ID)):', 'and False)):'),
 'missing-record-accepted':once('c.item(recorded, path,','c.item(True, path,'),
})
for name,body in mutants.items(): (mutdir/(name+'.py')).write_text(body)
def run(label,script,mode):
 argv=['rtk','proxy','python3','-B',str(script),mode,'--root',str(root)]
 start=time.time();r=subprocess.run(argv,cwd=root,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=180)
 (logs/(label+'.stdout')).write_bytes(r.stdout);(logs/(label+'.stderr')).write_bytes(r.stderr)
 return {'label':label,'argv':argv,'exit':r.returncode,'seconds':round(time.time()-start,3),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stdout':str((logs/(label+'.stdout')).relative_to(out)),'stderr':str((logs/(label+'.stderr')).relative_to(out))}
receipts=[]
for name,script in [('source',root/'scripts/ci_events.py'),('base',out/'disposable/base-ci_events.py')]:
 for mode in ['--check','--selftest']:
  r=run(name+mode,script,mode);receipts.append(r);assert r['exit']==0,r
# Independent weak validators judged only by normal CLI/default selftest.
def mutant(name):
 script=mutdir/(name+'.py');a=run(name+'--check',script,'--check');b=run(name+'--selftest',script,'--selftest')
 stdout=(out/b['stdout']).read_text()
 own=[l for l in stdout.splitlines() if l.startswith('  FAIL ') and 'rtl-script-439 ' in l]
 b['new_failures']=own;b['new_failure_count']=len(own)
 assert a['exit']==0,(name,a)
 assert b['exit']==1 and own,(name,b)
 assert not (out/b['stderr']).read_text(),name
 return [a,b]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(mutant,mutants):receipts.extend(result)
(out/'receipts/cli-results.json').write_text(json.dumps(receipts,indent=2)+'\n')
old=(logs/'base--selftest.stdout').read_text().splitlines();new=(logs/'source--selftest.stdout').read_text().splitlines()
def normalize_ok(line):
 return re.sub(r'fails all [0-9]+ arms','fails all <population> arms',line) if 'vacuity: a stub' in line else line
old_ok=collections.Counter(normalize_ok(l) for l in old if l.startswith('  ok'))
new_ok=collections.Counter(normalize_ok(l) for l in new if l.startswith('  ok'))
assert not(old_ok-new_ok),list((old_ok-new_ok).elements())
print(json.dumps({'source_check':(logs/'source--check.stdout').read_text().strip(),'source_selftest':new[-1],'base_selftest':old[-1],'prior_ok_lines_preserved':sum(old_ok.values()),'mutants':{r['label']:r['new_failure_count'] for r in receipts if 'new_failure_count' in r},'result':'PASS'},indent=2))
