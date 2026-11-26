#!/usr/bin/env python3
import argparse,pathlib,subprocess
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); ap.add_argument("--simulator",required=True); ap.add_argument("--case",choices=("rate-hold","rx-length"),default="rate-hold"); a=ap.parse_args()
r=a.repo.resolve(); p=pathlib.Path(__file__).resolve().parent; w=p/"scratch"/a.case; w.mkdir(parents=True,exist_ok=True)
rtl=r/"hdl/usbnet"; names=["pkg","rx_copy","tx_inject","tx_arb","tap"]
cmd=[a.simulator,"--cc","--exe","--build","-j","2","-Wall","-Wno-fatal","--top-module","KL_usbnet_tap","-GCLK_HZ_P=1000000","-GRATE_BPS_P=800000","-GBURST_OCTETS_P=3200","-GHOST_TIMEOUT_MS_P=3","--Mdir",str(w),"-CFLAGS",'-std=c++17 -O2 -I'+str(r/"tb/verilator/usbnet"),*[str(rtl/("KL_usbnet_"+n+".sv")) for n in names],str(p/("rate_hold_probe.cpp" if a.case=="rate-hold" else "rx_length_probe.cpp")),"-o","probe"]
b=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(p/(a.case+"-build.log")).write_text(b.stdout.replace(str(r),"$REPO").replace(str(p),"$PACKET")); assert b.returncode==0
v=subprocess.run([str(w/"probe")],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(p/(a.case+".log")).write_text(v.stdout.replace(str(p),"$PACKET")); (p/(a.case+".rc")).write_text(str(v.returncode)+"\n"); print(v.stdout); raise SystemExit(v.returncode)
