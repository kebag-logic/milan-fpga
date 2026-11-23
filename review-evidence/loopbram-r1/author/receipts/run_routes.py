import os,sys,subprocess,json,time,concurrent.futures
from pathlib import Path
w=Path('$SCRATCH/route')
slot='<home-path>/milan-fpga-management/2026-09-23/vivado-slot.sh'
vivado='<home-path>/Xilinx2/2026.1/Vivado/bin/vivado'
env=dict(os.environ,VIVADO_SLOTS='2',VIVADO_MIN_GB='20')

def run(cwd,tcl):
 cmd=[slot,vivado,'-mode','batch','-nojournal','-nolog','-source',str(tcl)]
 log=tcl.with_suffix('.log');start=time.time()
 with log.open('w') as stream:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=14400)
 result={'command':cmd,'cwd':str(cwd),'exit':r.returncode,'seconds':time.time()-start}
 tcl.with_suffix('.json').write_text(json.dumps(result,indent=2));print(tcl,'EXIT',r.returncode,flush=True)
 return r.returncode

def point(name):
 gate=w/name/'gateware';original=(gate/'alinx_ax7101.tcl').read_text()
 pre,post=original.split('# Add pre-placement commands',1)
 synth=gate/'measure_synth.tcl';synth.write_text(pre+'\nwrite_checkpoint -force measure_opt.dcp\nquit\n')
 if run(gate,synth):return False
 for directive in ['ExtraPostPlacementOpt','AltSpreadLogic_high','ExtraTimingOpt']:
  directory=gate/directive;directory.mkdir(exist_ok=True)
  rest=post.split('# Bitstream generation')[0].replace('place_design -directive ExtraPostPlacementOpt','place_design -directive '+directive)
  # Final resource count, after routing and physical optimization.
  rest+='\nreport_utilization -hierarchical -file routed_hier.rpt\nreport_utilization -file routed_util.rpt\nquit\n'
  route=directory/'measure_route.tcl';route.write_text('set_param general.maxThreads 16\nopen_checkpoint ../measure_opt.dcp\n'+rest)
  run(directory,route)
 return True
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 print(list(pool.map(point,['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8'])),flush=True)
