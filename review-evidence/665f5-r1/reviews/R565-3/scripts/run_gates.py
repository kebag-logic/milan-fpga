#!/usr/bin/env python3
"""Run independent review gates concurrently, wait for every foreground child."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root, packet, verilator = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3]
scratch = packet / "scratch"
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", VERILATOR=verilator, VBUILD_JOBS="1")
export = scratch / "mailbox-tree"
export.mkdir(exist_ok=True)
archive = subprocess.run(["git", "archive", "HEAD", "hdl/milan/mailbox", "sw/firmware/ctrl", "sw/firmware/ctrl_nvm", "sw/mailbox", "tb/verilator/mbx", "tb/common"], cwd=root, capture_output=True, check=True)
subprocess.run(["tar", "-x", "-C", str(export)], input=archive.stdout, check=True)
# The mailbox campaign appends four compile jobs per mutant; select one
# mutant worker explicitly so nested work stays inside the shared 16-job cap.
makefile=export/"tb/verilator/mbx/Makefile"
makefile.write_text(makefile.read_text().replace("mutants.py --quick\n", "mutants.py --quick --jobs 1\n"))
py = sys.executable
jobs = {
 "firmware-bank": [[py,"-B","sw/firmware/ctrl/test/test_ctrl_firmware.py","--require-rv32","--jobs","4","--build-dir",str(scratch/"bank")]],
 "aecp-suite": [[py,"-B","sw/firmware/ctrl/test/aecp_arms.py","--app","--interfaces",str(i),"--output",str(scratch/f"aecp-if{i}")] for i in (1,2)],
 "mailbox": [["make","-j16","-C",str(export/"tb/verilator/mbx"),"VBUILD_JOBS=1",f"VERILATOR={verilator}"]],
 "mailbox-generator": [[py,"-B","sw/mailbox/gen_mailbox.py","--check"]],
}
(packet/"receipts/gate-commands.json").write_text(json.dumps(jobs,indent=2)+"\n")
def task(item):
 name, commands = item
 start=time.monotonic(); codes=[]
 with (packet/f"receipts/{name}.log").open("w") as log:
  for command in commands:
   result=subprocess.run(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
   codes.append(result.returncode)
   if result.returncode: break
 rc=next((n for n in codes if n),0)
 (packet/f"receipts/{name}.rc").write_text(str(rc)+"\n")
 record={"gate":name,"rc":rc,"command_rc":codes,"seconds":round(time.monotonic()-start,2)}
 print(json.dumps(record),flush=True)
 return record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(task,jobs.items()))
(packet/"receipts/gates.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(int(any(r["rc"] for r in results)))
