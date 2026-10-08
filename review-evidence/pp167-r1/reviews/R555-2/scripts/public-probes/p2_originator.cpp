// Probe P2 (reviewer, disposable): KL_pp_originator at its default
// parameters. Owner 1 has one live exchange; its retry has been accepted and
// its second timeout fires. In the cycle the parked expiry is serviced (E),
// the probe presents a cancellation for owner `cancel_owner_at_e`
// (-1 = none). Owner 0 has no table entry, standing for a TIME_LIMITED
// drain's cancellation of a probe still in the frame builder. The cancel for
// owner 1 then follows at E+1, as the pending count-one cancel does.
// Prints whether fail_valid_o fired for owner 1, and at which offset.
#include <cstdint>
#include <cstdio>
#include "VKL_pp_originator.h"
#include "verilated.h"

static VKL_pp_originator* d;
static uint32_t now = 1000;
static int cyc = 0;
static int fail_cycle = -1;
static int fail_owner = -1;
static bool arm_seen = false;
static uint8_t arm_slot = 0, arm_owner = 0;

static void clr() {
  d->iss_valid_i = 0; d->cancel_valid_i = 0; d->rsp_valid_i = 0;
  d->exp_valid_i = 0; d->send_accept_valid_i = 0;
}
static void tick() {
  d->now_ms_i = now;
  d->clk_i = 0; d->eval();
  if (d->fail_valid_o && fail_cycle < 0) { fail_cycle = cyc; fail_owner = d->fail_owner_o; }
  if (d->tmr_arm_valid_o && !d->tmr_arm_cancel_o) {
    arm_seen = true; arm_slot = d->tmr_arm_slot_o; arm_owner = d->tmr_arm_owner_o;
  }
  d->clk_i = 1; d->eval();
  ++cyc;
}

static void scenario(int cancel_owner_at_e) {
  d->rst_n = 0; clr(); tick(); tick(); d->rst_n = 1; tick();
  fail_cycle = -1; fail_owner = -1; arm_seen = false;
  // issue owner 1 on TX slot 2, timer slot 60, 250 ms
  clr(); d->iss_valid_i = 1; d->iss_owner_i = 1; d->iss_tx_slot_i = 2;
  d->iss_key_i = 0x1234; d->iss_tmr_slot_i = 60; d->iss_timeout_ms_i = 250; tick();
  clr(); tick();
  for (int attempt = 0; attempt < 2; ++attempt) {
    clr(); d->send_accept_valid_i = 1; d->send_accept_slot_i = 2; tick();
    clr(); for (int i = 0; i < 4; ++i) tick();
    now += 300;
    if (attempt == 0) {
      clr(); d->exp_valid_i = 1; d->exp_slot_i = arm_slot; d->exp_owner_i = arm_owner; tick();
      clr(); for (int i = 0; i < 4; ++i) tick();         // first timeout -> resend
    }
  }
  // second timeout: the expiry pulse parks it; the next cycle (E) services it
  clr(); d->exp_valid_i = 1; d->exp_slot_i = arm_slot; d->exp_owner_i = arm_owner; tick();
  const int e = cyc;
  clr();
  if (cancel_owner_at_e >= 0) { d->cancel_valid_i = 1; d->cancel_owner_i = cancel_owner_at_e; }
  tick();                                                  // cycle E
  clr(); d->cancel_valid_i = 1; d->cancel_owner_i = 1; tick();   // E+1: pending cancel for owner 1
  clr(); for (int i = 0; i < 4; ++i) tick();
  printf("[probe P2] cancel_at_E=%d fail_for_owner1=%d fail_offset_from_E=%d\n",
         cancel_owner_at_e, int(fail_cycle >= 0 && fail_owner == 1),
         fail_cycle >= 0 ? fail_cycle - e : -1);
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = new VKL_pp_originator;
  scenario(0);    // drain cancel misses the table (probe in the builder)
  scenario(1);    // base timing: the command's own cancel lands at E
  scenario(-1);   // no cancel at E
  delete d;
  return 0;
}
