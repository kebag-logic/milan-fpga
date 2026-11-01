#!/usr/bin/env python3
"""Regression tests for the writable corrections."""
root = "$VALIDATION_STORAGE/829-a725/wt-bench/"
def patch(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old, s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)

patch("tb/verilator/gptp_txts/sim_main.cpp", [
("""  void prove_full_run_laws();

""", """  void prove_full_run_laws();
#ifdef GPTP_TXTS_LATW
  //! One graded exchange under the corrections then in force.
  struct LatGrade {
    bool ok = false;
    int64_t ingress = 0;     //! PHC at the request's first accepted beat, less t2
    int64_t net = 0;         //! PHC at the response's record, less the wire's t3
    int64_t pad_err = 0;     //! the wire's t3, less the PHC at the pads' launch
    int64_t pad_err_fu = 0;  //! the same for the Follow_Up's own launch
  };
  LatGrade lat_exchange(uint64_t write_after_ns = 0, uint16_t ing = 0,
                        uint16_t egr = 0);
  void set_lat(uint16_t ing, uint16_t egr);
  void prove_a_written_pair_moves_both_stamps();
  void prove_a_write_spoils_at_most_its_own_exchange();
#endif

"""),
("""void TxtsHarness::on_dp_edge() {
  if (dut->rx_tvalid_i && dut->rx_tready_i) { rx_pos_ += 8; dbg_rx_beats_++; }
""", """void TxtsHarness::on_dp_edge() {
#ifdef GPTP_TXTS_LATW
  //! the value the plane's arrival stamp reads on this very edge
  if (dut->rx_tvalid_i && dut->rx_tready_i && rx_pos_ == 0) {
    rx_first_phc_ = dut->phc_ns_o;
    rx_first_ns_ = now_;
  }
#endif
  if (dut->rx_tvalid_i && dut->rx_tready_i) { rx_pos_ += 8; dbg_rx_beats_++; }
"""),
("""  if (dp_posedge) {
    phc_samples_.emplace_back(now_, dut->phc_ns_o);
""", """  if (dp_posedge) {
    phc_samples_.emplace_back(now_, dut->phc_ns_o);
#ifdef GPTP_TXTS_LATW
    if (dut->rec_v_o && !dut->rec_kind_o) {
      rec_phc_.push_back({static_cast<uint16_t>(dut->rec_seq_o),
                          static_cast<uint8_t>(dut->rec_type_o),
                          dut->phc_ns_o});
    }
#endif
"""),
("""  dut->dp_rst_n = 1;
  dut->sys_rst_n = 1;
  dut->eth_rst_n = 1;
  run_ns(2000);
}
""", """  dut->dp_rst_n = 1;
  dut->sys_rst_n = 1;
  dut->eth_rst_n = 1;
  run_ns(2000);
}

#ifdef GPTP_TXTS_LATW
//! A nanosecond stamp from a frame body, 802.1AS's 48-bit seconds and 32-bit
//! nanoseconds at `at`, as the single scale the PHC counts in.
static uint64_t body_ts_ns(const std::vector<uint8_t> &b, size_t at) {
  uint64_t sec = 0;
  for (size_t i = 0; i < 6; i++) sec = (sec << 8) | b[at + i];
  uint64_t ns = 0;
  for (size_t i = 6; i < 10; i++) ns = (ns << 8) | b[at + i];
  return sec * 1000000000ull + ns;
}

//! Drive the two corrections as the CSR block's flops do: both change on one
//! plane edge, while the plane's clock is low.
void TxtsHarness::set_lat(uint16_t ing, uint16_t egr) {
  while (dut->dp_clk_i) step();
  dut->lat_ingress_ns_i = ing;
  dut->lat_egress_ns_i = egr;
}

//! One peer request and its two answers, graded on what the wire carries:
//! t2 from the Pdelay_Resp and t3 from the Follow_Up. `write_after_ns`, when
//! not zero, moves the corrections that long after the request is offered.
TxtsHarness::LatGrade TxtsHarness::lat_exchange(uint64_t write_after_ns,
                                                uint16_t ing, uint16_t egr) {
  LatGrade g;
  const size_t pads_before = pads_.size();
  const size_t recs_before = rec_phc_.size();
  const uint16_t seq = peer_seq_++;
  Frame req = ptp_frame(0x2, seq, 0x0000, 20, kPeerCid);
  req.u64v(0);
  req.u64v(0);
  req.u32(0);
  send_peer(req.b);
  const uint64_t offered = now_;
  const uint64_t until = now_ + kExchangeNs;
  const PadFrame *resp = nullptr;
  const PadFrame *fup = nullptr;
  bool written = write_after_ns == 0;
  while (now_ < until && !(resp && fup)) {
    if (!written && now_ >= offered + write_after_ns) {
      set_lat(ing, egr);
      written = true;
    }
    step();
    resp = nullptr;
    fup = nullptr;
    for (size_t i = pads_before; i < pads_.size(); i++) {
      if (!pads_[i].gptp || pads_[i].seq != seq) continue;
      if (pads_[i].type == 0x3) resp = &pads_[i];
      if (pads_[i].type == 0xA) fup = &pads_[i];
    }
  }
  run_ns(4000);
  sys_next_ += 1;
  if (!written) set_lat(ing, egr);
  if (!resp || !fup || resp->body.size() < 58 || fup->body.size() < 58) return g;
  uint64_t rec_phc = 0;
  bool have_rec = false;
  for (size_t i = recs_before; i < rec_phc_.size(); i++) {
    if (rec_phc_[i].seq == seq && rec_phc_[i].type == 0x3) {
      rec_phc = rec_phc_[i].phc;
      have_rec = true;
    }
  }
  if (!have_rec) return g;
  const uint64_t t2 = body_ts_ns(resp->body, 48);
  const uint64_t t3 = body_ts_ns(fup->body, 48);
  g.ingress = static_cast<int64_t>(rx_first_phc_) - static_cast<int64_t>(t2);
  g.net = static_cast<int64_t>(rec_phc) - static_cast<int64_t>(t3);
  g.pad_err = static_cast<int64_t>(t3) - phc_at(resp->ref_ns);
  g.ok = true;
  return g;
}
#endif
"""),
("""int TxtsHarness::run() {
  prove_bring_up();
""", """#ifdef GPTP_TXTS_LATW
//! A written pair moves the published stamps by exactly that pair, in each
//! direction on its own (issue #829). The ingress stamp and the wire's t3
//! against the PHC at the response's record are exact, with no phase term; the
//! pads grade the same t3 against the launch they saw, inside the bound.
void TxtsHarness::prove_a_written_pair_moves_both_stamps() {
  set_lat(0, 0);
  LatGrade base;
  for (int n = 0; n < 8; n++) base = lat_exchange();
  check.that("runtime: an exchange at the zero pair completes", base.ok);
  check.dec("runtime: at the zero pair t2 is the PHC at the first beat",
            base.ingress, 0);
  check.that("runtime: at the zero pair t3 is on the pads' launch",
             std::abs(base.pad_err) <= kBoundNs);
  std::printf("  zero pair: ingress gap %lld ns, net %lld ns, pad error %+lld ns\\n",
              static_cast<long long>(base.ingress),
              static_cast<long long>(base.net),
              static_cast<long long>(base.pad_err));
  //! Unequal and unrelated to any figure in the RTL, so a swap or a shared
  //! value goes red. The sum of the last two is what the MII port measured.
  static constexpr uint16_t kPairs[][2] = {
      {777, 333}, {1409, 100}, {1, 65535}, {65535, 1}, {0, 0}};
  for (const auto &pair : kPairs) {
    set_lat(pair[0], pair[1]);
    for (int n = 0; n < 3; n++) {
      const LatGrade g = lat_exchange();
      check.that("runtime: an exchange under a written pair completes", g.ok);
      check.dec("runtime: a written ingress moves t2 by exactly it",
                g.ingress - base.ingress, pair[0]);
      check.dec("runtime: a written egress moves t3 by exactly it",
                base.net - g.net, pair[1]);
      check.that("runtime: t3 less the egress is still on the pads' launch",
                 std::abs(g.pad_err - pair[1]) <= kBoundNs);
    }
    std::printf("  pair %u/%u: t2 moved %u ns, t3 moved %u ns\\n", pair[0],
                pair[1], pair[0], pair[1]);
  }
}

//! A write lands on one edge and a stamp reads one value, so an exchange a write
//! falls inside carries the old pair or the new one in each stamp, and the next
//! exchange carries the new pair whole (issue #829). The sweep puts the write
//! at every distance through the exchange, on either side of each stamp.
void TxtsHarness::prove_a_write_spoils_at_most_its_own_exchange() {
  set_lat(0, 0);
  LatGrade base;
  for (int n = 0; n < 2; n++) base = lat_exchange();
  static constexpr uint16_t kOldI = 1409;
  static constexpr uint16_t kOldE = 100;
  static constexpr uint16_t kNewI = 777;
  static constexpr uint16_t kNewE = 333;
  int straddled = 0;
  for (uint64_t at = 20; at < 12000 * kEthCycPerOctet; at += 170) {
    set_lat(kOldI, kOldE);
    lat_exchange();
    const LatGrade during = lat_exchange(at, kNewI, kNewE);
    check.that("runtime: an exchange a write falls inside completes", during.ok);
    const int64_t ing = during.ingress - base.ingress;
    const int64_t egr = base.net - during.net;
    check.that("runtime: t2 carries one whole correction, old or new",
               ing == kOldI || ing == kNewI);
    check.that("runtime: t3 carries one whole correction, old or new",
               egr == kOldE || egr == kNewE);
    if (ing != kNewI || egr != kNewE) straddled++;
    const LatGrade next = lat_exchange();
    check.that("runtime: the next exchange completes", next.ok);
    check.dec("runtime: the next exchange's t2 carries the new pair whole",
              next.ingress - base.ingress, kNewI);
    check.dec("runtime: the next exchange's t3 carries the new pair whole",
              base.net - next.net, kNewE);
  }
  std::printf("  %d of the writes landed inside the stamps' interval\\n", straddled);
  check.that("runtime: the sweep really did land a write between the stamps",
             straddled > 0);
  set_lat(0, 0);
}
#endif

int TxtsHarness::run() {
#ifdef GPTP_TXTS_LATW
  dut->lat_ingress_ns_i = 0;
  dut->lat_egress_ns_i = 0;
  prove_bring_up();
  prove_a_written_pair_moves_both_stamps();
  prove_a_write_spoils_at_most_its_own_exchange();
  return check.report();
#endif
  prove_bring_up();
"""),
])
s = open(root + "tb/verilator/gptp_txts/sim_main.cpp", encoding="utf-8").read()
anchor = "  int64_t phc_at(uint64_t when) const;\n"
assert s.count(anchor) == 1
s = s.replace(anchor, """#ifdef GPTP_TXTS_LATW
  struct RecPhc { uint16_t seq; uint8_t type; uint64_t phc; };
  std::vector<RecPhc> rec_phc_;
  uint64_t rx_first_phc_ = 0;
  uint64_t rx_first_ns_ = 0;
#endif
""" + anchor)
open(root + "tb/verilator/gptp_txts/sim_main.cpp", "w", encoding="utf-8").write(s)

