#!/usr/bin/env python3
"""refusal_spot.py CHECKOUT: the refusal's two lasting checks against planted defects, in a disposable checkout. refusal-removed
must fail ctrl_image_selftest; refusal-always must leave stopped_at_link false for the boundary gate's run."""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); f = root / 'sw/firmware/ctrl/test/ctrl_plat_image.py'; text = f.read_text()
GUARD = 'if flash_map is None and any(path.exists() for path in archives):'
assert text.count(GUARD) == 1
code = ("import sys,subprocess; from pathlib import Path; sys.path.insert(0,'sw/firmware/ctrl/test'); import ctrl_runs,tempfile\n"
        "w=Path(tempfile.mkdtemp()); r=[x for x in ctrl_runs.image_runs(w) if 'ctrl_plat_image' in x[0]][0]\n"
        "res=subprocess.run(r[1],cwd='.',capture_output=True,text=True); print('exit',res.returncode,'stopped_at_link',ctrl_runs.stopped_at_link(r[1],res))")
def st(): 
    d = subprocess.run([sys.executable,'-B','sw/firmware/ctrl/test/ctrl_image_selftest.py','--require-rv32'],cwd=root,capture_output=True,text=True)
    return d.returncode, ((d.stdout+d.stderr).strip().splitlines() or [''])[-1][:130]
def stopped():
    d = subprocess.run([sys.executable,'-B','-c',code],cwd=root,capture_output=True,text=True); return (d.stdout+d.stderr).strip().splitlines()[-1][:130]
print('head: selftest', st(), '|', stopped())
try:
    f.write_text(text.replace(GUARD,'if False:')); print('refusal-removed: selftest', st())
    f.write_text(text.replace(GUARD,'if flash_map is None:')); print('refusal-always: boundary run', stopped())
finally:
    f.write_text(text)
