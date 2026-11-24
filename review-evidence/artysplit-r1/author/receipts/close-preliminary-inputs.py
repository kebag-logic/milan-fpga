"""Attest measured inputs; for historical firmware trees, require a byte-identical rebuild.

Does not modify old build.json or grant build.reused permission. This is explicit
calibration provenance; final qualification builds from the installed row afresh.
"""
import datetime,hashlib,json,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
tree=build.tree_digest([root/t for t in build.FIRMWARE_TREES])
records=[]
for name in ['arm-a','arm-b','arm-a-full','arm-every','arm-fast','arm-valid','arm-declaring','arm-later','arm-two']:
 folder=r/name;spec=json.loads((folder/'build.json').read_text())
 try:
  build.reused(folder)
  row=dict(arm=name,status='PASS: original build.reused',firmware_tree=tree)
 except RuntimeError as exc:
  assert str(exc)=='reused build is stale: tree:firmware changed',str(exc)
  assert not build.cpu_clock_refusals(spec)
  verified=[];config_change=None
  for key,want in spec['inputs'].items():
   if key=='tree:firmware':continue
   got=build.tree_digest([root/'configs'/(spec['shape']+'.yaml')]) if key=='tree:config' else sha(build.resolve(key,folder))
   if got!=want and key=='tree:config':
    config=root/'configs'/(spec['shape']+'.yaml')
    old=config.read_bytes().replace(b'# #878: exact 800 MHz VCO / 10; split has no DDR3',b'# 83.333e6: the DDR3-666 window')
    old_digest=hashlib.sha256(str(config.relative_to(root)).encode()+b'\0'+hashlib.sha256(old).digest()).hexdigest()
    assert old_digest==want,(name,key,want,got)
    config_change=dict(old_digest=want,current_digest=got,change='Comment only; exact 80000000 Hz value unchanged')
   else:assert got==want,(name,key,want,got)
   verified.append(key)
  assert {build.input_key(p,folder) for p in build.run_inputs(folder,spec)}<=set(spec['inputs'])
  assert sha(folder/'native/Vsim')==spec['executable_sha256']
  out=r/'preliminary-relink'/name
  assert not out.exists(),out
  elf=build.firmware(out,spec['shape'],spec['interfaces'],spec['mutation'],spec['variant'],Path(spec['flash_map']))
  prior=sha(Path(spec['elf']));current=sha(elf)
  assert prior==current,(name,'relinked ELF differs',prior,current)
  row=dict(arm=name,status='PASS: historical source tree, byte-identical current-source ELF',
           original_reuse_refusal=str(exc),historical_firmware_tree=spec['inputs']['tree:firmware'],
           current_firmware_tree=tree,original_elf=spec['elf'],rebuilt_elf=str(elf),elf_sha256=prior,
           checked_input_keys=verified,config_comment_change=config_change)
 row['executable_sha256']=spec['executable_sha256'];records.append(row)
 (r/'preliminary-input-closure-progress.json').write_text(json.dumps(records,indent=2)+'\n')
 print(name,row['status'],flush=True)
assert tree==build.tree_digest([root/t for t in build.FIRMWARE_TREES])
(r/'preliminary-input-closure.json').write_text(json.dumps(dict(status='PASS',kind='Calibration provenance; no old build record changed',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),arms=records),indent=2)+'\n')
