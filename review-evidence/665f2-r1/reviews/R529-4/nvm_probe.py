#!/usr/bin/env python3
"""Exact-sized erased-record probes using the merged sanitizer recipe."""
import argparse,sys,shutil,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve();s=p/'scratch/nvm-probe';s.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(r/'sw/firmware/ctrl_nvm/test'));import test_ctrl_nvm as gate,nvm_bench as bench,fw_gtest
shape=gate.prepare(r/'configs/endstation_ax7101_1x1_tdm8.yaml',s/'shape');binary=next(b for b in bench.UNITS if b.name=='prefix');build=fw_gtest.Build(jobs=1);rows=[]
seam='pos + NVM_REC_HDR + r.plen > loaded'
for name,repl in [('positive',None),('wrong-total-bound','pos + NVM_REC_HDR + r.plen > end'),('eight-byte-overread','pos + NVM_REC_HDR + r.plen > loaded + 8u'),('reject-exact-end','pos + NVM_REC_HDR + r.plen >= loaded')]:
 tree=s/name/'tree';shutil.copytree(bench.TREE,tree,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
 if repl:
  f=tree/'nvm_klj2.c';text=f.read_text();assert text.count(seam)==1;f.write_text(text.replace(seam,repl))
 exe=bench.build_suite(shape.inputs,s/name/'build',build,binary,tree);ok,log=bench.run_suite(exe,shape.fixture)
 (p/'receipts'/f'nvm-probe-{name}.log').write_text(log)
 caught=ok if repl is None else not ok and 'codec_erased_loaded_prefix' in log and ('AddressSanitizer' in log or '[FAIL]' in log)
 rows.append(dict(name=name,caught=caught,positive_ok=ok));print(rows[-1],flush=True)
(p/'receipts/nvm-probes.json').write_text(json.dumps(rows,indent=2)+'\n');assert all(x['caught'] for x in rows)
