#!/usr/bin/env python3
"""Verify published source receipt bytes and write this packet's publication manifest."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
manifest={x['file']:x['published_sha256'] for x in json.loads((p/'public-MANIFEST.json').read_text())}
records=[]
for f in sorted((p/'public').rglob('*')):
 if not f.is_file():continue
 name=f.relative_to(p/'public').as_posix();data=f.read_bytes();expected=manifest[name]
 if hashlib.sha256(data).hexdigest()!=expected:
  # Text transport may normalize CSV CRLF or add one terminal newline.
  candidates=(data[:-1],data.replace(b'\n',b'\r\n'),data[:-1].replace(b'\n',b'\r\n'))
  matches=[d for d in candidates if hashlib.sha256(d).hexdigest()==expected]
  assert matches, name
  f.write_bytes(matches[0]);data=matches[0]
 records.append({'file':name,'sha256':hashlib.sha256(data).hexdigest(),'matches_public_manifest':True})
(p/'public-receipt-verification.json').write_text(json.dumps(records,indent=2)+'\n')
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R692] POSITIVE - exact head 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33'
assert 'SKELETON' not in report and report.splitlines()[-1]=='R692-1 FINISHED'
lines=[]
for f in sorted(p.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(p)
 if rel.parts[0]=='scratch' or rel.name=='MANIFEST.sha256':continue
 lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+rel.as_posix()+'\n')
(p/'MANIFEST.sha256').write_text(''.join(lines))
print(f'{len(records)} public source receipts verified; {len(lines)} packet files listed; scratch excluded')
