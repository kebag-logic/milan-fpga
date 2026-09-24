  // ==== R298-1 reviewer probe: a lower-index identical re-declaration must
  // not license a refused higher-index source (engine level, real ports) ====
  void probe_r298_cross_source() {
    const unsigned BIG = 700;              // (700+42)*64000 = 47.49 Mb/s: one fits 75 Mb/s, two do not
    for (int lstn : {DECL_READY, DECL_ASKFAIL}) {
      for (int b : {1, 7}) {
        for (unsigned phase = 0; phase < 8; ++phase) {
          h.reset(); d->link_up_i = 1; h.idle(40);
          const uint64_t sidA = (OWN_MAC << 16) | 0x500;
          const uint64_t sidB = (OWN_MAC << 16) | (0x500 + b);
          auto rA = h.op(OP_DECL_TK, 0, sidA, DA0, 2, BIG, 1);
          h.idle(64);
          auto rB = h.op(OP_DECL_TK, b, sidB, DA0 + b, 2, BIG, 1);
          h.idle(400);
          h.feed(mrpdu_body(true, {Msg{3, 8, true,
            {Vec{false, 1, fv_sid(sidA), {EV_NEW}, {DECL_READY}}}}}), true);
          h.feed(mrpdu_body(true, {Msg{3, 8, true,
            {Vec{false, 1, fv_sid(sidB), {EV_NEW}, {lstn}}}}}), true);
          h.idle(64);
          const unsigned mb = 1u << b;
          CHECK(rA.got && rB.got && (d->sr_admitted_o & 1) && h.active(0)
                && !(d->sr_admitted_o & mb) && h.tk_decl(b) == 2 && !h.active(b),
                "R298 setup: src0 admitted+active, src%d refused+Failed (lstn %d phase %u)",
                b, lstn, phase);
          // align the slope sampling phase, then IDENTICAL re-declaration of src 0
          for (unsigned n = 0; d->dbg_sample_index_o != phase && n < 8; ++n) h.cycle();
          h.sync();                         // drain queued frames, clean 200 ms slot
          for (unsigned n = 0; d->dbg_sample_index_o != phase && n < 8; ++n) h.cycle();
          h.samples.clear(); h.recording = true;
          auto r2 = h.op(OP_DECL_TK, 0, sidA, DA0, 2, BIG, 1);
          h.idle(200);
          h.recording = false;
          unsigned grant_cyc = 0, active_cyc = 0, adv_cyc = 0;
          uint64_t max_live = 0;
          for (const auto& x : h.samples) {
            grant_cyc  += (x.grants & mb) != 0;
            active_cyc += (x.active & mb) != 0;
            adv_cyc    += ((x.tk_decl >> (2 * b)) & 3) == 1;
            uint64_t live = 0;
            for (int s = 0; s < 8; ++s) live += x.slopes[s];
            max_live = std::max<uint64_t>(max_live, live);
          }
          // wire: does a Talker ADVERTISE for the refused stream appear?
          auto adv = h.wait_frame(true, 1000, [&](const std::vector<uint8_t>& fr) {
            return frame_has(fr, true, 1, sidB, EV_NEW) || frame_has(fr, true, 1, sidB, EV_JOININ);
          });
          printf("R298PROBE lstn=%d src_b=%d phase=%u redeclare_ok=%d refused_grant_cycles=%u "
                 "refused_active_cycles=%u refused_advertise_cycles=%u wire_advertise_for_refused=%d "
                 "max_live_sum=%llu final_tk_decl=%u\n",
                 lstn, b, phase, int(r2.got && r2.status == ST_OK), grant_cyc, active_cyc, adv_cyc,
                 int(!adv.empty()), (unsigned long long)max_live, h.tk_decl(b));
          CHECK(grant_cyc == 0, "R298: refused src%d never pulses sr_admitted (lstn %d phase %u): %u cycles",
                b, lstn, phase, grant_cyc);
          CHECK(adv_cyc == 0, "R298: refused src%d never swaps to Advertise (lstn %d phase %u): %u cycles",
                b, lstn, phase, adv_cyc);
          CHECK(active_cyc == 0, "R298: refused src%d never ACTIVE (lstn %d phase %u): %u cycles",
                b, lstn, phase, active_cyc);
          CHECK(adv.empty(), "R298: no Talker Advertise on the wire for refused src%d (lstn %d phase %u)",
                b, lstn, phase);
          CHECK(max_live <= LIMIT, "R298: live granted sum within ceiling");
        }
      }
    }
  }
