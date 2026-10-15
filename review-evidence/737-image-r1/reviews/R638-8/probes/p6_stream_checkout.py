"""Probe P6: a shell program streamed from an unchanged checkout file (`bash < file`, `bash -s < file`),
under the head's audit. The docs list "a file in the checkout, unchanged since the job started" among
accepted program texts. Usage: python3 -I p6_stream_checkout.py <checkout> <scratch>"""
import json, os, shutil, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); base = Path(sys.argv[2]).resolve()
shutil.rmtree(base, ignore_errors=True); base.mkdir(parents=True)
(base / "run.sh").write_text("echo STREAMED-CHECKOUT-RAN\n")   # present when the job starts
sys.path.insert(0, str(root / "ci/image"))
import exec_audit as A
names = A.allowlist()
env = {"PATH": os.environ["PATH"], "HOME": str(base), "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
for label, text in (("bash < checkout file", f"bash < {base}/run.sh"), ("bash -s < checkout file", f"bash -s < {base}/run.sh"),
                    ("control: bash checkout file", f"bash {base}/run.sh")):
    r = A.audit_step({"job": "probe", "label": label, "argv": ["bash", "-e", "-c", text], "text": text}, names, base, env)
    print(json.dumps({"step": label, "clean": r["clean"], "findings": [f["reason"] for f in r["findings"]]}), flush=True)
