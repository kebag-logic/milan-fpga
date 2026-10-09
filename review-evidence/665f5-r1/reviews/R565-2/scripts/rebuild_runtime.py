"""Replay the runtime recipe with the firmware no-stack-protector flag."""
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("source",type=Path)
ap.add_argument("output",type=Path)
a=ap.parse_args(); source=a.source.resolve(); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
shutil.copyfile(source/"picolibc.h",out/"picolibc.h")
p=json.loads((source/"provenance.json").read_text()); commands=[]
for command in p["commands"]:
 command=[s.replace(str(source),str(out)) for s in command]
 if "-c" in command: command.insert(1,"-fno-stack-protector")
 subprocess.run(command,check=True,timeout=120)
 commands.append(command)
records=[]
for record in p["files"]:
 path=Path(record["path"].replace(str(source),str(out)))
 records.append({"path":str(path),"size":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
(out/"provenance.json").write_text(json.dumps({"files":records,"commands":commands},indent=2)+"\n")
