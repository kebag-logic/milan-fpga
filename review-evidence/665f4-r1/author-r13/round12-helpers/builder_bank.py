from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parent
command=[sys.executable,str(r/"run.py"),"builder","env","MAKEFLAGS=-j8","python3","sw/builder/test_builder.py","--require-rv32"]
subprocess.run(command,cwd=r/"builder-tree",check=True)
