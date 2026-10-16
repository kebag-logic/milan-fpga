#!/usr/bin/env python3
"""Disposable reviewer probe: run the reviewed audit (audit_step) on the host for a step whose interpreter
script operand is a named pipe. The first writer supplies a checkout file's bytes, which the audit digests
by reading the pipe; a second writer then supplies the text the interpreter actually runs.

Usage: python3 -I fifo_probe.py <checkout> <scratch-dir>
"""
import json, sys
from pathlib import Path

checkout, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "ci/image"))
import exec_audit  # noqa: E402

root = scratch / "checkout"
root.mkdir(parents=True)
(root / "ok.sh").write_text("echo reviewed\n")
step = ("rm -f /tmp/zz-r638-9-fifo && mkfifo /tmp/zz-r638-9-fifo && "
        "{ printf 'echo reviewed\\n' > /tmp/zz-r638-9-fifo; sleep 2; printf 'echo UNREVIEWED-TEXT-RAN\\n' > /tmp/zz-r638-9-fifo; } & "
        "bash /tmp/zz-r638-9-fifo; wait; rm -f /tmp/zz-r638-9-fifo")
names = exec_audit.allowlist()
origin = exec_audit.Origin(root, names, scratch=(str(scratch),))
try:
    result = exec_audit.audit_step({"job": "probe", "label": "fifo", "argv": ["bash", "-c", step], "text": step},
                                   names, root, {"PATH": "/usr/bin:/bin", "HOME": str(scratch)}, origin=origin)
finally:
    origin.close()
print(json.dumps({"step": step, "clean": result["clean"], "findings": result["findings"],
                  "population": [r for r in result["population"] if r["kind"] != "program"]}, indent=1))
