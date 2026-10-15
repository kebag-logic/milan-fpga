#!/usr/bin/env python3
"""Verify public records and source identities without accepting summaries as execution."""
import ast,collections,hashlib,json,pathlib,re,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent;pub=out/'scratch/public'
sys.path.insert(0,str(root/'ci/image'));import build
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock=load(root/'ci/image/image.lock.json');cold=load(pub/'round6-cold-comparison.json');a,b=cold['cold_a'],cold['cold_b']
fields=['manifest','config','layers','diff_ids','recipe'];equal={k:a[k]==b[k] for k in fields}
assert all(equal.values()); layers=lock['base_layers']+lock['layers']
assert a['manifest']==lock['image_digest'] and a['config']==lock['image_id']
assert a['layers']==[r['oci_digest'] for r in layers] and a['diff_ids']==[r['diff_id'] for r in layers]
assert a['recipe']==lock['recipe_digest']==build.recipe_digest()
source=root/'sw/builder/test_builder.py';tree=ast.parse(source.read_text());main=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'")
loop=next(n for n in main.body if isinstance(n,ast.For) and ast.unparse(n.target)=='fn');names=[n.id for n in loop.iter.elts]
groups=[load(pub/f'builder-functions-{i}.json') for i in range(9)]
results=[r['name'] for g in groups for r in g['results']]
assert collections.Counter(results)==collections.Counter(names)
assert all(g['source_sha256']==sha(source) and g['require_rv32'] for g in groups)
assert all(g['group']==i and [r['name'] for r in g['results']]==g['groups'][i] and g['groups']==groups[0]['groups'] for i,g in enumerate(groups))
bg=load(pub/'builder-home-background.receipt.json');assert bg['rc']==0 and bg['source_sha256']==sha(source)
inv=load(root/'ci/image/tool-inventory.json');tools=inv['tools'];comparisons={}
for rev in ['e6b86814','e355f789','4391f353']:
 old=json.loads(subprocess.check_output(['git','show',rev+':ci/image/tool-inventory.json'],cwd=root));comparisons[rev]=old['tools']==tools
def normalize_tools(rows):
 return [{**r,'installed_by':sorted({json.dumps(p,sort_keys=True) for p in r['installed_by']})} for r in rows]
normalized={rev:normalize_tools(json.loads(subprocess.check_output(['git','show',rev+':ci/image/tool-inventory.json'],cwd=root))['tools'])==normalize_tools(tools) for rev in comparisons}
assert len(tools)==45 and all(normalized.values())
stale={k:{'recorded':v,'actual':sha(root/k)} for k,v in inv['inputs'].items() if (root/k).is_file() and sha(root/k)!=v}
audit=load(pub/'round6-exec-audit-receipt.json');docs=load(pub/'round6-docs-gate-results.json');rtl=load(pub/'round6-rtl-gate-results.json')
trace_commands=[s['argv'] for s in audit['steps']]
missing_nvm=[s for s in docs['steps'] if any('check_nvm_capture' in str(v) for v in s['command']) and s['command'] not in trace_commands]
job=load(out/'scratch/hosted-dev-docs-job.json');log=(out/'scratch/hosted-dev-docs.log').read_text();runner=(out/'scratch/runner-manifest.md').read_text()
excerpts=[re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',line) for line in log.splitlines() if ('SKIP: the MAKEFLAGS += -e mutation:' in line or 'Version: 20261004.327.1' in line or 'the calibration gate needs the mf48' in line and len(line)<500)]
excerpts=[re.sub(r'<home-path>/[^ )]+','$RUNNER_CALIBRATION_REPORT',line) for line in excerpts]
assert any('MAKEFLAGS += -e' in l for l in excerpts)
make_line=next(l for l in runner.splitlines() if l.startswith('| make '));assert '4.3-4.1build2' in make_line
checks=load(out/'scratch/head-checks.json')['check_runs']
report={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'cold_records':{'equal':equal,'layer_count':len(layers),'image_digest':a['manifest'],'config':a['config'],'recipe':a['recipe'],'scope':'Public records agree with lock; image archive bytes not inspected by this round.'},
 'builder_groups':{'source_sha256':sha(source),'invocations':len(names),'groups':len(groups),'exact_cover':True,'background_rc':bg['rc'],'background_head':bg['head'],'background_image':bg['image_manifest'],'scope':'Public author evidence at unchanged builder source; no reviewer or manager source bank.'},
 'inventory':{'tool_records':len(tools),'tools_raw_equal_previous':comparisons,'tools_equal_as_provenance_sets':normalized,'normalization_note':'One duplicate RV32 docs-check provenance entry was removed; tool pins and provenance sets are unchanged.','stale_inputs':stale},
 'audit_coverage':{'entries':len(audit['steps']),'full_docs_commands':docs['count'],'full_rtl_commands':rtl['count'],'docs_head':docs['head'],'rtl_head':rtl['head'],'missing_nvm_entries':missing_nvm,'scope':'Full gate results have no per-command traced program populations.'},
 'hosted_skip':{'head':job['head_sha'],'job_url':job['html_url'],'make_package':make_line,'excerpts':excerpts,'log_sha256':sha(out/'scratch/hosted-dev-docs.log'),'runner_manifest_sha256':sha(out/'scratch/runner-manifest.md')},
 'hosted_exact_head_snapshot':[{'name':c['name'],'status':c['status'],'conclusion':c['conclusion'],'url':c['html_url']} for c in checks]}
(out/'evidence-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('hosted_exact_head_snapshot','hosted_skip')},indent=2))
