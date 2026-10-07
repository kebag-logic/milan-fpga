#!/usr/bin/env python3
import argparse,sys,os,re,json
from pathlib import Path
from unittest.mock import patch
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve();s=p/'scratch/selector';s.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(r/'sw/firmware/gtest'));import fw_rv32
line=next(l for l in (r/'sw/firmware/ctrl/maap/README.md').read_text().splitlines() if '--require-rv32 --self-test' in l)
var=line.split('=',1)[0];assert var=='MILAN_RV32_CC'
requested=s/'requested-gcc';default=s/'competing-gcc'
for f in [requested,default]:f.write_text('#!/bin/sh\nexit 0\n');f.chmod(0o755)
results=[]
for candidates in [(),(str(default),)]:
 with patch.object(fw_rv32,'CANDIDATES',candidates),patch.dict(os.environ,{var:str(requested)}):
  chosen=fw_rv32.compiler();assert chosen==str(requested);results.append({'defaults':len(candidates),'requested_wins':True})
print(json.dumps({'documented_variable':var,'cases':results},indent=2))
