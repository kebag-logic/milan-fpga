#!/usr/bin/env python3
"""Run the focused review checks with bounded concurrency; all children are joined."""
import concurrent.futures, os, pathlib, shutil, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
scratch=out/"scratch"
scratch.mkdir(exist_ok=True)
env=dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
verilator=env.get("REVIEW_VERILATOR", "verilator")
env["VERILATOR"]=verilator
copy=scratch/"tdm"
for d in ("tb/verilator/tdm_render", "tb/common", "hdl/common", "hdl/ieee1722/aaf"):
    shutil.copytree(root/d, copy/d, dirs_exist_ok=True)
makefile=copy/"tb/verilator/tdm_render/Makefile"
makefile.write_text(makefile.read_text().replace("--build -j 0", "--build -j 2"))
checks=[
("tdm", ["make", "-j16", "all", f"VERILATOR={verilator}"], copy/"tb/verilator/tdm_render"),
("declarations", [sys.executable,"-B","-c","import test_declarations as t; t.test_stream_port_cluster_minimum(); t.test_input_cluster_pools()"],root/"sw/builder"),
("aecp-inputs",[sys.executable,"-B","sw/firmware/ctrl/test/aecp_arms.py","--output",str(scratch/"aecp"),"--inputs"],root),
]
def run(c):
    name,cmd,cwd=c
    with (out/(name+".log")).open("w") as log:
        log.write("command: "+repr(cmd)+"\n");log.flush()
        p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    (out/(name+".rc")).write_text(str(p.returncode)+"\n")
    return name,p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(run,checks): print(result,flush=True)
# Dependent mutation campaign reuses the isolated recipe after positive controls.
print(run(("tdm-mutants",["make","-j16","master-mutants",f"VERILATOR={verilator}"],copy/"tb/verilator/tdm_render")),flush=True)
