import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
for name in ("builder_bank.py","compiler_gates.py"):
 subprocess.run([sys.executable,str(r/name)],cwd=r/"builder-tree",check=True)
