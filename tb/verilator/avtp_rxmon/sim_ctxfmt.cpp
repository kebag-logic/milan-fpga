// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_ctxfmt.cpp - each Stream Input's format in its LCTX context, at the 8x8
// shape's eight contexts (#946): the lane-A stack of avtp_rxmon_nx_wrap
// (KL_stream_table, avtp_stream_parser, KL_avtp_rx_monitor_ctx, the
// depacketizer and the route) elaborated at N_STREAMS_P = 8.
//
// KL_avtp_rx_monitor_ctx judges a PDU of stream 0 against fmt0_i and a PDU of
// any other stream against its context's FMT_LO/FMT_HI words (LCTX w2/w3),
// which only the window port writes; a PDU not in its input's current format
// counts UNSUPPORTED_FORMAT and gets no accept verdict, so the depacketizer
// drops it (Milan v1.2 Table 5.6, 4.4.2.2). The split firmware writes each AAF
// input's current format there through the CSR window while the input is
// unbound (sw/firmware/ctrl/plat/ctrl_plat.c, sink_format). This harness holds
// the contract that relies on, for every context:
//
//   [CF1] a context whose format words were never written discards every
//         in-format PDU as UNSUPPORTED_FORMAT, stream 0 receiving (the state
//         the bench found at 8x8/1if, inputs 1 to 7)
//   [CF2] a format written through the window while the input is unbound
//         survives the bind's walk: inputs 1 to 7 each accept their first
//         in-format PDU, count it in FRAMES_RX and count no UNSUPPORTED_FORMAT,
//         and their words read back as written
//   [CF3] each context judges against its own words: input k accepts a PDU of
//         its own channel count and discards one of another input's
//   [CF4] a format written in the cycle before the bind, then a PDU at once:
//         the first PDU is accepted
//   [CF5] an unbind keeps the format, through the 100 ms silence unlock that
//         follows it: the next binding's first PDU is accepted with nothing
//         written again
//
// Usage: make -C tb/verilator/avtp_rxmon ctxfmt   (built at N_STREAMS_P=8)

#include <array>
#include <cstdint>
#include <cstdio>
#include <memory>
#include <vector>

#include "Vavtp_rxmon_nx_wrap.h"
#include "verilated.h"

