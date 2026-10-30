#!/usr/bin/env python3
"""Independent negative controls in a disposable clone; original source untouched."""
import os,pathlib,subprocess,sys,tempfile
src=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve()
root=pathlib.Path(tempfile.mkdtemp(prefix='probe-',dir=out/'scratch'))/'tree'
subprocess.run(['git','clone','-q','--shared',str(src),str(root)],check=True)
env=dict(os.environ,TMPDIR=str(out/'scratch'/'tmp'))
inv=root/'docs/INVENTORY.md'; original=inv.read_bytes()
def run(name,cmd,want,token=''):
 r=subprocess.run(cmd,cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/(name+'.log')).write_text(r.stdout); (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
 assert r.returncode==want and token in r.stdout,(name,r.returncode,r.stdout)
 print(name, r.returncode,token)
run('inventory-clean',['python3','scripts/check-doc-inventory.py'],0)
try:
 inv.write_bytes(original+b'\n| [`docs/deleted-page.md`](deleted-page.md) | history | reader | removed | current | checked |\n')
 run('inventory-stale-row',['python3','scripts/check-doc-inventory.py'],1,'NO FILE: docs/deleted-page.md')
finally: inv.write_bytes(original)
new=root/'docs/new-page.md'
try:
 new.write_text('# An unlisted page\n')
 run('inventory-missing-row',['python3','scripts/check-doc-inventory.py'],1,'NO ROW: docs/new-page.md')
finally: new.unlink()
page=root/'docs/GLOSSARY.md'; content=page.read_bytes()
try:
 page.unlink()
 run('inventory-missing-file',['python3','scripts/check-doc-inventory.py'],1,'NO FILE: docs/GLOSSARY.md')
finally: page.write_bytes(content)
try:
 page.write_bytes(content+b'\n[broken](absent-page.md#absent)\n')
 run('link-broken-file',['python3','scripts/check-links.py'],1,'missing target -> absent-page.md#absent')
finally: page.write_bytes(content)
try:
 page.write_bytes(content+b'\n[broken](architecture/02_interfaces.md#42-maap-address-allocation)\n')
 run('link-broken-anchor',['python3','scripts/check-links.py'],1,'missing anchor')
finally: page.write_bytes(content)
run('inventory-restored',['python3','scripts/check-doc-inventory.py'],0)
run('links-restored',['python3','scripts/check-links.py'],0)
subprocess.run(['git','diff','--exit-code'],cwd=root,check=True)
print('All required probes caught; disposable tracked source restored.')
