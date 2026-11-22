#!/usr/bin/env python3
"""Create an isolated, pinned disposable clone under packet scratch.
Usage: python3 prepare_clone.py EXACT_HEAD_CLONE
"""
from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
src=Path(sys.argv[1]).resolve();dst=p/"scratch/probe"
subprocess.run(["git","clone","--shared",str(src),str(dst)],check=True)
subs=["third_party/verilog-axis","protocol-processor","gptp-processor","third_party/tsn-c-stack","third_party/lwSRP"]
args=["git","-C",str(dst),"-c","protocol.file.allow=always"]
for s in subs:args += ["-c",f"submodule.{s}.url={src/s}"]
subprocess.run(args+["submodule","update","--init",*subs],check=True)
