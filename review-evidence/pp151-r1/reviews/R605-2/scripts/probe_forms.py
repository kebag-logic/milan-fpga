#!/usr/bin/env python3
"""Re-measure the documented severity forms with two available front ends."""
import argparse, concurrent.futures, json, os, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("packet",type=Path);ap.add_argument("--verilator",required=True);ap.add_argument("--jobs",type=int,default=4);a=ap.parse_args();p=a.packet.resolve()
forms=[("fatal",False),("error",False),("warning",False),("info",False),("fatal",True)]
def trial(item):
 (severity,initial),value=item;name=f"{severity}-{'initial' if initial else 'module'}-{value}";work=p/"scratch/forms"/name;work.mkdir(parents=True,exist_ok=True)
 task=f'${severity}('+('1, ' if severity=='fatal' else '')+'"R605 severity probe");'
 source='module r605_form #(parameter int unsigned P = 0)(output wire z);\nassign z = 1\'b0;\n'+('initial ' if initial else '')+'if (P > 0) begin : g_guard\n'+task+'\nend\nendmodule\n'
 (work/"r605_form.sv").write_text(source)
 v=subprocess.run([a.verilator,"--lint-only","-Wall","-Wno-DECLFILENAME","-Wno-UNUSEDSIGNAL","-Wno-UNUSEDPARAM",f"-GP={value}","r605_form.sv"],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 expected=int(value==1 and not initial and severity!='info');assert v.returncode==expected,(name,v.returncode,v.stdout)
 lowered=subprocess.run(["sv2v","r605_form.sv"],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);assert lowered.returncode==0
 (work/"all.v").write_text(lowered.stdout)
 y=subprocess.run(["yosys","-q","-p",f"read_verilog -defer all.v; chparam -set P {value} r605_form; hierarchy -check -top r605_form; proc; opt_clean"],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 expected_y=int(value==1 and severity=='fatal');assert y.returncode==expected_y,(name,y.returncode,y.stdout)
 dest=p/"receipts/forms";dest.mkdir(parents=True,exist_ok=True)
 (dest/(name+'.log')).write_text('VERILATOR rc='+str(v.returncode)+'\n'+v.stdout+'YOSYS rc='+str(y.returncode)+'\n'+y.stdout)
 return {"form":name,"verilator_rc":v.returncode,"yosys_rc":y.returncode}
with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:results=list(pool.map(trial,[(f,v) for f in forms for v in (0,1)]))
print(json.dumps({"forms":results,"result":"20/20 expected process statuses"},indent=2))
