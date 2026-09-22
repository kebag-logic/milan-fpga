"""R219 focused probes. Only disposable fixtures and in-memory objects mutate."""
from pathlib import Path
import collections
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import yaml

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('r219_ci_events', ROOT / 'scripts/ci_events.py')
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)
world = c.parse_world(c.read_tree(ROOT))
assert not c.check(world).findings
rows, receipts, inventory = [], [], []

def record(kind, identity, findings, want):
    ok = any(want in finding for finding in findings)
    receipts.append(dict(kind=kind, identity=identity, expected=want, findings=findings, passed=ok))
    assert ok, receipts[-1]

def normalized(body):
    # Independent transcription of the policy's allowed space/tab/LF normalization.
    return tuple(re.sub(r'[ \t]+', ' ', line).strip(' \t')
                 for line in body.replace('\\\n', '').split('\n') if line.strip(' \t'))

carriers = {'.github/workflows/docs.yml': ('docs-check', 'wire-accountability', 'docs-check-no-git'),
            '.github/workflows/elaborate.yml': ('elaborate',)}
for path, jids in carriers.items():
    document = yaml.safe_load((ROOT/path).read_text())
    node = yaml.compose((ROOT/path).read_text())
    jobs_node = next(v for k,v in node.value if k.value == 'jobs')
    for jid in jids:
        job_node = next(v for k,v in jobs_node.value if k.value == jid)
        steps_node = next(v for k,v in job_node.value if k.value == 'steps')
        for at, step in enumerate(document['jobs'][jid]['steps']):
            if 'run' not in step:
                continue
            canonical = normalized(step['run'])
            entry = c.CARRIER_STEP_LISTS[(path,jid)][at]
            assert canonical == entry['run'], (path,jid,at)
            name = step['name']
            identity = f'{path}: job `{jid}` step {at+1} (`{name}`)'
            inventory.append(dict(path=path, job=jid, step=at+1, name=name,
                                  line=steps_node.value[at].start_mark.line+1,
                                  normalized_lines=len(canonical), canonical=list(canonical),
                                  raw_sha256=hashlib.sha256(step['run'].encode()).hexdigest()))
            rows.append((path,jid,at,step,canonical,identity))

assert collections.Counter(row[1] for row in rows) == {
    'docs-check':41, 'wire-accountability':2, 'docs-check-no-git':1, 'elaborate':12}
(OUT/'inventory-56.json').write_text(json.dumps(inventory,indent=2)+'\n')

for path,jid,at,step,canonical,identity in rows:
    # Every normalized line is changed independently. Require the exact first difference.
    for n,line in enumerate(canonical):
        w = copy.deepcopy(world)
        changed = list(canonical)
        changed[n] = f'true # R219 altered line {n+1}'
        w[path]['jobs'][jid]['steps'][at]['run'] = '\n'.join(changed)
        record('each-line', identity, c.check(w).findings,
               f'{identity} script is not the canonical form: line {n+1} must be {line!r}')
    # Malformed/absent run values must not retire the named step's identity check.
    for value in (None, False, 0, [], {}, ''):
        w = copy.deepcopy(world)
        w[path]['jobs'][jid]['steps'][at]['run'] = value
        want = (identity+' script is not the canonical form:' if value == '' and isinstance(value,str)
                else f'job `{jid}` step {at+1} must be the step named `{step["name"]}`')
        record('invalid-live-body', identity, c.check(w).findings, want)
    w = copy.deepcopy(world)
    del w[path]['jobs'][jid]['steps'][at]['run']
    record('missing-live-body',identity,c.check(w).findings,
           f'job `{jid}` step {at+1} must be the step named `{step["name"]}`')
    # All old specialized checks are still live while the static record is corrupted.
    entry = c.CARRIER_STEP_LISTS[(path,jid)][at]
    saved = entry['run']
    try:
        del entry['run']
        record('missing-record',identity,c.check(world).findings,
               identity+' must record a canonical normalized `run` script')
        for value in (None, (), [], 'true', (True,)):
            entry['run'] = value
            record('invalid-record',identity,c.check(world).findings,
                   identity+' must record a canonical normalized `run` script')
    finally:
        entry['run'] = saved
    # These bodies are never executed; characters must cause a named refusal.
    for char in ('\u00a0','\u2028','\x00','\r'):
        w = copy.deepcopy(world)
        w[path]['jobs'][jid]['steps'][at]['run'] = step['run'] + char
        record('unsupported-character',identity,c.check(w).findings,
               identity+' script is not the canonical form:')

# Independent maintenance controls through the complete checker, not just the helper.
maintenance_names = {'Python idiom gate','Build the validated HDL reference',
                     'Boundary-unit naming ratchet','Fetch the engine authority the builder derives from',
                     'Apply the toolchain patch series'}
