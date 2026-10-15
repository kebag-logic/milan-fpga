"""Probe P2: run real steps under the head's seccomp exec audit (audit_step) on the host, and print
each step's findings.

Usage: python3 -I p2_trace.py <checkout> <scratch>
Steps run in a scratch root (no inventory, so every file there is "read by the walker").
The system-directory case points one extra system root at a writable stand-in for /usr/local/,
since the image's docs-check steps run as root and may write there; nothing else is changed."""
import json, os, shutil, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
shutil.rmtree(scratch, ignore_errors=True)
work = scratch / "root"; work.mkdir(parents=True)
fake = scratch / "usr-local"; (fake / "bin").mkdir(parents=True)
sys.path.insert(0, str(root / "ci/image"))
import exec_audit as A
A.SYSTEM_ROOTS = (*A.SYSTEM_ROOTS, f"{fake}/")
names = A.allowlist()
env = {"PATH": os.environ["PATH"], "HOME": str(scratch), "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
steps = [
  ("perl -e inline, unpinned", "perl -e 'print qq(PERL-E-RAN\\n)'"),
  ("perl -le inline, unpinned", "perl -le 'print q(PERL-LE-RAN)'"),
  ("node -e inline, unpinned", "node -e 'console.log(\"NODE-E-RAN\")'"),
  ("control: bash -c unpinned (nested)", "bash -c 'echo NESTED-BASH-RAN'"),
  ("control: appended copy under /tmp-like path", f"cp /usr/bin/printenv {work}/zz_appended && printf '\\0' >> {work}/zz_appended && {work}/zz_appended HOME"),
  ("appended copy under a system root with a listed name", f"cp /usr/bin/printenv {fake}/bin/cp && printf '\\0' >> {fake}/bin/cp && {fake}/bin/cp HOME"),
]
for label, text in steps:
    entry = {"job": "probe", "label": label, "argv": ["bash", "-c", text], "text": text, "working-directory": "."}
    out = A.audit_step(entry, names, work, env)
    print(json.dumps({"step": label, "exit": out["exit_status"], "clean": out["clean"],
                      "findings": [f["reason"] for f in out["findings"]],
                      "provenance": sorted({r["provenance"] for r in out["population"]})}), flush=True)
