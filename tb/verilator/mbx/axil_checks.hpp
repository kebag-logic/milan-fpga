// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// axil_checks.hpp - the AXI4-Lite adapter's handshake rules, driven channel
// by channel on the AXI4-Lite build only (#665 lane F0). The suite's polite
// master offers AW and W together and holds BREADY and RREADY high; these
// checks are the master a real interconnect can be (AMBA AXI, IHI0022H):
//
//   A1  AW before W, W arriving later        A4  BREADY low, BVALID held
//   A2  W before AW, AW arriving later       A5  RREADY low, RVALID and RDATA held
//   A3  a read offered beside a write        A6  reset with a transfer half taken
//   A0  no AXI output follows an AXI input inside a cycle (A3.1.1, A3.2.1),
//       measured by the bench's probe on every clock of the whole run
//
// THE ONE DECISION THAT MATTERS: every expectation is a handshake counted at
// an edge or a register read back afterwards, never the adapter's internal
// state, so a check passes only if the bus a hard core sees behaves.

#ifndef MBX_AXIL_CHECKS_HPP
#define MBX_AXIL_CHECKS_HPP

#include <cstdint>
#include <vector>

#include "../../common/verilator_harness.hpp"
#include "bench.hpp"
#include "mbx_contract.h"

namespace mbx_tb {

class AxilChecks {
 public:
    AxilChecks(Bench& bench, milan::tb::Checker& check) : b_(bench), d_(bench.dut()), ck_(check) {}

    void run() {
        b_.reset();
        split_aw_first();
        b_.reset();
        split_w_first();
        b_.reset();
        read_beside_write();
        b_.reset();
        b_backpressure();
        b_.reset();
        r_backpressure();
        b_.reset();
        reset_mid_transaction();
        ck_.dec("A0 no AXI4-Lite output followed an AXI4-Lite input inside a cycle (A3.1.1, A3.2.1)",
                b_.comb_paths, 0);
        ck_.that("A0 the structural probe ran on every clock of the AXI4-Lite run",
                 b_.probed == b_.cycles() && b_.probed > 1000u);
    }

 private:
    //! What handshook at one edge, and the response channels as they stood.
    struct Edge {
        bool aw;
        bool w;
        bool ar;
        bool b;
        bool r;
        bool bvalid;
        bool rvalid;
        std::uint32_t bresp;
        std::uint32_t rresp;
        std::uint32_t rdata;
    };

    //! One clock with the inputs as they stand. A VALID whose handshake
    //! happened at this edge is withdrawn, as a master with nothing more to
    //! send does.
    Edge clock() {
        d_->clk_i = 0;
        d_->eval();
        const Edge e{d_->s_awvalid_i && d_->s_awready_o,
                     d_->s_wvalid_i && d_->s_wready_o,
                     d_->s_arvalid_i && d_->s_arready_o,
                     d_->s_bvalid_o && d_->s_bready_i,
                     d_->s_rvalid_o && d_->s_rready_i,
                     d_->s_bvalid_o != 0,
                     d_->s_rvalid_o != 0,
                     d_->s_bresp_o,
                     d_->s_rresp_o,
                     d_->s_rdata_o};
        b_.step();
        if (e.aw) {
            d_->s_awvalid_i = 0;
        }
        if (e.w) {
            d_->s_wvalid_i = 0;
        }
        if (e.ar) {
            d_->s_arvalid_i = 0;
        }
        return e;
    }

    void offer_aw(std::uint32_t off) {
        d_->s_awaddr_i = off;
        d_->s_awvalid_i = 1;
    }
    void offer_w(std::uint32_t v) {
        d_->s_wdata_i = v;
        d_->s_wstrb_i = 0xF;
        d_->s_wvalid_i = 1;
    }
    void offer_ar(std::uint32_t off) {
        d_->s_araddr_i = off;
        d_->s_arvalid_i = 1;
    }

    //! Clocks until `n` B handshakes, or the patience runs out; the count.
    unsigned take_b(unsigned n, unsigned patience = 16) {
        unsigned got = 0;
        for (unsigned i = 0; i < patience && got < n; ++i) {
            const Edge e = clock();
            got += e.b ? 1u : 0u;
            bresp_ok_ = bresp_ok_ && (!e.bvalid || e.bresp == 0u);
        }
        return got;
    }

    void split_aw_first();
    void split_w_first();
    void read_beside_write();
    void b_backpressure();
    void r_backpressure();
    void reset_mid_transaction();