for path,jid,at,step,canonical,identity in rows:
    if step['name'] not in maintenance_names:
        continue
    w=copy.deepcopy(world)
    w[path]['jobs'][jid]['steps'][at]['run'] += '\necho R219-maintenance\n'
    record('unrecorded-maintenance',identity,c.check(w).findings,
           identity+' script is not the canonical form:')
    entry=c.CARRIER_STEP_LISTS[(path,jid)][at]
    saved=entry['run']
    try:
        entry['run']=(*saved,'echo R219-maintenance')
        findings=c.check(w).findings
        assert not findings, (identity,findings)
        receipts.append(dict(kind='paired-maintenance',identity=identity,findings=findings,passed=True))
    finally:
        entry['run']=saved

arms=c._mutations(world)
carrier_arms=[arm for arm in arms if arm[0].startswith('carrier-script-407 ')]
assert len({name for name,_,_ in arms})==len(arms)
counts=collections.Counter(name.rsplit(' ',1)[-1] for name,_,_ in carrier_arms)
population={'all_workflow_arms':len(arms),'new_workflow_arms':len(carrier_arms),
            'levers':dict(counts),'by_job':{jid:dict(collections.Counter(
                name.rsplit(' ',1)[-1] for name,_,_ in carrier_arms
                if name.startswith(f'carrier-script-407 {jid} ')))
                for jids in carriers.values() for jid in jids}}
assert len(c._run_mutations(lambda w: [],world))==len(arms)

# Observe real lost sensitivity with unrelated/specialized checks still enabled.
original=c.check_carrier_script
c.check_carrier_script=lambda *args: None
try:
    misses=c._run_mutations(lambda w:c.check(w).findings,world)
    assert len(misses)==187, len(misses)
    assert all('[carrier-script-407 ' in miss and 'continue-on-error]' not in miss for miss in misses)
    population['disabled_new_helper_missing_body_assertions']=len(misses)
    (OUT/'targeted-vacuity-misses.json').write_text(json.dumps(misses,indent=2)+'\n')
finally:
    c.check_carrier_script=original
assert not c.check(world).findings
(OUT/'probe-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
(OUT/'mutation-population.json').write_text(json.dumps(population,indent=2)+'\n')

# Actual CLI/selftest mutants live outside the checkout. No workflow commands execute.
source=(ROOT/'scripts/ci_events.py').read_text()
start=source.index('def check_carrier_script(')
end=source.index('\ndef check_carrier_steps(',start)
fragment=source[start:end]
comparison='c.item(tuple(lines) == canonical, path,'
assert fragment.count(comparison)==1
record_check='c.item(recorded, path,'
assert fragment.count(record_check)==1
variants={
    'comparison-disabled':source[:start]+fragment.replace(comparison,'c.item(True, path,')+source[end:],
    'record-refusal-disabled':source[:start]+fragment.replace(record_check,'c.item(True, path,')+source[end:],
    'paired-maintenance':source.replace("             'python3 scripts/check_py_idiom.py --selftest',",
                                       "             'python3 scripts/check_py_idiom.py --selftest',\n             'echo R219-maintenance',",1)}
cli=[]
for name,mutant in variants.items():
    tree=OUT/'fixtures'/name
    for rel,text in c.read_tree(ROOT).items():
        if name=='paired-maintenance' and rel=='.github/workflows/docs.yml':
            needle='          python3 scripts/check_py_idiom.py --selftest\n'
            assert text.count(needle)==1
            text=text.replace(needle,needle+'          echo R219-maintenance\n')
        p=tree/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    script=tree/'scripts/ci_events.py';script.parent.mkdir(exist_ok=True);script.write_text(mutant)
    for mode in ('--check','--selftest'):
        p=subprocess.run([sys.executable,'-B',str(script),mode],capture_output=True,text=True,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        log=f'{name}-{mode[2:]}.log';(OUT/log).write_text(p.stdout+p.stderr)
        expected=0 if mode=='--check' or name=='paired-maintenance' else 1
        assert p.returncode==expected,(name,mode,p.returncode,p.stdout[-1500:],p.stderr)
        failures=[l for l in p.stdout.splitlines() if l.startswith('  FAIL ')]
        cli.append(dict(variant=name,mode=mode,exit=p.returncode,expected=expected,
                        failure_count=len(failures),log=log))
    if name=='comparison-disabled': assert cli[-1]['failure_count']==187,cli[-1]
    if name=='record-refusal-disabled': assert cli[-1]['failure_count']==56,cli[-1]
(OUT/'cli-mutant-results.json').write_text(json.dumps(cli,indent=2)+'\n')
print(json.dumps({'inventory':len(inventory),'independent_probe_receipts':len(receipts),
                  'population':population,'cli':cli},indent=2))
print('R219 independent probes: PASS; checkout bytes never mutated')
