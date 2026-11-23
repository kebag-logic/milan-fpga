import sys,subprocess,json,hashlib
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH')
sys.path.insert(0,str(root/'sw/builder'));import endstation_builder as b
from test_input_loopback import image
records=[]
for name in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']:
 art=b._derive_artifacts(root/'configs'/(name+'.yaml'));out,_=b._write_artifact_dir(art,w/'off-final');(out/'sweep_opts.sh').write_text(art.sweep)
 rows=[]
 for before in sorted((w/'baseline'/name).iterdir()):
  if before.is_file():
   after=out/before.name
   if before.read_bytes()!=after.read_bytes():raise RuntimeError('artifact mismatch '+str(before))
   rows.append({'file':before.name,'sha256':hashlib.sha256(after.read_bytes()).hexdigest()})
 blob=image(art.overlay);(out/'aem_desc.bin').write_bytes(blob)
 inputs=json.loads((w/'builds'/(name+'-off')/'inputs.json').read_text());cmd=inputs['args'];cmd[0]=sys.executable;cmd[2]=str(w/'baseline_firmware.py');cmd[cmd.index('--output')+1]=str(w/'builds'/(name+'-baseline'))
 with (w/'builds'/(name+'-baseline.log')).open('w') as log:r=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
 if r.returncode:raise RuntimeError('baseline link refused '+name)
 sys.path.insert(0,str(root/'sw/litex'));import ctrl_memory as m
 a=m.read_elf(w/'builds'/(name+'-baseline')/'ctrl_app.elf');z=m.read_elf(w/'builds'/(name+'-off')/'ctrl_app.elf')
 before_words=m.rom_words(a);after_words=m.rom_words(z)
 if before_words!=after_words:raise RuntimeError('firmware ROM mismatch '+name)
 rom=b''.join(n.to_bytes(4,'little') for n in after_words)
 records.append({'shape':name,'artifacts':rows,'aemi_sha256':hashlib.sha256(blob).hexdigest(),'firmware_rom_bytes':len(rom),'firmware_rom_sha256':hashlib.sha256(rom).hexdigest(),'firmware_identity':'PASS','baseline_link_command':cmd})
 print(name,'OFF IDENTITY PASS',len(rows),'artifacts, firmware ROM',len(rom),flush=True)
(w/'identity.json').write_text(json.dumps(records,indent=2)+'\n')
