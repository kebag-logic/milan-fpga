#!/usr/bin/env python3
"""Focused independent audits, joined in the foreground."""
import concurrent.futures,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
env=dict(os.environ,TMPDIR=str(out/"scratch"),PYTHONDONTWRITEBYTECODE="1")
checks=[("configs-"+mode,[sys.executable,"-B",str(out/"audit_configs.py"),str(root),mode]) for mode in ("base","head")]
checks += [(p.removesuffix(".py"),[sys.executable,"-B","scripts/"+p]) for p in ("check_nvm_capture.py","check_nvm_format_32x32.py","check_nvm_record_space.py","check_entity_shape.py")]
checks += [("fw-service-oracle",[sys.executable,"-B","tb/verilator/fw_service_budget/run.py","--self-test"])]
def run(c):
 n,cmd=c
 with (out/(n+".log")).open("w") as log:
  log.write("command: "+repr(cmd)+"\n");log.flush()
  r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 (out/(n+".rc")).write_text(str(r.returncode)+"\n")
 print(n,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p: list(p.map(run,checks))
