"""Probe P5: a program outside the image whose file name is an interpreter's, under the head's audit.
(a) a copy of the host's bash, renamed dash, given an unpinned -c program;
(b) a non-interpreter binary (a copy of true with a byte appended) named python3, given a checkout script;
(c) control: the same appended copy under its own name.
Usage: python3 -I p5_interp_named.py <checkout> <scratch>"""
import json, os, shutil, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); base = Path(sys.argv[2]).resolve()
shutil.rmtree(base, ignore_errors=True); (base / "bin").mkdir(parents=True)
(base / "tool.py").write_text("print('checkout script')\n")   # present when the job starts: a checkout file
sys.path.insert(0, str(root / "ci/image"))
import exec_audit as A
names = A.allowlist()
env = {"PATH": os.environ["PATH"], "HOME": str(base), "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
steps = [
  ("(a) bash copied and renamed dash runs an unpinned -c program",
   f"cp /usr/bin/bash {base}/bin/dash && {base}/bin/dash -c 'echo RENAMED-BASH-RAN; shopt -s extglob; echo $BASH_VERSION'"),
  ("(b) unprovenanced binary named python3 given a checkout script",
   f"cp /usr/bin/true {base}/bin/python3 && printf '\\0' >> {base}/bin/python3 && {base}/bin/python3 {base}/tool.py"),
  ("(c) control: the same appended copy under its own name",
   f"cp /usr/bin/printenv {base}/bin/zz_appended && printf '\\0' >> {base}/bin/zz_appended && {base}/bin/zz_appended HOME"),
]
for label, text in steps:
    r = A.audit_step({"job": "probe", "label": label, "argv": ["bash", "-e", "-c", text], "text": text}, names, base, env)
    print(json.dumps({"step": label, "clean": r["clean"], "findings": [f["reason"] for f in r["findings"]],
                      "rows": [(x["kind"], x["invocation"], x["provenance"]) for x in r["population"]]}), flush=True)
