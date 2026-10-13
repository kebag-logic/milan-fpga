#!/usr/bin/env python3
"""Run the public probes unchanged plus focused exact-source fixtures."""
import argparse,json,os,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=argparse.ArgumentParser();p.add_argument("root",type=Path);p.add_argument("--verilator",required=True);p.add_argument("--jobs",type=int,default=2);p.add_argument("tasks",nargs="+");a=p.parse_args()
root=a.root.resolve();packet=Path(__file__).resolve().parent;scratch=packet/"scratch"
env=dict(os.environ,VERILATOR=a.verilator,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1")
wrapper=scratch/"verilator_bounded.py"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j':a[i+1]='2'\nos.execv("+repr(a.verilator)+",["+repr(a.verilator)+"]+a)\n")
wrapper.chmod(0o755)
(packet/"receipts").mkdir(exist_ok=True)

def run(task):
    work=scratch/task;work.mkdir(exist_ok=True)
    shape=8 if task.endswith("-8") else 1
    envtask=dict(env)
    if task.startswith("probe-"):
        variant=task[6:].rsplit("-",1)[0]
        cmd=[sys.executable,"-I","-B",str(packet/"prior-probes/probe_counters.py"),str(root),variant,str(shape),str(work)]
    elif task.startswith("f5-"):
        variant=task[3:].rsplit("-",1)[0]
        cmd=[sys.executable,"tb/verilator/milan_dp/stream_counter_f5.py","--shape",str(shape),"--variant",variant,"--work",str(work)]
    elif task=="snapshot":
        cmd=[sys.executable,"-B",str(packet/"prior-probes/probe_snapshot.py"),str(root),str(packet)]
    elif task=="make-counters":
        cmd=["make","-j16","-C","tb/verilator/milan_dp","counters"]
    elif task.startswith("unit-"):
        suite=task[5:]
        cmd=["make","-j16","-C",str(scratch/"suites/tb/verilator"/suite),"unit" if suite=="crf_rx" else "run"]
        envtask["VERILATOR"]=str(wrapper)
    elif task.startswith("before-"):
        cmd=[sys.executable,"tb/verilator/milan_dp/stream_counters.py","--shape",str(shape),"--variant","before","--work",str(work)]
    elif task=="tx-nodirty-8":
        cmd=[sys.executable,"tb/verilator/milan_dp/stream_counters.py","--shape","8","--variant","tx-nodirty","--work",str(work)]
    else:raise ValueError(task)
    with (packet/(task+".log")).open("w") as out:
        out.write("Command: "+repr(cmd)+"\n");out.flush()
        r=subprocess.run(cmd,cwd=root,env=envtask,stdout=out,stderr=subprocess.STDOUT)
    (packet/(task+".rc")).write_text(str(r.returncode)+"\n")
    assert r.returncode==0,(task,r.returncode)
    if task.startswith("probe-"):
        lines=(work/"run.log").read_text().splitlines()
        failed=[line for line in lines if "[FAIL]" in line]
        assert failed and all("[726 CADENCE]" in line for line in failed),(task,failed)
        cmd=[str(work/"obj/stream_counters")]
        envtask["COUNTERS_OMIT_CHECK"]="CADENCE"
        with (work/"escape.log").open("w") as out:
            r=subprocess.run(cmd,cwd=work/"tb/verilator/milan_dp",env=envtask,stdout=out,stderr=subprocess.STDOUT)
        assert r.returncode==0 and "RESULT: PASS" in (work/"escape.log").read_text(),task
    for name in ("build.log","run.log","escape.log"):
        if (work/name).exists():(packet/(task+"-"+name)).write_bytes((work/name).read_bytes())
    print(task,"PASS",flush=True)
with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(run,a.tasks))