    Bench& b_;
    Vtb_mbx_top* d_;
    milan::tb::Checker& ck_;
    bool bresp_ok_ = true;
};

inline void AxilChecks::split_aw_first() {
    b_.write(MBX_REG_OWN_EID_LO, 0x11111111u);
    d_->s_bready_i = 1;
    offer_aw(MBX_REG_OWN_EID_LO);
    bool aw_taken = false;
    bool b_early = false;
    for (unsigned i = 0; i < 6; ++i) {
        const Edge e = clock();
        aw_taken = aw_taken || e.aw;
        b_early = b_early || e.bvalid;
    }
    ck_.that("A1 AW offered alone is taken without its W", aw_taken);
    ck_.that("A1 and no B answers it before its W", !b_early);
    ck_.hex("A1 a read beside the half write sees the register unchanged", b_.read(MBX_REG_OWN_EID_LO), 0x11111111u);
    d_->s_bready_i = 1;
    offer_w(0xC0FFEE01u);
    ck_.dec("A1 W arriving later completes the write with exactly one B", take_b(2), 1);
    ck_.hex("A1 the late W's data lands at the early AW's address", b_.read(MBX_REG_OWN_EID_LO), 0xC0FFEE01u);
    ck_.that("A1 BRESP is OKAY whenever BVALID is high", bresp_ok_);
    d_->s_bready_i = 0;
}

inline void AxilChecks::split_w_first() {
    b_.write(MBX_REG_OWN_EID_HI, 0x22222222u);
    d_->s_bready_i = 1;
    offer_w(0x0BADF00Du);
    bool w_taken = false;
    bool b_early = false;
    for (unsigned i = 0; i < 6; ++i) {
        const Edge e = clock();
        w_taken = w_taken || e.w;
        b_early = b_early || e.bvalid;
    }
    ck_.that("A2 W offered alone is taken without its AW", w_taken);
    ck_.that("A2 and no B answers it before its AW", !b_early);
    ck_.hex("A2 a read beside the half write sees the register unchanged", b_.read(MBX_REG_OWN_EID_HI), 0x22222222u);
    d_->s_bready_i = 1;
    offer_aw(MBX_REG_OWN_EID_HI);
    ck_.dec("A2 AW arriving later completes the write with exactly one B", take_b(2), 1);
    ck_.hex("A2 the early W's data lands at the late AW's address", b_.read(MBX_REG_OWN_EID_HI), 0x0BADF00Du);
    d_->s_bready_i = 0;
}

inline void AxilChecks::read_beside_write() {
    b_.write(MBX_REG_OWN_EID_LO, 0x5A5A0001u);
    d_->s_bready_i = 1;
    d_->s_rready_i = 1;
    offer_aw(MBX_REG_OWN_EID_HI);
    offer_w(0x00C0FFEEu);
    offer_ar(MBX_REG_OWN_EID_LO);
    unsigned bs = 0;
    std::vector<std::uint32_t> rs;
    bool same_edge = false;
    for (unsigned i = 0; i < 16; ++i) {
        const Edge e = clock();
        if (i == 0) {
            same_edge = e.aw && e.w && e.ar;
        }
        bs += e.b ? 1u : 0u;
        if (e.r) {
            rs.push_back(e.rdata);
        }
    }
    ck_.that("A3 AW, W and AR offered in one cycle are all taken at its edge", same_edge);
    ck_.dec("A3 the write is answered by one B", bs, 1);
    ck_.dec("A3 the read is answered by one R", rs.size(), 1);
    ck_.hex("A3 the read answers its own address, not the write's", rs.empty() ? 0u : rs[0], 0x5A5A0001u);
    ck_.hex("A3 the write lands", b_.read(MBX_REG_OWN_EID_HI), 0x00C0FFEEu);

    // A master that offers a new write the cycle after each one is taken
    // must not hold a read off: the read is answered within a few clocks.
    d_->s_bready_i = 1;
    d_->s_rready_i = 1;
    offer_ar(MBX_REG_OWN_EID_LO);
    unsigned writes = 0;
    int read_at = -1;
    for (unsigned i = 0; i < 24; ++i) {
        if (!d_->s_awvalid_i && !d_->s_wvalid_i) {
            offer_aw(MBX_REG_MAAP_BASE_LO);
            offer_w(0x01000000u + i);
        }
        const Edge e = clock();
        writes += e.b ? 1u : 0u;
        if (e.r && read_at < 0) {
            read_at = static_cast<int>(i);
        }
    }
    d_->s_awvalid_i = 0;
    d_->s_wvalid_i = 0;
    b_.idle(8);
    ck_.that("A3 a read is answered within 8 clocks while writes keep coming", read_at >= 0 && read_at < 8);
    ck_.that("A3 and the writes keep flowing beside it (5 or more B in 24 clocks)", writes >= 5u);
    d_->s_bready_i = 0;
    d_->s_rready_i = 0;
}

inline void AxilChecks::b_backpressure() {
    d_->s_bready_i = 0;
    offer_aw(MBX_REG_OWN_EID_LO);
    offer_w(0xB0B0B0B0u);
    bool bvalid = false;
    for (unsigned i = 0; i < 8 && !bvalid; ++i) {
        bvalid = clock().bvalid;
    }
    ck_.that("A4 BVALID rises with BREADY low", bvalid);
    offer_aw(MBX_REG_OWN_EID_HI);
    offer_w(0x0D0D0D0Du);
    bool held = true;
    bool okay = true;
    bool aw2 = false;
    bool w2 = false;
    for (unsigned i = 0; i < 10; ++i) {
        const Edge e = clock();
        held = held && e.bvalid;
        okay = okay && e.bresp == 0u;
        aw2 = aw2 || e.aw;
        w2 = w2 || e.w;
    }
    ck_.that("A4 BVALID holds for 10 clocks while BREADY is low (A3.2.1)", held);
    ck_.that("A4 BRESP holds OKAY with it", okay);
    ck_.that("A4 a second write's AW and W are taken while the first B waits", aw2 && w2);
    d_->s_bready_i = 1;
    ck_.dec("A4 each write is answered by exactly one B once BREADY rises", take_b(3, 16), 2);
    d_->s_bready_i = 0;
    ck_.hex("A4 the first write lands", b_.read(MBX_REG_OWN_EID_LO), 0xB0B0B0B0u);
    ck_.hex("A4 the second write lands", b_.read(MBX_REG_OWN_EID_HI), 0x0D0D0D0Du);
}

inline void AxilChecks::r_backpressure() {
    b_.write(MBX_REG_OWN_EID_LO, 0x12345678u);
    b_.write(MBX_REG_OWN_EID_HI, 0x9ABCDEF0u);
    d_->s_rready_i = 0;
    offer_ar(MBX_REG_OWN_EID_LO);
    bool rvalid = false;
    for (unsigned i = 0; i < 8 && !rvalid; ++i) {
        rvalid = clock().rvalid;
    }
    ck_.that("A5 RVALID rises with RREADY low", rvalid);
    offer_ar(MBX_REG_OWN_EID_HI);
    bool held = true;
    bool data = true;
    bool ar2 = false;
    for (unsigned i = 0; i < 10; ++i) {
        const Edge e = clock();
        held = held && e.rvalid;
        data = data && e.rdata == 0x12345678u && e.rresp == 0u;
        ar2 = ar2 || e.ar;
    }
    ck_.that("A5 RVALID holds for 10 clocks while RREADY is low (A3.2.1)", held);
    ck_.that("A5 RDATA and RRESP hold with it, while a second read waits", data);
    ck_.that("A5 a second AR is taken while the first R waits", ar2);
    d_->s_rready_i = 1;
    std::vector<std::uint32_t> rs;
    for (unsigned i = 0; i < 16 && rs.size() < 3; ++i) {
        const Edge e = clock();
        if (e.r) {
            rs.push_back(e.rdata);
        }
    }
    d_->s_rready_i = 0;
    ck_.that("A5 each read is answered once, in order, with its own data once RREADY rises",
             rs == std::vector<std::uint32_t>{0x12345678u, 0x9ABCDEF0u});
}

inline void AxilChecks::reset_mid_transaction() {
    // An AW taken, its W not: the reset forgets it, so a W after the reset
    // waits for an AW of its own and never completes the old address.
    d_->s_bready_i = 1;
    offer_aw(MBX_REG_OWN_EID_LO);
    clock();
    b_.reset();
    d_->s_bready_i = 1;
    offer_w(0x77777777u);
    bool b_early = false;
    for (unsigned i = 0; i < 6; ++i) {
        b_early = b_early || clock().bvalid;
    }
    ck_.that("A6 an AW taken before a reset is forgotten: a W after it completes nothing", !b_early);
    offer_aw(MBX_REG_OWN_EID_HI);
    ck_.dec("A6 the W completes with the AW offered after the reset", take_b(2), 1);
    ck_.hex("A6 at that AW's address", b_.read(MBX_REG_OWN_EID_HI), 0x77777777u);
    ck_.hex("A6 and the forgotten address keeps its reset value", b_.read(MBX_REG_OWN_EID_LO), 0u);

    // A B and an R waiting at the reset are gone after it.
    d_->s_bready_i = 0;
    d_->s_rready_i = 0;
    offer_aw(MBX_REG_OWN_EID_LO);
    offer_w(0x88888888u);
    offer_ar(MBX_REG_ID);
    bool both = false;
    for (unsigned i = 0; i < 12 && !both; ++i) {
        const Edge e = clock();
        both = e.bvalid && e.rvalid;
    }
    ck_.that("A6 a B and an R wait with BREADY and RREADY low", both);
    b_.reset();
    d_->s_bready_i = 1;
    d_->s_rready_i = 1;
    bool stale = false;
    for (unsigned i = 0; i < 6; ++i) {
        const Edge e = clock();
        stale = stale || e.bvalid || e.rvalid;
    }
    ck_.that("A6 no B or R waiting at a reset is given after it (A3.1.2)", !stale);
    d_->s_bready_i = 0;
    d_->s_rready_i = 0;
    b_.write(MBX_REG_OWN_EID_LO, 0x99999999u);
    ck_.hex("A6 the bus works normally after the reset", b_.read(MBX_REG_OWN_EID_LO), 0x99999999u);
    ck_.dec("A6 no access went unanswered", b_.bus_timeouts, 0);
}

}  // namespace mbx_tb

#endif  // MBX_AXIL_CHECKS_HPP
