#!/usr/bin/env python3
"""Collect runtime receipts without publishing generated builds or host compiler paths."""
import argparse,hashlib,json,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);a=p.parse_args();root=a.packet.resolve();receipts=root/'receipts';sources=[]
for name in ['default','protocol','transport','render24','render32']:
 log=receipts/(name+'.log');data=log.read_bytes();sources.append({'name':name+'.log','raw_sha256':hashlib.sha256(data).hexdigest(),'raw_bytes':len(data)})
 lines=data.decode().splitlines()
 if name in ['default','render24','render32']:
  keep=[l for l in lines if l.startswith(('PASS ','== ','RESULT:','  [ ok ]','  [FAIL]','  dbg:'))]
 else: keep=[l for l in lines if l.startswith('{')]
 (receipts/(name+'-runtime.txt')).write_text('\n'.join(keep)+'\n')
for name in ['protocol','transport']:
 source=root/'scratch'/name;dest=receipts/(name+'-raw');dest.mkdir(exist_ok=True)
 shutil.copyfile(source/'results.json',dest/'results.json')
 for case in sorted(source.iterdir()):
  if not case.is_dir():continue
  log=case/'run.log'
  if log.exists():shutil.copyfile(log,dest/(case.name+'.log'))
(receipts/'runtime-provenance.json').write_text(json.dumps({'combined_build_logs':sources,'runtime_excerpts':'Exact selected stdout lines; compile lines omitted because they contain host installation paths. Campaign per-case run logs are copied byte-for-byte.'},indent=2)+'\n')
