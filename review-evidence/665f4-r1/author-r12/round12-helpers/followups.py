import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
jobs=[
 ("asan-final",["python3",str(r/"asan.py")]),
 ("new-plants-final",["python3",str(r/"new_plants.py")]),
 ("images-final",["python3",str(r/"images.py")]),
 ("f3-images",["python3","sw/firmware/ctrl/test/ctrl_image.py","--out",str(r/"f3-images")]),
 ("review11-final",["python3",str(r/"review11.py")]),
 ("review12-final",["python3",str(r/"review12.py")]),
 ("reviewer-probes",["python3",str(r/"review_probes.py")]),
 ("binding-probe",["python3",str(r/"binding_required.py")]),
 ("park-check",["python3",str(r/"park_check.py")]),
 ("reentry-oracle",["python3",str(r/"reentry_oracle.py")]),
 ("bound-table",["python3",str(r/"check_bounds.py")]),
 ("ci-scope",["python3","scripts/ci_scope.py","--selftest"]),
]
for label,command in jobs:
 subprocess.run([sys.executable,str(r/"run.py"),label,*command],check=True)
