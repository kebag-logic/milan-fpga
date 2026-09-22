from pathlib import Path
import hashlib,json,tarfile,urllib.request,time
p=Path('$VALIDATION_TOOLS/bootlin-504-probe');p.mkdir(exist_ok=True)
name='riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz'
url='https://toolchains.bootlin.com/downloads/releases/toolchains/riscv32-ilp32d/tarballs/'+name
archive=p/name
if not archive.exists():
 with urllib.request.urlopen(url,timeout=60) as source, archive.open('wb') as target:
  while chunk:=source.read(1024*1024): target.write(chunk)
actual=hashlib.sha256(archive.read_bytes()).hexdigest()
expected='d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f'
assert actual==expected,(actual,expected)
with tarfile.open(archive) as source:
 names=source.getnames(); tops=sorted(set(n.split('/')[0] for n in names));assert len(tops)==1
 dest=p/tops[0]
 if not dest.exists():source.extractall(p,filter='data')
record={'url':url,'sha256':actual,'bytes':archive.stat().st_size,'root':str(dest),'members':len(names)}
Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-probe/download.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
