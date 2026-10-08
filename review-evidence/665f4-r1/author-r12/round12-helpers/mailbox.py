import subprocess,sys,tarfile
from pathlib import Path
r=Path(__file__).resolve().parent
a=r/"mailbox-inputs.tar"
dest=r/"mailbox-tree"
dest.mkdir(exist_ok=True)
subprocess.run(["git","archive","--format=tar","--output",str(a),"HEAD","tb/verilator/mbx","tb/common","hdl/milan/mailbox","sw/firmware/ctrl","sw/firmware/ctrl_nvm","sw/mailbox"],check=True)
with tarfile.open(a) as f:f.extractall(dest,filter="data")
subprocess.run([sys.executable,str(r/"run.py"),"mailbox","make","-C","tb/verilator/mbx","-j8","VBUILD_JOBS=2"],cwd=dest,check=True)
