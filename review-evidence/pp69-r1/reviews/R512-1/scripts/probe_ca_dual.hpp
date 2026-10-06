// Reviewer probe (disposable; not a repository test). Included at the end of a
// scratch copy of tb/aecp_notify/port_tuple.hpp, third build (N_IF_P = 2,
// N_CTRL_P = 2). Question: when one controller holds two registry rows (same
// {Entity ID, MAC}, ports 0 and 1) and BOTH rows' CONTROLLER_AVAILABLE probes
// are live, does one command from that controller cancel both probes?
// Observed per cycle: ca_cancel_valid_o / ca_cancel_owner_o. Then the probe
// that was not cancelled is reported failed (ca_fail for its owner), as the
// originator would report an exchange nobody cancelled, and the row count and
// any DEREGISTER job are read.
static constexpr uint8_t PR_OWN_MON = 0xD0;
static constexpr uint8_t PR_REGMON_BASE = 25;
static constexpr uint8_t PR_N_CTRL = 2;

void probe_ca_dual(PortHarness& h) {
  auto* d = h.d;
  h.warm_reset();
  h.now = 5000;
  const uint64_t r0 = h.op(PortHarness::OP_REGISTER, PortHarness::EID_E, PortHarness::MAC_E, 0);
  const uint64_t r1 = h.op(PortHarness::OP_REGISTER, PortHarness::EID_E, PortHarness::MAC_E, 1);
  printf("PROBE registered: results %llu %llu, rows %u\n", (unsigned long long)r0,
         (unsigned long long)r1, h.rows());
  // serve the two monitor draws the REGISTERs requested
  int draws = 0;
  d->prng_draw_busy_i = 0;
  for (int c = 0; c < 200 && draws < 2; ++c) {
    d->clk_i = 0;
    d->eval();
    if (d->prng_draw_req_o) {
      h.tick();
      d->prng_draw_ms_i = 30000;
      d->prng_draw_valid_i = 1;
      h.tick();
      d->prng_draw_valid_i = 0;
      ++draws;
      continue;
    }
    h.tick();
  }
  d->prng_draw_busy_i = 1;
  h.idle(4);
  printf("PROBE monitor draws served: %d\n", draws);
  // both rows' monitor deadlines expire (probe requests held until observed)
  d->ca_ready_i = 0;
  for (uint8_t ix = 0; ix < 2; ++ix) {
    d->tmr_exp_slot_i = PR_REGMON_BASE + PR_N_CTRL + ix;
    d->tmr_exp_owner_i = PR_OWN_MON | ix;
    d->tmr_exp_valid_i = 1;
    h.tick();
    d->tmr_exp_valid_i = 0;
    h.idle(2);
  }
  // the probes are requested and taken (ca_ready_i = 1)
  int probes = 0;
  unsigned owners = 0;
  d->ca_ready_i = 1;
  for (int c = 0; c < 40; ++c) {
    d->clk_i = 0;
    d->eval();
    if (d->ca_valid_o && d->ca_ready_i) {
      ++probes;
      owners |= 1u << d->ca_owner_o;
    }
    h.tick();
  }
  printf("PROBE probes issued: %d (owner mask 0x%x)\n", probes, owners);
  // one command from E: watch every cancel for 16 cycles
  unsigned cancelled = 0;
  int cancels = 0;
  d->rx_cmd_eid_i = PortHarness::EID_E;
  d->rx_cmd_mac_i = PortHarness::MAC_E;
  d->rx_cmd_valid_i = 1;
  for (int c = 0; c < 16; ++c) {
    d->clk_i = 0;
    d->eval();
    if (d->ca_cancel_valid_o) {
      ++cancels;
      cancelled |= 1u << d->ca_cancel_owner_o;
    }
    h.tick();
    d->rx_cmd_valid_i = 0;
  }
  printf("PROBE one command from E: %d cancel strobe(s), cancelled owner mask 0x%x "
         "(probing owners 0x%x)\n", cancels, cancelled, owners);
  // the exchange nobody cancelled runs out at the originator
  const unsigned orphan = (owners & ~cancelled) & 3u;
  if (orphan != 0) {
    const uint8_t o = (orphan & 1u) ? 0 : 1;
    const unsigned before = h.rows();
    d->ca_fail_owner_i = o;
    d->ca_fail_valid_i = 1;
    h.tick();
    d->ca_fail_valid_i = 0;
    h.idle(8);
    const PortHarness::Job j = h.presented(h.now + 20);
    printf("PROBE ca_fail for un-cancelled owner %u: rows %u -> %u; next job (ms %u) kind %u to mac "
           "%012llx (kind 0 = DEREGISTER)\n", unsigned(o), before, h.rows(), unsigned(j.ms), unsigned(j.kind),
           (unsigned long long)j.mac);
  } else {
    printf("PROBE every probing owner was cancelled\n");
  }
}
