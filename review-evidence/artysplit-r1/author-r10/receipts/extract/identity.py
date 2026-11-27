"""Every file under DIR through the publication scrub: report each one the scrub would change, and how."""
import difflib,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,'$LANE_TOOLS'); sys.path.insert(0,'$SOURCE/scripts')
import privacy
root=Path(sys.argv[1]); changed=[]; n=0
for p in sorted(root.rglob('*')):
    if not p.is_file(): continue
    n+=1; data=p.read_bytes(); out=privacy.scrub_redact(data)
    if out!=data:
        a=data.decode('utf-8','replace').splitlines(); b=out.decode('utf-8','replace').splitlines()
        diff=[l for l in difflib.unified_diff(a,b,lineterm='',n=0) if l[:1] in '+-' and l[:3] not in ('+++','---')][:4]
        changed.append(dict(file=str(p.relative_to(root)),diff=[d[:200] for d in diff]))
        print('CHANGED',p.relative_to(root),diff[:2],flush=True)
print(json.dumps(dict(files=n,changed=len(changed))))
Path(sys.argv[2]).write_text(json.dumps(changed,indent=1))
