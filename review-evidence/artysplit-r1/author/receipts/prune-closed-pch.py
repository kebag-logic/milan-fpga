"""Reclaim generated precompiled headers from closed attempts only.

Every executable, ELF, source, trace and existing receipt remains byte-for-byte.
"""
import datetime,hashlib,json,re,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
closed=json.loads((r/'closed-intermediate-cleanup-plan.json').read_text())['by_closed_attempt']
roots=[r/name for name in closed]
paths=[]
for directory in roots:
 for path in directory.rglob('*.gch'):
  if path.is_symlink() or not path.is_file():continue
  assert path.resolve().is_relative_to(directory)
  if not re.fullmatch(r'V.+__pch\.h\.(fast|slow)\.gch',path.name):continue
  assert any(part=='native' or part=='obj_dir' or part.startswith('obj_') for part in path.relative_to(directory).parts[:-1])
  paths.append(path)
if '--apply' not in sys.argv:
 print(json.dumps(dict(status='PLAN ONLY',files=len(paths),allocated_bytes=sum(p.stat().st_blocks*512 for p in paths))))
 raise SystemExit(0)
for cmdline in Path('/proc').glob('[0-9]*/cmdline'):
 try:args=cmdline.read_bytes().split(b'\0')
 except OSError:continue
 for argument in args:
  if not argument.startswith(b'$VALIDATION_STORAGE/artysplit-a829/r4/'):continue
  raw=Path(argument.decode(errors='replace'))
  assert not any(raw.is_relative_to(directory) for directory in roots),f'Active process references closed attempt: {cmdline.parent.name}'
items=[]
for path in paths:
 with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
 items.append(dict(path=str(path),bytes=path.stat().st_size,allocated_bytes=path.stat().st_blocks*512,sha256=digest))
receipt=r/'closed-pch-cleanup.json'
assert not receipt.exists(),'Preserve the prior cleanup receipt'
record=dict(status='VALIDATED BEFORE DELETION',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 files=len(items),allocated_bytes=sum(x['allocated_bytes'] for x in items),items=items,
 claim='Only generated Verilator precompiled headers from closed historical attempts; no executables, firmware, source or traces removed.')
receipt.write_text(json.dumps(record,indent=2)+'\n')
for item in items:
 path=Path(item['path']);assert path.stat().st_size==item['bytes']
 path.unlink()
assert not any(Path(item['path']).exists() for item in items)
record.update(status='COMPLETE',finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
receipt.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='items'},indent=2))
