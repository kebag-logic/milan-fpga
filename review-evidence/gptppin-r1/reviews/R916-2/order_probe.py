#!/usr/bin/env python3
"""Test whether the race verdict enforces the measured re-election boundary."""
import argparse,difflib,os,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("repo",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("--compiler",required=True);a=p.parse_args()
a.repo=a.repo.resolve();a.packet=a.packet.resolve();root=a.packet/"scratch/order-probe";root.mkdir()
sys.path[:0]=[str(a.repo/"tb/verilator/gptp_shadow"),str(a.repo/"scripts")]
from private_inputs import copy_inputs
from owned_process import OwnedProcesses
with OwnedProcesses() as owner: copy_inputs(a.repo,a.repo/"tb/verilator/gptp_shadow",root,owner,set())
f=root/"tb/verilator/gptp_shadow/sim_main.cpp";before=f.read_text();s=before
old="""        run_to(t0 + a1_after);
        announce(tk_seq++, 100, GMID, PEER_CID, 0x00);
        a1_due = false;"""
new="""        dut->tx_tready_i = 0;
        run_to(t0 + a1_after);
        announce(tk_seq++, 100, GMID, PEER_CID, 0x00);
        dut->tx_tready_i = 1;
        a1_due = false;"""
assert s.count(old)==1;s=s.replace(old,new)
old="""    for (size_t i : master_announces(rise ? rise : cyc))
      if (txf_cyc[i] < rise + 2 * kSyncTicks) between++;"""
new="""    for (size_t i : master_announces(rise ? rise : cyc)) {
      std::printf("ORDER PROBE: Announce last beat %llu, re-election %llu, before=%d\\n",
        static_cast<unsigned long long>(txf_cyc[i]),
        static_cast<unsigned long long>(fall), txf_cyc[i] < fall);
      if (txf_cyc[i] < rise + 2 * kSyncTicks) between++;
    }"""
assert s.count(old)==1;s=s.replace(old,new);f.write_text(s)
(a.packet/"order-probe.patch").write_text("".join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile="a/tb/verilator/gptp_shadow/sim_main.cpp",tofile="b/tb/verilator/gptp_shadow/sim_main.cpp")))
env=dict(os.environ,VERILATOR=a.compiler,VERILATOR_JOBS="5",MAKEFLAGS="",CCACHE_DISABLE="1",TMPDIR=str(a.packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
with (a.packet/"order-probe.log").open("w") as log:
 rc=subprocess.run(["make","-j16","run"],cwd=f.parent,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(a.packet/"order-probe.rc").write_text(str(rc)+"\n")
print("order probe return code:",rc)