patch("tb/verilator/gptp_txts/Makefile", [
("""#: A green suite and a suite that cannot go red look the same from outside.
""", """#: The writable corrections (issue #829): the plane elaborated with the
#: corrections on its ports, in both shapes, each in its own object directory.
#: The default elaboration above stays the one every other proof grades.
.PHONY: run-latw
run-latw: run-latw-gmii run-latw-mii
.PHONY: run-latw-gmii
run-latw-gmii: gptp_ucode.hex model
	$(VERILATOR) $(VFLAGS) --Mdir obj_latw -DGPTP_TXTS_LATW -GLAT_WRITABLE_P=1 \\
	  -CFLAGS "-DGPTP_TXTS_LATW" \\
	  $(SRCS) $(CPP) -o Vgptp_txts_sim
	./obj_latw/Vgptp_txts_sim
.PHONY: run-latw-mii
run-latw-mii: gptp_ucode.hex model
	$(VERILATOR) $(VFLAGS) --Mdir obj_latw_mii -DGPTP_TXTS_MII -DGPTP_TXTS_LATW \\
	  -GLAT_WRITABLE_P=1 -GETH_TICK_NS_P=$(MII_ETH_TICK_NS) -GETH_CYC_PER_OCTET_P=2 \\
	  -CFLAGS "-DGPTP_TXTS_MII -DGPTP_TXTS_LATW" \\
	  $(SRCS_MII) $(CPP) -o Vgptp_txts_sim
	./obj_latw_mii/Vgptp_txts_sim 25

#: A green suite and a suite that cannot go red look the same from outside.
"""),
("""mutants: run run-mii
	python3 mutants.py
""", """mutants: run run-mii run-latw
	python3 mutants.py
"""),
])
patch("tb/verilator/gptp_txts/.gitignore", [
("""obj_pad_mii/
""", """obj_pad_mii/
obj_latw/
obj_latw_mii/
"""),
])

