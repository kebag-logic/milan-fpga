#!/usr/bin/env python3
"""Verify generated records and public input manifests; CHECKOUT PACKET."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'scripts'))
import check_port_contracts as ports,measure_naming as naming
scratch=packet/'scratch'
a=ports.audit(); assert not a['refusal']; ports.write_budget(a,scratch/'port_docs.budget')
assert (scratch/'port_docs.budget').read_bytes()==(root/'scripts/port_docs.budget').read_bytes();print('PASS port census generator is byte-identical')
rows,_,trees=naming.scan_repo(); naming.BUDGET=scratch/'naming.budget'; naming.write_budget(rows,trees)
assert naming.BUDGET.read_bytes()==(root/'scripts/naming.budget').read_bytes();print('PASS naming generator is byte-identical')
sha=lambda b:hashlib.sha256(b).hexdigest()
ledger={tuple(line.split()[:2]):line.split()[2] for line in (root/'syn/yosys/rom_digests.tsv').read_text().splitlines() if line and not line.startswith('#')}
for image,gen in [('ltn_rom.hex','hdl/acmp/rom/gen_ltn_rom.py'),('ucode.hex','hdl/aecp/ucode/gen_ucode.py')]:
 output=scratch/image; subprocess.run(['python3',str(root/'protocol-processor'/gen),'-o',str(output)],stdout=subprocess.DEVNULL,check=True)
 digest=sha(output.read_bytes())
 for pin in ['2cbed0a987c1e68402658d69459ab7e5aa571adc','2ad2f845dd583f8310075fa2380cb60a04fd091a']:assert ledger[(pin,image)]==digest
 print('PASS ROM generator',image,digest)
evidence=scratch/'review-evidence/708-r1'
manifest=json.loads((evidence/'MANIFEST.json').read_text())
for record in manifest: assert sha((evidence/record['file']).read_bytes())==record['published_sha256'],record['file']
print('PASS public archive checksums',len(manifest))
r=evidence/'author/evidence/resume'
base=json.loads(subprocess.check_output(['git','show','734eb780:syn/ooc/pp_resource_baseline.json'],cwd=root))
head=json.loads((root/'syn/ooc/pp_resource_baseline.json').read_text())
for endpoint in head['endpoints']:
 a=base['endpoints'][endpoint];b=head['endpoints'][endpoint]
 assert {k:v for k,v in a.items() if k not in ['record','measured']}=={k:v for k,v in b.items() if k not in ['record','measured']}
 assert a['record']['identity']==b['record']['identity'];print('PASS unchanged resource policy and flow identity',endpoint)
for endpoint,name in [('route-1x1','cand2-route'),('ooc-1x1','cand2-ax7101-ooc'),('ooc-8x8','cand2-ax8x8-ooc')]:
 m=json.loads((r/(name+'-manifest.json')).read_text());assert m['inputs_sha256']==head['endpoints'][endpoint]['record']['inputs_sha256']
 count=0
 for f in m['files']:
  if f['generated'] or not f['file'].startswith('$ROOT1/'):continue
  path=root/f['file'].split('/',1)[1]
  assert path.is_file() and sha(path.read_bytes())==f['sha256'],str(path)
  count+=1
 print('PASS published manifest bound to head',endpoint,count,'repository inputs; generated input hashes are author receipts')
a=json.loads((r/'base2-route-manifest.json').read_text());b=json.loads((r/'cand2-route-manifest.json').read_text())
assert a['images']==b['images'] and a['generics']==b['generics']
normalize=lambda m:{f['file'].split('/',1)[1]:f['sha256'] for f in m['files']}
af,bf=normalize(a),normalize(b); assert af.keys()==bf.keys()
delta=[k for k in af if af[k]!=bf[k]]
assert len(delta)==6 and all(k.startswith('protocol-processor/hdl/') for k in delta)
print('PASS base/candidate export: six processor files only; all six memory images equal')
for k in delta:print(k)
fw='sw/firmware/milan_baremetal/milan_baremetal.c'
assert subprocess.check_output(['git','show','734eb780:'+fw],cwd=root)==(root/fw).read_bytes()
print('PASS firmware source unchanged',sha((root/fw).read_bytes()))
