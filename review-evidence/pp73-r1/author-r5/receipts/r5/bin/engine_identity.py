from pathlib import Path
import subprocess
import shutil
import hashlib
from concurrent.futures import ThreadPoolExecutor
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
def build(side):
 root=r/'base' if side=='base' else r/'head'
 out=r/'elaboration'/side;out.mkdir(parents=True,exist_ok=True)
 sources=sorted(root.glob('hdl/**/*_pkg.sv'))+sorted(p for p in root.glob('hdl/**/*.sv') if not p.name.endswith('_pkg.sv'))
 with (out/'all.v').open('w') as f, (out/'convert.log').open('w') as err:
  subprocess.run(['$VALIDATION_STORAGE/pp73-a595/tools/bin/sv2v',*[str(p.relative_to(root)) for p in sources]],cwd=root,stdout=f,stderr=err,check=True)
 shutil.copyfile(r/'rom'/side/'ucode.hex',out/'ucode.hex')
 with (out/'engine.log').open('w') as f:
  subprocess.run(['/usr/bin/yosys','-Q','-T','-q','-p','read_verilog -defer all.v; hierarchy -check -top KL_aecp_engine; proc; opt_clean; write_rtlil engine.il'],cwd=out,stdout=f,stderr=subprocess.STDOUT,check=True)
with ThreadPoolExecutor(2) as pool:list(pool.map(build,['base','head']))
lines=[]
for name in ['all.v','engine.il']:
 b=(r/'elaboration/base'/name).read_bytes();h=(r/'elaboration/head'/name).read_bytes()
 assert b==h, name
 lines.append(f'{name}\t{len(b)}\t{hashlib.sha256(b).hexdigest()}\tbyte-identical')
(r/'elaboration-identity.tsv').write_text('artifact\tbytes\tsha256 at both sides\tidentity\n'+'\n'.join(lines)+'\n')
print('\n'.join(lines))
