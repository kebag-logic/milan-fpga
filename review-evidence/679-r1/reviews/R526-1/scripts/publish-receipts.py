#!/usr/bin/env python3
"""Publish path-scrubbed raw output, retaining original and public hashes."""
import hashlib,json,pathlib,re,sys
packet=pathlib.Path(__file__).resolve().parents[1];repo=pathlib.Path(sys.argv[1]).resolve()
items=[*sorted((packet/'scratch/raw').glob('*')),(packet/'scratch/sdk-install.raw')]
records=[]
for src in items:
 if not src.is_file():continue
 data=src.read_bytes();s=data.decode(errors='strict')
 s=s.replace(str(packet),'<packet>').replace(str(repo),'<checkout>')
 s=re.sub(r'/home/[^/\s]+','<home>',s)
 s=re.sub(r'\x1b\[[0-9;]*m','',s)
 dest=packet/'receipts'/('sdk-install.log' if src.name=='sdk-install.raw' else src.name)
 dest.write_text(s)
 records.append({'file':dest.relative_to(packet).as_posix(),'original_sha256':hashlib.sha256(data).hexdigest(),'published_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'path_or_ansi_scrubbed':data!=dest.read_bytes()})
(packet/'receipts/scrub-receipt.json').write_text(json.dumps(records,indent=2)+'\n')
print('Published',len(records),'receipts; paths and terminal color only normalized')
