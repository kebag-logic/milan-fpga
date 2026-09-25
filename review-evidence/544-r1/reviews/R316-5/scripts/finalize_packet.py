#!/usr/bin/env python3
"""Publishable receipt copies: redact workspace prefixes and hash selected files."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--sdk',type=Path,required=True);p.add_argument('--entry-bin',type=Path,required=True);a=p.parse_args()
replacements=[(str(a.packet),'$PACKET'),(str(a.root),'$CANDIDATE'),(str(a.sdk),'$SDK'),(str(a.entry_bin),'$PINNED_BIN'),(str(Path.home()),'$WORKSPACE_HOME')]
# The first four specific locations are replaced before their parent prefixes.
replacements.append((str(a.root.parents[1]),'$DATA_ROOT'))
receipts=a.packet/'receipts';receipts.mkdir(exist_ok=True)
redacted=[]
for source in sorted((a.packet/'scratch/raw').glob('*')):
 if not source.is_file():continue
 data=source.read_text();original=data
 for prefix,replacement in replacements:data=data.replace(prefix,replacement)
 (receipts/source.name).write_text(data)
 if data!=original:redacted.append(source.name)
(receipts/'redaction.json').write_text(json.dumps(dict(policy='Only local absolute path prefixes replaced; no verdict, reason, return code or digest edited.',placeholders=[v for _,v in replacements],files=redacted),indent=2)+'\n')
# Every copied Git evidence input remains byte-identical. Issue snapshots have URLs.
ref='4c97887dc83f46703b8d767dec671afcb9ebe206';inputs=[]
for f in sorted((a.packet/'public-inputs').rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(a.packet/'public-inputs').as_posix();b=f.read_bytes()
 if rel.startswith(('author-r3/','reviews/')):
  obj=ref+':review-evidence/544-r1/'+rel
  assert b==subprocess.check_output(['git','-C',str(a.root),'show',obj]),rel
  source='https://github.com/kebag-logic/milan-fpga/blob/'+ref+'/review-evidence/544-r1/'+rel
 else:
  number=rel.split('-')[1].split('.')[0];source='https://github.com/kebag-logic/milan-fpga/issues/'+number
  if '-comment-' in rel:source+='#issuecomment-'+rel.split('-comment-')[1].split('.')[0]
 inputs.append(dict(path='public-inputs/'+rel,source=source,sha256=hashlib.sha256(b).hexdigest()))
(receipts/'public-input-integrity.json').write_text(json.dumps(inputs,indent=2)+'\n')
files=[]
for folder in ('scripts','receipts','public-inputs'):
 files.extend(f for f in (a.packet/folder).rglob('*') if f.is_file())
files.append(a.packet/'source.diff')
(a.packet/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(a.packet).as_posix()+'\n' for f in sorted(files)))
print('Manifest files:',len(files));print('Raw receipt copies:',len(list(receipts.glob('*'))))
