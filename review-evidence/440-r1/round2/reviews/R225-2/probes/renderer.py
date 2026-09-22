import hashlib,json,re,subprocess,datetime
from pathlib import Path
out=Path(__file__).resolve().parents[1];dest=out/"renderer";dest.mkdir(exist_ok=True)
added=json.loads((out/"retention.json").read_text())["added_raw"]
rows=[dict(name=x["name"],text=x["page"],expected=0) for x in added]
for name,prefix in [("valid-cross-later","<pre>\n</style>\n"),("valid-cross-inline","<pre>x</TEXTAREA>\n")]:rows.append(dict(name=name,text=prefix+"## Probe\n",expected=1))
results=[]
for i,row in enumerate(rows):
 request=dict(text=row["text"],mode="gfm",context="kebag-logic/milan-fpga")
 body=json.dumps(request).encode();req=dest/f"{i:02}.request.json";req.write_bytes(body)
 response=dest/f"{i:02}.html"
 p=subprocess.run(["rtk","proxy","gh","api","--method","POST","markdown","--input",str(req)],capture_output=True)
 (dest/f"{i:02}.stderr").write_bytes(p.stderr);assert p.returncode==0,p.stderr
 response.write_bytes(p.stdout);count=len(re.findall(rb"<h2(?:\s|>)",p.stdout))
 results.append(dict(**row,h2=count,rc=p.returncode,request_sha256=hashlib.sha256(body).hexdigest(),response_sha256=hashlib.sha256(p.stdout).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request=str(req.relative_to(out)),response=str(response.relative_to(out))))
 assert count==row["expected"],results[-1]
(dest/"results.json").write_text(json.dumps(results,indent=2)+"\n")
print("Fresh synthetic GFM responses:",len(results),"all agree")
