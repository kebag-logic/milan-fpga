/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Fabric-gPTP CSR ownership harness. The live publication bank owns the
 * legacy GM/parent/pdelay addresses, and each 64-bit identity is returned as
 * one snapshot even when the bank changes between AXI reads.
 */

#include "../../common/verilator_harness.hpp"
#include "Vmilan_csr.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

constexpr uint32_t A_ADP_GMLO = 0x624;
constexpr uint32_t A_ADP_GMHI = 0x628;
constexpr uint32_t A_GPTP_PDELAY = 0x6E4;
constexpr uint32_t A_AS2_LO = 0x730;
constexpr uint32_t A_AS2_HI = 0x734;
constexpr uint32_t A_ASP_LO = 0x7DC;
constexpr uint32_t A_ASP_HI = 0x7E0;
constexpr uint32_t A_ASP_CMD = 0x7E4;

//! Cycle bound on every AXI4-Lite handshake wait below: large enough that a
//! healthy DUT never reaches it, small enough that a wedged one still exits.
constexpr unsigned kAxiGuard = 4096;
//! Reset is held this many clocks before aresetn is released.
constexpr unsigned kResetTicks = 8;
//! Words in the flattened AS_PATH vector: 7 slots x two 32-bit Verilator words.
constexpr unsigned kAspPathWords = 14;

//! The three GM identities and the three parent identities the snapshot arms
//! rotate through. They are shared by the legacy-write arm and the pair-read
//! arm, so they are named once here rather than in each.
constexpr uint64_t gm_a = 0x001BC50000C0FFEFULL;
constexpr uint64_t gm_b = 0x1021324354657687ULL;
constexpr uint64_t gm_c = 0x98A9BACBDCEDFE0FULL;
constexpr uint64_t parent_a = 0x3CC0C6FFFE0210AAULL;
constexpr uint64_t parent_b = 0x405162738495A6B7ULL;
constexpr uint64_t parent_c = 0xC8D9EAFB0C1D2E3FULL;

//! The AS_PATH slot payloads. `path1` outlives the arm that publishes it: the
//! forge arm proves a software COMMIT cannot move it.
constexpr uint64_t path1 = 0x1111222233334444ULL;
constexpr uint64_t path2 = 0x5555666677778888ULL;
constexpr uint64_t path3 = 0x9999AAAABBBBCCCCULL;

namespace {

//! Owns the model, the counters and the AXI4-Lite BFM for this scenario, so no
//! function here depends on state a reader has to find at file scope (I.2).
class FabricGptpCsrHarness {
 public:
  int run();

 private:
  void tick();
  void check(const char* label, uint64_t got, uint64_t expected);
  void set_fabric_path(unsigned slot, uint64_t value);
  uint64_t live_path(unsigned slot);
  void axi_write(uint32_t address, uint32_t data);
  uint32_t axi_read(uint32_t address);

  void reset_and_idle_the_bus();
  void legacy_writes_never_move_fabric_publication();
  void served_domain_is_the_engine_constant();
  void identity_pairs_read_as_one_snapshot();
  void fabric_raw_empty_owns_public_output();
  void fabric_path_owns_public_output();
  void software_commands_cannot_forge_the_path();
  void later_publication_moves_the_public_face();
  void maximum_publication_reaches_the_last_slot();
  void drop_diagnostics_are_live_and_write_inert();

