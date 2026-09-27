import hashlib, json, os, pathlib, subprocess, sys, time
root=pathlib.Path("/tmp/502-a345")
label=sys.argv[1]
command=sys.argv[2:]
log=root/(label+".log")
env=dict(os.environ)
env["PATH"]="/tmp/502-a345/bin:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:"+env["PATH"]
start=time.time()
with log.open("w") as output:
    proc=subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, env=env, timeout=43200)
record=dict(label=label, command=command, cwd=os.getcwd(), rc=proc.returncode, seconds=round(time.time()-start,1), log=str(log), size=log.stat().st_size, sha256=hashlib.sha256(log.read_bytes()).hexdigest())
with (root/"gates.jsonl").open("a") as output: output.write(json.dumps(record)+"\n")
print(json.dumps(record),flush=True)
print("\n".join(log.read_text(errors="replace").splitlines()[-22:]),flush=True)
sys.exit(proc.returncode)
