#!/usr/bin/env python3
"""Independent CLI oracles and mutation sensitivity for ROM cache identity."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT, OUT = (Path(v).resolve() for v in sys.argv[1:])
OUT.mkdir(parents=True)
SCRIPT = ROOT / 'syn/yosys/result_cache.py'
ROWS = []

def call(label, args, expected=0, script=SCRIPT):
    cmd = ['rtk', 'proxy', sys.executable, str(script), *map(str,args)]
    p = subprocess.run(cmd, capture_output=True, env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    (OUT/(label+'.stdout')).write_bytes(p.stdout)
    (OUT/(label+'.stderr')).write_bytes(p.stderr)
    ROWS.append(dict(label=label,command=cmd,expected=expected,exit=p.returncode))
    (OUT/'commands.json').write_text(json.dumps(ROWS,indent=2)+'\n')
    assert p.returncode==expected, (label,p.returncode,p.stderr)
    return p.stdout.decode().strip()

def sha(b): return hashlib.sha256(b).hexdigest()
def snapshot(root):
    return {str(p.relative_to(root)): [sha(p.read_bytes()),p.stat().st_mode & 0o777]
            for p in root.rglob('*') if p.is_file()}

names = ['gptp_ucode.hex','ltn_rom.hex','ucode.hex']
images = dict(zip(names,[b'\x00\xff01\n',b'01\r\n',b'abcdef\x00']))
rom = OUT/'rom'; rom.mkdir()
for name in reversed(names): (rom/name).write_bytes(images[name])
framed = b''.join(n.encode()+b'\0'+len(images[n]).to_bytes(8,'big')+images[n] for n in names)
digest = sha(framed)
assert call('digest-oracle',['rom-digest','--rom-dir',rom])==digest
(rom/'extra.hex').write_bytes(b'excluded')
for n in names: os.utime(rom/n,(1000000000,1000000000))
assert call('mtime-extra-invariant',['rom-digest','--rom-dir',rom])==digest
for n in names:
    p=rom/n; b=images[n]
    p.write_bytes(bytes([b[0]^1])+b[1:]);os.utime(p,(1000000000,1000000000))
    assert call('same-size-byte-'+n,['rom-digest','--rom-dir',rom])!=digest
    p.write_bytes(b'');call('empty-'+n,['rom-digest','--rom-dir',rom],2)
    p.write_bytes(b);p.rename(rom/(n+'.wrong'))
    call('wrong-name-'+n,['rom-digest','--rom-dir',rom],2)
    (rom/(n+'.wrong')).unlink();call('missing-'+n,['rom-digest','--rom-dir',rom],2)
    p.write_bytes(b)
(rom/names[0]).write_bytes(images[names[1]])
(rom/names[1]).write_bytes(images[names[0]])
assert call('swap-filenames',['rom-digest','--rom-dir',rom])!=digest
for n in names: (rom/n).write_bytes(images[n])
sv = OUT/'T.v';sv.write_bytes(b'module T; endmodule\n')
program = 'read_verilog @TMP@/T.v;\n hierarchy -check -top T; stat -json'
fields = {'top':'T','mode':'full','sv2v_sha256':sha(sv.read_bytes()),'program':program.replace('\n',' '),
          'yosys_version':'Yosys controlled identity','yosys_sha256':'ab'*32,'sv2v_version':'controlled sv2v','rom_sha256':digest}
schema='milan-yosys-result-cache/2'
canonical=schema+'\n'+''.join(k+'='+v+'\n' for k,v in fields.items())
key=sha(canonical.encode())
args=['--top','T','--mode','full','--sv2v-file',sv,'--program',program,'--yosys-version',fields['yosys_version'],
      '--yosys-bin-sha256',fields['yosys_sha256'],'--sv2v-version',fields['sv2v_version'],'--rom-sha256',digest]
assert call('canonical-key',['key',*args])==key
for i,bad in enumerate(['','a'*63,'a'*65,'A'*64,'g'*64,'a'*63+'\n']):
    call('invalid-digest-'+str(i),['key',*args[:-1],bad],2)
call('missing-digest-argument',['key',*args[:-2]],2)
statfile=OUT/'stat.json';statfile.write_text('{"design":{"num_cells":42}}\n')
head=OUT/'head';seed=OUT/'seed'
call('store',['store','--dir',head,*args,'--cells','42','--stat-json',statfile])
assert call('head-hit',['lookup','--dir',head,*args])=='cells=42'
shutil.copytree(head,seed)
for p in [seed,*seed.rglob('*')]:p.chmod(p.stat().st_mode & ~0o222)
before=snapshot(seed)
assert call('readonly-seed-hit',['lookup','--dir',OUT/'absent','--seed',seed,*args])=='cells=42'
assert snapshot(seed)==before
entry=head/key;record=(entry/'record').read_bytes();statbytes=(entry/'stat.json').read_bytes()
variants={
    'schema1':record.replace(schema.encode(),b'milan-yosys-result-cache/1').replace(('rom_sha256='+digest+'\n').encode(),b''),
    'missing-rom':record.replace(('rom_sha256='+digest+'\n').encode(),b''),
    'malformed-rom':record.replace(digest.encode(),b'not-a-digest'),
    'wrong-rom':record.replace(digest.encode(),b'f'*64),
    'duplicate-rom':record+('rom_sha256='+digest+'\n').encode(),
    'fail':record.replace(b'status=PASS',b'status=FAIL'),
    'forged-cells':record.replace(b'cells=42',b'cells=43'),
    'garbage':b'garbage\n',
}
for k,v in fields.items():
    variants['wrong-'+k]=record.replace((k+'='+v+'\n').encode(),(k+'=different\n').encode())
for label,b in variants.items():
    planted=OUT/('bad-'+label); e=planted/key;e.mkdir(parents=True)
    (e/'record').write_bytes(b);(e/'stat.json').write_bytes(statbytes)
    before=snapshot(planted)
    call(label+'-head',['lookup','--dir',planted,*args],2)
    for p in [planted,*planted.rglob('*')]:p.chmod(p.stat().st_mode & ~0o222)
    frozen=snapshot(planted)
    call(label+'-seed',['lookup','--dir',OUT/'absent','--seed',planted,*args],2)
    assert snapshot(planted)==frozen
    # First matching key refuses even with a valid later seed.
    call(label+'-shadow',['lookup','--dir',planted,'--seed',seed,*args],2)
legacy=OUT/'legacy'; oldkey=sha(('milan-yosys-result-cache/1\n'+''.join(k+'='+v+'\n' for k,v in fields.items() if k!='rom_sha256')).encode())
e=legacy/oldkey;e.mkdir(parents=True);(e/'record').write_bytes(variants['schema1']);(e/'stat.json').write_bytes(statbytes)
call('old-original-head',['lookup','--dir',legacy,*args],1)
call('old-original-seed',['lookup','--dir',OUT/'absent','--seed',legacy,*args],1)
for i,bad in enumerate([True,-1,1.25,'42',None]):
    (entry/'stat.json').write_text(json.dumps({'design':{'num_cells':bad}}))
    call('invalid-stat-'+str(i),['lookup','--dir',head,*args],2)
    call('invalid-store-'+str(i),['store','--dir',OUT/'bad-store',*args,'--cells','42','--stat-json',entry/'stat.json'],2)
(entry/'stat.json').write_bytes(statbytes)
call('store-disagrees',['store','--dir',head,*args,'--cells','43','--stat-json',statfile],2)
before=snapshot(head)
call('store-never-rewrites',['store','--dir',head,*args,'--cells','42','--stat-json',statfile])
assert snapshot(head)==before
source=SCRIPT.read_text()
mutants={
 'omit-gptp':source.replace('("gptp_ucode.hex", "ltn_rom.hex", "ucode.hex")','("ltn_rom.hex", "ucode.hex")'),
 'omit-acmp':source.replace('("gptp_ucode.hex", "ltn_rom.hex", "ucode.hex")','("gptp_ucode.hex", "ucode.hex")'),
 'omit-aecp':source.replace('("gptp_ucode.hex", "ltn_rom.hex", "ucode.hex")','("gptp_ucode.hex", "ltn_rom.hex")'),
 'ignore-bytes':source.replace('digest.update(content)','digest.update(b"constant")'),
 'omit-field-key':source.replace('lines.append(f"{name}={getattr(self, name).replace(chr(10), \' \')}")','if name != "rom_sha256":\n                lines.append(f"{name}={getattr(self, name).replace(chr(10), \' \')}")'),
 'ignore-record-rom':source.replace('if record.get(name) != want:', 'if name != "rom_sha256" and record.get(name) != want:'),
 'accept-schema1':source.replace('if record.get("schema") != SCHEMA:', 'if record.get("schema") not in (SCHEMA, "milan-yosys-result-cache/1"):').replace('if record.get(name) != want:', 'if name != "rom_sha256" and record.get(name) != want:'),
}
for name,modified in mutants.items():
    assert modified!=source,name
    p=OUT/('mutant-'+name+'.py');p.write_text(modified)
    call('mutant-'+name,['--selftest'],1,p)
(OUT/'complete.json').write_text(json.dumps({'result':'PASS','commands':len(ROWS),'mutants_killed':list(mutants),'expected_digest':digest,'expected_key':key},indent=2)+'\n')
print(f'PASS: {len(ROWS)} independent CLI controls, {len(mutants)} killed mutants')
