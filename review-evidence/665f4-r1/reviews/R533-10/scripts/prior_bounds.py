#!/usr/bin/env python3
import sys,shutil,json,argparse
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--interfaces',type=int,required=True);ap.add_argument('--source',type=Path,default=Path.cwd());ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args();r=a.source.resolve();p=a.packet.resolve()
sys.path[:0]=[str(r/'sw/firmware/ctrl/test'),str(p/'scripts/prior')]
import ctrl_build,srp_arms,fw_gtest,probe_mutants
plants=[tuple(line.split('\t')) for line in (p/'scripts/prior/bound_probes.tsv').read_text().splitlines()]
plants += [(name,*probe_mutants.PLANTS[name]) for name in ('code-poll-extra-read','code-send-extra-read')]
out=p/'scratch'/f'prior-bounds-if{a.interfaces}';src=out/'ctrl';build=fw_gtest.Build(jobs=a.jobs);results=[]
for name,path,old,new in [('control-none','srp/srp_bounds.h','',''),*plants]:
 shutil.copytree(ctrl_build.CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 target=src/path;original=target.read_text()
 if old:
  assert original.count(old)==1
  target.write_text(original.replace(old,new))
 result=srp_arms.arm_srp(ctrl_build.Tree(src,out/'build',out/'reuse',build),r/'third_party/lwSRP',a.interfaces,test='srp_app.cpp')
 (p/'receipts'/f'{name}-if{a.interfaces}.log').write_text(result.log)
 failures=[l for l in result.log.splitlines() if '[FAIL]' in l]
 equivalent=name=='rv-poll-per-if' and a.interfaces==1
 ok=(result.rc==0) if name=='control-none' or equivalent else (result.rc==1 and bool(failures))
 results.append({'plant':name,'interfaces':a.interfaces,'suite_rc':result.rc,'equivalent':equivalent,'ok':ok,'failed_checks':failures})
 print(json.dumps(results[-1]),flush=True)
(p/'receipts'/f'prior-bounds-if{a.interfaces}.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(not all(x['ok'] for x in results)))
