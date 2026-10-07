#!/usr/bin/env python3
"""Focused composition gates; two foreground workers, distinct receipts."""
import concurrent.futures, pathlib, subprocess, sys
packet=pathlib.Path(__file__).resolve().parents[1]
py=str(packet/"scratch/docs-venv/bin/python3")
gates={
 "docs-check":["scripts/docs_check.py"],
 "toc-check":["scripts/gen_toc.py","--check"],
 "toc-anchors":["scripts/gen_toc.py","--verify-anchors"],
 "em-dash":["scripts/check_em_dash.py","--base","64e62816ad21791f6df3657fadb935aec5555881"],
 "ci-events":["scripts/ci_events.py","--check"],
 "ci-events-selftest":["scripts/ci_events.py","--selftest"],
 "mailbox-contract":["sw/mailbox/gen_mailbox.py","--check","--crosscheck"],
 "mailbox-selftest":["sw/mailbox/gen_mailbox.py","--selftest"],
 "nvm-record-space":["scripts/check_nvm_record_space.py","--quiet"],
 "feature-status":["scripts/check_feature_status.py"],
}
def run(item):
 name,args=item
 return subprocess.run([sys.executable,str(packet/"scripts/run_receipt.py"),"--repo",str(pathlib.Path.cwd()),"--packet",str(packet),name,py,*args]).returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 codes=list(pool.map(run,gates.items()))
raise SystemExit(any(codes))
