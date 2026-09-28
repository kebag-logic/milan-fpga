// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "Vcarrier_probe.h"
#include "verilator_harness.hpp"
#include <array>
#include <string_view>

class Probe {
 public:
  milan::tb::Model<Vcarrier_probe> dut;
  milan::tb::Checker check{"carrier-probe"};
  unsigned cycles = 0;
  unsigned writes = 0;
  unsigned slot_acks = 0;
  unsigned port_completions = 0;
  unsigned memory_reads = 0;
  unsigned clear_cycle = 0;
  unsigned device_done_cycle = 0;
  unsigned port_done_cycle = 0;
  bool pending_seen = false;
  std::array<unsigned char, 4096> memory{};

  void tick() {
    dut->clk_i = 0;
    dut->eval();
    ++cycles;
    if (dut->device_write_o) ++writes;
    if (dut->port_done_o) { ++port_completions; port_done_cycle = cycles; }
    if (dut->device_done_o) device_done_cycle = cycles;
    if (dut->mem_read_o) ++memory_reads;
    if (dut->mem_write_o && dut->finish_memory_i) {
      for (unsigned lane = 0; lane < 8; ++lane) {
        if ((dut->mem_strb_o >> lane) & 1u)
          memory.at((dut->mem_addr_o - 0x1000u) + lane) =
              static_cast<unsigned char>(dut->mem_data_o >> (8u * lane));
      }
    }
    dut->clk_i = 1;
    dut->eval();
    if (dut->producer_pending_o) pending_seen = true;
    if (pending_seen && !dut->producer_pending_o && !clear_cycle) clear_cycle = cycles;
  }

  void wait_cycles(unsigned count) {
    for (unsigned i = 0; i < count; ++i) tick();
  }

  void csr(unsigned address, unsigned data) {
    if (address == 4 && (data & 2u)) ++slot_acks;
    dut->csr_we_i = 1;
    dut->csr_addr_i = address;
    dut->csr_data_i = data;
    tick();
    dut->csr_we_i = 0;
    tick();
  }

  void boot() {
    check.echo_passes();
    dut->rst_n = 0;
    dut->finish_memory_i = 1;
    wait_cycles(5);
    dut->rst_n = 1;
    wait_cycles(10);
    dut->go_i = 1;
    tick();
    dut->go_i = 0;
    for (unsigned i = 0; i < 1000 && !dut->restored_o; ++i) tick();
    check.that("BOOT: blank binding walk reaches RUN", dut->restored_o);
    csr(0, 0x1000);
    csr(1, 4096);
    csr(3, 0x10);  // valid image, no failure
    csr(4, 0x40);  // accepted boot RELOAD, not a slot ACK
    csr(4, 1);     // heartbeat
  }

  void materialize(bool stall) {
    dut->finish_memory_i = !stall;
    dut->change_i = 1;
    tick();
    dut->change_i = 0;
    wait_cycles(2000);
    check.that("CAPTURE: producer pending rose", pending_seen);
    if (stall) {
      check.that("CONTROL: unfinished window operation keeps producer pending",
                 dut->producer_pending_o && !clear_cycle && !dut->backend_dirty_o);
      return;
    }
    check.dec("WINDOW: exactly one record WRITE", writes, 1);
    check.dec("WINDOW: producer retired before slot ACK", dut->producer_pending_o, 0);
    check.dec("WINDOW: backend owns unsaved work", dut->backend_dirty_o, 1);
    check.dec("WINDOW: no slot ACK issued", slot_acks, 0);
    check.that("WINDOW: producer clear follows device completion",
               clear_cycle > device_done_cycle && clear_cycle == port_done_cycle);
    std::printf("TRACE window_device_done=%u port_done=%u producer_clear=%u slot_acks=%u\n",
                device_done_cycle, port_done_cycle, clear_cycle, slot_acks);
  }

  void fail_transactions(bool require_carrier) {
    for (unsigned attempt = 0; attempt < 3; ++attempt) {
      csr(4, 8);     // ARM captures the complete record work
      csr(4, 16);    // ATTEST the stable snapshot
      dut->csr_addr_i = 3;
      tick();
      constexpr unsigned capture_mask = (1u << 16) | (1u << 18) | (1u << 19);
      check.hex("CAPTURE: open, valid and attested before START",
                dut->csr_rdata_o & capture_mask, capture_mask);
      csr(4, 4);     // START
      csr(3, 0x1D);  // VD_VERIFY loss, with no ACK
      check.dec("FAILURE: backend retains unsaved work", dut->backend_dirty_o, 1);
      check.dec("FAILURE: stale reports the loss", dut->backend_stale_o, 1);
      check.dec("FAILURE: record producer remains retired", dut->producer_pending_o, 0);
      std::printf("TRACE attempt=%u cycle=%u pending=%u backend_dirty=%u stale=%u alarm=%u\n",
                  attempt + 1, cycles, dut->producer_pending_o, dut->backend_dirty_o,
                  dut->backend_stale_o, dut->alarm_o);
      csr(4, 32);    // RELEASE returns failed captured work to backend dirty
      if (attempt < 2) { wait_cycles(5000); csr(4, 1); wait_cycles(5000); }
    }
    check.dec("FAILURE: no slot ACK issued", slot_acks, 0);
    check.dec("FAILURE: no producer retry triggered", writes, 1);
    check.dec("FAILURE: no producer alarm", dut->alarm_o, 0);
    if (require_carrier)
      check.dec("DR2C-CARRIER-3: failed slot leaves record producer un-ACKed",
                dut->producer_pending_o, 1);
  }

  int run(bool require_carrier, bool stall) {
    boot();
    materialize(stall);
    if (!stall) fail_transactions(require_carrier);
    check.dec("SCOPE: no unsupported memory read used", memory_reads, 0);
    return check.report();
  }
};

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Probe probe;
  const std::string_view mode = argc > 1 ? argv[1] : "golden";
  return probe.run(mode == "require-carrier", mode == "stall-window");
}
