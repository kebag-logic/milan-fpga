import concurrent.futures, pathlib, subprocess, sys, os
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True)
b="tb/verilator/ctrl_service_budget/"
commands={
"record-classes":["python3","-I",b+"record_classes.py","--selftest"],
"shape-costs":["python3","-I",b+"shape_costs.py","--check","--selftest"],
"flip-selftest":["python3","-B",b+"flip_grade.py","--selftest"],
"flip-1x1":["python3","-B",b+"flip_grade.py","--check","--point","1x1/1if"],
"flip-8x8":["python3","-B",b+"flip_grade.py","--check","--point","8x8/1if"],
"rows-selftest":["python3","-B",b+"rows_tiers.py","--selftest"],
"load-check":["python3","-B",b+"load_grade.py","--check"],
"load-selftest":["python3","-B",b+"load_grade.py","--selftest"],
"ledger":["python3","-I",b+"egress_ledger.py","--selftest"],
"harness":["python3","-B",b+"run.py","--self-test"],
}
def run(item):
 name,cmd=item
 r=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(out.parent/"scratch")))
 (out/(name+".log")).write_text("COMMAND: "+" ".join(cmd)+"\n"+r.stdout)
 (out/(name+".rc")).write_text(str(r.returncode)+"\n")
 print(name,"rc",r.returncode,flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: codes=list(ex.map(run,commands.items()))
sys.exit(int(any(codes)))
