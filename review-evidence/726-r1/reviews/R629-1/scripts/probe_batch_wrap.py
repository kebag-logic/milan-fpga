#!/usr/bin/env python3
"""Reuse the clean shipping model; seed the pending AAF batch across UINT32_MAX."""
import argparse,os,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("packet",type=Path);a=ap.parse_args()
root=a.root.resolve();packet=a.packet.resolve();work=packet/"scratch/batch-wrap";work.mkdir(exist_ok=True)
obj=packet/"scratch/clean-1-clean/obj";suite=root/"tb/verilator/milan_dp"
header=(suite/"stream_counters.hpp").read_text()
assert header.count('frx_acc_r[s]=65534;')==1
header=header.replace('frx_acc_r[s]=65534;','frx_acc_r[s]=UINT32_MAX-1u;')
header=header.replace('"batch crosses 65535 without loss"','"pending batch wraps UINT32_MAX with three real packets"').replace('65537);','1);')
source=(suite/"sim_nxn.cpp").read_text().replace('#include "stream_counters.hpp"',header)
source=source.replace('#include "../../common/verilator_harness.hpp"','#include "'+str(root/"tb/common/verilator_harness.hpp")+'"')
cpp=work/"batch_wrap.cpp";cpp.write_text(source)
mk=work/"Probe.mk"
mk.write_text("include Vmilan_datapath.mk\n"+"batch_wrap.o: "+str(cpp)+"\n\t$(OBJCACHE) $(CXX) $(CXXFLAGS) $(CPPFLAGS) $(OPT_FAST) -c -o $@ $<\n"+"batch_wrap: batch_wrap.o $(VK_GLOBAL_OBJS) $(VM_PREFIX)__ALL.a\n\t$(LINK) $(LDFLAGS) $^ $(LOADLIBES) $(LDLIBS) $(LIBS) $(SC_LIBS) -o $@\n")
with (work/"build.log").open("w") as f:subprocess.run(["make","-j16","-f",str(mk),"batch_wrap"],cwd=obj,stdout=f,stderr=subprocess.STDOUT,check=True)
env=dict(os.environ);env.pop('COUNTERS_OMIT_CHECK',None)
with (packet/"receipts/batch-wrap.log").open("w") as f:r=subprocess.run([str(obj/"batch_wrap")],cwd=packet/"scratch/clean-1-clean/tb/verilator/milan_dp",env=env,stdout=f,stderr=subprocess.STDOUT)
(packet/"receipts/batch-wrap.rc").write_text(str(r.returncode)+"\n")
print("pending batch wrap probe rc",r.returncode)
raise SystemExit(r.returncode)
