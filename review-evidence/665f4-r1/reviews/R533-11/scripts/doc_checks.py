#!/usr/bin/env python3
"""Run focused documentation and contract gates with caller-selected Python."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p=Path(__file__).resolve().parents[1]
os.environ["TMPDIR"]=str(p/"scratch")
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
commands=[
    [sys.executable,"sw/mailbox/gen_mailbox.py","--check"],
    [sys.executable,"scripts/docs_check.py"],
    [sys.executable,"scripts/check_doc_style.py"],
    [sys.executable,"scripts/check_cpp_idiom.py"],
    [sys.executable,"scripts/check_py_idiom.py"],
    [sys.executable,"scripts/check_submodule_docs.py"],
    [sys.executable,"scripts/check_em_dash.py","--base","d8b355fe0f41d49dca6cae1cd8b3826e2edde364"],
    ["git","diff","--check","d8b355fe0f41d49dca6cae1cd8b3826e2edde364..HEAD"],
]
results=[]
for n,command in enumerate(commands):
    start=time.monotonic()
    with (p/"receipts"/f"docs-{n}.log").open("w") as log:
        rc=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT).returncode
    (p/"receipts"/f"docs-{n}.rc").write_text(str(rc)+"\n")
    results.append({"command":command,"rc":rc,"seconds":round(time.monotonic()-start,3)})
(p/"receipts/docs.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
raise SystemExit(int(any(r["rc"] for r in results)))
