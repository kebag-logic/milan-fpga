/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Fabric-gPTP CSR ownership harness. The live publication bank owns the
 * legacy GM/parent/pdelay addresses, and each 64-bit identity is returned as
 * one snapshot even when the bank changes between AXI reads.
 */

#include "Vmilan_csr.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

enum {
  A_ADP_GMLO = 0x624,
  A_ADP_GMHI = 0x628,
  A_GPTP_PDELAY = 0x6E4,
  A_AS2_LO = 0x730,
  A_AS2_HI = 0x734,
  A_ASP_LO = 0x7DC,
  A_ASP_HI = 0x7E0,
  A_ASP_CMD = 0x7E4,
};

static Vmilan_csr* dut;
static unsigned checks, failures;

static void tick() {
  dut->aclk = 1; dut->eval();
  dut->aclk = 0; dut->eval();
}

static void check(const char* label, uint64_t got, uint64_t expected) {
  checks++;
  if (got != expected) {
    failures++;
    std::printf("  [FAIL] %-52s got=0x%016llx exp=0x%016llx\n", label,
                (unsigned long long)got, (unsigned long long)expected);
  }
}

static void set_fabric_path(unsigned slot, uint64_t value) {
  dut->i_gptp_asp_path[2 * slot] = (uint32_t)value;
  dut->i_gptp_asp_path[2 * slot + 1] = (uint32_t)(value >> 32);
}

static uint64_t live_path(unsigned slot) {
  return ((uint64_t)dut->o_asp_path[2 * slot + 1] << 32)
       | dut->o_asp_path[2 * slot];
}

