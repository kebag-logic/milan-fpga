import datetime,json,pathlib,shlex,subprocess,sys,time
root=pathlib.Path(__file__).parent
tag=sys.argv[1]; argv=sys.argv[2:]
assert argv[0] == "rtk"
log=root/"logs"/(tag+".log")
assert not log.exists(), log
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
with log.open("wb") as out:
 p=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT)
record=dict(tag=tag,cwd=str(pathlib.Path.cwd()),argv=argv,command=shlex.join(argv),start=start,elapsed_seconds=time.monotonic()-t,exit_code=p.returncode,log=str(log))
with (root/"commands.jsonl").open("a") as out: out.write(json.dumps(record)+"\n")
print(json.dumps(record)); print(log.read_text(errors="replace")[-16000:])
sys.exit(p.returncode)
