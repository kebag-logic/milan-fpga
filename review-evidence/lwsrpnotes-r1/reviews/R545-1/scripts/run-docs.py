#!/usr/bin/env python3
"""Run independent documentation checks concurrently, staying in the foreground."""
import concurrent.futures, os, subprocess, sys
from pathlib import Path
packet=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
checks=[("sentences",["python3","doc/tools/check_sentences.py"]),
        ("references",["python3","doc/tools/check_references.py"]),
        ("reference-selftest",["python3","doc/tools/check_references.py","--self-test"]),
        ("links-public",["python3","doc/tools/check_links.py"]),
        ("links-auth",["python3","doc/tools/check_links.py","--github-auth"]),
        ("graphs",["python3","doc/tools/render_mermaid.py","--output",str(packet/"scratch"/"graphs"),"--puppeteer-config",str(packet/"scratch"/"puppeteer.json")])]
def run(item):
    name,cmd=item
    return subprocess.run([sys.executable,str(packet/"scripts"/"record.py"),"--name","docs-"+name,"--cwd",str(repo),"--",*cmd]).returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results=list(pool.map(run,checks))
raise SystemExit(int(any(results)))
