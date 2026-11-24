#!/usr/bin/env python3
"""Collect publishable receipts, preserving raw simulation bytes and redacting only build host paths."""
import pathlib,hashlib,re,json
P=pathlib.Path(__file__).resolve().parents[1];R=P/'receipts'
def public_build(text):
 text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff','<simulator-install>',text)
 text=re.sub(r'/home/[^/\s]+/litex-milan','<product-dependencies>',text)
 text=re.sub(r'/home/[^/\s]+/br-milan-rv32/host','<rv32-sdk>',text)
 text=re.sub(r'/home/[^/\s]+','<user-home>',text)
 return text
for f in list(R.glob('*.build.log'))+list(R.glob('*-build.log'))+list(R.glob('budget-driver.log'))+list(R.glob('budget.Os-build.log')):
 target=f.with_name(f.stem+'.public.log');target.write_text(public_build(f.read_text()))
exclude={'independent-findings.txt'}
files=[]
for f in sorted(R.rglob('*')):
 if not f.is_file() or f.name in exclude:continue
 if (f.name.endswith('.build.log') or f.name.endswith('-build.log') or f.name in ('budget-driver.log','budget.Os-build.log')) and not f.name.endswith('.public.log'):continue
 files.append(f)
files+=sorted((P/'scripts').glob('*.py'))
# Privacy check of exactly the publication population.
for f in files:
 text=f.read_text()
 assert not re.search(r'/home/[A-Za-z0-9_.-]+',text),f
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n' for f in sorted(files))
(P/'MANIFEST.sha256').write_text(manifest)
print('Publishable files:',len(files),'bytes:',sum(f.stat().st_size for f in files))
