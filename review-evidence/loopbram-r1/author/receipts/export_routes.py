import sys,subprocess,os,json
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH')
sys.path.insert(0,str(root/'sw/builder'));import endstation_builder as b
for name in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']:
 cfg=b.load_config(w/(name+'.yaml'));args=b.emit_soc_argv(cfg)
 args[args.index('--ctrl-firmware')+1]=str(w/'builds'/(name+'-on')/'ctrl_app.elf')
 out=w/'route'/name;out.mkdir(parents=True,exist_ok=True)
 args+=['--entity-gen-dir',str(root/'sw/builder/out/a826_measure'/name),'--output-dir',str(out),'--no-compile-software',
 '--synth-directive','AreaOptimized_high','--opt-directive','ExploreArea','--place-directive','ExtraPostPlacementOpt','--vivado-max-threads','16']
 cmd=[sys.executable,str(w/'measure_soc.py'),*args]
 (out/'export-command.json').write_text(json.dumps(cmd,indent=2))
 with (out/'export.log').open('w') as log:r=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
 print(name,'EXPORT',r.returncode,flush=True)
 if r.returncode:print((out/'export.log').read_text()[-3500:]);sys.exit(r.returncode)
