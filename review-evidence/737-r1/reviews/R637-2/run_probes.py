#!/usr/bin/env python3
"""Run the four disposable review probes and a read-only pin check."""
import concurrent.futures,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parent
items=[("probe_skipped_collector.py","skipped-collector.log"),("probe_collector_checkout.py","collector-checkout.log"),("probe_collector_observer.py","collector-observer.log"),("probe_failure_conclusions.py","failure-conclusion-mutations.log")]
def execute(item):
 script,log=item;cmd=["python3",str(packet/script),str(root)];start=time.monotonic()
 with (packet/log).open("w") as output:
  result=subprocess.run(cmd,cwd=root,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(packet/"scratch")),timeout=120)
 return {"script":script,"receipt":log,"returncode":result.returncode,"seconds":round(time.monotonic()-start,3)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(execute,items))
with (packet/"evidence-pins-check.log").open("w") as output:
 result=subprocess.run(["python3","scripts/generate_ci_evidence_pins.py","--check"],cwd=root,stdout=output,stderr=subprocess.STDOUT)
rows.append({"command":["python3","scripts/generate_ci_evidence_pins.py","--check"],"receipt":"evidence-pins-check.log","returncode":result.returncode})
(packet/"probe-results.json").write_text(json.dumps(rows,indent=2)+"\n")
print(json.dumps(rows,indent=2));raise SystemExit(any(row["returncode"] for row in rows))
