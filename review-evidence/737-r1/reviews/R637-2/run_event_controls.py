#!/usr/bin/env python3
"""Run the unchanged CI mutation selftest without a review harness deadline."""
import json,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parent
start=time.monotonic()
with (packet/"event-controls-rerun.log").open("w") as output:
 result=subprocess.run(["python3","scripts/ci_events.py","--selftest"],cwd=root,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1"))
receipt={"command":["python3","scripts/ci_events.py","--selftest"],"returncode":result.returncode,"seconds":round(time.monotonic()-start,3),"reason":"Initial review harness 420-second bound expired; unchanged test rerun with no harness time limit."}
(packet/"event-controls-rerun.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt));raise SystemExit(result.returncode)
