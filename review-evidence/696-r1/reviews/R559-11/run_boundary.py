#!/usr/bin/env python3
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--verilator",required=True);a=p.parse_args()
packet=Path(__file__).resolve().parent;obj=packet/"scratch/boundary";obj.mkdir(exist_ok=True)
argv=[a.verilator,"--cc","--exe","--build","-j","2","--top-module","KL_maap","-GCLK_FREQ_HZ_P=10000","-Wno-fatal","--Mdir",str(obj),"-CFLAGS","-std=c++17 -O2 -I"+str(a.root/"tb/common"),str(a.root/"hdl/ieee1722/maap/KL_maap.sv"),str(packet/"boundary_probe.cpp"),"-o","boundary"]
for name,cmd in [("boundary-build",argv),("boundary-run",[str(obj/"boundary")])]:
    with (packet/"receipts"/(name+".log")).open("w") as log:
        rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=obj).returncode
    (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(name,rc)
    if rc: raise SystemExit(rc)
