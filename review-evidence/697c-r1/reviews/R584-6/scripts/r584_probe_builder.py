#!/usr/bin/env python3
"""Disposable probe builder for sw/firmware/ctrl (never committed): compiles one trivial C file with a mode
given in one driver spelling. Usage: r584_probe_builder.py plain|rsp|wp|imacros"""
import subprocess, sys, tempfile
from pathlib import Path
spelling = sys.argv[1]
work = Path(tempfile.mkdtemp(prefix="r584-probe-"))
(work / "t.c").write_text("int r584_probe;\n")
if spelling == "plain":
    args = ["-DR584_PLAIN_MODE"]
elif spelling == "rsp":
    (work / "args.rsp").write_text("-DR584_RSP_MODE\n")
    args = [f"@{work / 'args.rsp'}"]
elif spelling == "wp":
    args = ["-Wp,-DR584_WP_MODE"]
elif spelling == "imacros":
    (work / "m.h").write_text("#define R584_IMACROS_MODE 1\n")
    args = ["-imacros", str(work / "m.h")]
else:
    raise SystemExit(f"unknown spelling {spelling}")
subprocess.run(["gcc", "-std=c11", *args, "-c", str(work / "t.c"), "-o", str(work / "t.o")], check=True)
print(f"probe builder compiled with {args}")
