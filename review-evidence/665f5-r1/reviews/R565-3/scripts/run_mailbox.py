#!/usr/bin/env python3
"""Fresh mailbox default target with explicitly bounded nested parallelism."""
import os,pathlib,subprocess,sys
root,packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3]);verilator=sys.argv[3]
out=packet/"scratch/mailbox-bounded";out.mkdir(exist_ok=True)
b=subprocess.check_output(["git","archive","HEAD","hdl/milan/mailbox","sw/firmware/ctrl","sw/firmware/ctrl_nvm","sw/mailbox","tb/verilator/mbx","tb/common"],cwd=root)
subprocess.run(["tar","-x","-C",str(out)],input=b,check=True)
f=out/"tb/verilator/mbx/Makefile";text=f.read_text();assert text.count("mutants.py --quick\n")==1
f.write_text(text.replace("mutants.py --quick\n","mutants.py --quick --jobs 1\n"))
env=dict(os.environ,VERILATOR=verilator,VBUILD_JOBS="1",TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
subprocess.run(["make","-j16","-C",str(out/"tb/verilator/mbx"),"VBUILD_JOBS=1",f"VERILATOR={verilator}"],env=env,check=True)
