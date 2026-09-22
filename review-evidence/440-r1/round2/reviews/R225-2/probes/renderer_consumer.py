import datetime,hashlib,json,re,subprocess
from pathlib import Path
out=Path(__file__).resolve().parents[1];dest=out/"renderer-consumer";dest.mkdir(exist_ok=True)
rows=json.loads((out/"consumer/head-correct/results.json").read_text())["rows"];results=[]
for row in rows:
 name=row["name"];body=json.dumps(dict(text=row["base_source"],mode="gfm",context="kebag-logic/milan-fpga")).encode(); req=dest/(name+".request.json");req.write_bytes(body)
 p=subprocess.run(["rtk","proxy","gh","api","--method","POST","markdown","--input",str(req)],capture_output=True)
 (dest/(name+".stderr")).write_bytes(p.stderr);assert p.returncode==0,p.stderr
 (dest/(name+".html")).write_bytes(p.stdout);h2=len(re.findall(rb"<h2(?:\s|>)",p.stdout)); expected=4 if name.startswith("style-") else 0
 assert h2==expected,(name,h2)
 results.append(dict(name=name,h2=h2,expected=expected,request_sha256=hashlib.sha256(body).hexdigest(),response_sha256=hashlib.sha256(p.stdout).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
(dest/"results.json").write_text(json.dumps(results,indent=2)+"\n");print("Fresh exact consumer-base GFM pages:",len(results),"PASS")
