# R437-3 directed checks on the drain bound (ZD1-ZD4), appended to T28f's
# function, run at the head and against the drain plants that left the suite
# and the randomized harness green (B6, B6b, B7, B8, B10, B12; exact text of
# spec_drain.py). Each ZD check is the head's T28f pattern in another state:
#   ZD1 a header READ abandoned before its 4th byte (S_RHCOLL), its device then
#       presenting bytes past the length: exactly the 5 owed are drained;
#   ZD2 a header READ abandoned in S_RHWAIT (all 8 bytes moved, done withheld),
#       its device then presenting more bytes: none is drained;
#   ZD3 a header READ the backend granted on the edge the deadline withdrew it
#       (the late registered grant), its device then presenting bytes past the
#       length: exactly the 8 owed are drained;
#   ZD4 a 600-byte payload READ abandoned before its 11th byte, whose device
#       then ends it at a legal pace (the T24/T28 served branch): the waiting
#       restore is served byte-exact.
# Each then ends the owed READ with the device's done and requires service.
ANCHOR = ('        "T28f ...the device\'s own done ends the READ, and the next restore is served "\n'
          '        "byte-exact (rc %d)", rc);\n'
          '  h.deadline_ok = false;\n}\n')
ZD = r'''
  // ---- R437-3 ZD1: S_RHCOLL ----
  auto babble_from_here = [&]() { h.sil_block = false; h.d_cur.len = 1 << 30; h.rstall = TMO / 2; };
  auto end_and_serve = [&](const char* id) {
    h.rstall = 0;
    h.end_command_now(false);
    for (int i = 0; i < 4; ++i) h.tick();
    h.ops.clear();
    const int r2 = h.restore(2);
    CHECK(r2 == 0 && h.rbytes == rec, "%s ...ended by the device's done, the next restore served (rc %d)", id, r2);
  };
  fresh_reset();
  h.deadline_ok = true;
  CHECK(h.commit(2, rec) == 0, "ZD1 setup: region 2 committed");
  rc = silenced(false, rec, SIL_BYTE, 0, -1, 3);
  CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "ZD1 setup: header READ abandoned before its 4th byte");
  babble_from_here();
  bool zw = wait_on_owed(false, rec, 0);
  rc = h.run_op();
  CHECK(zw && rc == 1 && h.last_cause == 3 && h.dev_rd == 5,
        "ZD1 S_RHCOLL: drained exactly the 5 header bytes owed, then DEADLINE (rc %d, cause %d, %d drained)",
        rc, h.last_cause, h.dev_rd);
  end_and_serve("ZD1");

  // ---- R437-3 ZD2: S_RHWAIT ----
  fresh_reset();
  h.deadline_ok = true;
  CHECK(h.commit(2, rec) == 0, "ZD2 setup: region 2 committed");
  rc = silenced(false, rec, SIL_DONE, 0, -1, 0);
  CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "ZD2 setup: header READ abandoned in S_RHWAIT");
  h.d_st = 1; babble_from_here();
  zw = wait_on_owed(false, rec, 0);
  rc = h.run_op();
  CHECK(zw && rc == 1 && h.last_cause == 3 && h.dev_rd == 0,
        "ZD2 S_RHWAIT: nothing owed is drained, then DEADLINE (rc %d, cause %d, %d drained)",
        rc, h.last_cause, h.dev_rd);
  end_and_serve("ZD2");

  // ---- R437-3 ZD3: the late registered grant of a header READ ----
  fresh_reset();
  h.deadline_ok = true;
  CHECK(h.commit(2, rec) == 0, "ZD3 setup: region 2 committed");
  h.rstall = TMO / 2;
  rc = silenced(false, rec, SIL_GNT, 0, TMO + 1, 0);
  const int zd3_before = h.dev_rd;
  CHECK(rc == 1 && h.last_cause == 3 && h.d_busy && h.late_gnts == 1,
        "ZD3 setup: header READ granted one cycle after its deadline (late %d)", h.late_gnts);
  h.d_cur.len = 1 << 30;
  zw = wait_on_owed(false, rec, 0);
  rc = h.run_op();
  CHECK(zw && rc == 1 && h.last_cause == 3 && zd3_before + h.dev_rd == 8,
        "ZD3 late grant: drained exactly the 8 header bytes owed, then DEADLINE (rc %d, cause %d, %d drained)",
        rc, h.last_cause, zd3_before + h.dev_rd);
  end_and_serve("ZD3");

  // ---- R437-3 ZD4: a large payload READ abandoned, then ended at a legal pace ----
  {
    const std::vector<uint8_t> big = frame(2, pattern(600, 0x5A));
    fresh_reset();
    h.deadline_ok = true;
    CHECK(h.commit(2, big) == 0, "ZD4 setup: region 2 committed with a 600-byte payload");
    rc = silenced(false, big, SIL_BYTE, 1, -1, 10);
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "ZD4 setup: payload READ abandoned before its 11th byte, 590 owed");
    h.sil_block = false;
    zw = wait_on_owed(false, big, 0);
    rc = h.run_op();
    CHECK(zw && rc == 0 && h.rbytes == big && h.dev_rd == 590 + 608,
          "ZD4 the 590 owed bytes drained, the device's done ends the READ, the waiting restore served "
          "byte-exact (rc %d, cause %d, %d moved)", rc, h.last_cause, h.dev_rd);
    fresh_reset();
    CHECK(h.commit(2, rec) == 0, "ZD4 teardown: region 2 committed back");
  }
'''
NEW = ANCHOR.replace("  h.deadline_ok = false;\n}\n", ZD + "  h.deadline_ok = false;\n}\n")
PROBES = {"ZD_head": [("SIM", ANCHOR, NEW)]}
RTL_PLANTS = {
    "B6_rhcoll_one_over": ("  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r))\n",
                           "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r) + 16'd1)\n"),
    "B6b_rhcoll_whole": ("  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r))\n",
                         "  assign left_w  = (state_r == S_RHCOLL) ? HDR_LEN_C\n"),
    "B7_request_one_over": ("                 : dev_len_o;\n",
                            "                 : (dev_len_o != 16'd0) ? (dev_len_o + 16'd1) : 16'd0;\n"),
    "B8_wait_states_owe_eight": ("                 : dev_len_o;\n",
                                 "                 : ((state_r == S_RHWAIT) || (state_r == S_RPWAIT)) ? HDR_LEN_C : dev_len_o;\n"),
    "B10_count_eight_bits": ("  logic       [15:0] owed_left_r;   // ...as many as it still owes",
                             "  logic        [7:0] owed_left_r;   // ...as many as it still owes"),
    "B12_drain_any_owed": ("  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 16'd0);\n",
                           "  assign drain_w = owed_r && (owed_left_r != 16'd0);\n"),
}
for k, (o, n) in RTL_PLANTS.items():
    PROBES["ZD_" + k] = [("SIM", ANCHOR, NEW), ("RTL", o, n)]
RUNS = [(p, m, t) for p in PROBES for m in ("pristine", "coincident completion") for t in (100, 37, 20)]
