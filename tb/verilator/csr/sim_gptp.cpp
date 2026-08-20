/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Fabric-gPTP CSR ownership harness. The publication bank owns the legacy
 * GM/parent/pdelay addresses when GPTP_PLANE_EN_P=1, and each 64-bit identity
 * is read as one atomic snapshot even if the live bank commits between the
 * two 32-bit AXI transactions. Both LO-first and HI-first readers are graded.
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
};

static Vmilan_csr* dut;
static unsigned checks, failures;

static void tick() {
  dut->aclk = 1;
  dut->eval();
  dut->aclk = 0;
  dut->eval();
}

static void check(const char* label, uint64_t got, uint64_t expected) {
  checks++;
  if (got != expected) {
    failures++;
    std::printf("  [FAIL] %-52s got=0x%016llx exp=0x%016llx\n", label,
                (unsigned long long)got, (unsigned long long)expected);
  } else {
    std::printf("  [ ok ] %-52s = 0x%016llx\n", label,
                (unsigned long long)got);
  }
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
    if (dut->s_axi_rvalid) {
      value = dut->s_axi_rdata;
      break;
    }
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
  dut->s_axi_awvalid = 0;
  dut->s_axi_wvalid = 0;
  dut->s_axi_bready = 0;
  dut->s_axi_arvalid = 0;
  dut->s_axi_rready = 0;
  dut->i_lctx_rd_valid = 1;
  dut->i_tctx_rd_valid = 1;
  dut->i_lctx_wr_rdy = 1;
  dut->i_tctx_wr_rdy = 1;
  for (unsigned i = 0; i < 8; i++) tick();
  dut->aresetn = 1;
  tick();

  const uint64_t gm_a = 0x001BC50000C0FFEFULL;
  const uint64_t gm_b = 0x1021324354657687ULL;
  const uint64_t gm_c = 0x98A9BACBDCEDFE0FULL;
  const uint64_t parent_a = 0x3CC0C6FFFE0210AAULL;
  const uint64_t parent_b = 0x405162738495A6B7ULL;
  const uint64_t parent_c = 0xC8D9EAFB0C1D2E3FULL;

  dut->i_gptp_gm_id = gm_a;
  dut->i_gptp_parent_id = parent_a;
  dut->i_gptp_pdelay_ns = 0x01020304;

  // Poison every legacy shadow. Live reads must still select the fabric bank.
  axi_write(A_ADP_GMLO, 0xDEADBEEF);
  axi_write(A_ADP_GMHI, 0xCAFEBABE);
  axi_write(A_AS2_LO, 0x0BADF00D);
  axi_write(A_AS2_HI, 0xFACEFEED);
  axi_write(A_GPTP_PDELAY, 0xA5A5A5A5);
  check("fabric pdelay wins over the software shadow",
        axi_read(A_GPTP_PDELAY), 0x01020304);
  check("fabric GM wins over the software shadow",
        ((uint64_t)axi_read(A_ADP_GMHI) << 32) | axi_read(A_ADP_GMLO), gm_a);
  check("fabric parent wins over the software shadow",
        ((uint64_t)axi_read(A_AS2_HI) << 32) | axi_read(A_AS2_LO), parent_a);

  // LO first: changing the live bank before HI must still reconstruct A.
  dut->i_gptp_gm_id = gm_a;
  const uint32_t gm_lo = axi_read(A_ADP_GMLO);
  dut->i_gptp_gm_id = gm_b;
  const uint32_t gm_hi = axi_read(A_ADP_GMHI);
  check("GM LO-first pair remains one publication", ((uint64_t)gm_hi << 32) | gm_lo,
        gm_a);

  // HI first is equally atomic.
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

  std::printf("checks: %u   failures: %u\n", checks, failures);
  delete dut;
  return failures ? 1 : 0;
}
