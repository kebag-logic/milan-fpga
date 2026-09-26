import datetime, json, os, pathlib, shlex, subprocess, sys, time
out=pathlib.Path(__file__).resolve().parent
label=sys.argv[1]
command=sys.argv[2:]
start=time.monotonic()
record={"gate": label, "command": shlex.join(command), "cwd": os.getcwd(), "start": datetime.datetime.now(datetime.timezone.utc).isoformat(), "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()}
log=out/(label+".log")
print("START "+label+" : "+record["command"], flush=True)
with log.open("w") as stream:
    stream.write(record["command"]+"\n"); stream.flush()
    result=subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
record.update(exit=result.returncode, seconds=round(time.monotonic()-start,3), log=log.name)
with (out/"gates.jsonl").open("a") as stream: stream.write(json.dumps(record)+"\n")
with (out/"HANDOFF.md").open("a") as stream: stream.write("\nGate `"+label+"`: exit "+str(result.returncode)+"; `"+record["command"]+"`; evidence `"+log.name+"`.\n")
print("END "+label+" rc="+str(result.returncode)+" seconds="+str(record["seconds"]), flush=True)
print("\n".join(log.read_text(errors="replace").splitlines()[-16:]), flush=True)
sys.exit(result.returncode)
