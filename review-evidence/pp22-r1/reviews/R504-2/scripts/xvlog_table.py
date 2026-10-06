#!/usr/bin/env python3
"""Per-file xvlog analysis over the processor's derived source list at one commit.

Usage: xvlog_table.py <repo> <commit> <export_root> <out.json> [--define SYNTHESIS]

The list is derived the way the consumer's pp_srcs.py derives it: tracked hdl/**/*.sv
at <commit>, files that declare a package first (sorted), then the rest (sorted).
A fresh work library; one `xvlog -sv --work work <file>` invocation per file.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

XVLOG = os.environ.get("XVLOG", "xvlog")  # set XVLOG to the analysis binary
repo, commit, exp, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve(), Path(sys.argv[4])
defines = sys.argv[sys.argv.index("--define") + 1:sys.argv.index("--define") + 2] if "--define" in sys.argv else []

ls = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit, "--", "hdl"], cwd=repo,
                    capture_output=True, text=True, check=True).stdout.split()
files = [f for f in ls if f.endswith(".sv")]
pkg_re = re.compile(r"^\s*package\s+\w+\s*;", re.M)
pkgs = sorted(f for f in files if pkg_re.search((exp / f).read_text()))
rest = sorted(f for f in files if not pkg_re.search((exp / f).read_text()))
rows = []
with tempfile.TemporaryDirectory(prefix="r504-xvlog-") as wd:
    # every xvlog call, this one included, runs in the scratch work dir: xvlog
    # writes xvlog.pb/xvlog.log into its cwd
    version = subprocess.run([XVLOG, "--version"], cwd=wd, capture_output=True, text=True).stdout.strip()
    for f in pkgs + rest:
        cmd = [XVLOG, "-sv", "--work", "work"]
        for d in defines:
            cmd += ["-d", d]
        cmd.append(str(exp / f))
        r = subprocess.run(cmd, cwd=wd, capture_output=True, text=True)
        txt = r.stdout + r.stderr
        errs = [l for l in txt.splitlines() if l.startswith("ERROR")]
        rows.append({"file": f, "rc": r.returncode,
                     "VRFC 10-3380": txt.count("VRFC 10-3380"),
                     "VRFC 10-8530": txt.count("VRFC 10-8530"),
                     "errors": [re.sub(r"\[/[^\]]*/(hdl/[^\]]+)\]", r"[\1]", e) for e in errs]})
summary = {"commit": commit, "defines": defines, "files": len(rows), "packages": len(pkgs),
           "rc_nonzero": sum(1 for r in rows if r["rc"]),
           "VRFC 10-3380": sum(r["VRFC 10-3380"] for r in rows),
           "VRFC 10-8530": sum(r["VRFC 10-8530"] for r in rows),
           "xvlog": version}
out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=1) + "\n")
print(json.dumps(summary))
for r in rows:
    if r["rc"] or r["VRFC 10-3380"] or r["VRFC 10-8530"]:
        print("NONZERO", r["file"], r["rc"], r["errors"][:3])
sys.exit(1 if summary["rc_nonzero"] else 0)
