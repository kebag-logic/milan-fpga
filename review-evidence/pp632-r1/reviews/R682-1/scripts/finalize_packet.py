#!/usr/bin/env python3
"""Apply path-only publication substitutions and write the publication allow-list."""
import hashlib
from pathlib import Path
import re
import shutil

p=Path(__file__).resolve().parents[1]
scripts=['limited-simulator.py','reproduce.py','d3_final.py','static_checks.py',
         'docs_check.py','d3_latency_probe.py','consumer_check.py','reconcile.py',
         'integrity.py','finalize_packet.py']
files=[p/'REPORT.md']+[p/'scripts'/s for s in scripts]
for f in sorted((p/'receipts').rglob('*')):
    if not f.is_file(): continue
    rel=f.relative_to(p).as_posix()
    if rel=='receipts/pr770-R677-2-public.txt': continue
    if rel.startswith('receipts/d3-supplement/'): continue
    if rel.startswith('receipts/d3/') and f.name!='golden-pp_top.log': continue
    files.append(f)
rawdir=p/'scratch/raw-before-path-substitution'
changes=[]
for f in files:
    rel=f.relative_to(p).as_posix()
    if not rel.startswith('receipts/') or rel.startswith('receipts/public/'):
        continue
    if f.suffix not in ('.log','.txt'): continue
    if f.name=='path-substitution.txt': continue
    raw=f.read_bytes()
    new=re.sub(rb'$WORKSPACE_HOME/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr',b'<toolchain>/usr',raw)
    new=new.replace(str(p).encode(),b'<packet>')
    new=new.replace(b'$REVIEWS/r682-1-pp632',b'<review-checkout>')
    if new!=raw:
        dest=rawdir/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists(): dest.write_bytes(raw)
        f.write_bytes(new)
        changes.append(f'{rel}: original sha256 {hashlib.sha256(raw).hexdigest()}; published sha256 {hashlib.sha256(new).hexdigest()}')
note=p/'receipts/path-substitution.txt'
if not note.exists():
    note.write_text('Path-only substitutions in reviewer execution logs: compiler installation -> <toolchain>; packet root -> <packet>; review source clone -> <review-checkout>. No test/result line is removed or summarized. Published source receipts under receipts/public remain byte-identical to their Git blobs. Original reviewer log bytes are retained only under unpublished scratch/.\n\n'+'\n'.join(changes)+'\n')
if note not in files: files.append(note)
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R682] POSITIVE - exact head 51f88c7e14e7e2527c09ff9a23b93dd6b857fd50'
assert report.splitlines()[-1]=='R682-1 FINISHED'
assert 'SKELETON' not in report
for rc in ('notify-campaign','decode-sweep','command-gate','docs-checks','d3-final','consumer-notify','consumer-control','consumer-restored-rom'):
    assert (p/'receipts'/f'{rc}.rc').read_text().strip()=='0',rc
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix()+'\n' for f in sorted(set(files)))
(p/'MANIFEST.sha256').write_text(manifest)
print('Publication files:',len(set(files)))
print('Report verdict and terminal marker verified; required execution return codes are zero.')
