#!/usr/bin/env python3
"""Read-only source/evidence checks, with item reconstruction confined to scratch."""
import hashlib,io,json,re,subprocess,sys,tarfile
from pathlib import Path
repo=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
head='96d3b78384f34a630d6056ebd8fa5e30f6836650'
base='09e357fb4bf3d35c8a9deba9a787e13f74d08c83'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
e=packet/'public/author/round2-recovery';out={}
for variant,rev in [('base',base),('merged','fee74ef'),('compare-byte',head)]:
 expected=json.loads((e/'area'/variant/'inputs.json').read_text())
 mismatches=[f for f,h in expected.items() if sha(git('show',rev+':'+f))!=h]
 out[variant+'_area_inputs']=dict(files=len(expected),mismatches=mismatches)
 assert not mismatches
recipe='syn/ooc/protocol_processor_ooc.tcl'
expected=json.loads((e/'area-recipe-identity.json').read_text())
out['recipe']=dict(sha256=sha(git('show',head+':'+recipe)),unchanged=git('show',head+':'+recipe)==git('show',base+':'+recipe))
assert out['recipe']['unchanged'] and all(v['sha256']==out['recipe']['sha256'] for v in expected.values())
items=[]
for item in ['LD1','LD2','LD3','TD1','VLAN','guard']:
 d=packet/'scratch'/('item-audit-'+item);d.mkdir(exist_ok=True)
 with tarfile.open(fileobj=io.BytesIO(git('archive',base))) as tf:tf.extractall(d,filter='data')
 patch=e/('item-'+item+'.patch')
 subprocess.run(['git','apply','--unsafe-paths',str(patch)],cwd=d,check=True)
 expected=json.loads((e/'area'/item/'inputs.json').read_text())
 mismatches=[f for f,h in expected.items() if sha((d/f).read_bytes())!=h]
 assert not mismatches
 result=json.loads((e/'area'/item/'result.json').read_text())
 items.append(dict(item=item,input_files=len(expected),mismatches=mismatches,result=result))
out['items']=items
summary=json.loads((e/'area-summary.json').read_text());computed=[]
for item in ['base','merged','compare-byte','LD1','LD2','LD3','TD1','VLAN','guard']:
 text=(e/'area'/item/'util.rpt').read_text()
 lut=int(re.search(r'\| Slice LUTs\*?\s*\|\s*(\d+)',text).group(1))
 ff=int(re.search(r'\| Slice Registers\s*\|\s*(\d+)',text).group(1))
 computed.append(dict(variant=item,lut=lut,ff=ff,rc=int((e/'area'/item/'run.rc').read_text())))
out['raw_area_reports']=computed
assert computed[2]['lut']-computed[0]['lut']==29 and computed[2]['ff']-computed[0]['ff']==14
out['sum_individual_deltas']=dict(lut=sum(x['lut']-computed[0]['lut'] for x in computed[3:]),ff=sum(x['ff']-computed[0]['ff'] for x in computed[3:]))
# The public declarations and unchanged host map implementations are byte equal.
file='hdl/top/protocol_processor_top.sv'
out['top_first_1000_lines_equal']=git('show',base+':'+file).splitlines()[:1000]==git('show',head+':'+file).splitlines()[:1000]
assert out['top_first_1000_lines_equal']
out['subject_gitlinks']=[x.decode() for x in git('ls-tree','-r',head).splitlines() if x.startswith(b'160000')]
out['round2_changed_files']=git('diff','--name-only',base,head).decode().splitlines()
out['merge_parents']=git('show','-s','--format=%P','fee74ef').decode().strip().split()
out['remerge_diff_empty']=not git('show','--format=','--remerge-diff','fee74ef')
assert out['remerge_diff_empty']
# Audit all five processor gates and all 13 campaigns at both revisions.
gates={}
for revision in ['base','head']:
 rows=[]
 for f in sorted((e/(revision+'-logs')).glob('*-receipt.json')):
  j=json.loads(f.read_text());rc=int(f.with_name(f.name.replace('-receipt.json','.rc')).read_text())
  assert j['rc']==0 and rc==0
  rows.append(dict(name=f.name.removesuffix('-receipt.json'),command=j['command'],rc=rc))
 assert len(rows)==18
 suites=(e/(revision+'-logs')/'suites.log').read_text()
 names=re.findall(r'^PASS (\S+) \((\d+) checks: (\d+) PASS, 0 FAIL\)',suites,re.M)
 assert len(names)==33 and all(c==p for _,c,p in names)
 gates[revision]=dict(gates=rows,suites=names,total_checks=sum(int(c) for _,c,_ in names))
out['published_gates']=gates
archive_records=[]
for label,revision in [('base',base),('merged','fee74ef'),('head',head)]:
 data=git('archive',revision);j=json.loads((e/(label+'-source.json')).read_text())
 expected=j.get('archive_sha256',j.get('sha256'));size=j.get('archive_size',j.get('size'))
 assert sha(data)==expected and len(data)==size
 archive_records.append(dict(label=label,sha256=sha(data),size=len(data),matches=True))
out['source_archive_hashes']=archive_records
canonical=[]
for name,key in [('pp_top-aecp_dispatch_mutants','arm'),('pp_top-d3_mutants','mutant'),('pp_top-gsi_mutants','variant'),('pp_top-name_wr_mutant','variant'),('pp_top-notify_mutants','mutant')]:
 a={x[key]:x for x in json.loads((e/'base-campaigns'/name/'results.json').read_text())}
 b={x[key]:x for x in json.loads((e/'head-campaigns'/name/'results.json').read_text())}
 assert a==b
 canonical.append(dict(campaign=name,identical_records=len(a)))
out['identical_canonical_campaigns']=canonical
w=json.loads((e/'comparison/new-check-witnesses.json').read_text())
assert len(w)==18 and all(x['verdict']=='KILLED' and x['build_rc']==0 and x['completed'] and not x['missing'] for x in w)
out['published_new_mutants']=dict(count=len(w),all_required_witnesses=True)
(packet/'receipts/evidence-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: measured inputs, six item patches, raw area totals, interface boundary, merge, 36 gate receipts, 66 suite tallies, 18 mutation witnesses')
