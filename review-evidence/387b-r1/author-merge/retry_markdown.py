from pathlib import Path
import datetime,json,os,shlex,subprocess,time,sys
out=Path(__file__).resolve().parent
root=Path("$LANES/387-media-rebase")
env=dict(os.environ,PATH=str(out/"gate-venv/bin")+os.pathsep+os.environ["PATH"])
commands=[("em-dash",["python3","scripts/check_em_dash.py","--base","57456af96b3127b9d309a995bbbd35a6113ce52d"]),("toc",["python3","scripts/gen_toc.py","--check"])]
results=[]
for name,command in commands:
    log=out/(name+"-retry.log")
    started=time.monotonic()
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("START "+shlex.join(command),flush=True)
    with log.open("w") as stream:
        stream.write("Head: e68c1b1ac08c8b1e12a28e281b266d06f881e402\nCommand: "+shlex.join(command)+"\nEnvironment: PATH begins with gate-venv/bin (locked Markdown dependencies)\n\n")
        stream.flush()
        rc=subprocess.run(["rtk","proxy",*command],cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=14400).returncode
    result=dict(name=name,command=command,cwd=str(root),head="e68c1b1ac08c8b1e12a28e281b266d06f881e402",rc=rc,elapsed_seconds=round(time.monotonic()-started,2),started_utc=stamp,log=log.name)
    results.append(result)
    (out/"markdown-retries.json").write_text(json.dumps(results,indent=2)+"\n")
    print(log.read_text(),flush=True)
    print("DONE "+name+": rc="+str(rc),flush=True)
sys.exit(int(any(r["rc"] for r in results)))
