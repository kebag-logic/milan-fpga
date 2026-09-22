import datetime,json,os,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
label=sys.argv[1]; command=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); tick=time.monotonic()
env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
p=subprocess.run(command,capture_output=True,text=True,env=env)
log=root/"commands";log.mkdir(exist_ok=True)
(log/(label+".log")).write_text(p.stdout+p.stderr)
record={"command":command,"cwd":str(Path.cwd()),"start":start,"seconds":time.monotonic()-tick,"exit":p.returncode}
(log/(label+".json")).write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record)); print((p.stdout+p.stderr)[-6500:])
sys.exit(p.returncode)
