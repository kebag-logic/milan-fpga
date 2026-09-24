// ==== R299-2 reviewer probe: the cross-source rule at protocol_processor_top.
// Through the real svc_* face and a real inbound MSRP Listener Ready for both
// streams. Source 0 (~69.95 Mb/s) is admitted, source 7 (~15.49 Mb/s) is
// refused by the 75 Mb/s ceiling of the bench's 100 Mb/s port. Source 0 is
// re-declared identically (mode 0), shrunk to ~60.29 Mb/s (mode 1, still
// refusing 7), or shrunk to 224 bytes (mode 2, frees capacity for 7), at
// every sampling phase. Observed EVERY clock at the processor top level:
// srp_sr_admitted_w[7], srp_active_w[7], their AND, the declared Talker
// state of source 7, srp_sum_slope_w / srp_over_limit_w (must hold until the
// grant of source 0 is republished), and source 0's own grant latency.
struct ReviewerCrossProbe {
  H& h;
  unsigned runs = 0, with_grant = 0, with_conf = 0, with_adv = 0, with_wire = 0,
           agg_moved = 0, max_lat = 0, freed_ok = 0;
  static uint64_t slope(unsigned f) { return (std::max(f + 22u, 68u) + 20ull) * 64000ull; }
  void run() {
    const int lo = 0, hi = 7;
    const unsigned F_LO = 1051, F_SHR = 900, F_FREE = 224, F_HI = 200;
    const uint64_t sid_lo = (OWN_MAC << 16) | 0x0500, sid_hi = (OWN_MAC << 16) | 0x0507;
    const uint64_t da_lo = 0x91E0F0000540ull, da_hi = 0x91E0F0000547ull;
    for (int mode = 0; mode < 3; ++mode) {
      for (unsigned phase = 0; phase < 8; ++phase) {
        for (auto& region : h.nv_mem) std::fill(region.begin(), region.end(), 0xFF);
        h.nv_st = H::NvState::NV_IDLE;
        h.nv_done_lag = 0;
        h.reset();
        h.d->restore_go_i = 1; h.idle(5); h.d->restore_go_i = 0;
        unsigned budget = 400000;
        while (!h.d->restore_done_o && budget-- != 0) h.step();
        h.d->link_up_i = 1; h.d->entity_enable_i = 1;
        h.run_ms(30);
        auto rl = h.svc(OP_DECL_TK, lo, sid_lo, da_lo, 2, F_LO, 0);
        auto rh = h.svc(OP_DECL_TK, hi, sid_hi, da_hi, 2, F_HI, 0);
        h.run_ms(5);
        Msg lsn{3, 8, true, {Vec{false, 1, fv_sid(sid_lo), {EV_NEW}, {DECL_READY}},
                             Vec{false, 1, fv_sid(sid_hi), {EV_NEW}, {DECL_READY}}}};
        h.feed(mrpdu_frame(true, T1_MAC, {lsn}));
        h.run_ms(900);
        const bool pre = rl.got && rl.status == ST_OK && rh.got && rh.status == ST_OK &&
                         (h.d->dbg_p_adm_o & 1u) && !(h.d->dbg_p_adm_o & 0x80u) &&
                         (h.d->dbg_p_act_o & 1u) && ((h.d->dbg_p_tkdecl_o >> 14) & 3u) == 2u;
        CHECK(pre, "RP precondition mode %d phase %u: 0 granted+ACTIVE, 7 refused and Failed "
              "(adm=%02x act=%02x decl=%04x)", mode, phase, unsigned(h.d->dbg_p_adm_o),
              unsigned(h.d->dbg_p_act_o), unsigned(h.d->dbg_p_tkdecl_o));
        const uint32_t sum0 = h.d->dbg_p_sum_o;
        const bool over0 = h.d->dbg_p_over_o;
        CHECK(sum0 == slope(F_LO) && over0, "RP precondition aggregate mode %d phase %u", mode, phase);
        h.q_msrp.clear();
        for (unsigned n = 0; h.d->dbg_p_sample_o != phase && n < 8; ++n) h.step();
        const unsigned f_new = mode == 0 ? F_LO : mode == 1 ? F_SHR : F_FREE;
        // issue the re-declaration by hand so every clock is observed
        while (!h.d->svc_ready_o) h.step();
        h.d->svc_valid_i = 1; h.d->svc_op_i = OP_DECL_TK; h.d->svc_index_i = lo;
        h.d->svc_stream_id_i = sid_lo; h.d->svc_da_i = da_lo; h.d->svc_vid_i = 2;
        h.d->svc_max_frame_i = f_new; h.d->svc_lstn_state_i = 0;
        h.step();
        h.d->svc_valid_i = 0;
        unsigned grant = 0, conf = 0, adv = 0, moved = 0;
        int lo_drop = -1, lo_back = -1, hi_first = -1;
        for (int c = 0; c < 200; ++c) {
          const bool g0 = h.d->dbg_p_adm_o & 1u;
          const bool g7 = (h.d->dbg_p_adm_o >> 7) & 1u;
          const bool a7 = (h.d->dbg_p_act_o >> 7) & 1u;
          if (lo_drop < 0 && !g0) lo_drop = c;
          if (lo_drop >= 0 && lo_back < 0 && g0) lo_back = c;
          if (hi_first < 0 && g7) hi_first = c;
          if (mode < 2) {
            grant += g7; conf += g7 && a7;
            adv += ((h.d->dbg_p_tkdecl_o >> 14) & 3u) == 1u;
          }
          if (lo_drop >= 0 && lo_back < 0)
            moved += h.d->dbg_p_sum_o != sum0 || bool(h.d->dbg_p_over_o) != over0;
          h.step();
        }
        const unsigned lat = lo_back >= 0 && lo_drop >= 0 ? unsigned(lo_back - lo_drop) : 999;
        max_lat = std::max(max_lat, lat);
        h.run_ms(900);
        unsigned wire = 0;
        for (auto& fr : h.q_msrp) {
          auto p = parse_mrpdu(fr);
          for (auto& v : p.vecs)
            if (v.type == 1 && v.fv.size() >= 8 && fv_u64(v.fv, 0, 8) == sid_hi) ++wire;
        }
        printf("RP mode=%s phase=%u src0_hold_cycles=%u src7_grant_cycles=%u "
               "src7_active_and_grant_cycles=%u src7_declared_advertise_cycles=%u "
               "aggregate_moved_during_hold=%u src7_first_grant_rel=%d src0_regrant_rel=%d "
               "wire_src7_talker_advertise=%u settled_adm=%02x settled_decl7=%u\n",
               mode == 0 ? "identical" : mode == 1 ? "shrink-still-refused" : "shrink-frees",
               phase, lat, grant, conf, adv, moved, hi_first, lo_back,
               wire, unsigned(h.d->dbg_p_adm_o), unsigned((h.d->dbg_p_tkdecl_o >> 14) & 3u));
        CHECK(lo_drop >= 0 && lo_back > lo_drop, "RP source 0 retires at acceptance and re-grants");
        CHECK(lat <= 24, "RP source 0 grant latency within 3*N (%u)", lat);
        CHECK(moved == 0, "RP aggregate holds while source 0 is pending");
        if (mode < 2) {
          CHECK(grant == 0 && conf == 0 && adv == 0 && wire == 0,
                "RP refused source 7 never granted/ACTIVE/Advertise (mode %d phase %u)", mode, phase);
          with_grant += grant != 0; with_conf += conf != 0; with_adv += adv != 0;
          with_wire += wire != 0;
        } else {
          const bool same = hi_first == lo_back;
          CHECK(same && (h.d->dbg_p_adm_o & 0x81u) == 0x81u,
                "RP freed source 7 is granted on source 0's republication clock (%d vs %d)",
                hi_first, lo_back);
          freed_ok += same;
        }
        agg_moved += moved != 0;
        ++runs;
      }
    }
    printf("RP SUMMARY runs=%u refused_runs_with_grant=%u with_active_and_grant=%u "
           "with_declared_advertise=%u with_wire_advertise=%u runs_with_aggregate_move=%u "
           "max_src0_hold_cycles=%u freed_same_clock=%u/8\n",
           runs, with_grant, with_conf, with_adv, with_wire, agg_moved, max_lat, freed_ok);
  }
};
