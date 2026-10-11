#!/usr/bin/env python3
"""Recheck the evidence disposition and receipt guard's failure controls."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
env=dict(os.environ,TMPDIR=str(packet/"scratch/tmp"),PYTHONDONTWRITEBYTECODE="1")
checks=[("test-evidence-selftest",["python3","scripts/measure_test_evidence.py","--selftest"],0)]
checks += [("capture-mutation-"+name,["python3","scripts/check_nvm_capture.py","--mutation",name],1)
           for name in ("bytes","records","clock","ignore-off-timing","receipt-opt-out")]
def run(case):
    name,command,expected=case
    start=time.monotonic()
    with (packet/"receipts"/(name+".log")).open("w") as log:
        result=subprocess.run(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
    (packet/"receipts"/(name+".rc")).write_text(str(result.returncode)+"\n")
    row=dict(name=name,argv=command,expected_rc=expected,rc=result.returncode,seconds=round(time.monotonic()-start,3))
    print(json.dumps(row),flush=True)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    rows=list(executor.map(run,checks))
(packet/"receipts/resolution-checks.json").write_text(json.dumps(rows,indent=2)+"\n")
sys.exit(int(any(r["rc"] != r["expected_rc"] for r in rows)))
