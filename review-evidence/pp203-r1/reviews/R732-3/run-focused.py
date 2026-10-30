import pathlib,subprocess,sys,tarfile,io,os
P=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(sys.argv[1]).resolve()
name=sys.argv[2]; suite=sys.argv[3] if len(sys.argv)>3 else "pp_top"
work=P/"scratch"/name
if not work.exists():
 work.mkdir(parents=True)
 tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","-C",str(SRC),"archive","013ee63fd42455987ddbbbeb3b66f5af106b5793"]))).extractall(work,filter="data")
wrapper=P/"scratch"/"bounded-simulator.py"
sim=os.environ.get('REVIEW_SIMULATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x == '-j': a[i+1]='8'\nos.execv("+repr(sim)+",['verilator']+a)\n")
wrapper.chmod(0o755)
j4=P/'scratch/simulator-j4.py'
j4.write_text(wrapper.read_text().replace("a[i+1]='8'","a[i+1]='4'"));j4.chmod(0o755)
cmd=["make","-j16","-C",str(work/"tb"/suite),"VERILATOR="+str(wrapper)]
if suite=="pp_top": cmd += ["reboot"]
(P/(name+".cmd")).write_text(" ".join(cmd)+"\n")
with (P/(name+".log")).open("w") as f: rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT).returncode
(P/(name+".rc")).write_text(str(rc)+"\n")
print(name, "rc",rc,flush=True)
print("\n".join((P/(name+".log")).read_text().splitlines()[-5:]))
sys.exit(rc)
