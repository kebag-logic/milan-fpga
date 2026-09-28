  // ============ reviewer probes (R375-2, round 2), disposable ============
  // Release bounds of a canceled empty reservation as documented in
  // docs/architecture/10_srp_engine.md section 6.5 (link down: the next
  // unsuperseded own action within T-MRP-LEAVEALL + T-MRP-JOIN; link down then
  // up: link-up content). Observes wrapper debug outputs and the wire only.
  void r375_parked_bounds() {
    for (int variant = 0; variant < 2; variant++) {
      h.reset(); d->link_up_i = 1; h.run_ms(700);
      const uint32_t deadline = d->dbg_la_deadline_o;
      until_ms(deadline - 20); d->block_alloc_i = 1; d->link_up_i = 0;
      until_ms(deadline + 250);
      const uint32_t next = d->dbg_la_deadline_o;
      h.feed(mrpdu_body(true, {la_only(3, 8, true)}), true);
      d->block_alloc_i = 0; h.run_ms(5);
      CHECK(d->dbg_enc_state_o == 16 && d->dbg_enc_count_o == 0,
            "R8a: canceled empty reservation parked with the link down (variant=%d)", variant);
      const uint32_t entered = d->now_ms_o;
      const size_t base = h.archive.size();
      uint32_t up_at = 0;
      if (variant == 1) { h.run_ms(3000); d->link_up_i = 1; up_at = d->now_ms_o; }
      int guard = 20000 * MS_CYC;
      while (d->dbg_enc_state_o == 16 && guard-- > 0) h.cycle();
      const uint32_t released = d->now_ms_o;
      h.run_ms(50);
      const int flagged = leaveall_frames(h, base);
      printf("R375_PARK variant=%d cancel_deadline=%u entered=%u next_deadline=%u link_up_at=%u "
             "released=%u dwell_ms=%u actions=%zu flagged_frames=%d frames_after=%zu\n",
             variant, deadline, entered, next, up_at, released, released - entered,
             h.la_cycles.size(), flagged, h.archive.size() - base);
      if (variant == 0) {
        CHECK(guard > 0 && released >= next && released <= next + 240
              && h.la_cycles.size() == 1 && flagged == 1,
              "R8b: link-down park is released by the next own sLA within T-MRP-JOIN of its expiry");
        CHECK(released - entered <= 15000 + 240,
              "R8c: link-down dwell within T-MRP-LEAVEALL + T-MRP-JOIN (%u ms)", released - entered);
      } else {
        CHECK(guard > 0 && released >= up_at && released <= up_at + 1240
              && h.la_cycles.empty() && h.archive.size() > base && flagged == 0,
              "R9: link-up content releases the parked reservation (%u ms after link-up)",
              released - up_at);
      }
    }
  }
  // ========== end reviewer probes (round 2) ==========
