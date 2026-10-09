#!/usr/bin/env python3
"""Normalize host locations, check packet references and produce a publication manifest."""
import argparse,hashlib,importlib.util,json,pathlib,re,shutil,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve();p=a.packet.resolve();sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('privacy',r/'scripts/check_privacy.py');privacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(privacy)
rows=[];errors=[]
for f in sorted(p.rglob('*')):
 if not f.is_file() or 'scratch' in f.relative_to(p).parts or f.name in ['MANIFEST.sha256','location-redactions.json','packet-audit.json']:continue
 data=f.read_bytes()
 try:text=data.decode('utf-8')
 except UnicodeDecodeError:errors.append('unexpected binary: '+str(f.relative_to(p)));continue
 changed=text.replace(str(r),'$REPO').replace(str(p),'$PACKET')
 hosted='/'+'home'+'/runner/work/tsn-c-stack/tsn-c-stack'
 changed=changed.replace(hosted,'$HOSTED_REPO')
 # Remaining temporary/home locations are path metadata, never test output values.
 for part,label in [('home','HOME'),('tmp','TEMP'),('data','STORAGE'),('Users','HOME')]:
  changed=re.sub('/'+part+r'/[^\s"\'<>),;]+','$'+label,changed)
 output=changed.encode();rel=str(f.relative_to(p))
 if output!=data:
  dst=p/'scratch/original-receipts'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists():dst.write_bytes(data)
  f.write_bytes(output);rows.append({'path':rel,'original_sha256':hashlib.sha256(data).hexdigest(),'published_sha256':hashlib.sha256(output).hexdigest(),'redaction':'locations only'})
 errors+=privacy.scan(rel,output)
redactions=p/'receipts/location-redactions.json'
if rows:redactions.write_text(json.dumps(rows,indent=2)+'\n')
elif not redactions.exists():redactions.write_text('[]\n')
report=(p/'REPORT.md').read_text();first='[R557] NEGATIVE - exact head 625b001173fda5f6401af1dceaef8d8ab86f5ae9'
if report.splitlines()[0]!=first:errors.append('wrong report first line')
if report.splitlines()[-1]!='R557-4 FINISHED':errors.append('wrong report last line')
if 'SKELETON' in report:errors.append('skeleton remains')
for f in [p/'REPORT.md',p/'REPLAY.md']:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if target.startswith(('http:','https:')):continue
  if not (f.parent/target.split('#')[0]).exists():errors.append('missing report target: '+target)
for row in json.loads((p/'receipts/prior-script-provenance.json').read_text()):
 if hashlib.sha256((p/row['path']).read_bytes()).hexdigest()!=row['sha256']:errors.append('unchanged script changed: '+row['path'])
audit={'errors':errors,'redacted_files':len(json.loads(redactions.read_text())),'report_first_line':report.splitlines()[0],'report_last_line':report.splitlines()[-1]};(p/'receipts/packet-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
if errors:print(json.dumps(audit,indent=2));raise SystemExit(1)
files=[f for f in sorted(p.rglob('*')) if f.is_file() and 'scratch' not in f.relative_to(p).parts and f.name!='MANIFEST.sha256']
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
print(json.dumps({'publishable_files':len(files),'bytes':sum(f.stat().st_size for f in files),**audit}))
