import hashlib,json,pathlib
out=pathlib.Path(__file__).resolve().parent.parent
files=sorted(p for p in out.rglob('*') if p.is_file() and p.relative_to(out).as_posix() not in ('SHA256SUMS','seal.json'))
entries=[(hashlib.sha256(p.read_bytes()).hexdigest(),p.relative_to(out).as_posix()) for p in files]
manifest=''.join(f'{h}  {p}\n' for h,p in entries)
(out/'SHA256SUMS').write_text(manifest)
for h,p in entries:assert hashlib.sha256((out/p).read_bytes()).hexdigest()==h,p
summary={'files':len(entries),'sha256sums_sha256':hashlib.sha256(manifest.encode()).hexdigest(),'verified':True,'report_first_line':(out/'REPORT.md').read_text().splitlines()[0],'report_last_line':(out/'REPORT.md').read_text().splitlines()[-1]}
(out/'seal.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
