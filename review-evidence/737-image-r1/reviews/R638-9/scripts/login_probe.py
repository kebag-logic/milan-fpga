#!/usr/bin/env python3
"""Disposable reviewer probe: run the reviewed audit (audit_step) on the host for one step in which a shell
is started with a leading '-' in argv[0] (bash's `exec -l`), so it reads login start files before its
pinned inline program. Reports the audit verdict and whether the start file ran.

Usage: python3 -I login_probe.py <checkout> <scratch-dir>
"""
import hashlib, json, sys
from pathlib import Path

checkout, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "ci/image"))
import exec_audit  # noqa: E402

root, home = scratch / "checkout", scratch / "home"
root.mkdir(parents=True); home.mkdir()
marker = scratch / "profile-ran"
(home / ".bash_profile").write_text(f"touch {marker}\n")
inner = "echo program ran"
outer = f"exec -l bash -c '{inner}'"
names = exec_audit.allowlist()
names["inline_programs"] = {hashlib.sha256(inner.encode()).hexdigest(): {"interpreter": "shell", "text": inner}}
origin = exec_audit.Origin(root, names, scratch=(str(scratch),))
try:
    result = exec_audit.audit_step({"job": "probe", "label": "login", "argv": ["bash", "-c", outer], "text": outer},
                                   names, root, {"PATH": "/usr/bin:/bin", "HOME": str(home)}, origin=origin)
finally:
    origin.close()
summary = {"step": outer, "clean": result["clean"], "findings": result["findings"],
           "population": [r for r in result["population"] if r["kind"] != "program"],
           "start_file_ran": marker.exists()}
print(json.dumps(summary, indent=1))
