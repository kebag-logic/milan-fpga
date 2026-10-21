// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #193: handover preserves broadcasts coincident with control or transfer.
#define main original_suite_main
#include "sim_main.cpp"
#undef main
int main(int argc,char** argv) {
  Verilated::commandArgs(argc,argv);
  const milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  Hn h(model.get());auto* d=model.get();int fails=0,checks=0;
  for(int settle=0;settle<2;++settle) for(int offset=0;offset<2;++offset)
    for(int broadcast=1;broadcast<4;++broadcast) {
      h.reset();h.ctl(true,0,SID0,DA0,VID0);h.ctl(true,5,SID0,DA0,VID0);
      h.inject(true,1,SID0,DA0,VID0,3,0,500);
      for(int n=0;n<4;++n)h.tick();
      if(h.l_app(0)!=QA || h.l_app(5)!=VO)return 2;
      h.clear_logs();
      d->ctl_valid_i=1;d->ctl_settle_i=settle;d->ctl_sink_i=0;
      d->ctl_stream_id_i=SID0+1;d->ctl_da_i=DA0+1;d->ctl_vid_i=VID0;
      if(offset)h.step();
      d->periodic_tick_i=(broadcast&1)!=0;
      d->leaveall_rx_i=(broadcast&2)?kLaListener:0;
      d->join_tick_i=1;
      h.step();h.idle(100);
      auto words=listener_words(h.l_push,SID0);
      bool pass=words=="3/2" && h.l_decl(5)==2 && h.l_decl(0)==0;
      ++checks;fails+=!pass;
      printf("%s: control=%s broadcast=%d offset=%d wire-events='%s' decl=%d/%d\n",
             pass?"PASS":"FAIL",settle?"settle":"teardown",broadcast,offset,
             words.c_str(),h.l_decl(0),h.l_decl(5));
    }
  printf("%d checks: %d PASS, %d FAIL\n",checks,checks-fails,fails);
  return fails?1:0;
}
