"""MAAP ceiling instrument (syn/ooc/milan_datapath_ooc.tcl, one synthesis/general thread) at dev and at the merged head.

Runs under the exclusive Vivado lock. The ceiling is +60 LUT / +60 FF at g_maap.maap_engine over the
6aa25dec base of 439 LUT / 280 FF measured with this same instrument (ruling 6079087547).
"""
import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
vendor='<synthesis-install>/Vivado/bin/vivado'
trees=[('dev',Path('<workspace>/tmp/696-a570/base'),'8b61b70902f3ebf118e56967277e2686731081bd'),
       ('merged',w/'docs','0df486370990fddf9b60096be2f2371150692a10')]
files=['hdl/ieee1722/maap/KL_maap.sv','hdl/milan/milan_datapath.sv','syn/ooc/milan_datapath_ooc.tcl']
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1')
rows=[]
for label,tree,commit in trees:
 assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==commit
 subprocess.run(['git','-C',str(tree),'diff','--quiet'],check=True)
 assert shutil.disk_usage(w).free>30*1024**3
 o=w/('maap-ooc-'+label);o.mkdir()
 inputs={p:hashlib.sha256((tree/p).read_bytes()).hexdigest() for p in files}
 (o/'run.tcl').write_text(f'set_param general.maxThreads 1\nset_param synth.maxThreads 1\nsource {{{tree}/syn/ooc/milan_datapath_ooc.tcl}}\nquit\n')
 print('START',label,time.strftime('%H:%M:%S'),flush=True);start=time.time()
 with (o/'launcher.log').open('w') as f:
  rc=subprocess.run([vendor,'-mode','batch','-source','run.tcl','-nojournal','-log','baseline.log'],cwd=o,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (o/'run.rc').write_text(str(rc)+'\n')
 row=dict(label=label,commit=commit,inputs=inputs,rc=rc,seconds=round(time.time()-start,1))
 if rc==0:
  lines=(o/'util_hier_base.rpt').read_text().splitlines()
  head=next([c.strip() for c in l.split('|')][1:-1] for l in lines if 'Instance' in l and 'Total LUTs' in l)
  r=next(r for r in ([c.strip() for c in l.split('|')][1:-1] for l in lines if 'maap_engine' in l) if r[0]=='g_maap.maap_engine')
  lut,ff=int(r[head.index('Total LUTs')]),int(r[head.index('FFs')])
  diag=sum(l.count('Synth 8-4445') for l in (o/'baseline.log').read_text(errors='replace').splitlines() if not l.startswith(('set_msg_config','#')))
  row.update(lut=lut,ff=ff,delta_lut=lut-439,delta_ff=ff-280,within_ceiling=lut<=499 and ff<=340,synth_8_4445_lines=diag)
  assert inputs=={p:hashlib.sha256((tree/p).read_bytes()).hexdigest() for p in files}
 rows.append(row);(w/'maap-ooc-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(row,flush=True)
 if rc:raise SystemExit(rc)
