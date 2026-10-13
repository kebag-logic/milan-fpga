#!/usr/bin/env python3
"""Apply the unchanged public shift launcher to both current-head binaries."""
import argparse,subprocess,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
packet=Path(__file__).resolve().parent

def run(item):
    shape,shift=item;work=packet/"scratch"/("makeflags-1" if shape==1 else "frames-only-8")
    log=packet/f"shift-{shape}-{shift}.log"
    subprocess.run(["sh",str(packet/"prior-probes/run_shift.sh"),str(work),str(shift),str(log)],check=True)
    text=log.read_text();assert text.endswith("rc=0\n") and "RESULT: PASS" in text,(shape,shift)
    print(shape,shift,"PASS",flush=True)
with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(run,[(shape,shift) for shape in (1,8) for shift in (0,200,300,800,900,1000000)]))
