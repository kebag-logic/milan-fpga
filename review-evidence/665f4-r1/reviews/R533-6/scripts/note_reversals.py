#!/usr/bin/env python3
"""Select only the three unchanged upstream note-4/5 reversals."""
import sys
import shutil
from pathlib import Path
repo=Path(sys.argv[1]);mode=sys.argv[2];prefix=Path(sys.argv[3])
packet=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(repo/'third_party/lwSRP/tests'))
import check_reversals as checks
labels={'point-to-point-condition','pending-point-to-point-condition','shared-in-condition'}
checks.CASES=tuple(c for c in checks.CASES if c[0] in labels)
assert len(checks.CASES)==3,[c[0] for c in checks.CASES]
work=packet/'scratch'/f'notes-{mode}'
sys.argv=[sys.argv[0],'--work-dir',str(work),'--prefix',str(prefix),'--milan',mode]
rc=checks.main()
dest=packet/'receipts'/f'notes-{mode}';dest.mkdir(exist_ok=True)
for f in work.glob('*.log'):shutil.copyfile(f,dest/f.name)
shutil.copyfile(work/'commands.json',dest/'commands.json')
raise SystemExit(rc)
