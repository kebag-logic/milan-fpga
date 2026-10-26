#!/usr/bin/env python3
"""Preserve raw receipts under scratch, redact local paths, and hash the public packet."""
import hashlib,pathlib,re,shutil,sys
p=pathlib.Path(__file__).resolve().parent
checkout=pathlib.Path(sys.argv[1]).resolve()
raw=p/'scratch/unredacted-receipts'; raw.mkdir(parents=True,exist_ok=True)
for file in p.iterdir():
    if not file.is_file() or file.suffix not in ('.log','.json','.txt'): continue
    if not (raw/file.name).exists(): shutil.copyfile(file,raw/file.name)
    text=file.read_text()
    text=text.replace(str(checkout),'<checkout>').replace(str(p),'<packet>')
    text=re.sub(r'/home/[^/\s]+/[^\s\"\x27<>),;]*','<local-dependency>',text)
    text=re.sub(r'~/litex-milan/[^\s)\"\x27]+','<calibration-build-report>',text)
    file.write_text(text)
report=(p/'REPORT.md').read_text()
assert report.startswith('[R702] NEGATIVE - exact head 44d95625bde2c46d7070c090fc29ed0ba85ab64a\n')
assert report.endswith('R702-3 FINISHED\n')
assert 'SKELETON' not in report
assert all('| '+lens+' |' in report for lens in ['Conformance','RTL','Robustness','Tests','Docs'])
files=sorted(x for x in p.iterdir() if x.is_file() and x.name!='MANIFEST.sha256')
lines=[hashlib.sha256(x.read_bytes()).hexdigest()+'  '+x.name for x in files]
(p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print('Publishable files:',len(files))
print('Manifest paths are relative; scratch is excluded.')
