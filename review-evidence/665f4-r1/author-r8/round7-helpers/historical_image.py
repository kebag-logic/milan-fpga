import os,sys
from pathlib import Path
root=Path.cwd()
sys.path.append(str(root/"scripts"))
sys.path.insert(0,str(Path(os.environ["SCRATCH"])/"round5/sw/firmware/ctrl/test"))
import ctrl_arms,ctrl_image,srp_arms
# The two pins have identical src tree f46e01d3bf1c753009479d32e69d00263ee124ed.
# Keep the current checkout guard, while compiling the archived Round 5 adapter.
ctrl_arms.LWSRP_REV="9197193e47a6bb1c45a56d90a18c1784123aba44"
ctrl_image.ROOT=root
ctrl_image.CTRL=root/"sw/firmware/ctrl"
srp_arms.CTRL=ctrl_image.CTRL
raise SystemExit(ctrl_image.main())
