#!/usr/bin/env python3
"""Create a disposable exact-head clone with registered pinned submodules."""
import pathlib,subprocess,sys
repo,packet=map(pathlib.Path,sys.argv[1:3]);repo=repo.resolve();packet=packet.resolve()
dest=packet/"scratch/probe"
assert not dest.exists(), "use a new packet scratch directory"
subprocess.run(["git","clone","--shared","--no-checkout",str(repo),str(dest)],check=True)
subprocess.run(["git","-C",str(dest),"checkout","--detach","ba080007a402dced74fa74656338710e0b6cb880"],check=True)
modules=("third_party/verilog-axis","protocol-processor","gptp-processor")
for name in modules:
    subprocess.run(["git","-C",str(dest),"config",f"submodule.{name}.url",str(repo/name)],check=True)
subprocess.run(["git","-C",str(dest),"-c","protocol.file.allow=always","submodule","update","--init",*modules],check=True)
