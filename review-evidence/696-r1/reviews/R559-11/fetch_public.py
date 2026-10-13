#!/usr/bin/env python3
import base64, concurrent.futures, hashlib, json, subprocess
from pathlib import Path
packet=Path(__file__).resolve().parent
out=packet/"scratch/public"; out.mkdir(parents=True,exist_ok=True)
base="review-evidence/696-r1/author-r14/round14-receipts"
ref="217cf1306f90460527ab5cf477ad3c16bdaa72d9"
names=["MANIFEST-01.sha256","accepted-validation.json","validation-summary.json","validation-resume-results.json","merge-provenance.json","maap-ceiling.json","resource-results.json","measurement-records.json","final-integrity.json","source-inputs.json","shipping-image-comparison.json","submodule-verification.json","candidate-route-check.log","candidate-ooc-1x1-check.log","candidate-ooc-8x8-check.log","suite-comparison.json","firmware-comparison.json"]
names += ["validation/maap.log", "validation/maap-coverage.log", "validation/maap-integration.log", "validation/suite-tally.log", "validation/portability.log", "validation/builder.log"]
names += ["maap-ooc-candidate/util_hier_base.rpt", "shipping-candidate/ax7101/gateware/alinx_ax7101_route_status.rpt", "shipping-candidate/ax7101/gateware/baseline_utilization.rpt"]
def fetch(name):
    if (out/name).exists():
        data=(out/name).read_bytes()
        return {"file":name,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"url":f"https://github.com/kebag-logic/milan-fpga/blob/{ref}/{base}/{name}"}
    info=json.loads(subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/contents/{base}/{name}?ref={ref}"]))
    data=base64.b64decode(info["content"])
    (out/name).parent.mkdir(parents=True,exist_ok=True)
    (out/name).write_bytes(data)
    return {"file":name,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"url":info["html_url"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(fetch,names))
(packet/"public-receipts.json").write_text(json.dumps(rows,indent=2)+"\n")
print("Downloaded",len(rows),"public evidence artifacts at",ref)
