#!/usr/bin/env python3
"""Generate both ROMs and constrain the changed words to SET_CONFIGURATION."""
import hashlib,json,pathlib,subprocess,sys
packet=pathlib.Path(__file__).resolve().parents[1];source=pathlib.Path(sys.argv[1]).resolve();roms=[];digests={}
for rev,label in [('22c139a4323bc96c779d13e3f6774480c5fb9b75','base'),('ebc3b6bcd6e2c789c1c80c9e285193628567ea33','head')]:
 d=packet/'scratch'/('rom-'+label);d.mkdir(exist_ok=True)
 for name in ['gen_ucode.py','aecp_commands.json']:(d/name).write_bytes(subprocess.check_output(['git','show',rev+':hdl/aecp/ucode/'+name],cwd=source))
 subprocess.run([sys.executable,'-B',str(d/'gen_ucode.py'),'-o',str(d/'ucode.hex')],check=True)
 roms.append((d/'ucode.hex').read_text().splitlines());digests[label+'_sha256']=hashlib.sha256((d/'ucode.hex').read_bytes()).hexdigest()
changed=[i for i,(a,b) in enumerate(zip(*roms)) if a!=b];assert changed==[1459,1475]+list(range(1553,1566))
assert digests['head_sha256']=='a3b62cabe2cb091383f999bf58b830ff2d3ab63cd8699b95d2529dbf4d02bcb3'
result=dict(**digests,changed_word_addresses=changed,outside_E_SCFG_family_changed=False)
(packet/'receipts/rom-scope.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
