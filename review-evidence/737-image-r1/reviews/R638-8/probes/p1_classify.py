"""Probe P1: how the head's exec audit judges interpreter invocations (no exec; the head's own
Origin.judge and judge() over hand-built instances, as _Trace.admit would pass them).

Usage: python3 -I p1_classify.py <checkout> <scratch-root>"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]); scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "ci/image"))
import exec_audit as A
names = A.allowlist()
origin = A.Origin(scratch, names, watch=False)
cases = {
  "perl -e":          ["perl", "-e", "print 1"],
  "perl -le":         ["perl", "-le", "print 1"],
  "perl -E":          ["perl", "-E", "say 1"],
  "node -e":          ["node", "-e", "console.log(1)"],
  "node --eval=":     ["node", "--eval=console.log(1)"],
  "python3 -c (ctl)": ["python3", "-c", "print(2)"],
  "bash -c (ctl)":    ["bash", "-c", "echo unpinned-xyz"],
}
for label, argv in cases.items():
    prog = "/usr/bin/" + argv[0]
    inst = {"pid": 1, "file": prog, "program": prog, "argv": argv, "directory": str(scratch),
            "streams": {"0": "/dev/null", "1": "pipe:[1]"}}
    inst["provenance"] = origin.judge(inst)
    what = A.invocation(inst)
    _, findings = A.judge({"instances": [inst], "exit_status": 0}, names)
    print(json.dumps({"case": label, "kind": what["kind"], "provenance": inst["provenance"],
                      "findings": [f["reason"] for f in findings]}))
