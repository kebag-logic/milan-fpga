#!/usr/bin/env python3
"""Isolate phase detector boundary behavior without modifying tracked sources."""
import argparse,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument("repo",type=pathlib.Path);p.add_argument("--compiler",required=True);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parent;b=r/"scratch/boundary-build";l=r/"receipts";l.mkdir(exist_ok=True)
cmd=[a.compiler,"--cc","--exe","--build","-j","2","--public-flat-rw","-Wno-fatal","--top-module","KL_mmcm_drp_servo","-GTICK_CYC_P=32","--Mdir",str(b),str(a.repo/"hdl/common/cdc_pulse.sv"),str(a.repo/"hdl/common/cdc_handshake.sv"),str(a.repo/"hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"),str(r/"probe_phase_boundary.cpp"),"-CFLAGS","-std=c++17"]
with (l/"boundary-build.log").open("w") as f: rc=subprocess.call(cmd,stdout=f,stderr=subprocess.STDOUT)
(l/"boundary-build.rc").write_text(str(rc)+"\n")
if rc:raise SystemExit(rc)
with (l/"boundary-probe.log").open("w") as f:
    f.write("Fold-boundary stimulus (10416 ns, outside band):\n"); f.flush()
    rc=subprocess.call([str(b/"VKL_mmcm_drp_servo"),"10416"],stdout=f,stderr=subprocess.STDOUT)
    f.write("Near-zero positive control (100 ns, inside band):\n"); f.flush()
    rc |= subprocess.call([str(b/"VKL_mmcm_drp_servo"),"100"],stdout=f,stderr=subprocess.STDOUT)
(l/"boundary-probe.rc").write_text(str(rc)+"\n")
print((l/"boundary-probe.log").read_text());raise SystemExit(rc)