static void axi_write(uint32_t address, uint32_t data) {
  dut->s_axi_awaddr = address;
  dut->s_axi_awvalid = 1;
  dut->s_axi_wdata = data;
  dut->s_axi_wstrb = 0xF;
  dut->s_axi_wvalid = 1;
  dut->s_axi_bready = 1;
  for (unsigned guard = 0; guard < 4096; guard++) {
    dut->eval();
    const bool accepted = dut->s_axi_awready && dut->s_axi_wready;
    tick();
    if (accepted) break;
  }
  dut->s_axi_awvalid = 0;
  dut->s_axi_wvalid = 0;
  for (unsigned guard = 0; guard < 4096 && !dut->s_axi_bvalid; guard++) tick();
  tick();
  dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint32_t address) {
  dut->s_axi_araddr = address;
  dut->s_axi_arvalid = 1;
  dut->s_axi_rready = 1;
  for (unsigned guard = 0; guard < 4096; guard++) {
    dut->eval();
    const bool accepted = dut->s_axi_arready;
    tick();
    if (accepted) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t value = 0;
  for (unsigned guard = 0; guard < 4096; guard++) {
    dut->eval();
    if (dut->s_axi_rvalid) { value = dut->s_axi_rdata; break; }
    tick();
  }
  tick();
  dut->s_axi_rready = 0;
  return value;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vmilan_csr;
  dut->aresetn = 0;
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0; dut->s_axi_bready = 0;
  dut->s_axi_arvalid = 0; dut->s_axi_rready = 0;
  dut->i_lctx_rd_valid = 1; dut->i_tctx_rd_valid = 1;
  dut->i_lctx_wr_rdy = 1; dut->i_tctx_wr_rdy = 1;
  dut->i_gptp_asp_count = 0;
  dut->i_gptp_asp_gen = 0;
  for (unsigned i = 0; i < 14; i++) dut->i_gptp_asp_path[i] = 0;
  for (unsigned i = 0; i < 8; i++) tick();
  dut->aresetn = 1; tick();

  const uint64_t gm_a = 0x001BC50000C0FFEFULL;
  const uint64_t gm_b = 0x1021324354657687ULL;
  const uint64_t gm_c = 0x98A9BACBDCEDFE0FULL;
  const uint64_t parent_a = 0x3CC0C6FFFE0210AAULL;
  const uint64_t parent_b = 0x405162738495A6B7ULL;
  const uint64_t parent_c = 0xC8D9EAFB0C1D2E3FULL;
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
        ((uint64_t)axi_read(A_ADP_GMHI) << 32) | axi_read(A_ADP_GMLO), gm_a);
  check("fabric parent ignores legacy writes",
        ((uint64_t)axi_read(A_AS2_HI) << 32) | axi_read(A_AS2_LO), parent_a);

  // The engine speaks only domain 0 (802.1AS 8.1). A legacy write must not
  // move the served domain: the readback AND the o_adp_gptp_domain port every
  // protocol face consumes stay at the engine constant. The option-off arm
  // proves the other exact contract: structural domain zero and inert writes,
  // with no alternate publication owner.
  axi_write(0x62C, 0x00000005);
  dut->eval();
  check("fabric domain readback is the engine constant", axi_read(0x62C), 0);
  check("fabric domain port is the engine constant",
        dut->o_adp_gptp_domain, 0);

  dut->i_gptp_gm_id = gm_a;
  const uint32_t gm_lo = axi_read(A_ADP_GMLO);
  dut->i_gptp_gm_id = gm_b;
  const uint32_t gm_hi = axi_read(A_ADP_GMHI);
  check("GM LO-first pair remains one publication",
        ((uint64_t)gm_hi << 32) | gm_lo, gm_a);
  const uint32_t gm_hi_first = axi_read(A_ADP_GMHI);
  dut->i_gptp_gm_id = gm_c;
  const uint32_t gm_lo_second = axi_read(A_ADP_GMLO);
  check("GM HI-first pair remains one publication",
        ((uint64_t)gm_hi_first << 32) | gm_lo_second, gm_b);

  dut->i_gptp_parent_id = parent_a;
  const uint32_t parent_lo = axi_read(A_AS2_LO);
  dut->i_gptp_parent_id = parent_b;
  const uint32_t parent_hi = axi_read(A_AS2_HI);
  check("parent LO-first pair remains one publication",
        ((uint64_t)parent_hi << 32) | parent_lo, parent_a);
  const uint32_t parent_hi_first = axi_read(A_AS2_HI);
  dut->i_gptp_parent_id = parent_c;
  const uint32_t parent_lo_second = axi_read(A_AS2_LO);
  check("parent HI-first pair remains one publication",
        ((uint64_t)parent_hi_first << 32) | parent_lo_second, parent_b);

  // Issue #116: in the product elaboration the public AS_PATH face and
  // 0x7E4 are live fabric outputs. The old staging pair remains mapped but is
  // inert: reads are zero and no write may forge the served path or advance
  // the engine-owned generation.
  //! Mutation bar for the fabric raw-empty contract: unlike option-off #227,
  //! the selected donor's count zero is not an alternate spelling of `[GM]`.
  //! CSR has no GM input and must pass the fabric owner tuple through exactly.
  dut->i_gptp_asp_count = 0;
  dut->i_gptp_asp_gen = 7;
  dut->eval();
  check("fabric raw-empty count owns public output", dut->o_asp_count, 0);
  check("fabric raw-empty generation owns public output", dut->o_asp_gen, 7);
  check("0x7E4 preserves fabric raw-empty {generation,count}",
        axi_read(A_ASP_CMD), 0x00000070);

  const uint64_t path1 = 0x1111222233334444ULL;
  const uint64_t path2 = 0x5555666677778888ULL;
  const uint64_t path3 = 0x9999AAAABBBBCCCCULL;
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

  const uint64_t forged = 0xDEADBEEF01234567ULL;
  axi_write(A_ASP_LO, (uint32_t)forged);
  axi_write(A_ASP_HI, (uint32_t)(forged >> 32));
  check("retired staging LO reads zero", axi_read(A_ASP_LO), 0);
  check("retired staging HI reads zero", axi_read(A_ASP_HI), 0);
  axi_write(A_ASP_CMD, 0xC0000107u); // COMMIT slot 1 + PUBLISH count 7
  check("software COMMIT/PUBLISH cannot forge live slot", live_path(0), path1);
  check("software COMMIT/PUBLISH cannot forge live count", dut->o_asp_count, 4);
  check("software COMMIT/PUBLISH cannot spend fabric generation",
        dut->o_asp_gen, 9);
  check("0x7E4 still reads fabric state after software command",
        axi_read(A_ASP_CMD), 0x00000094);

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

  const uint64_t path7 = 0xD1D2D3D4D5D6D7D8ULL;
  set_fabric_path(6, path7);
  dut->i_gptp_asp_count = 8;
  dut->i_gptp_asp_gen = 11;
  dut->eval();
  check("maximum fabric AS_PATH count owns public output", dut->o_asp_count, 8);
  check("maximum fabric AS_PATH reaches public slot 7", live_path(6), path7);
  check("0x7E4 follows maximum fabric publication",
        axi_read(A_ASP_CMD), 0x000000B8);

  std::printf("checks: %u   failures: %u\n", checks, failures);
  delete dut;
  return failures ? 1 : 0;
}
