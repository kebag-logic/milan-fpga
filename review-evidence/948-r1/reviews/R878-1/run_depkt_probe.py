#!/usr/bin/env python3
import os,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent;r=pathlib.Path(sys.argv[1]).resolve();v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
cmd=[v,'--cc','--exe','--build','-j','4','-Wno-fatal','--top-module','KL_aaf_rx_depacketizer','-GN_STREAMS_P=8','-GPAY_LEAD_CYC_P=16','--Mdir',str(p/'scratch/obj_depkt'),str(r/'hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv'),str(p/'probe_depkt.cpp')]
with (p/'depkt-build.log').open('w') as f:
 f.write(repr(cmd)+'\n');f.flush();b=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
(p/'depkt-build.rc').write_text(str(b.returncode)+'\n')
if b.returncode:sys.exit(b.returncode)
with (p/'depkt-probe.log').open('w') as f:b=subprocess.run([str(p/'scratch/obj_depkt/VKL_aaf_rx_depacketizer')],stdout=f,stderr=subprocess.STDOUT)
(p/'depkt-probe.rc').write_text(str(b.returncode)+'\n');print((p/'depkt-probe.log').read_text());sys.exit(b.returncode)
