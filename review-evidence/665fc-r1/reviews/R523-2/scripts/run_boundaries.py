#!/usr/bin/env python3
import argparse,concurrent.futures,os,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--verilator",required=True);p.add_argument("--jobs",type=int,default=3);a=p.parse_args();root=a.source.resolve();out=a.packet.resolve();work=out/"scratch/boundaries";work.mkdir(exist_ok=True);os.environ["TMPDIR"]=str(out/"scratch");os.environ["VERILATOR"]=a.verilator;sys.dont_write_bytecode=True;sys.path.insert(0,str(root/"tb/verilator/mbx"));import mutants
src=out/"scripts/boundary_probe.cpp"; fw=root/"sw/firmware/ctrl";tb=root/"tb/verilator/mbx"
def call(name,argv,cwd=tb):
 q=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,timeout=590);(out/"receipts"/(name+".log")).write_text(q.stdout+q.stderr);(out/"receipts"/(name+".rc")).write_text(str(q.returncode)+"\n");print(name,q.returncode,flush=True);return q.returncode

def rtl(h):
 recipe=mutants.recipe();recipe[recipe.index("-j")+1]="4";recipe += ["-CFLAGS", f"-I{tb}"];d=work/f"rtl-{h}"
 rc=call(f"boundary-{h}-build",recipe+[f"-GHOST_P={h}","--Mdir",d,*[mutants.RTL/f for f in mutants.RTL_FILES],tb/"tb_mbx_top.sv",src,"-o","probe"])
 return rc or call(f"boundary-{h}",[d/"probe",h])
def model():
 inc=[f"-I{x}" for x in (out/"scratch/if2-gen",fw/"mbx",fw/"wire",fw/"host",fw/"test",tb)]
 rc=call("boundary-model-build-c",["cc","-std=c11","-O2","-Wall","-Wextra","-Werror",*inc,"-c",fw/"host/mbx_model.c","-o",work/"model.o"])
 if rc:return rc
 rc=call("boundary-model-build-cpp",["c++","-std=c++17","-O2","-Wall","-Wextra","-Werror","-DMODEL",*inc,src,work/"model.o","-o",work/"model"])
 if rc:return rc
 rc=call("boundary-model",[work/"model"])
 if rc:return rc
 rc=call("if2-model-build",["c++","-std=c++17","-O2","-Wall","-Wextra","-Werror",*inc,tb/"model_main.cpp",work/"model.o","-o",work/"if2-suite"])
 return rc or call("if2-model-suite",[work/"if2-suite"])
with concurrent.futures.ThreadPoolExecutor(max_workers=min(3,a.jobs)) as ex:
 results=[f.result() for f in [ex.submit(rtl,0),ex.submit(rtl,1),ex.submit(model)]]
sys.exit(any(results))
