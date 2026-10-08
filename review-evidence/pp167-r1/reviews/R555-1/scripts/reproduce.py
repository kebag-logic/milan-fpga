#!/usr/bin/env python3
"""Replay the focused review in disposable trees; no full banks or source edits.
Usage: python3 scripts/reproduce.py SOURCE_CHECKOUT [ABSOLUTE_COMPILER_PATH]
Requires git, make, C++ compiler and the documentation gate dependencies.
The two-instance wrapper bounds concurrent compilation and uses four workers each.
"""
import concurrent.futures, os, pathlib, subprocess, sys
packet=pathlib.Path(__file__).resolve().parents[1]; root=pathlib.Path(sys.argv[1]).resolve()
if len(sys.argv)>2: os.environ["REVIEW_VERILATOR"]=str(pathlib.Path(sys.argv[2]).resolve())
head="f3fef22448ce4f9bed8fd249a21a5d472148bd3d"; base="ed340b9b85258194247334b85e62cf9c23d4d051"
assert subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()==head
wrapper=str(packet/"scripts/limited_verilator.py"); runner=str(packet/"scripts/run_record.py")
for name in ["replay-head","replay-base-sc1"]:
    dest=packet/"scratch"/name
    subprocess.run(["git","clone","--quiet","--shared","--no-checkout",str(root),str(dest)],check=True)
    subprocess.run(["git","-C",str(dest),"checkout","--quiet","--detach",head],check=True)
    if name.endswith("base-sc1"):
        f="hdl/aecp/KL_aecp_notify.sv"
        (dest/f).write_bytes(subprocess.check_output(["git","-C",str(root),"show",base+":"+f]))
work=packet/"scratch/replay-head"
tasks=[
 ("replay-notify-suite",work/"tb/aecp_notify",["make","-j16","VERILATOR="+wrapper],0),
 ("replay-base-sc1",packet/"scratch/replay-base-sc1/tb/aecp_notify",["make","-j16","collision","VERILATOR="+wrapper],2),
 ("replay-originator",work/"tb/originator",["make","-j16","VERILATOR="+wrapper],0),
 ("replay-docs",work,["make","-j16","check"],0),
 ("replay-campaign",root,["python3","tb/pp_top/notify_mutants.py","--output",str(packet/"receipts/replay-campaign"),"--verilator",wrapper,"--jobs","4","--only","cancel_collision_drops_command","cancel_one_clock_late","cancel_one_per_command"],0),
]
def run(task):
    name,cwd,command,want=task
    got=subprocess.run([sys.executable,runner,name,str(cwd),*command]).returncode
    assert got==want,(name,got,want)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: list(pool.map(run,tasks))
print("Focused replay complete. The independently authored 16-controller probe is reproducible with prepare_robust_probe.py and make -j16 collision in its scratch tree.")
