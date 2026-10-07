# SPDX-License-Identifier: Apache-2.0
"""Compile and execute independent probes without editing the source tree."""
import argparse, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument("--source",type=pathlib.Path,required=True)
p.add_argument("--packet",type=pathlib.Path,required=True)
p.add_argument("--library",type=pathlib.Path,required=True)
p.add_argument("--label",default="default")
p.add_argument("--sanitize",action="store_true")
a=p.parse_args();packet=a.packet.resolve();source=a.source.resolve();library=a.library.resolve()
exe=packet/"scratch"/("edge_probes-"+a.label)
flags=["-fsanitize=address,undefined","-fno-omit-frame-pointer"] if a.sanitize else []
cmd=["cc","-std=c11","-Wall","-Wextra","-Werror",*flags,"-I"+str(source/"src/include"),"-I"+str(source/"src"),str(packet/"scripts/edge_probes.c"),"-L"+str(library),"-lshlan","-Wl,-rpath,"+str(library),"-o",str(exe)]
runner=[sys.executable,str(packet/"scripts/run.py"),"--source",str(source),"--packet",str(packet)]
if subprocess.run([*runner,"--label","edge-build-"+a.label,"--",*cmd]).returncode:sys.exit(2)
failed=0
for case in ["controls","versions","overflow","invalid-then-valid","rejoin"]:
 r=subprocess.run([*runner,"--label","edge-"+a.label+"-"+case,"--",str(exe),case])
 failed+=r.returncode!=0
print(f"Specification discrepancies: {failed}; legal boundary controls must return zero.")
sys.exit(int(bool(failed)))
