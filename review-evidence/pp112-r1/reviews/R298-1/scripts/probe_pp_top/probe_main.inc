// ==== R298-1 reviewer probe at protocol_processor_top: the original stale
// grant idea (previous TSpec 224 B admitted, re-declared at 20000 B which the
// 75 Mb/s ceiling refuses), driven through the real svc face. Observes the
// top-level srp_sr_admitted_o bit on every clock, relative to the SRP
// service gate acceptance (read-only probe of KL_srp_top.gate_acc_w).
static void r298_top_probe(H& h) {
  Vpp_top_wrap* d = h.d;
  unsigned pulses_total = 0;
  for (int variant = 0; variant < 2; ++variant) {       // 0: withdraw first, 1: direct re-declare
    for (int src : {0, 1, 7}) {
      for (unsigned gap = 0; gap < 8; ++gap) {
        h.reset(); d->link_up_i = 1; h.idle(200);
        const uint64_t sid = (OWN_MAC << 16) | (0x600 + src);
        const uint64_t da = 0x91E0F0000600ULL + src;
        auto r1 = h.svc(0, src, sid, da, 2, 224, 0);
        h.idle(300);
        const bool was_admitted = (d->r298_adm_o >> src) & 1;
        CHECK(r1.got && r1.status == 0 && was_admitted,
              "R298 top: 224 B declaration admitted (src %d)", src);
        if (variant == 0) {
          auto rw = h.svc(1, src, sid, da, 2, 0, 0);
          h.idle(300);
          CHECK(rw.got && !((d->r298_adm_o >> src) & 1), "R298 top: withdrawn (src %d)", src);
        }
        h.idle(gap);
        while (!d->svc_ready_o) h.step();
        d->svc_valid_i = 1; d->svc_op_i = 0; d->svc_index_i = src;
        d->svc_stream_id_i = sid; d->svc_da_i = da; d->svc_vid_i = 2;
        d->svc_max_frame_i = 20000; d->svc_lstn_state_i = 0;
        h.step();
        d->svc_valid_i = 0;
        int accepted = -1;
        unsigned high_after = 0, active_after = 0;
        bool rsp_ok = false;
        for (int i = 0; i < 1200; ++i) {
          h.step();
          rsp_ok |= d->svc_rsp_valid_o && d->svc_rsp_status_o == 0;
          if (accepted < 0 && d->r298_gate_acc_o) { accepted = i; continue; }
          if (accepted >= 0) {
            high_after += (d->r298_adm_o >> src) & 1;
            active_after += (d->r298_active_o >> src) & 1;
          }
        }
        pulses_total += high_after;
        printf("R298TOP variant=%s src=%d gap=%u accepted_at=%d admitted_cycles_after_accept=%u "
               "active_cycles_after_accept=%u final_admitted=%u rsp_ok=%d\n",
               variant ? "direct-redeclare" : "withdraw-then-declare", src, gap, accepted,
               high_after, active_after, unsigned((d->r298_adm_o >> src) & 1), int(rsp_ok));
        CHECK(accepted >= 0 && rsp_ok, "R298 top: 20000 B declaration accepted (src %d)", src);
        CHECK(high_after == 0,
              "R298 top: refused 20000 B re-declaration never shows srp_sr_admitted_o (src %d gap %u): %u cycles",
              src, gap, high_after);
      }
    }
  }
  printf("R298TOP total admitted cycles after refused re-declaration: %u\n", pulses_total);
}
