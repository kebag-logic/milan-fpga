#!/usr/bin/env python3
"""After probe.py, observe takeover addend and run the parent shadow slice.
Usage: python3 follow_probe.py REPO OUTPUT VERILATOR
Uses the three existing disposable clones only. Runs at most 15 compiler jobs.
"""
import concurrent.futures, os, pathlib, subprocess, sys
repo,out,simulator=(pathlib.Path(s).resolve() for s in sys.argv[1:])
def run(case):
 tree=out/"scratch"/case
 path=tree/"tb/verilator/gptp_plane/sim_main.cpp"
 s=path.read_text(); anchor="    const size_t gm_first = txf.size();"
 assert s.count(anchor)==1
 s=s.replace(anchor,'    printf("OBSERVED master addend Q8.24: %d\\n", adj_seen.empty() ? 0 : static_cast<int32_t>(adj_seen.back()));\n'+anchor)
 path.write_text(s)
 (out/(case+"-observation.patch")).write_text(subprocess.check_output(["git","diff","--",str(path.relative_to(tree))],cwd=tree,text=True))
 env=os.environ.copy();env.update(MAKEFLAGS="--no-print-directory",CCACHE_DISABLE="1",PYTHONDONTWRITEBYTECODE="1")
 def command(args,name):
  logfile=out/(case+"-"+name+".log")
  with logfile.open("w") as log:
   log.write("COMMAND "+" ".join(map(str,args)).replace(str(repo),"<source>")+"\n");log.flush()
   r=subprocess.run(list(map(str,args)),cwd=tree,stdout=log,stderr=subprocess.STDOUT,env=env)
  logfile.write_text(logfile.read_text().replace(str(out),"<packet>").replace(str(repo),"<source>"))
  (out/(case+"-"+name+".rc")).write_text(str(r.returncode)+"\n")
  return r.returncode
 command(["make","-j16","--no-print-directory","-C","tb/verilator/gptp_plane","run","VERILATOR="+str(simulator)],"observed")
 subprocess.run(["git","config","submodule.third_party/verilog-axis.url",str(repo/"third_party/verilog-axis")],cwd=tree,check=True)
 assert command(["git","-c","protocol.file.allow=always","submodule","update","--init","third_party/verilog-axis"],"axis-setup")==0
 rc=command(["make","-j16","--no-print-directory","-C","tb/verilator/gptp_shadow","run","VERILATOR_JOBS=5","VERILATOR="+str(simulator)],"shadow")
 return case,rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for case,rc in pool.map(run,["baseline","delayed-announce","retained-slave-rate"]): print(case,rc,flush=True)
