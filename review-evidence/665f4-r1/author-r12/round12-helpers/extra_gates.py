import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
commands=[
 ("nvm-campaign",["python3","sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py","--require-rv32","--self-test","--jobs","4"]),
 ("maap-diff",["python3","sw/firmware/ctrl/test/maap_differential.py","--self-test","--keep",str(r/"maap-diff")]),
 ("image-selftest",["python3","sw/firmware/ctrl/test/ctrl_image_selftest.py","--require-rv32"])]
for label,command in commands:
 subprocess.run([sys.executable,str(r/"run.py"),label,*command],check=True)
subprocess.run([sys.executable,str(r/"shared.py")],check=True)