  const milan::tb::Model<Vmilan_csr> model;
  Vmilan_csr* dut = model.get();
  unsigned checks = 0;
  unsigned failures = 0;
};

void FabricGptpCsrHarness::tick() {
  dut->aclk = 1; dut->eval();
  dut->aclk = 0; dut->eval();
}

void FabricGptpCsrHarness::check(const char* label, uint64_t got, uint64_t expected) {
  checks++;
  if (got != expected) {
    failures++;
    std::printf("  [FAIL] %-52s got=0x%016llx exp=0x%016llx\n", label,
                static_cast<unsigned long long>(got),
                static_cast<unsigned long long>(expected));
  }
}

void FabricGptpCsrHarness::set_fabric_path(unsigned slot, uint64_t value) {
  dut->i_gptp_asp_path[2 * slot] = static_cast<uint32_t>(value);
  dut->i_gptp_asp_path[2 * slot + 1] = static_cast<uint32_t>(value >> 32);
}

uint64_t FabricGptpCsrHarness::live_path(unsigned slot) {
  return (static_cast<uint64_t>(dut->o_asp_path[2 * slot + 1]) << 32)
       | dut->o_asp_path[2 * slot];
}

void FabricGptpCsrHarness::axi_write(uint32_t address, uint32_t data) {
  dut->s_axi_awaddr = address;
  dut->s_axi_awvalid = 1;
  dut->s_axi_wdata = data;
  dut->s_axi_wstrb = 0xF;
  dut->s_axi_wvalid = 1;
  dut->s_axi_bready = 1;
  for (unsigned guard = 0; guard < kAxiGuard; guard++) {
    dut->eval();
    const bool accepted = dut->s_axi_awready && dut->s_axi_wready;
    tick();
    if (accepted) break;
  }
  dut->s_axi_awvalid = 0;
  dut->s_axi_wvalid = 0;
  for (unsigned guard = 0; guard < kAxiGuard && !dut->s_axi_bvalid; guard++)
    tick();
  tick();
  dut->s_axi_bready = 0;
}

uint32_t FabricGptpCsrHarness::axi_read(uint32_t address) {
  dut->s_axi_araddr = address;
  dut->s_axi_arvalid = 1;
  dut->s_axi_rready = 1;
  for (unsigned guard = 0; guard < kAxiGuard; guard++) {
    dut->eval();
    const bool accepted = dut->s_axi_arready;
    tick();
    if (accepted) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t value = 0;
  for (unsigned guard = 0; guard < kAxiGuard; guard++) {
    dut->eval();
    if (dut->s_axi_rvalid) { value = dut->s_axi_rdata; break; }
    tick();
  }
  tick();
  dut->s_axi_rready = 0;
  return value;
}

void FabricGptpCsrHarness::reset_and_idle_the_bus() {
  dut->aresetn = 0;
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0; dut->s_axi_bready = 0;
  dut->s_axi_arvalid = 0; dut->s_axi_rready = 0;
  dut->i_lctx_rd_valid = 1; dut->i_tctx_rd_valid = 1;
  dut->i_lctx_wr_rdy = 1; dut->i_tctx_wr_rdy = 1;
  dut->i_gptp_asp_count = 0;
  dut->i_gptp_asp_gen = 0;
  for (unsigned i = 0; i < kAspPathWords; i++) dut->i_gptp_asp_path[i] = 0;
  for (unsigned i = 0; i < kResetTicks; i++) tick();
  dut->aresetn = 1; tick();
}

void FabricGptpCsrHarness::legacy_writes_never_move_fabric_publication() {
  dut->i_gptp_gm_id = gm_a;
  dut->i_gptp_parent_id = parent_a;
  dut->i_gptp_pdelay_ns = 0x01020304;

  axi_write(A_ADP_GMLO, 0xDEADBEEF);
  axi_write(A_ADP_GMHI, 0xCAFEBABE);
  axi_write(A_AS2_LO, 0x0BADF00D);
  axi_write(A_AS2_HI, 0xFACEFEED);
  axi_write(A_GPTP_PDELAY, 0xA5A5A5A5);
  check("fabric pdelay ignores legacy writes",
        axi_read(A_GPTP_PDELAY), 0x01020304);
  check("fabric GM ignores legacy writes",
        (static_cast<uint64_t>(axi_read(A_ADP_GMHI)) << 32)
            | axi_read(A_ADP_GMLO),
        gm_a);
  check("fabric parent ignores legacy writes",
        (static_cast<uint64_t>(axi_read(A_AS2_HI)) << 32) | axi_read(A_AS2_LO),
        parent_a);
}

// The engine speaks only domain 0 (802.1AS 8.1). A legacy write must not
// move the served domain: the readback AND the o_adp_gptp_domain port every
// protocol face consumes stay at the engine constant. The option-off arm
// proves the other exact contract: structural domain zero and inert writes,
// with no alternate publication owner.
void FabricGptpCsrHarness::served_domain_is_the_engine_constant() {
  axi_write(0x62C, 0x00000005);
  dut->eval();
  check("fabric domain readback is the engine constant", axi_read(0x62C), 0);
  check("fabric domain port is the engine constant",
        dut->o_adp_gptp_domain, 0);
}

void FabricGptpCsrHarness::identity_pairs_read_as_one_snapshot() {
  dut->i_gptp_gm_id = gm_a;
  const uint32_t gm_lo = axi_read(A_ADP_GMLO);
  dut->i_gptp_gm_id = gm_b;
  const uint32_t gm_hi = axi_read(A_ADP_GMHI);
  check("GM LO-first pair remains one publication",
        (static_cast<uint64_t>(gm_hi) << 32) | gm_lo, gm_a);
  const uint32_t gm_hi_first = axi_read(A_ADP_GMHI);
  dut->i_gptp_gm_id = gm_c;
  const uint32_t gm_lo_second = axi_read(A_ADP_GMLO);
  check("GM HI-first pair remains one publication",
        (static_cast<uint64_t>(gm_hi_first) << 32) | gm_lo_second, gm_b);

  dut->i_gptp_parent_id = parent_a;
  const uint32_t parent_lo = axi_read(A_AS2_LO);
  dut->i_gptp_parent_id = parent_b;
  const uint32_t parent_hi = axi_read(A_AS2_HI);
  check("parent LO-first pair remains one publication",
        (static_cast<uint64_t>(parent_hi) << 32) | parent_lo, parent_a);
  const uint32_t parent_hi_first = axi_read(A_AS2_HI);
  dut->i_gptp_parent_id = parent_c;
  const uint32_t parent_lo_second = axi_read(A_AS2_LO);
  check("parent HI-first pair remains one publication",
        (static_cast<uint64_t>(parent_hi_first) << 32) | parent_lo_second,
        parent_b);
}

// Issue #116: in the product elaboration the public AS_PATH face and
// 0x7E4 are live fabric outputs. The old staging pair remains mapped but is
// inert: reads are zero and no write may forge the served path or advance
// the engine-owned generation.
//! Mutation bar for the fabric raw-empty contract: unlike option-off #227,
//! the selected donor's count zero is not an alternate spelling of `[GM]`.
//! CSR has no GM input and must pass the fabric owner tuple through exactly.
void FabricGptpCsrHarness::fabric_raw_empty_owns_public_output() {
  dut->i_gptp_asp_count = 0;
  dut->i_gptp_asp_gen = 7;
  dut->eval();
  check("fabric raw-empty count owns public output", dut->o_asp_count, 0);
  check("fabric raw-empty generation owns public output", dut->o_asp_gen, 7);
  check("0x7E4 preserves fabric raw-empty {generation,count}",
        axi_read(A_ASP_CMD), 0x00000070);
}

void FabricGptpCsrHarness::fabric_path_owns_public_output() {
  set_fabric_path(0, path1);
  set_fabric_path(1, path2);
  set_fabric_path(2, path3);
  dut->i_gptp_asp_count = 4;
  dut->i_gptp_asp_gen = 9;
  dut->eval();
  check("fabric AS_PATH count owns public output", dut->o_asp_count, 4);
  check("fabric AS_PATH generation owns public output", dut->o_asp_gen, 9);
  check("fabric AS_PATH slot 1 owns public output", live_path(0), path1);
  check("fabric AS_PATH slot 2 owns public output", live_path(1), path2);
  check("fabric AS_PATH slot 3 owns public output", live_path(2), path3);
  check("0x7E4 reads live fabric {generation,count}",
        axi_read(A_ASP_CMD), 0x00000094);
}

void FabricGptpCsrHarness::software_commands_cannot_forge_the_path() {
  const uint64_t forged = 0xDEADBEEF01234567ULL;
  axi_write(A_ASP_LO, static_cast<uint32_t>(forged));
  axi_write(A_ASP_HI, static_cast<uint32_t>(forged >> 32));
  check("retired staging LO reads zero", axi_read(A_ASP_LO), 0);
  check("retired staging HI reads zero", axi_read(A_ASP_HI), 0);
  axi_write(A_ASP_CMD, 0xC0000107u); // COMMIT slot 1 + PUBLISH count 7
  check("software COMMIT/PUBLISH cannot forge live slot", live_path(0), path1);
  check("software COMMIT/PUBLISH cannot forge live count", dut->o_asp_count, 4);
  check("software COMMIT/PUBLISH cannot spend fabric generation",
        dut->o_asp_gen, 9);
  check("0x7E4 still reads fabric state after software command",
        axi_read(A_ASP_CMD), 0x00000094);
}

void FabricGptpCsrHarness::later_publication_moves_the_public_face() {
  const uint64_t path1b = 0x0102030405060708ULL;
  set_fabric_path(0, path1b);
  dut->i_gptp_asp_count = 2;
  dut->i_gptp_asp_gen = 10;
  dut->eval();
  check("later fabric publication moves live slot", live_path(0), path1b);
  check("later fabric publication moves live count", dut->o_asp_count, 2);
  check("later fabric publication moves live generation", dut->o_asp_gen, 10);
  check("0x7E4 follows later fabric publication",
        axi_read(A_ASP_CMD), 0x000000A2);
}

void FabricGptpCsrHarness::maximum_publication_reaches_the_last_slot() {
  const uint64_t path7 = 0xD1D2D3D4D5D6D7D8ULL;
  set_fabric_path(6, path7);
  dut->i_gptp_asp_count = 8;
  dut->i_gptp_asp_gen = 11;
  dut->eval();
  check("maximum fabric AS_PATH count owns public output", dut->o_asp_count, 8);
  check("maximum fabric AS_PATH reaches public slot 7", live_path(6), path7);
  check("0x7E4 follows maximum fabric publication",
        axi_read(A_ASP_CMD), 0x000000B8);
}

// ---- issue #207: gPTP drop diagnostics at 0x7E8/0x7EC ------------------
// RO live, one-access-coherent packing, writes inert. The sources are the
// plane's three free-running 16-bit counters; the CSR truncates nothing.
void FabricGptpCsrHarness::drop_diagnostics_are_live_and_write_inert() {
  dut->i_gptp_tap_drop = 0; dut->i_gptp_rx_drop = 0; dut->i_gptp_ev_drop = 0;
  dut->eval();
  check("0x7E8 drop word idles at zero", axi_read(0x7E8), 0);
  check("0x7EC event word idles at zero", axi_read(0x7EC), 0);
  dut->i_gptp_tap_drop = 0xA1B2; dut->i_gptp_rx_drop = 0x0304;
  dut->i_gptp_ev_drop = 0xFFFF;
  dut->eval();
  check("0x7E8 packs {tap, rx} in one access", axi_read(0x7E8), 0xA1B20304u);
  check("0x7EC zero-extends the event count", axi_read(0x7EC), 0x0000FFFFu);
  axi_write(0x7E8, 0xDEADBEEFu);
  axi_write(0x7EC, 0xDEADBEEFu);
  check("0x7E8 write is inert", axi_read(0x7E8), 0xA1B20304u);
  check("0x7EC write is inert", axi_read(0x7EC), 0x0000FFFFu);
  dut->i_gptp_rx_drop = 0x0305;
  dut->eval();
  check("0x7E8 reads live, never a stale snapshot",
        axi_read(0x7E8), 0xA1B20305u);
}

int FabricGptpCsrHarness::run() {
  reset_and_idle_the_bus();
  legacy_writes_never_move_fabric_publication();
  served_domain_is_the_engine_constant();
  identity_pairs_read_as_one_snapshot();
  fabric_raw_empty_owns_public_output();
  fabric_path_owns_public_output();
  software_commands_cannot_forge_the_path();
  later_publication_moves_the_public_face();
  maximum_publication_reaches_the_last_slot();
  drop_diagnostics_are_live_and_write_inert();

  std::printf("checks: %u   failures: %u\n", checks, failures);
  return failures ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  FabricGptpCsrHarness harness;
  return harness.run();
}
