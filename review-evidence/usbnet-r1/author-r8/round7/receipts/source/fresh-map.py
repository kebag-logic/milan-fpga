import hashlib,json,subprocess,time
from pathlib import Path
scratch=Path('$VALIDATION_STORAGE/usbnet-a855/round7')
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
root=Path('$LANES/usbnet-1011')
old=json.loads(Path('$VALIDATION_STORAGE/usbnet-a855/round5/route/gen-final.command.json').read_text())
assert '--build' not in old
commands=[];results=[]
def run(label,cmd,cwd):
 log=packet/(label+'.log')
 with log.open('w') as f:r=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
 commands.append(dict(label=label,command=cmd,cwd=str(cwd),rc=r.returncode,log=log.name))
 (packet/'fresh-map-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 print(label,r.returncode,flush=True);assert r.returncode==0
for tag in ('candidate','baseline'):
 tree=root if tag=='candidate' else scratch/'baseline'
 out=scratch/'fresh-map'/tag
 run('fresh-map-'+tag+'-entity',['nice','-n','19','$WORKSPACE_HOME/litex-milan/venv/bin/python3','-B','sw/builder/endstation_builder.py','configs/endstation_arty_split.yaml'],tree)
 cmd=[v.replace(str(root),str(tree)) for v in old]
 cmd[cmd.index('--output-dir')+1]=str(out)
 cmd[cmd.index('--ctrl-firmware')+1]=str(scratch/'product'/tag/'arty/ctrl_app.elf')
 if tag=='baseline':cmd.remove('--usb-net')
 run('fresh-map-'+tag+'-soc',cmd,tree)
 mapped=out/'mapped'
 run('fresh-map-'+tag+'-flash',['nice','-n','19','$WORKSPACE_HOME/litex-milan/venv/bin/python3','-B','sw/firmware/ctrl_nvm/plat/gen_flash_port.py','--csr-csv',str(out/'csr.csv'),'--csr-h',str(out/'software/include/generated/csr.h'),'--out',str(mapped)],tree)
 prior=scratch/'product'/tag/'arty/flash-map'
 entries=[]
 for f in sorted(prior.rglob('*')):
  if not f.is_file() or f.suffix not in ('.h','.ld'):continue
  other=mapped/f.relative_to(prior)
  assert other.read_bytes()==f.read_bytes(),(f,other)
  entries.append(dict(file=str(f.relative_to(prior)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),identical=True))
 assert entries
 results.append(dict(tree=tag,head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=tree,text=True).strip(),generated_headers=entries,csr_csv_sha256=hashlib.sha256((out/'csr.csv').read_bytes()).hexdigest()))
 (packet/'fresh-map-identity.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS current generated flash-map headers reproduce the firmware build inputs')
