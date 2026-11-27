#!/usr/bin/env python3
"""Normalize machine paths in receipts and write a publication manifest."""
import argparse, hashlib, json, pathlib, shutil
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('packet',type=pathlib.Path); a=p.parse_args()
src,out=a.source.resolve(),a.packet.resolve()
backup=out/'scratch/prepublication'
backup.mkdir(parents=True,exist_ok=True)
def digest(data): return hashlib.sha256(data).hexdigest()
changes=[]
for f in sorted(out.rglob('*')):
    if not f.is_file() or f.is_relative_to(out/'scratch') or f.name in ['MANIFEST.sha256','normalization.json'] or f.suffix=='.py':
        continue
    raw=f.read_bytes()
    data=raw
    for old,new in [(str(src),'<SOURCE>'),(str(out),'<PACKET>'),('$VALIDATION_TOOLS','<TOOLCHAIN>'),('<home-path>/work','<HOSTED_WORK>')]:
        data=data.replace(old.encode(),new.encode())
    if data!=raw:
        dest=backup/f.relative_to(out); dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(f,dest); f.write_bytes(data)
        changes.append(dict(path=str(f.relative_to(out)),original_sha256=digest(raw),published_sha256=digest(data),transformation='machine path prefixes only'))
(out/'normalization.json').write_text(json.dumps(changes,indent=2)+'\n')
files=[f for f in sorted(out.rglob('*')) if f.is_file() and not f.is_relative_to(out/'scratch') and f.name!='MANIFEST.sha256']
(out/'MANIFEST.sha256').write_text(''.join(digest(f.read_bytes())+'  '+str(f.relative_to(out))+'\n' for f in files))
report=(out/'REPORT.md').read_text()
assert report.startswith('[R956] NEGATIVE - exact head 5d03517f2ab42416654a8f2be2f71cfc51d82440\n')
assert 'SKELETON' not in report and report.rstrip().endswith('R956-1 FINISHED')
print(json.dumps(dict(publishable_files=len(files),path_normalized_files=len(changes),scratch_excluded=True,report_final=True)))
