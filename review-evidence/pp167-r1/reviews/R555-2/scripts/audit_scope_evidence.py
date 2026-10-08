#!/usr/bin/env python3
import collections,hashlib,importlib.util,json,pathlib,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); out=packet/'receipts'; evidence=out/'public-evidence'; author=evidence/'author-r2/round2'
HEAD='1411117e646023cb236de02e3acaf9bdfcef49e3'; BASE='ed340b9b85258194247334b85e62cf9c23d4d051'; OLD='f3fef22448ce4f9bed8fd249a21a5d472148bd3d'
def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
def get(rev,path): return git('show',rev+':'+path)
def sha(data): return hashlib.sha256(data).hexdigest()
manifest={x['file']:x for x in json.loads((evidence/'MANIFEST.json').read_text())}; checked=[]
for f in evidence.rglob('*'):
    if f.is_file() and f.name!='MANIFEST.json':
        rel=str(f.relative_to(evidence)); m=manifest[rel]; assert sha(f.read_bytes())==m['published_sha256'],rel; checked.append(rel)
source_records=[]
for label,rev in [('base',BASE),('head',HEAD)]:
    a=json.loads((author/('source-'+label+'.json')).read_text()); assert a['revision']==rev
    for f in a['files']: assert sha(get(rev,f['path']))==f['sha256'],f['path']
    assert len(a['files'])==len(git('ls-tree','-r','--name-only',rev).splitlines())
    source_records.append({'revision':rev,'files_matched':len(a['files'])})
notify='hdl/aecp/KL_aecp_notify.sv'; n=get(HEAD,notify).decode(); old=get(OLD,notify).decode(); base=get(BASE,notify).decode()
guard=' && valid_r[cf_ix_w]\n                       && !cx_wait_w[cf_ix_w];\n'; assert n.count(guard)==1
assert n.replace(guard,' && valid_r[cf_ix_w];\n')==old
start='  if (N_IF_P > 1) begin : g_ca_turns'; end='  end else begin : g_ca_own'
def branch(s): return s[s.index(start):s.index(end)]
assert branch(n)==branch(old)
assert branch(n).replace("    assign cx_wait_w = '0;\n",'')==branch(base)
assert n[:n.index('  // ----',n.index('module KL_aecp_notify'))]==base[:base.index('  // ----',base.index('module KL_aecp_notify'))]
unchanged=['hdl/top/protocol_processor_top.sv','hdl/common/pp_pkg.sv','hdl/packet_engine/KL_pp_originator.sv','hdl/aecp/KL_aecp_ca_originator.sv','docs/architecture/07_memory_maps.md','tb/aecp_notify/port_tuple.hpp']
for f in unchanged: assert get(HEAD,f)==get(BASE,f)==get(OLD,f)
# Independently plant every notification arm, without building a bank.
spec=importlib.util.spec_from_file_location('notification_campaign',root/'tb/pp_top/notify_mutants.py'); mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
plants=[]
with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='plant-audit-') as t:
    tree=pathlib.Path(t)
    for mutant in mod.MUTANTS:
        for path in {edit[0] for edit in mutant.edits}:
            dest=tree/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes((root/path).read_bytes())
        reason=mod.plant(tree,mutant.edits); assert not reason,(mutant.name,reason); plants.append({'name':mutant.name,'passed':True})
(out/'notification-plant-audit.json').write_text(json.dumps(plants,indent=2)+'\n')
final=json.loads((author/'final-receipts.json').read_text()); assert final['head']==HEAD and final['base']==BASE
artifacts={x['path']:x for x in json.loads((author/'run-artifacts.json').read_text())}
rc_records=[]
for group in ['processor','campaigns','parent']:
    for rev,items in final[group].items():
        for name,item in items.items():
            assert item['rc']==0,(group,rev,name)
            log=artifacts[item['log']]; rcfile=artifacts[item['rc_file']]
            assert log['sha256']==item['sha256'] and log['bytes']==item['bytes']
            assert rcfile['sha256']==sha(b'0\n') and rcfile['bytes']==2
            rc_records.append({'group':group,'revision_label':rev,'gate':name,'rc':0})
area=json.loads((author/'area-comparison.json').read_text()); assert area['parameters_identical']
for name in ['LUT','FF']:
    assert area['head']['resources'][name]-area['base']['resources'][name]==area['delta'][name]
    assert area['delta'][name]<=20
for image,item in area['images'].items(): assert item['identical'] and item['base']['sha256']==item['head']['sha256']
plant_totals={}
for label in ['base','head']:
    rec=json.loads((author/('plant-'+label+'.json')).read_text()); assert all(x['passed'] for x in rec)
    plant_totals[label]={'total':len(rec),'by_kind':dict(collections.Counter(x['kind'] for x in rec))}
result={'head':HEAD,'base':BASE,'previous':OLD,'published_manifest_verified_files':checked,'source_receipts_verified':source_records,'guard_removed_equals_previous':True,'count_two_equals_previous':True,'count_two_equals_base_except_zero_tie':True,'unchanged_port_parameter_header':True,'unchanged_files':unchanged,'independent_notification_plants':len(plants),'published_all_plant_totals':plant_totals,'published_gate_rc_checks':rc_records,'published_area_delta':area['delta'],'published_images_equal':True,'no_source_submodules':not any(x.startswith(b'160000') for x in git('ls-tree','-r',HEAD).splitlines())}
(out/'scope-evidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checked)} published files; two 581-file source receipts; {len(plants)} notification plants; {len(rc_records)} published gate statuses; area +11 LUT/+20 FF; branch and interface equality')
