"""R254 independent finite-content probes; no workflow commands are executed."""
import ast, collections, copy, hashlib, itertools, json, pathlib, re, subprocess, sys, types
ROOT=pathlib.Path(sys.argv[1]).resolve()
OUT=pathlib.Path(sys.argv[2]).resolve()
BASE='483a133ed08867ea0d300d2b4a027b5b48a4282f'
HEAD='f01f237d4b48c7b1ed59c80aca51430901791624'
# Frozen #439 scope / policy items 4,12. Deliberately not a candidate table.
SCOPE={'.github/workflows/rtl.yml':('verilator-shards','verilator-suites','yosys-shards','yosys-portability'),'.github/workflows/rtl-fast.yml':('verilator-lint','bdd-conformance','yosys-elaboration')}
SHA_NAME='Print the event and pin the one SHA this run validates'
def norm(body):
    assert all(c in ' \t\n' or (c.isprintable() and not c.isspace()) for c in body)
    return tuple(' '.join(re.findall(r'[^ \t]+',l)) for l in body.replace('\\\n','').split('\n') if l.strip(' \t'))
def module(text, name):
    m=types.ModuleType(name); m.__file__=str(ROOT/'scripts/ci_events.py'); sys.modules[name]=m
    exec(compile(text,m.__file__,'exec'),m.__dict__); return m
source=(ROOT/'scripts/ci_events.py').read_text()
base_source=subprocess.check_output(['rtk','proxy','git','-C',str(ROOT),'show',BASE+':scripts/ci_events.py'],text=True)
c=module(source,'r254_candidate'); b=module(base_source,'r254_base')
world=c.parse_world(c.read_tree(ROOT))
import yaml
raw={p:yaml.load((ROOT/p).read_text(),Loader=yaml.BaseLoader) for p in SCOPE}
scoped=[]
for path,jids in SCOPE.items():
    for jid in jids:
        for i,step in enumerate(raw[path]['jobs'][jid]['steps']):
            if 'run' in step: scoped.append((path,jid,i,step))
sha=[(i,s) for i,s in enumerate(raw['.github/workflows/rtl.yml']['jobs']['full-ci-gate']['steps']) if s.get('name')==SHA_NAME]
assert len(sha)==1
scoped.append(('.github/workflows/rtl.yml','full-ci-gate',*sha[0]))
assert len(scoped)==38
assert set(c.RTL_STEP_LISTS)=={(p,j) for p,js in SCOPE.items() for j in js}
rows=[]; receipts=[]
def save(name, obj): (OUT/'receipts'/name).write_text(json.dumps(obj,indent=2)+'\n')
def target(w,p,j,i): return w[p]['jobs'][j]['steps'][i]
def diagnostic(p,j,i,s,expected,actual):
    d=next(n for n,(e,a) in enumerate(itertools.zip_longest(expected,actual),1) if e!=a)
    e=expected[d-1] if d<=len(expected) else None
    return f"{p}: job `{j}` step {i+1} (`{s['name']}`) script is not the canonical form: line {d} must be {e!r}"
def trial(p,j,i,s,lines,lever,body):
    w=copy.deepcopy(world); target(w,p,j,i)['run']=body
    findings=c.check(w).findings
    want=diagnostic(p,j,i,s,lines,norm(body))
    own=[f for f in findings if want in f]
    receipts.append({'job':j,'step':i+1,'lever':lever,'required':want,'findings':findings,'pass':bool(own)})
    assert own,(j,i,lever,findings)
