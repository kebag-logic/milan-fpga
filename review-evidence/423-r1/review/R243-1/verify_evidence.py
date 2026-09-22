import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent;p=root/'public-candidate1'
f=json.loads((p/'manager-builder-final/results.json').read_bytes());o=json.loads((p/'manager-builder/results.json').read_bytes());c=json.loads((p/'whitespace-correction/results.json').read_bytes())
assert len(f['results'])==46 and len(o['results'])==46 and len(c['results'])==1
for i,row in enumerate(f['results']):
 source=json.loads((p/row['receipt_origin']).read_bytes())['results'][row['receipt_row']]
 assert {k:v for k,v in row.items() if not k.startswith('receipt_')}==source
 assert row['exit_code']==0
assert [i for i,r in enumerate(o['results']) if r['exit_code']!=0]==[44]
assert o['results'][44]['exit_code']==128 and f['superseded_command']==o['results'][44]
assert c['results'][0]['command'][-2:]==[f['base'],f['head']]
assert (p/'whitespace-correction/01.log').read_bytes()==b''
assert b'bad object 5bbf' in (p/'manager-builder/45.log').read_bytes()
n=json.loads((p/'full-native/results.json').read_bytes());assert len(n['results'])==5 and all(x['exit_code']==0 for x in n['results'])
assert f['head']==n['head']=='df53dfa116b34816db0193230ad9833e67bf46dd'
assert f['base']==n['base']=='52711029f374650dc93830d5ea28e81cb5c8f410'
print('46 builder rows independently traced to 45 original successes and one separate measured correction; 5 native groups at assigned head/base; stale original remains exit128')
