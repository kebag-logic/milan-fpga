#!/usr/bin/env python3
"""Reuse the clean shipping model to cross the pending batch's 32-bit boundary."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('packet',type=Path);a=ap.parse_args()
    root=a.root.resolve();packet=a.packet.resolve();base=packet/'scratch/frames-only-1';work=packet/'scratch/batch-wrap'
    work.mkdir(parents=True,exist_ok=True)
    shutil.copytree(base/'obj',work/'obj',dirs_exist_ok=True)
    cpp=root/'tb/verilator/milan_dp/sim_nxn.cpp'
    source=cpp.read_text().replace('../../common/verilator_harness.hpp',str(root/'tb/common/verilator_harness.hpp'))
    (work/'sim_nxn.cpp').write_text(source)
    hdr=(root/'tb/verilator/milan_dp/stream_counters.hpp').read_text()
    assert hdr.count('=65534;')==1 and hdr.count(']),65537);')==1
    hdr=hdr.replace('=65534;','=UINT32_MAX-1u;').replace(']),65537);',']),1);')
    hdr=hdr.replace('batch crosses 65535 without loss','pending 32-bit batch wraps MAX-1 plus three to one')
    (work/'stream_counters.hpp').write_text(hdr)
    makefile=work/'obj/Vmilan_datapath.mk'
    makefile.write_text(makefile.read_text().replace(str(cpp),str(work/'sim_nxn.cpp')))
    (work/'obj/sim_nxn.o').unlink()
    with (packet/'receipts/batch-wrap.build.log').open('w') as log:
        subprocess.run(['make','-j16','-f','Vmilan_datapath.mk'],cwd=work/'obj',stdout=log,stderr=subprocess.STDOUT,check=True)
    with (packet/'receipts/batch-wrap.run.log').open('w') as log:
        r=subprocess.run([str(work/'obj/stream_counters')],cwd=base/'tb/verilator/milan_dp',stdout=log,stderr=subprocess.STDOUT)
    (packet/'receipts/batch-wrap.rc').write_text(str(r.returncode)+'\n')
    text=(packet/'receipts/batch-wrap.run.log').read_text()
    assert r.returncode==0 and 'pending 32-bit batch wraps MAX-1 plus three to one' in text
    print('PASS: 32-bit pending batch wraps to one after three real AVTPDUs')

if __name__=='__main__':main()
