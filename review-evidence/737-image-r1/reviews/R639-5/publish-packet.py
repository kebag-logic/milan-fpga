import pathlib,sys,hashlib,json,re,shutil
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve()
excluded={'MANIFEST.sha256','publication-redactions.json','public-737-authority.json','public-738-authority.json','prior-public-findings.json','public-evidence-index.json','reference-extraction.json','fetch-public.py','verify-public-gates.py','round5-public-index.json'}
files=[f for f in p.iterdir() if f.is_file() and f.name not in excluded]+list((p/'public').iterdir())+list((p/'gate-logs').iterdir())
changes=[]
for f in sorted(files):
 b=f.read_bytes();s=b.decode();updated=s
 if f.suffix!='.py':
  updated=updated.replace(str(root),'${CHECKOUT}').replace(str(p),'${PACKET}')
 if f.relative_to(p).as_posix()=='public/builder-home-background.receipt.json':
  record=json.loads(updated);argv=record['command'];argv[argv.index('-u')+1]='executor';updated=json.dumps(record,indent=2)+'\n'
 if updated!=s:
  backup=p/'scratch/publication-originals'/f.relative_to(p);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
  f.write_text(updated);changes.append({'file':str(f.relative_to(p)),'original_sha256':hashlib.sha256(b).hexdigest(),'published_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'change':'local path or account role label only'})
(p/'publication-redactions.json').write_text(json.dumps(changes,indent=2)+'\n');files.append(p/'publication-redactions.json')
lines=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix() for f in sorted(set(files))]
(p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n');print('published files',len(lines),'path/role redactions',len(changes))
