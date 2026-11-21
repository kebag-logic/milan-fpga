#!/usr/bin/env python3
import concurrent.futures,os,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent;r=pathlib.Path(sys.argv[1]).resolve();v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
base=p/'scratch/base_depkt.sv';base.write_bytes(subprocess.check_output(['git','-C',str(r),'show','15168e14:hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv']))
def run(which):
 out=p/'scratch'/('obj_tail_'+which)
 cmd=[v,'--cc','--exe','--build','-j','4','-Wno-fatal','--top-module','KL_aaf_rx_depacketizer','--Mdir',str(out)]
 if which=='base':cmd+=['-CFLAGS','-DBASE',str(base),str(r/'third_party/verilog-axis/rtl/axis_fifo.v')]
 else:cmd+=[str(r/'hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv')]
 cmd+=[str(p/'probe_tail.cpp')]
 with (p/('tail-'+which+'-build.log')).open('w') as f:
  f.write(repr(cmd)+'\n');f.flush();b=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 if b.returncode:return which,b.returncode
 s=subprocess.run([str(out/'VKL_aaf_rx_depacketizer')],capture_output=True,text=True)
 (p/('tail-'+which+'.log')).write_text(s.stdout+s.stderr);(p/('tail-'+which+'.rc')).write_text(str(s.returncode)+'\n')
 return which,s.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(run,['base','head']):print(result)
a=(p/'tail-base.log').read_text();b=(p/'tail-head.log').read_text();print(a);print('base/head observations equal:',a==b)
(p/'tail-comparison.txt').write_text('Base 15168e14 and exact head direct depacketizer probe.\n'+a+'base/head observations equal: '+str(a==b)+'\nNon-multiple-of-eight input is outside Milan base-format payloads; no regression inferred.\n')
