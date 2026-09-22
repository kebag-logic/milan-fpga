import concurrent.futures,json,os,subprocess
from pathlib import Path
out=Path(__file__).resolve().parents[1];scratch=Path((out/"scratch-path.txt").read_text().strip())
variants=[v+"-"+t for v in ("old","head") for t in ("correct","div","title","xmp")]
def trial(label):
 dest=out/"consumer"/label
 if not (dest/"results.json").exists():
  p=subprocess.run(["rtk","proxy","python3","-B",str(out/"probes/consumer.py"),str(scratch/label),str(dest)],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
  dest.mkdir(parents=True,exist_ok=True);(dest/"driver.log").write_text(p.stdout+p.stderr);assert p.returncode==0,(label,p.stderr)
 r=json.loads((dest/"results.json").read_text());version,tag=label.split("-")
 assert r["cli"]["rc"]==(2 if version=="head" and tag!="correct" else 1)
 for row in r["rows"]:
  exempt=row["name"].split("-")[0] in ("style",tag)
  assert (len(row["findings"]),row["exempt"])==((0,1) if exempt else (1,0)),row
  assert row["base_probe_kind"]==("prose line" if exempt else "raw HTML line"),row
 return dict(variant=label,cli_rc=r["cli"]["rc"],per_page=[dict(name=x["name"],findings=len(x["findings"]),exempt=x["exempt"],kind=x["base_probe_kind"]) for x in r["rows"]])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(trial,variants))
(out/"consumer.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
