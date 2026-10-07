#!/usr/bin/env python3
"""Replay focused receipts into a NEW packet directory, from the exact checkout."""
import argparse,io,pathlib,subprocess,sys,tarfile
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--verilator",required=True);a=p.parse_args();root=a.source.resolve();out=a.packet.resolve();scripts=pathlib.Path(__file__).resolve().parent
assert not out.exists(),"Use a new output directory"
(out/"receipts").mkdir(parents=True);(out/"scratch").mkdir();(out/"scripts").mkdir()
# The boundary driver opens its C++ probe relative to the output packet.
(out/"scripts/boundary_probe.cpp").write_bytes((scripts/"boundary_probe.cpp").read_bytes())
def run(name,argv,cwd=root):
    with (out/"receipts"/(name+".log")).open("w") as log:
        q=subprocess.run(list(map(str,argv)),cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
    (out/"receipts"/(name+".rc")).write_text(str(q.returncode)+"\n")
    if q.returncode:raise SystemExit(q.returncode)
for script,name in (("focused_review.py","focused-campaign"),("run_boundaries.py","boundary-campaign")):
    run(name,[sys.executable,"-B",scripts/script,"--source",root,"--packet",out,"--verilator",a.verilator,"--jobs",3])
copy=out/"scratch/cosim-source";copy.mkdir()
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","archive","HEAD"],cwd=root))) as t:
    t.extractall(copy,filter="data")
flags='--cc --exe --build -j 4 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
run("cosim",["make","-j16","-C",copy/"tb/verilator/mbx","run-cosim","VERILATOR="+a.verilator,"VFLAGS="+flags])
run("source-invariants",[sys.executable,"-B",scripts/"source_invariants.py","--source",root,"--packet",out])
run("integrity",[sys.executable,"-B",scripts/"integrity.py","--source",root])
