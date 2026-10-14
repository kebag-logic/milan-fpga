#!/usr/bin/env python3
"""Inject exhausted API reads; no network calls or writes are made."""
import contextlib,io,json,os,pathlib,sys
from unittest.mock import patch
from urllib.error import HTTPError
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/"scripts"))
packet=pathlib.Path(__file__).resolve().parent
scratch=packet/"scratch"/"collector-observer";scratch.mkdir(parents=True,exist_ok=True)
import ci_runtime_evidence as runtime
from ci_fail_fast import API,tail_failed,observe
from ci_workflow_plan import committed_plan
source=committed_plan(root,"2658a64c408bf87ae36574f36a6deeb34b2f297f")
event=scratch/"event.json";event.write_text("{}")
for label,exc in [(str(code),HTTPError("https://invalid.example/",code,"injected exhausted read",{},None)) for code in (403,429,502)]+[("timeout",TimeoutError("injected exhausted read"))]:
 out=scratch/(label+".json");output=io.StringIO()
 with patch.dict(os.environ,{"GITHUB_EVENT_PATH":str(event),"GITHUB_EVENT_NAME":"push","GITHUB_REPOSITORY":"fixture/repo","GH_TOKEN":"fixture", "ACT":"false"}),patch.object(sys,"argv",["collector","collect","--run","1","--artifacts",str(scratch),"--output",str(out)]),patch("ci_workflow_plan.committed_plan",return_value=source),patch.object(runtime,"context_evidence",return_value=({},{},{})),patch.object(API,"request",side_effect=exc),contextlib.redirect_stderr(output):
  rc=runtime.main()
 assert rc==1 and not out.exists()
 row={"name":"Collect CI manifest","status":"completed","conclusion":"failure"}
 complete,failed=observe([row],{row["name"]})
 tail=tail_failed({"ci-manifest":{"result":"failure"}})
 assert failed==row and tail
 print(json.dumps({"injected_exhausted_read":label,"collector_exit":rc,"manifest_emitted":out.exists(),"watcher_failure":failed["name"],"tail_requests_cancellation":tail,"stderr":output.getvalue().strip()}))
print("PASS reproduction: all four observer failures become confirmed cancellation authority through the collector.")