patch("tb/verilator/milan_dp/sim_gptp.cpp", [
("""  // Keep answering Pdelay while the selected peer's Announce expires.
  // The resulting GM Sync/Follow_Up and one peer request exercise all five
""", """#ifdef GPTP_LAT_WRITABLE_TB
  //! One responder exchange under the corrections then in force, as the T-LAT
  //! leg grades it: t2 against the boundary, t3 against the observed launch.
  bool responder_gaps(Vmilan_datapath *dut, uint16_t seq, int64_t *ing,
                      int64_t *egr) {
    Frame request = ptp(0x2, seq, 0, 0x0000, 20);
    request.ts(0);
    request.u64(0); request.u16(0);
    send_wide(dut, request.b);
    const uint64_t req_arrival = rx_sof_phc;
    std::vector<uint8_t> resp;
    std::vector<uint8_t> fup;
    uint64_t resp_launch = 0;
    for (int n = 0; n < 400; n++) {
      run_peer(dut, 2000);
      if (tx_of(0x3, seq, &resp) && tx_of(0xA, seq, &fup)
          && observer.t1_of(0x3, seq, &resp_launch))
        break;
    }
    if (resp.size() < 58 || fup.size() < 58 || resp_launch == 0) return false;
    *ing = static_cast<int64_t>(req_arrival)
         - static_cast<int64_t>(wire_ts_ns(resp, 48));
    *egr = static_cast<int64_t>(wire_ts_ns(fup, 48))
         - static_cast<int64_t>(resp_launch);
    return true;
  }

  //! [T-LATW] THE WRITABLE CORRECTIONS THROUGH THE REAL CSR BLOCK (issue #829).
  //! Under the build key the elaborated pair is only the reset value of 0x540
  //! and 0x544; a bus write moves each stamp by its own value, GPTP_LAT reads
  //! back what is applied, and the plane is still the only consumer.
  void prove_the_written_pair_reaches_both_stamps(Vmilan_datapath *dut) {
    const uint32_t reset_pair = (static_cast<uint32_t>(kLatIngNs) << 16)
                              | static_cast<uint32_t>(kLatEgrNs);
    expect("[T-LATW] 0x540 resets to the build's ingress value",
           axi_read(dut, 0x540), kLatIngNs);
    expect("[T-LATW] 0x544 resets to the build's egress value",
           axi_read(dut, 0x544), kLatEgrNs);
    expect("[T-LATW] GPTP_LAT resets to the build's pair",
           axi_read(dut, 0x7F0), reset_pair);
    int64_t ing0 = 0;
    int64_t egr0 = 0;
    uint16_t seq = 0x5900;
    expect("[T-LATW] an exchange at the reset pair completes",
           responder_gaps(dut, seq++, &ing0, &egr0) ? 1 : 0, 1);
    expect("[T-LATW] the reset pair is what the ingress stamp carries",
           static_cast<uint64_t>(ing0), static_cast<uint64_t>(kRxStampLagNs + kLatIngNs));
    expect("[T-LATW] the reset pair is what the egress stamp carries",
           static_cast<uint64_t>(egr0), static_cast<uint64_t>(kLatEgrNs));

    static constexpr uint32_t kPairs[][2] = {
        {777, 333}, {1409, 100}, {0, 0}, {65535, 1}};
    for (const auto &pair : kPairs) {
      axi_write(dut, 0x540, pair[0]);
      axi_write(dut, 0x544, pair[1]);
      expect("[T-LATW] GPTP_LAT reads the written pair back",
             axi_read(dut, 0x7F0), (pair[0] << 16) | pair[1]);
      int64_t ing = 0;
      int64_t egr = 0;
      expect("[T-LATW] an exchange under a written pair completes",
             responder_gaps(dut, seq++, &ing, &egr) ? 1 : 0, 1);
      expect("[T-LATW] the written ingress moves t2 by exactly it",
             static_cast<uint64_t>(ing - ing0 + kLatIngNs), pair[0]);
      expect("[T-LATW] the written egress moves t3 by exactly it",
             static_cast<uint64_t>(egr - egr0 + kLatEgrNs), pair[1]);
    }
    //! One direction's write leaves the other's correction where it was, and
    //! the high half of a word stays readable and is not applied.
    axi_write(dut, 0x540, 0xA5A50000u | 123u);
    expect("[T-LATW] 0x540 returns the whole word written",
           axi_read(dut, 0x540), 0xA5A50000u | 123u);
    expect("[T-LATW] an ingress write moves GPTP_LAT's ingress half alone",
           axi_read(dut, 0x7F0), (123u << 16) | 1u);
    axi_write(dut, 0x540, static_cast<uint32_t>(kLatIngNs));
    axi_write(dut, 0x544, static_cast<uint32_t>(kLatEgrNs));
    expect("[T-LATW] the reset pair written back is applied",
           axi_read(dut, 0x7F0), reset_pair);
  }
#endif

  // Keep answering Pdelay while the selected peer's Announce expires.
  // The resulting GM Sync/Follow_Up and one peer request exercise all five
"""),
("""  prove_the_board_latency_corrections_reach_both_stamps(dut);
  emit_every_gptp_tx_flag_type(dut);
""", """  prove_the_board_latency_corrections_reach_both_stamps(dut);
#ifdef GPTP_LAT_WRITABLE_TB
  prove_the_written_pair_reaches_both_stamps(dut);
#endif
  emit_every_gptp_tx_flag_type(dut);
"""),
])
patch("tb/verilator/milan_dp/Makefile", [
("""exec-gptp-lat:
	./obj_gptplat/Vmilan_dp_gptplat
""", """exec-gptp-lat:
	./obj_gptplat/Vmilan_dp_gptplat

# issue #829: THE SAME LEG ELABORATED WITH THE WRITABLE KEY. Everything the
# `gptp-lat` leg proves of the pair must hold of it as a reset value, and the
# bus then moves each stamp by exactly what is written.
gptp-latw: build-gptp-latw
	$(MAKE) --no-print-directory exec-gptp-latw

build-gptp-latw: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_ON_VFLAGS) --Mdir obj_gptplatw \\
	  -GMILAN_CLK_FREQ_HZ=2000000 -GGPTP_PHC_TICK_NS_P=8 \\
	  -GGPTP_INGRESS_LAT_NS_P=$(GPTP_LAT_ING) \\
	  -GGPTP_EGRESS_LAT_NS_P=$(GPTP_LAT_EGR) \\
	  -GGPTP_LAT_WRITABLE_P=1 \\
	  -CFLAGS "-DGPTP_LAT_ING_TB=$(GPTP_LAT_ING) -DGPTP_LAT_EGR_TB=$(GPTP_LAT_EGR) -DGPTP_LAT_WRITABLE_TB -Wall -Wextra" \\
	  $(SRCS) sim_gptp.cpp -o Vmilan_dp_gptplatw

exec-gptp-latw:
	./obj_gptplatw/Vmilan_dp_gptplatw
"""),
("""PREFIX_CASES = gptp gptp-lat $(COUNTER_CASES)
""", """PREFIX_CASES = gptp gptp-lat gptp-latw $(COUNTER_CASES)
"""),
])
