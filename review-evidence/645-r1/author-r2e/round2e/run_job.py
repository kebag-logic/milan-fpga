import json,os,signal,subprocess,sys,time
signal.signal(signal.SIGHUP, signal.SIG_DFL)
from pathlib import Path
w=Path(__file__).resolve().parent
name=sys.argv[1]
spec=json.loads((w/"jobs"/(name+".json")).read_text())
e=os.environ.copy()
e.update(PYTHONUNBUFFERED="1",PYTHONDONTWRITEBYTECODE="1",PYTHONHASHSEED="0",MAKEFLAGS="-j16",VERILATOR_JOBS="4",VERILATOR=str(w/"functional/run-simulator-limited"),SWEEP_JOBS="8",SIM_JOBS="8",PULLIN_JOBS="8",TMPDIR=str(w/"tmp"),MILAN_LITEX_PYTHON=str(Path.home()/"litex-milan/venv/bin/python3"),LITEX_ENV_CC_TRIPLE="riscv32-linux",SUITE_TIMEOUT="14400")
e.update(spec.get("env",{}))
e["PATH"]=str(w/"functional/shims")+":$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/231-a337-sdk/bin:"+e["PATH"]
t=time.time()
try:
 with (w/"logs"/(name+".log")).open("w") as log:
  rc=subprocess.run(spec["argv"],cwd=spec["cwd"],env=e,stdout=log,stderr=subprocess.STDOUT).returncode
except BaseException as err:
 (w/"logs"/(name+".error")).write_text(repr(err));rc=125
(w/"logs"/(name+".rc")).write_text(str(rc)+"\n")
(w/"logs"/(name+".receipt.json")).write_text(json.dumps(dict(**spec,rc=rc,seconds=round(time.time()-t,1)),indent=2)+"\n")
raise SystemExit(rc)
