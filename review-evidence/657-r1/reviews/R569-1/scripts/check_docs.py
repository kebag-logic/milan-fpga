#!/usr/bin/env python3
"""Focused read-only source and documentation gates."""
import argparse, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser(); p.add_argument("--source",type=pathlib.Path,required=True); p.add_argument("--python",required=True)
a=p.parse_args(); packet=pathlib.Path(__file__).resolve().parents[1]
checks=["scripts/docs_check.py", "scripts/check_doc_style.py", "scripts/check_doc_paths.py", "scripts/check_cpp_idiom.py", "scripts/check_py_idiom.py", "scripts/gen_toc.py --check", "scripts/gen_toc.py --verify-anchors", "scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee"]
results=[]; env=os.environ.copy(); env["TMPDIR"]=str(packet/"scratch"); env["PYTHONDONTWRITEBYTECODE"]="1"
for i,cmd in enumerate(checks):
    start=time.monotonic(); argv=[a.python,"-B"]+cmd.split()
    r=subprocess.run(argv,cwd=a.source,env=env,capture_output=True,text=True)
    (packet/"receipts"/f"docs-{i+1}.log").write_text(r.stdout+r.stderr)
    results.append({"command":"python3 -B "+cmd,"rc":r.returncode,"seconds":time.monotonic()-start})
    print(cmd, r.returncode, flush=True)
(packet/"receipts/docs-local.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(int(any(r["rc"] for r in results)))
