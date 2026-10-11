#!/usr/bin/env python3
"""Run independent focused gates concurrently, with one log and status each."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
env = {**os.environ, "TMPDIR": str(packet / "scratch/tmp"), "PYTHONDONTWRITEBYTECODE": "1", "GIT_NO_REPLACE_OBJECTS": "1"}
cases = {
    "ci-events-check": ["scripts/ci_events.py", "--check"],
    "ci-events-selftest": ["scripts/ci_events.py", "--selftest"],
    "shards-selftest": ["sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"],
    "coverage-selftest": ["sw/firmware/gtest/fw_coverage.py", "--selftest"],
    "ci-scope-selftest": ["scripts/ci_scope.py", "--selftest"],
    "docs-check": ["scripts/docs_check.py"],
    "doc-style": ["scripts/check_doc_style.py"],
    "python-idiom": ["scripts/check_py_idiom.py"],
    "em-dash": ["scripts/check_em_dash.py", "--base", "ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5"],
}


def run_case(item):
    name,args = item
    started=time.monotonic()
    with (packet/"receipts"/(name+".log")).open("w") as log:
        result=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=480)
    elapsed=time.monotonic()-started
    (packet/"receipts"/(name+".rc")).write_text(str(result.returncode)+"\n")
    print(f"{name}: rc={result.returncode}, seconds={elapsed:.3f}",flush=True)
    return {"name":name,"command":["python3",*args],"rc":result.returncode,"seconds":elapsed}


with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run_case,cases.items()))
(packet/"receipts/focused-gates.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(int(any(r["rc"] for r in results)))
