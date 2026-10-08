// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R554-2): failure-report offset sweep around a command
// cancellation at one AVB interface (KL_aecp_notify, N_CTRL_P=2, N_IF_P=1).
//
// Mode C (coincident): row `expired` is TIME_LIMITED; both rows have live
// probes. The TIME_LIMITED expiry drains `expired`; in the drain's cancel cycle
// (cycle 0) the other ("live") controller sends one command. A failure for the
// live owner is presented at cycle k (k = -1: no failure).
// Mode U (uncontended): no expiry; the live controller's command is cycle 0 and
// its failure is presented at cycle k.
// Each line reports every cancellation (owner@cycle), the final registry count
// and whether a DEREGISTER targeted the live controller.
#include <array>
#include <cstdint>
#include <cstdio>
#include <string>
#include "VKL_aecp_notify.h"
#include "verilated.h"

static constexpr uint8_t OWN_TL = 0xA0;
static constexpr uint8_t OWN_MON = 0xD0;
static constexpr uint8_t REGMON_BASE = 25;
static constexpr uint8_t N_CTRL = 2;
static constexpr uint8_t KIND_DEREG = 0;

struct P {
  VKL_aecp_notify* d;
  uint32_t now = 1000;
  void tick() { d->now_ms_i = now; d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
  void idle(int n) { for (int i = 0; i < n; ++i) tick(); }
  void init() {
    d->rgy_req_i = 0; d->rgy_state_i = 0; d->rgy_op_i = 0; d->rgy_eid_i = 0; d->rgy_mac_i = 0;
    d->rgy_tl_i = 0; d->ev_stri_in_i = 0; d->ev_stri_out_i = 0; d->ev_avb_i = 0; d->ev_asp_i = 0;
    d->ev_amap_i = 0; d->ev_amap_remove_i = 0; d->ev_amap_type_i = 0; d->ev_amap_index_i = 0;
    d->ev_amap_count_i = 0; d->ev_amap_excl_eid_i = 0; d->ev_ctr_i = 0; d->ev_ctr_type_i = 0;
    d->ev_ctr_index_i = 0; d->ev_cmd_i = 0; d->ev_cmd_class_i = 0; d->ev_cmd_type_i = 0;
    d->ev_cmd_index_i = 0; d->ev_cmd_arg0_i = 0; d->ev_cmd_arg1_i = 0; d->ev_cmd_excl_eid_i = 0;
    d->rx_cmd_valid_i = 0; d->rx_cmd_eid_i = 0; d->rx_cmd_mac_i = 0; d->prng_draw_busy_i = 1;
    d->prng_draw_valid_i = 0; d->prng_draw_ms_i = 0; d->ca_ready_i = 1; d->ca_rsp_valid_i = 0;
    d->ca_rsp_owner_i = 0; d->ca_fail_valid_i = 0; d->ca_fail_owner_i = 0; d->uns_done_i = 1;
    d->tmr_exp_valid_i = 0; d->tmr_exp_slot_i = 0; d->tmr_exp_owner_i = 0;
    d->rst_n = 0; idle(4); d->rst_n = 1; idle(2);
  }
  bool registers(uint64_t eid, uint64_t mac, bool tl) {
    d->rgy_state_i = 0; d->rgy_op_i = 0; d->rgy_eid_i = eid; d->rgy_mac_i = mac;
    d->rgy_tl_i = tl; d->rgy_req_i = 1;
    int g = 0;
    while (g++ < 24) { d->clk_i = 0; d->eval(); if (!d->rgy_wait_o) break; tick(); }
    bool ok = g < 24 && d->rgy_data_o == 0;
    tick(); d->rgy_req_i = 0; idle(2);
    return ok;
  }
  bool draws() {
    d->prng_draw_busy_i = 0;
    int g = 0;
    while (g++ < 16) { d->clk_i = 0; d->eval(); if (d->prng_draw_req_o) break; tick(); }
    bool ok = g < 16;
    d->prng_draw_ms_i = 30000; d->prng_draw_valid_i = 1; tick();
    d->prng_draw_valid_i = 0; d->prng_draw_busy_i = 1; idle(2);
    return ok;
  }
  void expire(uint8_t slot, uint8_t owner) {
    d->tmr_exp_slot_i = slot; d->tmr_exp_owner_i = owner; d->tmr_exp_valid_i = 1; tick();
    d->tmr_exp_valid_i = 0;
  }
};

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const std::string tag = argc > 1 ? argv[1] : "tree";
  const std::array<uint64_t, N_CTRL> eids = {0x1111000000000001ull, 0x3333000000000003ull};
  const std::array<uint64_t, N_CTRL> macs = {0x020000000001ull, 0x020000000003ull};
  int setup_fail = 0;
  for (char mode : {'U', 'C'}) {
    for (unsigned expired = 0; expired < N_CTRL; ++expired) {
      for (int k = -1; k <= 3; ++k) {
        VerilatedContext ctx;
        VKL_aecp_notify* dut = new VKL_aecp_notify{&ctx};
        P p{dut};
        p.init();
        const unsigned live = 1 - expired;
        bool ok = true;
        for (unsigned row = 0; row < N_CTRL; ++row) {
          ok &= p.registers(eids[row], macs[row], mode == 'C' && row == expired);
          ok &= p.draws();
          p.expire(REGMON_BASE + N_CTRL + row, OWN_MON | row);
          bool probe = false;
          for (int c = 0; c < 12; ++c) {
            dut->clk_i = 0; dut->eval();
            if (dut->ca_valid_o) { probe = dut->ca_owner_o == row; p.tick(); break; }
            p.tick();
          }
          ok &= probe;
        }
        if (mode == 'C') p.expire(REGMON_BASE + expired, OWN_TL | expired);
        else p.idle(3);
        std::string cancels;
        int c0 = (mode == 'U') ? 0 : -1;
        unsigned dereg_live = 0, dereg_expired = 0;
        for (int c = 0; c < 400; ++c) {
          dut->rx_cmd_valid_i = 0; dut->ca_fail_valid_i = 0;
          dut->clk_i = 0; dut->eval();
          if (c0 < 0 && dut->ca_cancel_valid_o && dut->ca_cancel_owner_o == expired) c0 = c;
          if (c == c0) {
            dut->rx_cmd_eid_i = eids[live]; dut->rx_cmd_mac_i = macs[live];
            dut->rx_cmd_valid_i = 1; dut->eval();
          }
          if (c0 >= 0 && k >= 0 && c == c0 + k) {
            dut->ca_fail_valid_i = 1; dut->ca_fail_owner_i = live; dut->eval();
          }
          if (dut->ca_cancel_valid_o)
            cancels += std::to_string(dut->ca_cancel_owner_o) + "@" + std::to_string(c - c0) + " ";
          if (dut->uns_valid_o && dut->uns_kind_o == KIND_DEREG) {
            if (static_cast<uint64_t>(dut->uns_mac_o) == macs[live]) ++dereg_live;
            if (static_cast<uint64_t>(dut->uns_mac_o) == macs[expired]) ++dereg_expired;
          }
          p.tick();
        }
        if (!ok || c0 < 0) ++setup_fail;
        printf("%s mode=%c expired=%u live=%u fail_k=%+d setup=%s cancels=[%s] entries=%u "
               "dereg_live_jobs=%u dereg_expired_jobs=%u live_row=%s\n",
               tag.c_str(), mode, expired, live, k, (ok && c0 >= 0) ? "ok" : "BAD",
               cancels.c_str(), dut->dbg_reg_cnt_o, dereg_live, dereg_expired,
               (mode == 'C' ? dut->dbg_reg_cnt_o == 1 : dut->dbg_reg_cnt_o == 2) ? "KEPT" : "REMOVED");
        dut->final();
        delete dut;
      }
    }
  }
  printf("%s setup failures: %d\n", tag.c_str(), setup_fail);
  return setup_fail ? 1 : 0;
}
