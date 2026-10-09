// SPDX-License-Identifier: CERN-OHL-W-2.0
// Read-only issue 168 diagnostic, using the committed listener harness.
// No reference-model expectations are used by the diagnostic cases.
#define main committed_listener_suite_main
#include "sim_main.cpp"
#undef main

struct Diagnostic {
  const milan::tb::Model<VKL_pp_acmp_listener> dut;
  Harness h{dut.get()};
  int checks = 0;
  int fails = 0;

  Diagnostic() {
    auto* d = dut.get();
    d->rst_n = 0; d->txn_valid_i = 0; d->evt_tk_valid_i = 0;
    d->pre_valid_i = 0; d->lock_held_i = 0; d->lock_ctlr_i = 0;
    d->entity_id_i = OUR_EID;
    for (int i = 0; i < 4; ++i) h.tick();
    d->rst_n = 1;
    for (int i = 0; i < 12; ++i) h.tick();
    CHECK(d->txn_ready_o == 1, "diagnostic reset completes");
    h.col.clear();
  }
  void drive(const Stim& s) {
    h.col.clear();
    CHECK(h.drive(0, s), "diagnostic stimulus completes");
  }
  Pdu bind(uint64_t controller) {
    Stim s; s.msg = M_BIND; s.tk_eid = TK_A; s.tk_uid = TKUID_A;
    s.ctlr = controller; s.seq = 0x4100;
    drive(s);
    Pdu probe{};
    for (const auto& frame : h.col.frames)
      if (frame.b[1] == M_PROBE_CMD) probe = frame;
    return probe;
  }
  Stim response(const Pdu& probe) {
    auto read = [&](int off, int n) {
      uint64_t v = 0;
      for (int i = 0; i < n; ++i) v = (v << 8) | probe.b[off + i];
      return v;
    };
    Stim s; s.msg = M_PROBE_RESP; s.ctlr = read(12, 8);
    s.tk_eid = read(20, 8); s.tk_uid = uint16_t(read(36, 2));
    s.seq = uint16_t(read(48, 2)); s.sid = 0x5544332211002233ull;
    s.da = 0x91E0F0004455ull; s.vlan = 2;
    return s;
  }
  int vlan() {
    const Pdu probe = bind(CTL1);
    auto s = response(probe); s.vlan = 0xA123;
    drive(s);
    CHECK(h.col.settle, "VLAN response settles");
    printf("OBS VLAN received=0x%04x action=0x%04x record=0x%04x\n",
           s.vlan, h.col.settle_vlan, h.shadow[0].vlan);
    // Milan v1.2 5.3.8.9: preserve the received SRP parameter.
    CHECK(h.col.settle_vlan == s.vlan, "VLAN full field at settle action");
    Stim get; get.msg = M_GETRX; get.ctlr = CTL1; get.seq = 0x4300;
    drive(get);
    CHECK(h.col.frames.size() == 1, "VLAN GET_RX_STATE response exists");
    if (h.col.frames.size() == 1) {
      const auto& p = h.col.frames[0];
      unsigned observed = (unsigned(p.b[52]) << 8) | p.b[53];
      printf("OBS VLAN GET_RX_STATE=0x%04x expected=0x%04x\n", observed, s.vlan);
      // Milan v1.2 Table 5.38 and 5.3.8.9.
      CHECK(observed == s.vlan, "VLAN full field in GET_RX_STATE");
    }
    return fails;
  }
  int old_controller() {
    const Pdu probe = bind(CTL1);
    bind(CTL2);
    CHECK(h.shadow[0].bind_ctlr == CTL2 && h.shadow[0].sm == S_PWR,
          "same-talker rebind changes binding controller while probe remains pending");
    drive(response(probe));
    printf("OBS saved-controller response settle=%u state=%s\n",
           unsigned(h.col.settle), SN[h.shadow[0].sm]);
    // Milan v1.2 5.5.3.5.17 step 2 and 5.5.3.5.18 step 1.
    CHECK(h.col.settle && h.shadow[0].sm == S_SNR,
          "guard accepts controller from sent probe after same-talker rebind");
    return fails;
  }
  int new_controller() {
    const Pdu probe = bind(CTL1);
    bind(CTL2);
    auto s = response(probe); s.ctlr = CTL2;
    drive(s);
    printf("OBS current-controller response settle=%u state=%s\n",
           unsigned(h.col.settle), SN[h.shadow[0].sm]);
    // Milan v1.2 5.5.3.5.18 step 1: current binding is not the sent probe.
    CHECK(!h.col.settle && h.shadow[0].sm == S_PWR,
          "guard rejects controller absent from sent probe after same-talker rebind");
    return fails;
  }
  int duplicate() {
    const Pdu probe = bind(CTL1);
    bind(CTL2);
    Stim expiry; expiry.k = Stim::EXP;
    drive(expiry);
    CHECK(h.col.frames.size() == 1, "duplicate probe exists");
    if (h.col.frames.size() == 1) {
      const auto& retry = h.col.frames[0];
      bool same = memcmp(probe.b, retry.b, PDU_BYTES) == 0;
      printf("OBS retry byte-identical=%u\n", unsigned(same));
      // Milan v1.2 5.5.3.5.16 step 1.
      CHECK(same, "retry preserves original probe after same-talker rebind");
    }
    return fails;
  }
};

int main(int argc, char** argv) {
  if (argc > 1 && std::string(argv[1]) == "--baseline")
    return committed_listener_suite_main(argc, argv);
  Verilated::commandArgs(argc, argv);
  int failures = 0;
  { Diagnostic d; failures += d.vlan(); }
  { Diagnostic d; failures += d.old_controller(); }
  { Diagnostic d; failures += d.new_controller(); }
  { Diagnostic d; failures += d.duplicate(); }
  printf("STOP diagnostic: %d clause failures\n", failures);
  return failures ? 1 : 0;
}
