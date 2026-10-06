#!/usr/bin/env python3
"""Exercise the exact capture/packetizer RTL at all six output phases."""
import os, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
C=P/"scratch/tb/verilator/chmap_capture"
src=C/"sim_main.cpp"
original=src.read_text()
probe=r"""
void ChanMapCaptureHarness::lrc_span_probe() {
  printf("\n[SPAN] exact RTL: five held pops at each output packet phase\n");
  lb_set_chans(kLrcStream, 4);
  a_map_wr(1, ent_lb(1, kLrcStream, 0));
  a_map_wr(2, ent_lb(1, kLrcStream, 1));
  a_map_wr(3, ent(0, 0, 0)); a_map_wr(4, ent(0, 0, 0));
  for (int phase=0; phase<6; ++phase) {
    dut->a_lb_flush_i=0xFF; cyc(); dut->a_lb_flush_i=0; cyc(2);
    lrc_align();
    for (int k=0;k<phase;++k) a_tick();
    drv_lb_pdu(kLrcStream,4,6,1);
    for (int k=0;k<6;++k) a_tick();
    cyc(400); afr.clear();
    const long dup0=dut->a_dup_cnt_o, skip0=dut->a_skip_cnt_o;
    lrc_pulse();
    drv_lb_pdu(kLrcStream,4,6,7);
    for (int k=0;k<6;++k) a_tick();
    drv_lb_pdu(kLrcStream,4,6,13);
    for (int k=0;k<6;++k) a_tick();
    cyc(400);
    int last=6-phase, affected=0, repeats=0;
    unsigned packet=0;
    for (const auto& frame:afr) {
      if(frame.size()!=234) continue;
      int packet_repeats=0;
      printf("SPAN phase=%d pdu=%u samples=",phase,packet++);
      for(int s=0;s<6;++s) {
        int event=static_cast<int>(be(frame,42+32*s,3)&0xF);
        if(event==last) ++packet_repeats;
        printf("%s%d",s?",":"",event);
        last=event;
      }
      printf(" repeats=%d\n",packet_repeats);
      if(packet_repeats) ++affected;
      repeats+=packet_repeats;
    }
    printf("SPAN RESULT phase=%d affected_output_pdus=%d repeated_events=%d dup_delta=%ld skip_delta=%ld\n",phase,affected,repeats,static_cast<long>(dut->a_dup_cnt_o)-dup0,static_cast<long>(dut->a_skip_cnt_o)-skip0);
    ck("SPAN: exact declared five repeated events",repeats,5);
    ck("SPAN: no duplicate slip count",static_cast<long>(dut->a_dup_cnt_o)-dup0,0);
    ck("SPAN: no skip slip count",static_cast<long>(dut->a_skip_cnt_o)-skip0,0);
    ck("SPAN: declaration stays inside one output PDU",affected,1);
  }
}
"""
text=original.replace("  void lrc_align();","  void lrc_align();\n  void lrc_span_probe();")
text=text.replace("  pin_starved_pair_pegs_and_holds();","  lrc_span_probe();")
text=text.replace("void ChanMapCaptureHarness::pin_starved_pair_pegs_and_holds() {",probe+"\nvoid ChanMapCaptureHarness::pin_starved_pair_pegs_and_holds() {")
assert text!=original
src.write_text(text)
try:
  env=dict(os.environ,MAKEFLAGS="-j16")
  cmd=["make","-j16","-C","obj_dir","-f","Vchmap_wrap.mk"]
  with (P/"receipts/span-build.log").open("w") as log:
    print("COMMAND",cmd,file=log,flush=True)
    rc=subprocess.run(cmd,cwd=C,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
  (P/"receipts/span-build.rc").write_text(str(rc)+"\n")
  if rc: raise SystemExit(rc)
  with (P/"receipts/span-probe.log").open("w") as log:
    rc=subprocess.run(["./obj_dir/Vchmap_wrap"],cwd=C,stdout=log,stderr=subprocess.STDOUT).returncode
  (P/"receipts/span-probe.rc").write_text(str(rc)+"\n")
  print("span probe RTL verdict",rc,flush=True)
finally:
  src.write_text(original)