for p,j,i,s in scoped:
    lines=norm(s['run']); record=c.RTL_SEQUENCE_PINS[(p,j)][i]
    assert record['name']==s['name']; assert isinstance(record['run'],tuple)
    assert record['run']==lines,(j,i)
    rows.append({'path':p,'job':j,'step':i+1,'name':s['name'],'raw_script':s['run'],'canonical':list(record['run']),'lines':len(lines)})
    for n,line in enumerate(lines):
        for lever,mut in [('swallow',(*lines[:n],line+' || true',*lines[n+1:])),('delete',(*lines[:n],*lines[n+1:])),('replace',(*lines[:n],': # reviewer replacement',*lines[n+1:]))]:
            trial(p,j,i,s,lines,f'{lever}-{n+1}','\n'.join(mut))
    for lever,body in [('append','\n'.join((*lines,'echo R254_extra'))),('prepend','\n'.join(('set +e',*lines))),('empty',''),('blank',' \t\n'),('noop',':')]:
        trial(p,j,i,s,lines,lever,body)
    # Every record shape is checked through the full checker, not just a helper.
    for lever,value in [('missing',None),('empty',()),('blank',('',)),('spaces',(' \t',)),('wrong-string','true'),('wrong-list',list(lines)),('wrong-dict',{}),('mixed-type',(lines[0],17)),('stale',('echo R254_stale',*lines[1:]))]:
        original=copy.deepcopy(record)
        if lever=='missing': record.pop('run')
        else: record['run']=value
        try:
            findings=c.check(copy.deepcopy(world)).findings
            want=(f"{p}: job `{j}` step {i+1} (`{s['name']}`) must record a canonical normalized `run` script" if lever in ('missing','empty','wrong-string','wrong-list','wrong-dict','mixed-type') else diagnostic(p,j,i,s,value,lines))
            assert any(want in f for f in findings),(j,i,lever,findings)
            receipts.append({'job':j,'step':i+1,'lever':'record-'+lever,'required':want,'findings':findings,'pass':True})
        finally: record.clear();record.update(original)
    # Prove maintenance through the sequence path for every step.
    w=copy.deepcopy(world); pins=copy.deepcopy(c.RTL_SEQUENCE_PINS)
    maintained=(*lines,'echo R254_maintenance')
    target(w,p,j,i)['run']='\n'.join(maintained);pins[(p,j)][i]['run']=maintained
    contract=c.Contract();c.check_sequence_pin_coverage(contract,w,pins)
    assert not contract.findings,(j,i,contract.findings)
    receipts.append({'job':j,'step':i+1,'lever':'matched-sequence-maintenance','findings':contract.findings,'pass':True})
    # Normalization positives per body; whitespace only, continuation within first word.
    w=copy.deepcopy(world)
    first=lines[0]; continued=first[:1]+'\\\n'+first[1:]
    target(w,p,j,i)['run']='\n\n'.join(' \t'+l+' \t' for l in (continued,*lines[1:]))+'\n'
    findings=c.check(w).findings
    base_findings=b.check(w).findings
    assert findings==base_findings,(j,i,findings,base_findings)
    seq=c.Contract();c.check_sequence_pin_coverage(seq,w);assert not seq.findings
    receipts.append({'job':j,'step':i+1,'lever':'whitespace-continuation','findings':findings,'base_findings':base_findings,'sequence_findings':seq.findings,'pass':True})
    target(w,p,j,i)['run']='\n\n'.join(' \t'+l+' \t' for l in lines)+'\n'
    findings=c.check(w).findings;assert not findings
    receipts.append({'job':j,'step':i+1,'lever':'whitespace-blank-indent','findings':findings,'pass':True})
# Exact reported SHA escapes and baseline reproduction.
p,j,i,s=scoped[-1];lines=norm(s['run']);start=lines.index('if [ "$head" != "$GITHUB_SHA" ]; then');end=lines.index('fi',start)
for lever,mut in [('whole-sha-mismatch-block',(*lines[:start],*lines[end+1:])),('sha-exit-true',tuple('true' if l=='exit 1' else l for l in lines))]:
    w=copy.deepcopy(world); target(w,p,j,i)['run']='\n'.join(mut)
    old=b.check(w).findings;assert not old,(lever,old)
    trial(p,j,i,s,lines,lever,'\n'.join(mut))
    receipts[-1]['base_findings']=old
# Full-check maintenance in ordinary and sibling scripts.
for p,j,i,s in (scoped[0],scoped[-1]):
    record=c.RTL_SEQUENCE_PINS[(p,j)][i];old=record['run'];w=copy.deepcopy(world)
    record['run']=(*old,'echo R254_maintenance'); target(w,p,j,i)['run']='\n'.join(record['run'])
    try:
        findings=c.check(w).findings;assert not findings,findings
        receipts.append({'job':j,'step':i+1,'lever':'matched-full-check-maintenance','findings':findings,'pass':True})
    finally: record['run']=old
