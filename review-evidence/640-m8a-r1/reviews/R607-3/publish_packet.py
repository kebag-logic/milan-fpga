#!/usr/bin/env python3
"""Prepare public receipts with only local path substitutions, then hash the allowlist."""
import argparse,hashlib,pathlib
ap=argparse.ArgumentParser();ap.add_argument('--source-checkout',type=pathlib.Path,required=True);ap.add_argument('--tools',type=pathlib.Path,required=True);a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parent;s=p/'scratch';out=p/'receipts';out.mkdir(exist_ok=True)
replacements=[(str(s/'candidate'),'$REVIEW_TREE'),(str(s),'$REVIEW_SCRATCH'),(str(p),'$REVIEW_PACKET'),(str(a.source_checkout.resolve()),'$SOURCE_CHECKOUT'),(str(a.tools.resolve()),'$TOOLS'),(str(pathlib.Path.home()),'$HOME')]
def clean(data):
 text=data.decode()
 for old,new in replacements:text=text.replace(old,new)
 return text.encode()
for source in sorted((s/'raw').glob('*')):
 if source.is_file():(out/source.name).write_bytes(clean(source.read_bytes()))
for source in sorted((s/'sims').glob('*.log')):
 (out/('aggregate-'+source.name)).write_bytes(clean(source.read_bytes()))
(s/'publish-allowlist.txt').write_text('')
files=[p/'REPORT.md',p/'round3-diff.patch',p/'history.txt',p/'independent-pass.txt',p/'hosted-snapshot.json',p/'pr-body-as-examined.md']
files+=list(p.glob('scope-*.txt'))
files+=[p/f'evidence-{n}.txt' for n in [6107961867,6108233154]]
files+=list(out.glob('*'))
files+=list(p.glob('*.py'))
files+=list((p/'public-evidence').rglob('*'))
files=sorted({f for f in files if f.is_file()})
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files)
(p/'MANIFEST.sha256').write_text(manifest)
print('Publishable files:',len(files),'(scratch and previous report comment captures excluded)')
