#!/usr/bin/env python3
"""Independent boundary and destination-identity probes, in a disposable tree."""
import argparse,json,os,pathlib,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--simulator",required=True);a=p.parse_args();packet=a.packet.resolve()
tree=packet/"scratch/extra-boundaries"
shutil.copytree(packet/"scratch/head",tree,dirs_exist_ok=True)
cpp=tree/"tb/aecp_notify/sim_main.cpp";s=cpp.read_text()
s=s.replace("    uint64_t mac = 0;", "    uint64_t mac = 0;\n    uint64_t eid = 0;")
s=s.replace("d->uns_seq_o, d->uns_mac_o};", "d->uns_seq_o, d->uns_mac_o, d->uns_ctlr_eid_o};")
s=s.replace("&& j.arg1 == want.arg1 && j.seq == want.seq;", "&& j.arg1 == want.arg1 && j.seq == want.seq\n           && j.eid == (mac == Harness::MAC_C ? Harness::EID_C : 0x4444000000000004ull);")
s=s.replace("  void dereg_counter_round();", "  void review_boundaries();\n  void dereg_counter_round();")
s=s.replace("  dereg_round_waits();", "  dereg_round_waits();\n  review_boundaries();")
extra=r'''
void Harness::review_boundaries() {
  constexpr uint64_t EID_D = 0x4444000000000004ull;
  constexpr uint64_t MAC_D = 0x020000000004ull;
  const UnsJob own0{0, KIND_DEREG, 0, 0, 0, 0, 0, 0};
  const UnsJob own1{0, KIND_DEREG, 0, 0, 0, 0, 1, 0};
  // The last row is removed before its round job; N_EMIT_RD ends by skip.
  warm_reset(); d->uns_done_i=0; now=40000;
  register_row(EID_C, MAC_C, false); register_row(EID_D, MAC_D, true);
  counter_change(); (void)job_presented(now+WALK_MS);
  expire(REGMON_BASE+1, OWN_TL+1); (void)retire();
  auto rest=sent_at_once(now+8*WALK_MS); print_jobs("RB1",rest);
  CHECK(rest.size()==1 && one_job(rest,MAC_D,own0),
        "RB1: last row drained before service; skip ends round and sends its own seq0 DEREGISTER");
  // Both rows expire while the first job waits. The second parked row remains
  // valid until the first held deregistration can leave, and is then removed.
  warm_reset(); d->uns_done_i=0; now=45000;
  register_row(EID_C, MAC_C, true); register_row(EID_D, MAC_D, true);
  counter_change(); (void)job_presented(now+WALK_MS);
  expire(REGMON_BASE, OWN_TL); expire(REGMON_BASE+1, OWN_TL+1); (void)retire();
  rest=sent_at_once(now+12*WALK_MS); print_jobs("RB2",rest);
  std::vector<UnsJob> deregs, counters;
  for(const auto& j:rest) (j.kind==KIND_DEREG?deregs:counters).push_back(j);
  const UnsJob round{0,KIND_CTRS,DT_AVB_INTERFACE,0,0,0,0,0};
  CHECK(rest.size()==3 && counters.size()==1 && one_job(counters,MAC_D,round)
        && deregs.size()==2 && one_job(deregs,MAC_C,own1) && one_job(deregs,MAC_D,own1),
        "RB2: two pending removals preserve surviving round job and both targeted identities/sequences");
  // Command requester exclusion must survive the drain and end by skip.
  warm_reset(); d->uns_done_i=0; now=50000;
  register_row(EID_C, MAC_C, true); register_row(EID_D, MAC_D, false);
  d->ev_cmd_class_i=7; d->ev_cmd_type_i=0x0005; d->ev_cmd_index_i=1;
  d->ev_cmd_arg0_i=2; d->ev_cmd_arg1_i=3; d->ev_cmd_excl_eid_i=EID_D;
  d->ev_cmd_i=1; tick(); d->ev_cmd_i=0; ++now;
  (void)job_presented(now+WALK_MS); expire(REGMON_BASE, OWN_TL); (void)retire();
  rest=sent_at_once(now+8*WALK_MS); print_jobs("RB3",rest);
  CHECK(rest.size()==1 && one_job(rest,MAC_C,own1),
        "RB3: requester exclusion survives drain; skipped last row releases targeted DEREGISTER");
  d->uns_done_i=1;
}
'''
s=s.replace("#else\n// ---- FT:",extra+"\n#else\n// ---- FT:")
assert "void Harness::review_boundaries()" in s
cpp.write_text(s)
subprocess.run(["diff","-u","--label","a/tb/aecp_notify/sim_main.cpp","--label","b/tb/aecp_notify/sim_main.cpp",str(packet/"scratch/head/tb/aecp_notify/sim_main.cpp"),str(cpp)],stdout=(packet/"receipts/extra-boundaries.patch").open("w"))
env=os.environ.copy();env.update(TMPDIR=str(packet/"scratch"),MAKEFLAGS="-j16",REVIEW_SIMULATOR=str(pathlib.Path(a.simulator).resolve()))
with (packet/"receipts/extra-boundaries.log").open("w") as f:
 r=subprocess.run(["make","-j16","run","VERILATOR="+str(packet/"scripts/simulator-bounded.py")],cwd=tree/"tb/aecp_notify",env=env,stdout=f,stderr=subprocess.STDOUT)
(packet/"receipts/extra-boundaries.rc").write_text(str(r.returncode)+"\n")
print("boundary probe rc",r.returncode);assert r.returncode==0