namespace {

constexpr int kStreams = 8;
constexpr int kIval = 2000;                     // the wrap's IVAL_CYC_P
constexpr int kLctxTimeoutCycles = 64;
constexpr int kSilenceCycles = 10500;            // past the 100 ms unlock at the wrap's 100 kHz clock
constexpr int W_FMT_LO = 2, W_FMT_HI = 3, W_UF = 22, W_FRX = 25;
//! AAF PCM32 48 kHz with `ch` channels (Milan v1.2 Table 6.2): HI word {subtype, sv/ut/nsr, format, depth}
constexpr uint32_t kFmtHi = 0x02050220u;
constexpr uint32_t fmt_lo(unsigned ch) { return (ch << 22) | 0x6000u; }
constexpr uint64_t fmt(unsigned ch) { return (static_cast<uint64_t>(kFmtHi) << 32) | fmt_lo(ch); }
constexpr uint64_t sid(int s) { return 0x020000FFFE000000ULL | (static_cast<uint64_t>(s + 1) << 16); }

class CtxFmt {
 public:
    int run() {
        bring_up();
        never_written_discards_every_pdu();
        written_unbound_survives_the_bind();
        each_context_judges_against_its_own_words();
        written_the_cycle_before_the_bind();
        unbind_keeps_the_format();
        std::printf("\n======================================================================\n");
        std::printf("CTXFMT N=8: %ld checks, %ld failures\nRESULT: %s\n", checks, fails, fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

 private:
    std::unique_ptr<Vavtp_rxmon_nx_wrap> dut = std::make_unique<Vavtp_rxmon_nx_wrap>();
    long checks = 0, fails = 0;
    std::array<long, kStreams> accepts{};
    std::array<uint8_t, kStreams> seq{};

    void ck(const char* t, int s, long got, long exp) {
        checks++;
        if (got != exp) {
            fails++;
            std::printf("  [FAIL] %s: input %d got=%ld exp=%ld\n", t, s, got, exp);
        } else {
            std::printf("  [ ok ] %s: input %d = %ld\n", t, s, got);
        }
    }

    void lo() { dut->clk = 0; dut->eval(); }
    void hi() {
        dut->clk = 1;
        dut->eval();
        if (dut->pdu_accept_p_o && dut->pdu_accept_idx_o < kStreams) accepts[dut->pdu_accept_idx_o]++;
    }
    void cyc(int n = 1) { for (int i = 0; i < n; i++) { lo(); hi(); } }
    void flush_iv() { cyc(kIval + 80); }

    // an AAF PDU of stream s with `ch` channels, its own next sequence number
    std::vector<uint8_t> aaf(int s, unsigned ch) {
        std::vector<uint8_t> f(120, 0);
        for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
        f[12] = 0x22; f[13] = 0xF0;
        const int o = 14;
        f[o + 0] = 0x02;                          // AAF
        f[o + 1] = 0x81;                          // sv, tv
        f[o + 2] = seq[s]++;
        for (int i = 0; i < 8; i++) f[o + 4 + i] = static_cast<uint8_t>(sid(s) >> (8 * (7 - i)));
        f[o + 12] = 0xA5; f[o + 13] = 0x5A; f[o + 14] = 0xC3; f[o + 15] = 0x3C;
        f[o + 16] = 0x02;                         // INT32
        f[o + 17] = 0x05 << 4;                    // 48 kHz
        f[o + 18] = static_cast<uint8_t>(ch);
        f[o + 19] = 32;
        f[o + 21] = 0x40;                         // 64 bytes
        for (int i = 0; i < 64; i++) f[o + 24 + i] = static_cast<uint8_t>(0x30 + i);
        return f;
    }

    void feed(const std::vector<uint8_t>& f, int headroom = 40) {
        const int beats = static_cast<int>(f.size() + 7) / 8;
        for (int b = 0; b < beats; b++) {
            uint64_t d = 0;
            int vb = 0;
            for (int k = 0; k < 8; k++) {
                const size_t idx = static_cast<size_t>(b) * 8 + static_cast<size_t>(k);
                if (idx < f.size()) { d |= static_cast<uint64_t>(f[idx]) << (8 * k); vb++; }
            }
            dut->s_tdata_i = d;
            dut->s_tkeep_i = (vb == 8) ? 0xFF : ((1u << vb) - 1);
            dut->s_tvalid_i = 1;
            dut->s_tlast_i = (b == beats - 1);
            cyc();
        }
        dut->s_tvalid_i = 0;
        dut->s_tlast_i = 0;
        cyc(headroom);
    }

    // bind or unbind input s: stream 0 through its alias level, every other through its table entry
    void bind(int s, bool on) {
        if (s == 0) {
            dut->bound0_i = on;
        } else {
            dut->tbl_wr_en_i = 1;
            dut->tbl_wr_idx_i = static_cast<uint8_t>(s);
            dut->tbl_wr_sid_i = on ? sid(s) : 0;
            dut->tbl_wr_valid_i = on;
            cyc();
            dut->tbl_wr_en_i = 0;
        }
    }

    uint32_t lctx_rd(int s, int w) {
        dut->lctx_rd_en_i = 1;
        dut->lctx_rd_addr_i = static_cast<uint8_t>((s << 5) | w);
        for (int i = 0; i < kLctxTimeoutCycles; i++) {
            cyc();
            if (dut->lctx_rd_valid_o) {
                dut->lctx_rd_en_i = 0;
                const uint32_t v = dut->lctx_rd_data_o;
                cyc();
                return v;
            }
        }
        dut->lctx_rd_en_i = 0;
        ck("the window read answers", s, 0, 1);
        return 0xDEADBEEF;
    }

    // one window write, held until the engine takes it (the CSR's request contract), then `after` cycles
    void lctx_wr(int s, int w, uint32_t v, int after = 1) {
        dut->lctx_wr_en_i = 1;
        dut->lctx_wr_addr_i = static_cast<uint8_t>((s << 5) | w);
        dut->lctx_wr_data_i = v;
        for (int i = 0; i < kLctxTimeoutCycles; i++) {
            lo();
            const bool rdy = dut->lctx_wr_rdy_o;
            hi();
            if (rdy) {
                dut->lctx_wr_en_i = 0;
                cyc(after);
                return;
            }
        }
        dut->lctx_wr_en_i = 0;
        ck("the window write is taken", s, 0, 1);
    }

    void write_format(int s, uint64_t f, int after = 1) {
        lctx_wr(s, W_FMT_LO, static_cast<uint32_t>(f), 1);
        lctx_wr(s, W_FMT_HI, static_cast<uint32_t>(f >> 32), after);
    }

    void bring_up() {
        dut->bound0_i = 0;
        dut->sid0_i = sid(0);
        dut->fmt0_i = fmt(8);
        dut->tbl_wr_en_i = 0;
        dut->lctx_wr_en_i = 0;
        dut->lctx_rd_en_i = 0;
        dut->route_wr_en_i = 0;
        dut->ptp_now_i = 0xA55AC33CUL - 1000000;
        dut->pres_ofs_i = 2000000;
        dut->clk_src_i = 0;
        dut->servo_conv_i = 0;
        dut->s_tvalid_i = 0;
        dut->resetn = 0;
        cyc(6);
        dut->resetn = 1;
        cyc(4);
        std::printf("== LCTX format contract, N=8 (#946) ==\n");
    }

    void never_written_discards_every_pdu() {
        std::printf("\n[CF1] format words never written: every in-format PDU above 0 is UNSUPPORTED_FORMAT\n");
        for (int s = 0; s < kStreams; s++) bind(s, true);
        cyc(200);                                 // every bind's walk
        const auto before = accepts;
        for (int s = 0; s < kStreams; s++) feed(aaf(s, 8));
        flush_iv();
        for (int s = 0; s < kStreams; s++) {
            ck("[CF1] accept verdicts for the in-format PDU", s, accepts[s] - before[s], s == 0 ? 1 : 0);
            ck("[CF1] UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF), s == 0 ? 0 : 1);
        }
        for (int s = 0; s < kStreams; s++) bind(s, false);
        cyc(200);
    }

    void written_unbound_survives_the_bind() {
        std::printf("\n[CF2] the format written while unbound survives the bind's walk\n");
        for (int s = 1; s < kStreams; s++) write_format(s, fmt(8));
        for (int s = 0; s < kStreams; s++) bind(s, true);
        cyc(200);
        const auto before = accepts;
        for (int s = 0; s < kStreams; s++) feed(aaf(s, 8));
        flush_iv();
        for (int s = 0; s < kStreams; s++) {
            ck("[CF2] the first in-format PDU is accepted", s, accepts[s] - before[s], 1);
            ck("[CF2] FRAMES_RX counts it", s, lctx_rd(s, W_FRX), 1);
            ck("[CF2] UNSUPPORTED_FORMAT stays 0", s, lctx_rd(s, W_UF), 0);
        }
        for (int s = 1; s < kStreams; s++) {
            ck("[CF2] FMT_LO reads back as written", s, lctx_rd(s, W_FMT_LO), fmt_lo(8));
            ck("[CF2] FMT_HI reads back as written", s, lctx_rd(s, W_FMT_HI), kFmtHi);
        }
        for (int s = 0; s < kStreams; s++) bind(s, false);
        cyc(200);
    }

    void each_context_judges_against_its_own_words() {
        std::printf("\n[CF3] each context judges against its own words (input k: k+1 channels)\n");
        for (int s = 1; s < kStreams; s++) write_format(s, fmt(static_cast<unsigned>(s + 1)));
        for (int s = 1; s < kStreams; s++) bind(s, true);
        cyc(200);
        auto before = accepts;
        for (int s = 1; s < kStreams; s++) feed(aaf(s, static_cast<unsigned>(s + 1)));
        for (int s = 1; s < kStreams; s++) {
            ck("[CF3] a PDU of the input's own channel count is accepted", s, accepts[s] - before[s], 1);
        }
        before = accepts;
        // another input's count: input k gets k+2 channels (input 7 gets 2)
        for (int s = 1; s < kStreams; s++) feed(aaf(s, s == kStreams - 1 ? 2u : static_cast<unsigned>(s + 2)));
        flush_iv();
        for (int s = 1; s < kStreams; s++) {
            ck("[CF3] a PDU of another input's channel count is discarded", s, accepts[s] - before[s], 0);
            ck("[CF3] ...and counts UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF), 1);
        }
        for (int s = 1; s < kStreams; s++) bind(s, false);
        cyc(200);
    }

    void written_the_cycle_before_the_bind() {
        std::printf("\n[CF4] written the cycle before the bind, then a PDU at once\n");
        for (int s = 1; s < kStreams; s++) {
            write_format(s, fmt(4), 0);           // FMT_HI taken; the bind's table write next cycle
            bind(s, true);
            const auto before = accepts;
            feed(aaf(s, 4));
            ck("[CF4] the first PDU after the bind is accepted", s, accepts[s] - before[s], 1);
            bind(s, false);
            cyc(200);
        }
    }

    void unbind_keeps_the_format() {
        std::printf("\n[CF5] an unbind keeps the format through the silence unlock: the next binding receives\n");
        // the contexts hold 4 channels since [CF4], each unbound and locked by its one PDU; the silence
        // watchdog unlocks each through its walk, and nothing is written again
        cyc(kSilenceCycles);
        for (int s = 1; s < kStreams; s++) bind(s, true);
        cyc(200);
        const auto before = accepts;
        for (int s = 1; s < kStreams; s++) feed(aaf(s, 4));
        flush_iv();
        for (int s = 1; s < kStreams; s++) {
            ck("[CF5] the rebound input's first PDU is accepted", s, accepts[s] - before[s], 1);
            ck("[CF5] UNSUPPORTED_FORMAT stays 0", s, lctx_rd(s, W_UF), 0);
        }
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    CtxFmt h;
    return h.run();
}
