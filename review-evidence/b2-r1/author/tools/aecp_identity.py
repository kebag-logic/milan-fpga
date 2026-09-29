"""Compare the DUT's live ENTITY 0 and CONFIGURATION 0 descriptors with aem_desc.bin.

usage: aecp_identity.py <identity-aecp.jsonl> <aem_desc.bin>
The jsonl holds avdecc_ro.py 'aem' READ_DESCRIPTOR responses; the response
payload is configuration_index, reserved, then the descriptor bytes.
"""
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.startswith('{"cmd"') or '"type":"aem"' in l]
image=open(sys.argv[2],'rb').read()
ok=True
for r in rows:
 if r.get('type')!='aem':continue
 kind=int(r['req'][8:12],16);name={0:'ENTITY',1:'CONFIGURATION'}[kind]
 body=bytes.fromhex(r['payload'])[4:] if r.get('status')=='SUCCESS' else b''
 off=image.find(body) if body else -1
 exact=off>=0 and len(body)>0
 diffs=[] if exact else ['no exact occurrence']
 print(f"{name} 0: status={r.get('status')} bytes={len(body)} image_offset={hex(off) if off>=0 else None} exact_match={exact}")
 if name=='ENTITY' and body:
  print(f"  entity_id={body[4:12].hex()} model_id={body[12:20].hex()}")
 ok=ok and exact and r.get('status')=='SUCCESS'
print('AECP identity:', 'PASS' if ok and len([r for r in rows if r.get('type')=='aem'])==2 else 'FAIL')
sys.exit(0 if ok else 1)
