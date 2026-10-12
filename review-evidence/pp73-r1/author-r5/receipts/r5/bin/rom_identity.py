from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,hashlib,json
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
def build(side):
    out=r/'rom'/side;out.mkdir(parents=True,exist_ok=True)
    root=r/side
    for program,name in [('hdl/aecp/ucode/gen_ucode.py','ucode.hex'),('hdl/acmp/rom/gen_ltn_rom.py','ltn_rom.hex')]:
        with (out/(name+'.log')).open('w') as f:
            subprocess.run(['python3','-B',program,'-o',str(out/name)],cwd=root,stdout=f,stderr=subprocess.STDOUT,check=True)
with ThreadPoolExecutor(2) as pool:list(pool.map(build,['base','head']))
lines=['artifact\tbytes\tsha256\tidentity']
for name in ['ucode.hex','ltn_rom.hex']:
    values=[(r/'rom'/side/name).read_bytes() for side in ['base','head']]
    values.append((r.parent/'r4/rom/base'/name).read_bytes())
    assert all(b==values[0] for b in values),name
    lines.append(f'{name}\t{len(values[0])}\t{hashlib.sha256(values[0]).hexdigest()}\toriginal base, merged main and candidate byte-identical')
(r/'rom-identity.tsv').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
