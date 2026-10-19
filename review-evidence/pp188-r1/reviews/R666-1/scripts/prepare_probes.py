#!/usr/bin/env python3
"""Add reviewer-owned tests to disposable copies; leave all production RTL exact."""
from pathlib import Path
import shutil
import sys

root, packet = map(Path,sys.argv[1:])
dest=packet/'scratch/probes'
for directory in ['hdl','tb/common','tb/pp_top','tb/srp_stream_fsms']:
    shutil.copytree(root/directory,dest/directory,dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('obj*','*.hex','__pycache__'))

p=dest/'tb/pp_top/sim_main.cpp'
text=p.read_text()
anchor='    as_unbind_withdraws_and_clears();'
assert text.count(anchor)==1
text=text.replace(anchor,'    review_stalled_swaps();\n'+anchor)
probe=r'''
  void review_stalled_swaps() {
    const bool stall = std::getenv("REVIEW_NO_TX_STALL") == nullptr;
    for (bool final_failed : {false, true}) {
      h2.feed(final_failed ? failed(SID_L, DA_L, VID_L, EV_JOININ)
                           : advertise(SID_L, DA_L, VID_L, EV_JOININ));
      h2.run_ms(20);
      auto before = get_rx_state(0x4B80);
      CHECK(before == rx_state_settled(0x4B80, final_failed ? 0x0042 : 0x0002),
            "REVIEW: initial declaration and GET_RX_STATE agree (failed %d)",final_failed);
      h2.mac_tx_ready = !stall;
      for (unsigned i=0; i<6; ++i) {
        h2.feed(acmp_frame(CTLR_MAC, 10, 0, 0, CTLR2_EID, 0, EID, 0, LS, 0, 0,
                           uint16_t(0x4C00+i), 0, 0));
        h2.run_ms(2);
      }
      const unsigned free = h2.snap(25) & 7u;
      const unsigned trace_begin = h2.snap(15) & 0xffffu;
      h2.feed(final_failed ? advertise(SID_L, DA_L, VID_L, EV_JOININ)
                           : failed(SID_L, DA_L, VID_L, EV_JOININ));
      h2.run_ms(2);
      const unsigned middle = tk_reg();
      h2.feed(final_failed ? failed(SID_L, DA_L, VID_L, EV_JOININ)
                           : advertise(SID_L, DA_L, VID_L, EV_JOININ));
      h2.run_ms(2);
      const unsigned latest = tk_reg();
      h2.mac_tx_ready = true;
      h2.run_ms(50);
      unsigned coalesced=0, deliveries=0;
      const unsigned trace_end=h2.snap(15)&0xffffu;
      for (unsigned i=trace_begin;i<trace_end;++i) {
        const uint32_t event=h2.trace_lane(i&255u,1);
        if ((event>>24)==LS) {++deliveries;coalesced+=(event>>16)&1u;}
      }
      CHECK(coalesced == (stall ? 1u : 0u) && deliveries == (stall ? 1u : 2u),
            "REVIEW: trace confirms pending type-event delivery (stall %d, delivered %u, coalesced %u)",
            stall,deliveries,coalesced);
      printf("REVIEW evidence: stall=%d final_failed=%d delivered=%u coalesced=%u\n",
             stall,final_failed,deliveries,coalesced);
      h2.q_acmp.clear();
      auto g = get_rx_state(0x4C80);
      CHECK((!stall || free == 1) && middle == (final_failed ? 1u : 2u)
            && latest == (final_failed ? 2u : 1u),
            "REVIEW: separate type-change frames register with four standard TX slots full "
            "and the reserved slot free (free %u, middle %u, latest %u)",free,middle,latest);
      CHECK(g == rx_state_settled(0x4C80, final_failed ? 0x0042 : 0x0002),
            "REVIEW: after TX resumes GET_RX_STATE follows latest type "
            "(registration %u, declaration %u, flags 0x%04x, expected 0x%04x)",
            tk_reg(),lstn_decl(),g.size()>65 ? unsigned(fv_u64(g,64,2)) : 0xffffu,
            final_failed ? 0x0042 : 0x0002);
      h2.feed(final_failed ? failed(SID_L, DA_L, VID_L, EV_JOININ)
                           : advertise(SID_L, DA_L, VID_L, EV_JOININ));
      h2.run_ms(500);
      g = get_rx_state(0x4C81);
      CHECK(g == rx_state_settled(0x4C81, final_failed ? 0x0042 : 0x0002),
            "REVIEW: unchanged refresh also leaves GET_RX_STATE on current type "
            "(flags 0x%04x, expected 0x%04x)",
            g.size()>65 ? unsigned(fv_u64(g,64,2)) : 0xffffu,final_failed ? 0x0042 : 0x0002);
      // Restore the precondition using individually consumed changes.
      h2.feed(failed(SID_L, DA_L, VID_L, EV_JOININ)); h2.run_ms(20);
      h2.feed(advertise(SID_L, DA_L, VID_L, EV_JOININ)); h2.run_ms(20);
      last_join=h2.now_ms();
    }
  }
'''
anchor='  // ---- AS6: UNBIND_RX'
assert text.count(anchor)==1
p.write_text(text.replace(anchor,probe+'\n'+anchor))

