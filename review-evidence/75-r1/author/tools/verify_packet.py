"""Verify the existing manifest hierarchy without rewriting it."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent.parent
seen=set()
def verify(directory):
 manifest=directory/'MANIFEST.sha256';seen.add(manifest)
 actual=set()
 for line in manifest.read_text().splitlines():
  digest,name=line.split('  ',1)
  target=directory/name
  assert target.is_file() and target.resolve().is_relative_to(root.resolve()),name
  assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,name
  actual.add(target);seen.add(target)
 expected={f for f in directory.iterdir() if f.is_file() and f!=manifest}
 expected.update(d/'MANIFEST.sha256' for d in directory.iterdir() if d.is_dir())
 assert actual==expected,(directory,'manifest inventory mismatch')
 for d in directory.iterdir():
  if d.is_dir():verify(d)
verify(root)
files={f for f in root.rglob('*') if f.is_file()}
assert seen==files,'unmanifested artifact'
assert max(f.stat().st_size for f in files)<=200000,'oversized packet artifact'
print('PASS:',len(files),'files verified; all files at most 200,000 bytes')
