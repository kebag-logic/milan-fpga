#!/usr/bin/env python3
"""Run focused builds concurrently and retain per-command receipts."""
import concurrent.futures, os, subprocess
from pathlib import Path
P = Path(__file__).resolve().parents[1]
S = P / "scratch"
V = os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
env = dict(os.environ, VERILATOR=V, VERILATOR_JOBS="2", MAKEFLAGS="-j16")
def run(name, commands, cwd):
    with (P / "receipts" / (name + ".log")).open("w") as log:
        rc=0
        for command in commands:
            print("COMMAND", command, file=log, flush=True)
            rc=subprocess.run(command,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
            if rc: break
    (P / "receipts" / (name + ".rc")).write_text(str(rc)+"\n")
    print(name, rc, flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(run,"follow-build",[["make","-j16","build","VERILATOR_JOBS=2"]], S/"tb/verilator/follow_ring"),
               pool.submit(run,"capture-unit",[[V,"--cc","--exe","--build","-j","2","--top-module","chmap_wrap","--Mdir","obj_dir","-Wall","-Wno-fatal","-Wno-UNUSEDSIGNAL","-Wno-WIDTHEXPAND","-Wno-WIDTHTRUNC","-Wno-PINCONNECTEMPTY","-Wno-UNUSEDPARAM","-CFLAGS","-std=c++17 -O2 -Wall -Wextra","../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv","../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv","../../../hdl/ieee1722/aaf/KL_tone_gen.sv","chmap_wrap.sv","sim_main.cpp"],["./obj_dir/Vchmap_wrap"]],S/"tb/verilator/chmap_capture")]
    results=[f.result() for f in futures]
raise SystemExit(int(any(results)))
