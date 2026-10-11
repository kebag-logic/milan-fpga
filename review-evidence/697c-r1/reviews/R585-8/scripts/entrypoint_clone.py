#!/usr/bin/env python3
"""Make an isolated disposable clone and exercise 17 pin entry points under five states."""
import argparse, os, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("work",type=Path)
a=p.parse_args();root=a.checkout.resolve();work=a.work.resolve();work.mkdir(parents=True,exist_ok=True);clone=work/"checkout"
def run(cmd):subprocess.run(cmd,check=True)
run(["git","clone","--quiet","--shared","--no-checkout",str(root),str(clone)])
run(["git","-C",str(clone),"checkout","--quiet","--detach","feed95bbb6429e5af0ee3f0a24c531777279e9de"])
run(["git","-C",str(clone),"config","submodule.third_party/tsn-c-stack.url",str(root/"third_party/tsn-c-stack")])
run(["git","-C",str(clone),"-c","protocol.file.allow=always","submodule","update","--init","third_party/tsn-c-stack"])
run([sys.executable,"-B",str(Path(__file__).with_name("entrypoints.py")),str(clone),str(work/"probes")])
