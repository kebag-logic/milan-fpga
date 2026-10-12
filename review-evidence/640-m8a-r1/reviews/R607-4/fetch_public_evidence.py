#!/usr/bin/env python3
"""Download only selected public executable receipts, never review reports or handoffs."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess, sys
out=pathlib.Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
ref="b68338bfdaf0535576335d7fae6a877c2bbe6d7d"
root="review-evidence/640-m8a-r1/"
paths=[
"author/evidence-m81/ctrl_memory_ooc.tsv",
"author/evidence-m81/ctrl_memory_plan.json",
"author/evidence-m81/map.rc",
"author/evidence-m81/map-receipts.sha256",
"author/evidence-m81/digest-ax7101.txt",
"author/evidence-m81/digest-ax8x8.txt",
"author/evidence-m81/gates-final-summary.tsv",
"author/evidence-m81/gates-long-summary.tsv",
"author-r3/evidence-r3/gates/test_builder_elab.log",
"author-r3/evidence-r3/gates/test_ctrl_memory-ci-head-aggregate.log",
"author-r3/evidence-r3/gates/litex-sims-ci-head.log",
"author-r3/evidence-r3/gates/scripts_ci_events.py_--check.log",
"author-r3/evidence-r3/gates/scripts_ci_scope.py_--selftest.log",
"author-r3/evidence-r3/docs-parity/summary.tsv",
"author-r3/evidence-r3/rom-digest-after.txt",
"author-r3/evidence-r3/rom-digest-before.txt",
"author-r3/evidence-r3/venv-freeze.txt",
]
def get(path):
 data=json.loads(subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/contents/{root}{path}?ref={ref}"]))
 raw=base64.b64decode(data["content"])
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==data["sha"]
 target=out/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 return {"path":path,"sha256":hashlib.sha256(raw).hexdigest(),"git_blob":data["sha"],"url":data["html_url"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(get,paths))
(out/"sources.json").write_text(json.dumps(rows,indent=2)+"\n")
print(f"PASS: {len(rows)} public author receipts downloaded and Git blob hashes verified at {ref}")