p=dest/'tb/srp_stream_fsms/sim_main.cpp'
text=p.read_text()
anchor='  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);'
assert text.count(anchor)==1
probe=r'''
  // Successive bindings share one old declaration debt until it is sent.
  constexpr uint64_t B=0x02AABBCCDDEE0002ull, C=0x02AABBCCDDEE0003ull;
  h.reset(); l_goto(h,QA);
  h.ctl(false,0,SID0,DA0,VID0);
  h.ctl(true,0,B,DA0,VID0); h.inject(true,1,B,DA0,VID0,3);
  h.ctl(false,0,B,DA0,VID0);
  h.ctl(true,0,C,DA0,VID0); h.inject(true,1,C,DA0,VID0,3);
  h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,5,2,SID0),"REVIEW: three-stream chain keeps original Leave");
  h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,0,2,C),"REVIEW: three-stream chain declares latest value");
  h.reset(); l_goto(h,QA);
  h.ctl(false,0,SID0,DA0,VID0); h.ctl(true,0,B,DA0,VID0);
  h.ctl(false,0,B,DA0,VID0); h.ctl(true,0,SID0,DA0,VID0);
  h.inject(true,1,SID0,DA0,VID0,3); h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,0,2,SID0),"REVIEW: return to old value rejoins its applicant");
  h.reset(); l_goto(h,QA);
  h.inject(true,2,SID0,DA0,VID0,3,0,500,0x1234,1); h.tick(); h.tick(); h.tick();
  h.ctl(false,0,SID0,DA0,VID0); h.ctl(true,0,B,DA0,VID0);
  h.inject(true,1,B,DA0,VID0,3); h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,5,1,SID0),"REVIEW: old Failed declaration keeps AskingFailed on Leave");
  h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,0,2,B),"REVIEW: new Advertise declares Ready after failed old value");
  h.reset(); l_goto(h,QA);
  h.ctl(false,0,SID0,DA0,VID0); h.ctl(true,0,B,DA0,VID0);
  h.inject(true,1,B,DA0,VID0,3); h.la_own(); h.clear_logs(); h.tick();
  CHECK(h.l_push.empty(),"REVIEW: own LeaveAll obeys LA txLA no-message action");
  h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,4,2,SID0),"REVIEW: old LO sends Empty after own LeaveAll");
  h.clear_logs(); h.tick();
  CHECK(one_listener_push(h.l_push,0,2,B),"REVIEW: new declaration follows old LO retirement");
  h.reset(); l_goto(h,QA);
  h.ctl(false,0,SID0,DA0,VID0); h.ctl(true,0,B,DA0,VID0);
  h.reset(); h.tick();
  CHECK(h.l_push.empty(),"REVIEW: reset discards stale leave-copy validity");
'''
p.write_text(text.replace(anchor,probe+'\n'+anchor))
print('Prepared test-only probes at',dest)
