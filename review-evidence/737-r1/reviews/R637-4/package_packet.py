#!/usr/bin/env python3
"""Publish only packet files; preserve raw local logs privately and hash path-redacted logs."""
import hashlib,json,pathlib,re,sys
out=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve()
redactions=json.loads((out/'log-redactions.json').read_text()) if (out/'log-redactions.json').exists() else []
for path in sorted(out.glob('*.log')):
 raw=path.read_bytes();text=raw.decode()
 cleaned=text.replace(str(root),'$REVIEW_ROOT').replace(str(out),'$REVIEW_PACKET')
 cleaned=re.sub(r'/home/[^/\s\"\']+', '$HOME', cleaned)
 if cleaned!=text:
  saved=out/'scratch/raw-logs'/path.name;saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(raw)
  path.write_text(cleaned)
  redactions.append({'file':path.name,'kind':'local-path-only','original_sha256':hashlib.sha256(raw).hexdigest(),'published_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(out/'log-redactions.json').write_text(json.dumps(redactions,indent=2)+'\n')
report=(out/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R637] POSITIVE - exact head 08adb21af0a72d839ce30b6c461503dad269d4d6'
assert report.splitlines()[-1]=='R637-4 FINISHED' and 'SKELETON' not in report
files=sorted(p for p in out.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(out).parts and p.name!='MANIFEST.sha256')
for p in files:
 text=p.read_text();assert str(root) not in text and str(out) not in text and not re.search(r'/home/[A-Za-z0-9_.-]+/',text),p.name
(out/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(out).as_posix()+'\n' for p in files))
print(json.dumps({'publishable_files':len(files),'path_redacted_logs':len(redactions),'report_first_line':report.splitlines()[0],'report_last_line':report.splitlines()[-1]},indent=2))
