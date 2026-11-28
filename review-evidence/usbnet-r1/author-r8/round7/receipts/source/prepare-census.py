import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path('$LANES/usbnet-1011')
OUT=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
OLD=Path('$VALIDATION_STORAGE/artysplit-a829/r10/final-census')
PRIOR=Path('$LANES/arty-int-1127')
PACKET=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
sys.path.insert(0,str(ROOT/'tb/verilator/usbnet'))
import egress_census
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import build
OUT.mkdir(exist_ok=True)
rows=[]
for variant in ('none','answering-ports','answering-every-port','valid-destinations','declaring-outputs','answering-later','talker-notices','shutdown-entry'):
 old=OLD/variant; new=OUT/variant
 assert not new.exists()
 spec=json.loads((old/'build.json').read_text())
 # All inherited input digests are checked before copying or replacing anything.
 for key,want in spec['inputs'].items():
  if key=='tree:firmware': got=build.tree_digest([ROOT/t for t in build.FIRMWARE_TREES])
  elif key=='tree:config': got=build.tree_digest([ROOT/'configs'/(spec['shape']+'.yaml')])
  else: got=hashlib.sha256(build.resolve(key,old).read_bytes()).hexdigest()
  assert got==want,(variant,key,got,want)
 assert hashlib.sha256((old/'native/Vsim').read_bytes()).hexdigest()==spec['executable_sha256']
 assert shutil.disk_usage('/data').free>19_000_000_000
 shutil.copytree(old,new,ignore=shutil.ignore_patterns('results','__pycache__'))
 raw=json.dumps(spec).replace(str(old),str(new)).replace(str(PRIOR),str(ROOT))
 spec=json.loads(raw)
 main,queue=egress_census.sources(new)
 mk=new/'native/Vsim.mk'
 text=mk.read_text().replace(str(old),str(new)).replace(str(PRIOR),str(ROOT))
 text=text.replace(str(ROOT/'tb/verilator/ctrl_service_budget/sim_main.cpp'),str(main))
 mk.write_text(text)
 # Copied model objects are unchanged. Rebuild only the new queue/main and relink.
 with (PACKET/('census-build-'+variant+'.log')).open('w') as log:
  result=subprocess.run(['make','-j4','-C',str(new/'native'),'-f','Vsim.mk','Vsim','OPT_FAST=-O3','OBJCACHE=ccache'],stdout=log,stderr=subprocess.STDOUT)
 assert result.returncode==0,variant
 spec['inputs']=build.digest(build.run_inputs(new,spec)+[main,queue,ROOT/'tb/verilator/usbnet/egress_census.py',ROOT/'tb/verilator/usbnet/egress_usb.py'],new)
 spec['inputs']['tree:firmware']=build.tree_digest([ROOT/t for t in build.FIRMWARE_TREES])
 spec['inputs']['tree:config']=build.tree_digest([ROOT/'configs'/(spec['shape']+'.yaml')])
 spec['executable_sha256']=hashlib.sha256((new/'native/Vsim').read_bytes()).hexdigest()
 spec['usbnet_injection_ps']=egress_census.INJECT_PS
 spec['usbnet_handshake_ps']=egress_census.HANDSHAKE_PS
 (new/'build.json').write_text(json.dumps(spec,indent=2)+'\n')
 build.reused(new)
 rows.append(dict(variant=variant,old_executable_sha256=json.loads((old/'build.json').read_text())['executable_sha256'],executable_sha256=spec['executable_sha256'],firmware_sha256=hashlib.sha256(Path(spec['elf']).read_bytes()).hexdigest(),inherited_inputs_verified=True))
 (PACKET/'census-build-identity.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('BUILT',variant,flush=True)
