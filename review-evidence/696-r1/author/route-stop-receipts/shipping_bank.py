import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
main=Path('$LANES/696-maap-annexb')
repo=Path('$VALIDATION_STORAGE/696-a570/resume-area/validation')
shipping=Path('$VALIDATION_STORAGE/696-a570/resume-differential/shipping')
vendor='$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin/vivado'
sys.path.insert(0,str(main/'syn/ooc'))
import pp_resource_gate
head=subprocess.check_output(['git','-C',str(main),'rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==head
for root in [main,repo]:
 subprocess.run(['git','-C',str(root),'diff','--quiet'],check=True)
 subprocess.run(['git','-C',str(root),'diff','--cached','--quiet'],check=True)
env=dict(os.environ,TMPDIR=str(shipping),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
def snapshot():
 result={}
 for shape in ['ax7101','ax8x8']:
  directory=shipping/shape/'gateware'
  script=(directory/'baseline_integrated.tcl').read_text()
  for item in json.loads((directory/'baseline_images.json').read_text()):
   assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
  result[shape]=pp_resource_gate.inputs(directory,script)
 return result
before=snapshot()
rows=[]
def save():
 (w/'shipping-results.json').write_text(json.dumps(dict(head=head,before=before,rows=rows),indent=2)+'\n')
def run(name,args,cwd=main,fatal=True):
 assert shutil.disk_usage(shipping).free>30*1024**3
 print('START',name,flush=True);start=time.time()
 with (w/(name+'.log')).open('w') as log:
  rc=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (w/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=list(map(str,args)),cwd=str(cwd),rc=rc,seconds=round(time.time()-start,1)));save()
 print(name,rc,flush=True)
 if rc and fatal:raise SystemExit(rc)
 return rc
gate=shipping/'ax7101/gateware'
run('route',[vendor,'-mode','batch','-source','baseline_integrated.tcl','-nojournal','-log','baseline.log'],gate)
# Comparison against the current record; exit 1 is recorded, not fatal, so all three endpoints are measured.
run('check-before-route-1x1',['python3','syn/ooc/pp_resource_gate.py','check',str(gate),'--endpoint','route-1x1'],fatal=False)
# The recipe permits RTL elaboration as the 8x8 parameter authority.
eight=shipping/'ax8x8/gateware';rtl=shipping/'ax8x8-rtl';rtl.mkdir()
for p in eight.iterdir():
 if p.suffix in ('.xdc','.init'):shutil.copy2(p,rtl/p.name)
lines=(eight/'baseline_integrated.tcl').read_text().splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('synth_design '))
(rtl/'rtl.tcl').write_text('\n'.join(lines[:idx]+[lines[idx]+' -rtl -rtl_skip_mlo','quit'])+'\n')
run('rtl-8x8',[vendor,'-mode','batch','-source','rtl.tcl','-nojournal','-log','baseline.log'],rtl)
for shape,integrated,endpoint in [('ax7101',gate,'ooc-1x1'),('ax8x8',rtl,'ooc-8x8')]:
 out=shipping/(shape+'-ooc')
 run(shape+'-prepare-ooc',['python3','syn/ooc/pp_baseline.py',str(shipping/shape/'gateware'),'--single-thread-synthesis','--integrated-clock','--output',str(out),'--integrated-log',str(integrated/'baseline.log')])
 run(shape+'-ooc',[vendor,'-mode','batch','-source','baseline_ooc.tcl','-nojournal','-log','baseline.log'],out)
 run('check-before-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','check',str(out),'--endpoint',endpoint],fatal=False)
after=snapshot()
(w/'shipping-results.json').write_text(json.dumps(dict(head=head,before=before,after=after,rows=rows),indent=2)+'\n')
assert before==after,'measurement inputs changed'
print('all three endpoints measured',flush=True)
