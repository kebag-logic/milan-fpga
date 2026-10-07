#!/usr/bin/env python3
import argparse,sys,subprocess,types,dataclasses,json,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve();sys.path.insert(0,str(r/'sw/firmware/ctrl/test'))
def catalog(ref,name):
 code=subprocess.check_output(['git','show',ref+':sw/firmware/ctrl/test/ctrl_mutants.py'],cwd=r,text=True)
 mod=types.ModuleType(name);mod.__file__=str(r/'sw/firmware/ctrl/test/ctrl_mutants.py');sys.modules[name]=mod;exec(compile(code,mod.__file__,'exec'),mod.__dict__)
 return {m.name:dataclasses.asdict(m) for m in mod.MUTANTS}
old=catalog('8b78a8fd','old_catalog');dev=catalog('d51b373a','dev_catalog');head=catalog('HEAD','head_catalog');union=old|dev
assert head==union
assert subprocess.run(['git','diff','--quiet','8b78a8fd','HEAD','--','sw/firmware/ctrl/test/maap_mutants.py'],cwd=r).returncode==0
parts=[list(head)[i::4] for i in range(4)];assert len(set(sum(parts,[])))==len(head)==sum(map(len,parts))
print(json.dumps({'round3':len(old),'dev':len(dev),'head':len(head),'unchanged_union':head==union,'maap':sum(n.startswith('maap-') for n in head),'partition_sizes':list(map(len,parts))},indent=2))
(p/'receipts/catalog.json').write_text(json.dumps({'old':old,'dev':dev,'head':head,'partitions':parts},indent=2)+'\n')
