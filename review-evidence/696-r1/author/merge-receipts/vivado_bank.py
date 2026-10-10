"""One exclusive-lock job: parser, shipping route, routed-checkpoint queries, both standalone endpoints.

Runs under `flock $VIVADO_LOCK` (exclusive) at the merged lane head.
Gate comparisons are recorded, not fatal, so every endpoint is measured.
"""
import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
main=Path('<lane>')
repo=Path('<validation-tree>')
shipping=w/'shipping'
vendor='<synthesis-install>/Vivado/bin/vivado'
sys.path.insert(0,str(main/'syn/ooc'))
import pp_resource_gate
head=subprocess.check_output(['git','-C',str(main),'rev-parse','HEAD'],text=True).strip()
assert head==sys.argv[1],(head,sys.argv[1])
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==head
for root in [main,repo]:
 subprocess.run(['git','-C',str(root),'diff','--quiet'],check=True)
 subprocess.run(['git','-C',str(root),'diff','--cached','--quiet'],check=True)
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
(w/'tmp').mkdir(exist_ok=True)
def verify():
 rows=[]
 for shape in ['ax7101','ax8x8']:
  directory=shipping/shape/'gateware'
  script=(directory/'baseline_integrated.tcl').read_text()
  files,roots=pp_resource_gate.located(directory,script)
  compared=0;problems=[]
  for p in files:
   if p.is_relative_to(repo):
    relative=p.relative_to(repo);source=main/relative
    if not source.is_file() or p.read_bytes()!=source.read_bytes():problems.append(str(relative))
    compared+=1
  images=json.loads((directory/'baseline_images.json').read_text())
  for item in images:
   assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
  rows.append(dict(shape=shape,input_files=len(files),lane_file_comparisons=compared,verified_images=len(images),inputs_sha256=pp_resource_gate.inputs(directory,script),problems=problems))
  assert compared>100 and not problems,rows[-1]
 return rows
before=verify()
rows=[]
def save(after=None):
 (w/'vivado-results.json').write_text(json.dumps(dict(head=head,before=before,after=after,rows=rows),indent=2)+'\n')
save()
def run(name,args,cwd=main):
 assert shutil.disk_usage(w).free>30*1024**3
 print('START',name,time.strftime('%H:%M:%S'),flush=True);start=time.time()
 with (w/(name+'.log')).open('w') as log:
  rc=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (w/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=list(map(str,args)),cwd=str(cwd),rc=rc,seconds=round(time.time()-start,1)));save()
 print(name,rc,flush=True)
 return rc
# The parser analyses the lane tree; it is read-only with --check.
run('parser',['python3','scripts/xvlog_gate.py','--check'])
gate=shipping/'ax7101/gateware'
if run('route',[vendor,'-mode','batch','-source','baseline_integrated.tcl','-nojournal','-log','baseline.log'],gate):raise SystemExit('route failed')
run('check-route-1x1',['python3','syn/ooc/pp_resource_gate.py','check',str(gate),'--endpoint','route-1x1'])
# Read-only timing queries on the routed checkpoint, inside the same lock hold.
q=w/'route-queries';q.mkdir()
(q/'queries.tcl').write_text(f'''set_param general.maxThreads 8
open_checkpoint {{{gate}/alinx_ax7101_route.dcp}}
set maap [get_cells -hierarchical -filter {{IS_SEQUENTIAL && NAME =~ "*g_maap.maap_engine/*"}}]
puts "MAAP sequential cells: [llength $maap]"
report_timing -to $maap -max_paths 3 -nworst 1 -delay_type max -file maap_to.rpt
report_timing -from $maap -max_paths 3 -nworst 1 -delay_type max -file maap_from.rpt
report_timing -to $maap -max_paths 3 -nworst 1 -delay_type min -file maap_to_hold.rpt
report_timing -max_paths 10 -nworst 1 -delay_type max -file worst10.rpt
report_timing -max_paths 1 -nworst 1 -delay_type max -file worst_path.rpt
foreach dir {{to from}} {{
  if {{$dir eq "to"}} {{set p [get_timing_paths -to $maap -max_paths 1 -delay_type max]}} else {{set p [get_timing_paths -from $maap -max_paths 1 -delay_type max]}}
  puts "MAAP $dir worst setup slack: [get_property SLACK $p] ns, levels [get_property LOGIC_LEVELS $p], [get_property STARTPOINT_PIN $p] -> [get_property ENDPOINT_PIN $p]"
}}
set h [get_timing_paths -to $maap -max_paths 1 -delay_type min]
puts "MAAP to worst hold slack: [get_property SLACK $h] ns"
set x [get_timing_paths -max_paths 1 -delay_type max]
puts "design worst setup slack: [get_property SLACK $x] ns, levels [get_property LOGIC_LEVELS $x], [get_property STARTPOINT_PIN $x] -> [get_property ENDPOINT_PIN $x]"
quit
''')
run('route-queries',[vendor,'-mode','batch','-source','queries.tcl','-nojournal','-log','queries.log'],q)
# The recipe permits RTL elaboration as the 8x8 parameter authority.
eight=shipping/'ax8x8/gateware';rtl=shipping/'ax8x8-rtl';rtl.mkdir()
for p in eight.iterdir():
 if p.suffix in ('.xdc','.init'):shutil.copy2(p,rtl/p.name)
lines=(eight/'baseline_integrated.tcl').read_text().splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('synth_design '))
(rtl/'rtl.tcl').write_text('\n'.join(lines[:idx]+[lines[idx]+' -rtl -rtl_skip_mlo','quit'])+'\n')
if run('rtl-8x8',[vendor,'-mode','batch','-source','rtl.tcl','-nojournal','-log','baseline.log'],rtl):raise SystemExit('rtl-8x8 failed')
for shape,integrated,endpoint in [('ax7101',gate,'ooc-1x1'),('ax8x8',rtl,'ooc-8x8')]:
 out=shipping/(shape+'-ooc')
 if run(shape+'-prepare-ooc',['python3','syn/ooc/pp_baseline.py',str(shipping/shape/'gateware'),'--single-thread-synthesis','--integrated-clock','--output',str(out),'--integrated-log',str(integrated/'baseline.log')]):raise SystemExit('prepare failed')
 if run(shape+'-ooc',[vendor,'-mode','batch','-source','baseline_ooc.tcl','-nojournal','-log','baseline.log'],out):raise SystemExit('ooc failed')
 run('check-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','check',str(out),'--endpoint',endpoint])
after=verify()
save(after)
assert [r['inputs_sha256'] for r in before]==[r['inputs_sha256'] for r in after],'measurement inputs changed'
print('all endpoints measured',time.strftime('%H:%M:%S'),flush=True)
