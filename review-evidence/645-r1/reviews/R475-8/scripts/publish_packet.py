#!/usr/bin/env python3
"""Normalize local paths for publication, retain raw hashes, and seal the packet."""
import argparse,hashlib,json,pathlib,re,shutil
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('packet',type=pathlib.Path);a=p.parse_args();packet=a.packet.resolve();source=a.source.resolve()
raw=packet/'scratch/raw-before-normalization';raw.mkdir(exist_ok=True)
changes=[]
for f in sorted((packet/'receipts').rglob('*')):
 if not f.is_file():continue
 data=f.read_bytes()
 try:text=data.decode()
 except UnicodeDecodeError:continue
 normalized=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[a-f0-9]+/diff/usr', '$SIM_ROOT', text)
 normalized=re.sub(r'/home/[^/\s]+', '$USER_HOME', normalized)
 normalized=normalized.replace(str(source),'$SOURCE').replace(str(packet),'$PACKET')
 if normalized!=text:
  relative=f.relative_to(packet);dest=raw/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  new=normalized.encode();f.write_bytes(new)
  changes.append({'path':str(relative),'raw_sha256':hashlib.sha256(data).hexdigest(),'published_sha256':hashlib.sha256(new).hexdigest(),'normalization':'Local source, packet and simulator installation paths replaced by placeholders; test values and verdicts unchanged'})
(packet/'receipts/path-normalization.json').write_text(json.dumps(changes,indent=2)+'\n')
files=[packet/'REPORT.md']+sorted(f for folder in ['scripts','receipts'] for f in (packet/folder).rglob('*') if f.is_file())
for f in files:
 text=f.read_text()
 assert not re.search(r'/home/[A-Za-z0-9_.-]+/',text), f
 if f.name=='REPORT.md': assert 'SKELETON' not in text, f
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(packet))+'\n' for f in files)
(packet/'MANIFEST.sha256').write_text(manifest)
print(f'MANIFEST: {len(files)} files; {len(changes)} receipts normalized; scratch excluded')
