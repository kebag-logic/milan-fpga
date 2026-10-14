#!/usr/bin/env python3
"""Exercise actual skipped-job names through watcher and manifest readers."""
import json,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve(); sys.path.insert(0,str(root/"scripts"))
from ci_workflow_plan import committed_plan
from ci_runtime_evidence import api_evidence
from ci_fail_fast import observe,tail_failed
from ci_gate_workflows import generate,load_template
fixture=json.loads((pathlib.Path(__file__).resolve().parent/"hosted-skipped-matrix-fixture.json").read_text())
observed_raw={job["name"] for job in fixture["jobs"] if job["conclusion"]=="skipped"}
source=committed_plan(root,"2658a64c408bf87ae36574f36a6deeb34b2f297f")
workflow=generate("rtl",load_template(root,"rtl"))
step=next(s for s in workflow["jobs"]["ci-fail-fast"]["steps"] if s.get("id")=="ci_observe")
expected=set(json.loads(step["env"]["EXPECTED_JOBS"])); skipped=json.loads(step["env"]["SKIPPED_MATRICES"])
rows=[{"name":label,"status":"completed","conclusion":"success","steps":[]} for label in sorted(expected) if not any(label in values for values in skipped.values())]
assert set(skipped).issubset(observed_raw)
print("Raw skipped labels verified against public run 38273578232; this is a shape fixture, not current-head execution.")
rows += [{"name":label,"status":"completed","conclusion":"skipped","steps":[]} for label in skipped]
print("watcher complete and first failure:",observe(rows,expected,skipped))
assert observe(rows,expected,skipped)==(True,None)
for row in rows:
 if row["name"] not in skipped:continue
 try:api_evidence(source,[row],".github/workflows/rtl.yml")
 except ValueError as exc:print("collector refuses legitimate skip:",str(exc))
 else:raise AssertionError("reproduction no longer fails")
print("collector failure requests tail cancellation:",tail_failed({"ci-manifest":{"result":"failure"}}))
print("Reproduced: allowed matrix skips fail collection and become cancellation authority.")
