#!/usr/bin/env python3
"""Show the head firmware passes a peer that also refuses registers 4 and 0, and
that the surviving NAK mutants then fail. usage: phy_nak_probe.py <repo> <work> <patched phy_host.c>"""
import re, shutil, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); root=Path(sys.argv[2]).resolve(); drv=Path(sys.argv[3]).resolve()
sys.path.insert(0,str(repo/'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as nvm, test_phy_firmware as phy
G="\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 0;\n"
cases={'head':None,'nak-reg4-unguarded':(G,"\tif (gigabit < 0 || control < 0)\n\t\treturn 0;\n"),'nak-reg0-unguarded':(G,"\tif (advertisement < 0 || gigabit < 0)\n\t\treturn 0;\n")}
if root.exists(): shutil.rmtree(root)
src=nvm.FENCE_RE.sub("(void)0;",nvm.FIRMWARE.read_text())
for n,c in cases.items():
    w=root/n; w.mkdir(parents=True)
    nvm.make_bench(repo/'configs/endstation_ax7101_1x1_tdm8.yaml',w,nvm.FIRMWARE.read_text()); phy.phy_csr(w)
    (w/'milan_baremetal.c').write_text(src.replace(*c) if c else src)
    d=w/'phy_host.c'; shutil.copy(drv,d); shutil.copy(repo/'sw/firmware/nvm_hosttest/phy_peer.h',w/'phy_peer.h')
    subprocess.run(["gcc","-std=gnu11","-O1","-Wall","-Wextra","-Wno-format","-ffunction-sections","-fdata-sections","-Wl,--gc-sections",f"-I{w}",f"-I{nvm.STUBS}",str(d),"-o",str(w/'phy')],check=True,capture_output=True,timeout=180)
    r=subprocess.run([str(w/'phy')],capture_output=True,text=True,timeout=120)
    a=re.search(r"Assertion `(.*?)' failed",r.stderr)
    print(f"NAKPROBE {n}: rc={r.returncode} {a[1] if a else 'PHY_OK' if 'PHY_OK' in r.stdout else ''}",flush=True)
