#!/usr/bin/env python3
"""Plant a missing record terminator and ask the existing whole tap suite to detect it."""
import argparse,pathlib,shutil,subprocess
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); ap.add_argument("--simulator",required=True); a=ap.parse_args()
r=a.repo.resolve(); p=pathlib.Path(__file__).resolve().parent; w=p/"scratch/last-plant"; rtl=w/"rtl"; shutil.copytree(r/"hdl/usbnet",rtl,dirs_exist_ok=True)
f=rtl/"KL_usbnet_rx_copy.sv"; s=f.read_text(); old="m_last_o  = words_r == 11'd1;"; assert s.count(old)==1; f.write_text(s.replace(old,"m_last_o  = 1'b0;"))
flags='--cc --exe --build -j 2 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-PROCASSINIT -Werror-UNDRIVEN -Werror-MULTIDRIVEN -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
cmd=["make","-j16","-C",str(r/"tb/verilator/usbnet"),"tap","RTL="+str(rtl),"OBJ="+str(w/"obj"),"VERILATOR="+a.simulator,"VFLAGS="+flags]
v=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(p/"last-plant.log").write_text(v.stdout.replace(str(r),"$REPO").replace(str(p),"$PACKET")); (p/"last-plant.rc").write_text(str(v.returncode)+"\n"); print("existing suite return code with every up.last removed:",v.returncode)
print("\n".join(x for x in v.stdout.splitlines() if x.startswith(("PASS","FAIL"))))
raise SystemExit(v.returncode)
