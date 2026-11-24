"""Inventory only reproducible intermediates from closed historical attempts.

Do not touch traces, source snapshots, executables, firmware images, manifests,
the current refined campaign or its native-optimization dependency.
"""
import json
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
names=('final-census','final-census-before-comment-correction','arm-a','arm-a-full',
 'arm-b','arm-fast','arm-declaring','arm-valid','arm-later','arm-every','arm-two',
 'arty-boot','final-boot-positive-fixedseed','final-boot-controls','final-boot-controls-fixedseed',
 'arty-region','arty-region-cached','rtl-fixture','final-firmware')
items=[];totals={}
for name in names:
 directory=r/name
 if not directory.exists():continue
 assert not directory.is_symlink() and directory.resolve()==directory
 subtotal=0
 for path in directory.rglob('*'):
  if path.is_symlink() or not path.is_file():continue
  resolved=path.resolve()
  if not resolved.is_relative_to(directory):continue
  relative=path.relative_to(directory)
  generated=(path.name.startswith('V') and path.suffix in ('.cpp','.h')
             and any(part=='native' or part=='obj_dir' or part.startswith('obj_') for part in relative.parts[:-1]))
  if path.suffix not in ('.o','.a','.d') and not generated:continue
  size=path.stat().st_size;allocated=path.stat().st_blocks*512
  items.append(dict(path=str(path),bytes=size,allocated_bytes=allocated,
                    kind='generated native source' if generated else 'compiled intermediate'))
  subtotal+=allocated
 totals[name]=subtotal
record=dict(status='INVENTORY ONLY; NOTHING DELETED',files=len(items),
 allocated_bytes=sum(totals.values()),by_closed_attempt=totals,items=items,
 exclusions=['refined','native-optimization','snapshots','all logs/results','all Vsim/ELF/images/manifests'])
(r/'closed-intermediate-cleanup-plan.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='items'},indent=2))
