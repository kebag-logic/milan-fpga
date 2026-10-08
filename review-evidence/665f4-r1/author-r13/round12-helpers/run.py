import hashlib,json,os,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
label=sys.argv[1]
command=sys.argv[2:]
env=os.environ.copy()
env.update(TMPDIR=str(root),PYTHONDONTWRITEBYTECODE="1",PYTHONUNBUFFERED="1",
 VERILATOR=os.environ["PINNED_HDL_LIMITED"],VERILATOR_JOBS="2",
 MILAN_RV32_CC=os.environ["MILAN_RV32_CC"])
env["PATH"]=os.environ["DOCS_ENV"]+"/bin:"+os.environ["PINNED_HDL_DIR"]+":"+env["PATH"]
log=root/(label+".log")
start=time.monotonic()
print("START",label,flush=True)
with log.open("w") as stream:
 try:
  rc=subprocess.run(command,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=21600).returncode
 except subprocess.TimeoutExpired:
  rc=124
record=dict(command=command,cwd=os.getcwd(),rc=rc,seconds=round(time.monotonic()-start,3),log=log.name,
 size=log.stat().st_size,sha256=hashlib.sha256(log.read_bytes()).hexdigest())
(root/(label+".rc")).write_text(str(rc)+"\n")
(root/(label+".json")).write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record),flush=True)
print("\n".join(log.read_text(errors="replace").splitlines()[-18:]),flush=True)
raise SystemExit(rc)
