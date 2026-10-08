import json,os,shlex,subprocess,signal
from pathlib import Path
signal.signal(signal.SIGHUP,signal.SIG_DFL)
w=Path(__file__).resolve().parent
root=w/"functional/route"
out=w/"timing/elaboration"
out.mkdir(parents=True,exist_ok=True)
e=os.environ.copy();e.update(PYTHONDONTWRITEBYTECODE="1",PYTHONHASHSEED="0",MAKEFLAGS="-j16",TMPDIR=str(w/"tmp"),LITEX_ENV_CC_TRIPLE="riscv32-linux")
e["PATH"]=str(Path.home()/"litex-milan/venv/bin")+":$VALIDATION_STORAGE/231-a337-sdk/bin:"+e["PATH"]
def run(name,argv,cwd):
 with (out/(name+".log")).open("w") as f: rc=subprocess.run(argv,cwd=cwd,env=e,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(name+".rc")).write_text(str(rc)+"\n")
 print(name,rc,flush=True)
 if rc:raise SystemExit(rc)
for cfg in ("ax8x8",):
 run(cfg+"-dry-run",["bash","sw/litex/build.sh",cfg,"--dry-run"],root)
 lines=[x for x in (out/(cfg+"-dry-run.log")).read_text().splitlines() if "exec python3 milan_soc.py " in x]
 assert len(lines)==1
 argv=shlex.split(lines[0].split("exec python3 ",1)[1]);argv.remove("--build")
 argv[argv.index("--output-dir")+1]=str(w/"timing"/cfg)
 argv[argv.index("--vivado-max-threads")+1]="32"
 (out/(cfg+"-argv.json")).write_text(json.dumps(argv,indent=2)+"\n")
 run(cfg+"-elaboration",[str(Path.home()/"litex-milan/venv/bin/python3"),*argv],root/"sw/litex")
 args=["python3","-B","syn/ooc/pp_baseline.py",str(w/"timing"/cfg/"gateware"),"--single-thread-synthesis"]
 if cfg=="ax8x8":args+=["--synthesis-only"]
 run(cfg+"-baseline",args,root)
(w/"elaboration.rc").write_text("0\n")