# Malformed live input and non-shell whitespace must fail, with concrete diagnostics.
p,j,i,s=scoped[0]
for lever,body in [('missing',None),('boolean',True),('list',['true']),('NBSP','git\u00a0submodule update --init'),('CR','git\rsubmodule'),('U2028','git\u2028submodule')]:
    w=copy.deepcopy(world)
    if lever=='missing': target(w,p,j,i).pop('run')
    else: target(w,p,j,i)['run']=body
    findings=c.check(w).findings
    assert findings and any(f'job `{j}` step {i+1}' in f for f in findings)
    receipts.append({'job':j,'step':i+1,'lever':'body-'+lever,'findings':findings,'pass':True})
# All prior named mutations retain their reason and exact edited world.
before=b._mutations(world);after=c._mutations(world)
oldmap={name:(mut,reason) for name,mut,reason in before};newmap={name:(mut,reason) for name,mut,reason in after}
assert len(oldmap)==len(before);assert len(newmap)==len(after)
prior=[]
for name,(mut,reason) in oldmap.items():
    newer,nreason=newmap[name];assert reason==nreason,name
    w1=copy.deepcopy(world);w2=copy.deepcopy(world);mut(w1);newer(w2);assert w1==w2,name
    assert any(reason in f for f in c.check(w2).findings),name
    prior.append({'name':name,'reason':reason,'same_mutation':True})
# New arms' expectations and edits independently judged against live inventory.
new_arms=[]
byid={(p,j,i):s for p,j,i,s in scoped}
for name,mut,reason in after:
    if name in oldmap: continue
    w=copy.deepcopy(world);mut(w)
    changed=[(p,j,i,s) for p,j,i,s in scoped if target(w,p,j,i)!=target(world,p,j,i)]
    assert len(changed)==1,name
    p,j,i,s=changed[0]; actual=norm(target(w,p,j,i)['run']);expected=norm(s['run'])
    want=diagnostic(p,j,i,s,expected,actual).removeprefix(p+': ')
    assert reason==want,(name,reason,want)
    assert any(reason in f for f in c.check(w).findings),name
    new_arms.append({'name':name,'reason':reason,'job':j,'step':i+1})
# AST comparison proves unchanged functions and module assignments.
def functions(text):
    result={}
    for node in ast.parse(text).body:
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str): node.body=node.body[1:]
            result[node.name]=ast.dump(node,include_attributes=False)
    return result
a0,a1=functions(base_source),functions(source)
changed=sorted(k for k in a0 if a0[k]!=a1.get(k));added=sorted(a1.keys()-a0.keys())
assert changed==['_mutations','check_carrier_steps','selftest'],changed
assert c.CARRIER_STEP_LISTS==b.CARRIER_STEP_LISTS
for table in ['RTL_STEP_LISTS','RTL_SIBLING_STEP_LISTS','RTL_SEQUENCE_PINS','STEP_LISTS']:
    stripped=copy.deepcopy(getattr(c,table))
    for key,entries in stripped.items():
        if key not in b.CARRIER_STEP_LISTS:
            for entry, old_entry in zip(entries,getattr(b,table)[key],strict=True):
                if 'run' not in old_entry: entry.pop('run',None)
    assert stripped==getattr(b,table),table
# All prior global assignments except the four extended tables have identical AST.
def assigns(text):
    out={}
    for n in ast.parse(text).body:
        if isinstance(n,(ast.Assign,ast.AnnAssign)):
            for t in n.targets if isinstance(n,ast.Assign) else [n.target]:
                if isinstance(t,ast.Name): out[t.id]=ast.dump(n,include_attributes=False)
    return out
g0,g1=assigns(base_source),assigns(source)
changed_globals=sorted(k for k in g0 if g0[k]!=g1.get(k));assert changed_globals==['RTL_SIBLING_STEP_LISTS','RTL_STEP_LISTS'],changed_globals
save('inventory.json',rows);save('independent-probes.json',receipts);save('prior-arms.json',prior);save('new-arms.json',new_arms)
summary={'head':HEAD,'base':BASE,'bodies':len(rows),'normalized_lines':sum(r['lines'] for r in rows),'jobs':dict(collections.Counter(r['job'] for r in rows)),'independent_probes':len(receipts),'prior_arms':len(before),'candidate_arms':len(after),'new_arms':len(new_arms),'unchanged_functions':len(a0)-len(changed),'changed_functions':changed,'added_functions':added,'changed_assignments':changed_globals,'prior_module_assignments':len(g0),'result':'PASS'}
save('probe-summary.json',summary);print(json.dumps(summary,indent=2))
(OUT/'disposable/base-ci_events.py').write_text(base_source)
