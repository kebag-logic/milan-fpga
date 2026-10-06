"""Require the complete successful restore inventory before equality."""
import json,sys
from pathlib import Path

def load(path):
 rows=[json.loads(x) for x in Path(path).read_text().splitlines()]
 expected=set();found={}
 for role,inputs,outputs in [('dut',2,2),('peer',10,4)]:
  expected.add((role,'inventory',None,None))
  for dt,n in ((5,inputs),(6,outputs)):
   for i in range(n):
    for category in ('binding','format'):expected.add((role,category,dt,i))
  expected.add((role,'clock',36,0))
  for dt in (14,15):expected.add((role,'map',dt,0))
 for r in rows:
  k=(r['role'],r['category'],r.get('descriptor_type'),r.get('descriptor_index'))
  if k in found or k not in expected:raise ValueError('duplicate or unexpected observation')
  cat=r['category']
  if cat=='inventory':
   if not isinstance(r.get('counts'),dict) or not r['counts']:raise ValueError('missing descriptor population')
   v={q:r[q] for q in ('configuration','counts')}
  else:
   if (type(r['status']) is not int or r['status']!=0) if cat=='binding' else r['status']!='SUCCESS':raise ValueError('failed response')
   if cat=='binding':
    if type(r['connections']) is not int or r['connections']!=0:raise ValueError('binding remains')
    v={'connections':r['connections']}
   elif cat=='format':
    v={'value':r['value']}
    if len(v['value'])!=16 or any(c not in '0123456789abcdef' for c in v['value']):raise ValueError('invalid format')
   elif cat=='clock':
    v={'value':r['value']}
    if type(v['value']) is not int or not 0<=v['value']<65536:raise ValueError('invalid source')
   else:
    v={q:r[q] for q in ('mapping_count','effective_sha256')}
    if type(v['mapping_count']) is not int or v['mapping_count']<0 or len(v['effective_sha256'])!=64:raise ValueError('invalid map digest')
  found[k]=v
 if set(found)!=expected:raise ValueError('incomplete inventory')
 return found

def compare(start,end):
 a,b=load(start),load(end)
 changed=[list(k) for k in a if a[k]!=b[k]]
 if changed:raise ValueError('changed effective state: '+str(changed))
 return {'result':'PASS','successful_observations_per_snapshot':42,'inventory_rows_per_snapshot':2,'zero_binding_readbacks_per_snapshot':18,'map_comparison':'complete payload SHA-256; mapping content withheld','groups':[{'role':role,'category':cat,'count':sum(1 for k in a if k[:2]==(role,cat)),'equal':True} for role in ('dut','peer') for cat in ('binding','format','map','clock')]}
if __name__=='__main__':
 try:print(json.dumps(compare(*sys.argv[1:]),indent=2))
 except (ValueError,KeyError,TypeError) as e:print(json.dumps({'result':'FAIL','reason':str(e)}));sys.exit(1)
