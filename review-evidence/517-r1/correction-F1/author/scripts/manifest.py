from pathlib import Path
import hashlib,json,os,stat,sys
root=Path(sys.argv[1]).resolve();rows=[];sums=[]
for path in sorted(root.rglob('*')):
 relative=str(path.relative_to(root))
 if relative in ('MANIFEST.json','SHA256SUMS') or path.is_dir():continue
 info=path.lstat();kind='regular' if stat.S_ISREG(info.st_mode) else 'symlink' if stat.S_ISLNK(info.st_mode) else 'fifo' if stat.S_ISFIFO(info.st_mode) else 'special'
 row={'path':relative,'kind':kind,'mode':oct(stat.S_IMODE(info.st_mode)),'size':info.st_size}
 if kind=='regular':
  digest=hashlib.sha256(path.read_bytes()).hexdigest();row['sha256']=digest;sums.append(digest+'  '+relative)
 elif kind=='symlink':row['target']=os.readlink(path)
 rows.append(row)
(root/'MANIFEST.json').write_text(json.dumps({'source':json.loads((root/'candidate.json').read_text()),'exclusions':['MANIFEST.json','SHA256SUMS'],'entries':rows},indent=2)+'\n')
(root/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
print(json.dumps({'entries':len(rows),'regular_files':len(sums),'regular_bytes':sum(r['size'] for r in rows if r['kind']=='regular'),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()}))
