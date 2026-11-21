// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_fanout.cpp - one talker stream bound to several Stream Inputs (#948), at
// the 8x8 shape's eight contexts: the multi-stream receive stack of
// avtp_rxmon_nx_wrap (KL_stream_table, avtp_stream_parser,
// KL_avtp_rx_monitor_ctx, the depacketizer and the route) at N_STREAMS_P = 8.
//
// IEEE 1722.1-2021 8.2 lets each sink bind on its own, so one stream_id can be
// the source of several of an entity's Stream Inputs. Each such input receives
// every PDU of the stream: it is judged against its own format and counted in
// its own Table 5.6 counters (Milan v1.2 5.3.8.10), and its payload reaches
// the depacketizer's output under its own index, the render path's input.
//
//   [FO1] two inputs bound to one stream: each accepts every PDU, counts it
//         in FRAMES_RX and its DEPKT tally, locks, and receives every
//         payload byte for byte under its own index
//   [FO2] three inputs bound to one stream: the same for each of the three
//   [FO3] unbinding one of them leaves the other two receiving, and the
//         unbound input receives and counts nothing more
//   [FO4] each input judges the one PDU on its own: an input whose format
//         differs counts UNSUPPORTED_FORMAT and receives nothing, the others
//         accept it; once both have settled, a sequence gap counts in each
//         accepting input's own SEQ_NUM_MISMATCH and STREAM_INTERRUPTED
//   [FO5] two streams back to back, one bound to two inputs and one to a
//         third: each input receives exactly its own stream's payloads, in
//         order, and nothing is dropped
//   [FO6] all eight inputs bound to one stream: each receives every PDU
//   [FO7] a PDU no bound input accepts, then one they do, back to back: the
//         first is delivered to no input, the second to each
//   [FO8] a frame that ends on its eighth beat, the one the parser matches
//         on, then a full PDU with no gap: the short frame is gone before
//         its PDU is queued, so it is delivered to no input, and the full
//         one is delivered to each, its own payload
//
// Usage: make -C tb/verilator/avtp_rxmon fanout   (built at N_STREAMS_P=8)

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
constexpr int W_FMT_LO = 2;                     // LCTX words (KL_avtp_rx_monitor_ctx's record)
constexpr int W_FMT_HI = 3;
constexpr int W_DEPKT = 11;
constexpr int W_ML = 16;
constexpr int W_SI = 18;
constexpr int W_SM = 19;
constexpr int W_UF = 22;
constexpr int W_FRX = 25;
constexpr unsigned kPayloadBytes = 192;         // 6 events of 8 channels of 4 bytes (48 kHz, Milan v1.2 6.2)
//! AAF PCM32 48 kHz with `ch` channels (Milan v1.2 Table 6.2): HI word {subtype, sv/ut/nsr, format, depth}
constexpr uint32_t kFmtHi = 0x02050220u;
constexpr uint32_t fmt_lo(unsigned ch) { return (ch << 22) | 0x6000u; }
constexpr uint64_t fmt(unsigned ch) { return (static_cast<uint64_t>(kFmtHi) << 32) | fmt_lo(ch); }
constexpr uint64_t kTalkerA = 0x0202DEADBEEF0001ull;  // the talker's stream_ids
constexpr uint64_t kTalkerB = 0x0202DEADBEEF0002ull;

using Pdu = std::vector<uint8_t>;

class FanOut {
 public:
    int run() {
        bring_up();
        two_inputs_on_one_stream();
        three_inputs_on_one_stream();
        unbinding_one_leaves_the_others_receiving();
        each_input_judges_the_pdu_on_its_own();
        two_streams_back_to_back();
        all_eight_inputs_on_one_stream();
        a_pdu_no_input_accepts_then_one_they_do();
        a_frame_ending_on_its_match_beat_then_a_full_one();
        std::printf("\n======================================================================\n");
        std::printf("FANOUT N=8: %ld checks, %ld failures\nRESULT: %s\n", checks, fails, fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

 private:
    std::unique_ptr<Vavtp_rxmon_nx_wrap> dut = std::make_unique<Vavtp_rxmon_nx_wrap>();
    long checks = 0;
    long fails = 0;
    std::array<long, kStreams> accepts{};
    //! the depacketizer's output, one PDU per input that received it
    std::array<std::vector<Pdu>, kStreams> got{};
    std::array<Pdu, 16> cur{};
    std::array<uint8_t, 2> seq{};               // the next sequence_num of talker A and B
    unsigned pdu_no = 0;                        // tags each payload

    void ck(const char* t, int s, long have, long exp) {
        checks++;
        if (have != exp) {
            fails++;
            std::printf("  [FAIL] %s: input %d got=%ld exp=%ld\n", t, s, have, exp);
        } else {
            std::printf("  [ ok ] %s: input %d = %ld\n", t, s, have);
        }
    }

    void lo() { dut->clk = 0; dut->eval(); }
    void hi() {
        dut->clk = 1;
        dut->eval();
        if (dut->pdu_accept_p_o && dut->pdu_accept_idx_o < kStreams) accepts[dut->pdu_accept_idx_o]++;
        if (dut->dp_tvalid_o) {
            const unsigned u = dut->dp_tuser_o & 0xF;
            for (int k = 0; k < 8; k++) cur[u].push_back(static_cast<uint8_t>(dut->dp_tdata_o >> (8 * k)));
            if (dut->dp_tlast_o) {
                if (u < kStreams) got[u].push_back(cur[u]);
                cur[u].clear();
            }
        }
    }
    void cyc(int n = 1) { for (int i = 0; i < n; i++) { lo(); hi(); } }
    void flush_iv() { cyc(kIval + 80); }

    // the payload of the next PDU: every byte names the PDU it belongs to
    Pdu payload() {
        Pdu p(kPayloadBytes);
        for (unsigned i = 0; i < kPayloadBytes; i++) p[i] = static_cast<uint8_t>(pdu_no * 29u + i * 3u + 1u);
        pdu_no++;
        return p;
    }

    // an AAF PDU of talker `t` (0 = A, 1 = B) with `ch` channels and the given payload, its sequence_num
    // the talker's next unless `skip` numbers are left out first
    std::vector<uint8_t> aaf(int t, unsigned ch, const Pdu& p, unsigned skip = 0) {
        std::vector<uint8_t> f(14 + 24 + p.size(), 0);
        for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
        f[12] = 0x22; f[13] = 0xF0;
        const int o = 14;
        const uint64_t id = t == 0 ? kTalkerA : kTalkerB;
        seq[t] = static_cast<uint8_t>(seq[t] + skip);
        f[o + 0] = 0x02;                          // AAF
        f[o + 1] = 0x81;                          // sv, tv
        f[o + 2] = seq[t]++;
        for (int i = 0; i < 8; i++) f[o + 4 + i] = static_cast<uint8_t>(id >> (8 * (7 - i)));
        f[o + 12] = 0xA5; f[o + 13] = 0x5A; f[o + 14] = 0xC3; f[o + 15] = 0x3C;
        f[o + 16] = 0x02;                         // INT32
        f[o + 17] = 0x05 << 4;                    // 48 kHz
        f[o + 18] = static_cast<uint8_t>(ch);
        f[o + 19] = 32;
        f[o + 20] = static_cast<uint8_t>(p.size() >> 8);
        f[o + 21] = static_cast<uint8_t>(p.size());
        for (size_t i = 0; i < p.size(); i++) f[o + 24 + i] = p[i];
        return f;
    }

    void feed(const std::vector<uint8_t>& f, int headroom = 60) {
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

    // bind input s to stream_id `id`, or unbind it: input 0 through its ACMP alias level, every other
    // through its table entry
    void bind(int s, uint64_t id, bool on) {
        if (s == 0) {
            dut->sid0_i = id;
            dut->bound0_i = on;
            cyc();
        } else {
            dut->tbl_wr_en_i = 1;
            dut->tbl_wr_idx_i = static_cast<uint8_t>(s);
            dut->tbl_wr_sid_i = on ? id : 0;
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

    void lctx_wr(int s, int w, uint32_t v) {
        dut->lctx_wr_en_i = 1;
        dut->lctx_wr_addr_i = static_cast<uint8_t>((s << 5) | w);
        dut->lctx_wr_data_i = v;
        for (int i = 0; i < kLctxTimeoutCycles; i++) {
            lo();
            const bool rdy = dut->lctx_wr_rdy_o;
            hi();
            if (rdy) {
                dut->lctx_wr_en_i = 0;
                cyc();
                return;
            }
        }
        dut->lctx_wr_en_i = 0;
        ck("the window write is taken", s, 0, 1);
    }

    // input s's current format: stream 0's is fmt0_i, every other's its LCTX words (written while unbound)
    void set_format(int s, unsigned ch) {
        if (s == 0) {
            dut->fmt0_i = fmt(ch);
            cyc();
        } else {
            lctx_wr(s, W_FMT_LO, fmt_lo(ch));
            lctx_wr(s, W_FMT_HI, kFmtHi);
        }
    }

    struct Snap {
        std::array<long, kStreams> acc;
        std::array<size_t, kStreams> pdus;
        std::array<uint32_t, kStreams> frx, depkt, sm, si, uf;
    };
    Snap snap() {
        Snap n{};
        n.acc = accepts;
        for (int s = 0; s < kStreams; s++) {
            n.pdus[s] = got[s].size();
            n.frx[s] = lctx_rd(s, W_FRX);
            n.depkt[s] = lctx_rd(s, W_DEPKT) & 0xFFFF;
            n.sm[s] = lctx_rd(s, W_SM);
            n.si[s] = lctx_rd(s, W_SI);
            n.uf[s] = lctx_rd(s, W_UF);
        }
        return n;
    }

    // the input received `n` new PDUs since `b`, each the sent payload byte for byte, in order
    void received(const char* tag, int s, const Snap& b, const std::vector<Pdu>& sent) {
        char t[160];
        std::snprintf(t, sizeof t, "%s accept verdicts", tag);
        ck(t, s, accepts[s] - b.acc[s], static_cast<long>(sent.size()));
        std::snprintf(t, sizeof t, "%s payloads reach the depacketizer's output under the input's index", tag);
        ck(t, s, static_cast<long>(got[s].size() - b.pdus[s]), static_cast<long>(sent.size()));
        long exact = 0;
        for (size_t k = 0; k < sent.size() && b.pdus[s] + k < got[s].size(); k++)
            if (got[s][b.pdus[s] + k] == sent[k]) exact++;
        std::snprintf(t, sizeof t, "%s payloads equal the sent ones, byte for byte, in order", tag);
        ck(t, s, exact, static_cast<long>(sent.size()));
        std::snprintf(t, sizeof t, "%s FRAMES_RX counts them", tag);
        ck(t, s, lctx_rd(s, W_FRX) - b.frx[s], static_cast<long>(sent.size()));
        std::snprintf(t, sizeof t, "%s the DEPKT tally counts them", tag);
        ck(t, s, (lctx_rd(s, W_DEPKT) & 0xFFFF) - b.depkt[s], static_cast<long>(sent.size()));
    }

    void nothing(const char* tag, int s, const Snap& b) {
        char t[160];
        std::snprintf(t, sizeof t, "%s no accept verdict", tag);
        ck(t, s, accepts[s] - b.acc[s], 0);
        std::snprintf(t, sizeof t, "%s no payload", tag);
        ck(t, s, static_cast<long>(got[s].size() - b.pdus[s]), 0);
        std::snprintf(t, sizeof t, "%s FRAMES_RX unchanged", tag);
        ck(t, s, lctx_rd(s, W_FRX) - b.frx[s], 0);
    }

    void bring_up() {
        dut->bound0_i = 0;
        dut->sid0_i = 0;
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
        for (int s = 1; s < kStreams; s++) set_format(s, 8);
        std::printf("== one stream bound to several Stream Inputs, N=8 (#948) ==\n");
    }

    std::vector<Pdu> send(int t, int n, int headroom = 60) {
        std::vector<Pdu> sent;
        for (int k = 0; k < n; k++) {
            sent.push_back(payload());
            feed(aaf(t, 8, sent.back()), headroom);
        }
        return sent;
    }

    void two_inputs_on_one_stream() {
        std::printf("\n[FO1] inputs 0 and 1 bound to one talker stream: each receives every PDU\n");
        bind(0, kTalkerA, true);
        bind(1, kTalkerA, true);
        cyc(200);
        const Snap b = snap();
        const auto sent = send(0, 4);
        flush_iv();
        for (int s : {0, 1}) {
            received("[FO1]", s, b, sent);
            ck("[FO1] MEDIA_LOCKED", s, lctx_rd(s, W_ML), 1);
            ck("[FO1] SEQ_NUM_MISMATCH stays 0", s, lctx_rd(s, W_SM), 0);
        }
        for (int s = 2; s < kStreams; s++) nothing("[FO1] an unbound input:", s, b);
    }

    void three_inputs_on_one_stream() {
        std::printf("\n[FO2] input 5 bound to the same stream as well: each of the three receives every PDU\n");
        bind(5, kTalkerA, true);
        cyc(200);
        const Snap b = snap();
        const auto sent = send(0, 4);
        flush_iv();
        for (int s : {0, 1, 5}) received("[FO2]", s, b, sent);
        ck("[FO2] MEDIA_LOCKED of the input bound last", 5, lctx_rd(5, W_ML), 1);
        for (int s : {2, 3, 4, 6, 7}) nothing("[FO2] an unbound input:", s, b);
    }

    void unbinding_one_leaves_the_others_receiving() {
        std::printf("\n[FO3] input 1 unbound: inputs 0 and 5 go on receiving, input 1 receives nothing\n");
        bind(1, kTalkerA, false);
        cyc(200);
        const Snap b = snap();
        const auto sent = send(0, 4);
        flush_iv();
        for (int s : {0, 5}) received("[FO3]", s, b, sent);
        nothing("[FO3] the unbound input:", 1, b);
    }

    void each_input_judges_the_pdu_on_its_own() {
        std::printf("\n[FO4] per-input verdicts on one PDU: input 5 at 2 channels, inputs 0 and 1 at 8\n");
        bind(5, kTalkerA, false);
        cyc(200);
        set_format(5, 2);
        bind(5, kTalkerA, true);
        bind(1, kTalkerA, true);
        cyc(200);
        Snap b = snap();
        // ten PDUs: the rebound input 1 locks and leaves its eight-PDU settle, inside which a gap is no
        // mismatch (KL_avtp_rx_monitor_ctx's settle), so the gap below counts in both 8-channel inputs
        auto sent = send(0, 10);
        flush_iv();
        for (int s : {0, 1}) received("[FO4] an 8-channel input:", s, b, sent);
        nothing("[FO4] the 2-channel input:", 5, b);
        ck("[FO4] the 2-channel input counts UNSUPPORTED_FORMAT", 5, lctx_rd(5, W_UF) - b.uf[5], 1);
        for (int s : {0, 1}) ck("[FO4] an 8-channel input counts no UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF) - b.uf[s], 0);
        std::printf("  a gap of three sequence numbers\n");
        b = snap();
        sent.clear();
        sent.push_back(payload());
        feed(aaf(0, 8, sent.back(), 3));
        flush_iv();
        for (int s : {0, 1}) {
            received("[FO4] after the gap:", s, b, sent);
            ck("[FO4] SEQ_NUM_MISMATCH counts the gap", s, lctx_rd(s, W_SM) - b.sm[s], 1);
            ck("[FO4] STREAM_INTERRUPTED counts the gap", s, lctx_rd(s, W_SI) - b.si[s], 1);
        }
        ck("[FO4] the 2-channel input's SEQ_NUM_MISMATCH stays", 5, lctx_rd(5, W_SM) - b.sm[5], 0);
        bind(5, kTalkerA, false);
        cyc(200);
        set_format(5, 8);
    }

    void two_streams_back_to_back() {
        std::printf("\n[FO5] talker A on inputs 0 and 1, talker B on input 2, their PDUs back to back\n");
        bind(2, kTalkerB, true);
        cyc(200);
        const Snap b = snap();
        const long drops = dut->pcm_drops_o;
        std::vector<Pdu> sa, sb;
        for (int k = 0; k < 3; k++) {
            sa.push_back(payload());
            feed(aaf(0, 8, sa.back()), 2);
            sb.push_back(payload());
            feed(aaf(1, 8, sb.back()), 2);
        }
        cyc(1500);
        flush_iv();
        for (int s : {0, 1}) received("[FO5] talker A's input:", s, b, sa);
        received("[FO5] talker B's input:", 2, b, sb);
        ck("[FO5] nothing dropped", 0, dut->pcm_drops_o - drops, 0);
        bind(2, kTalkerB, false);
        cyc(200);
    }

    void all_eight_inputs_on_one_stream() {
        std::printf("\n[FO6] all eight inputs bound to one talker stream\n");
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, true);
        cyc(200);
        const Snap b = snap();
        const long drops = dut->pcm_drops_o;
        const auto sent = send(0, 3, 600);
        flush_iv();
        for (int s = 0; s < kStreams; s++) received("[FO6]", s, b, sent);
        ck("[FO6] nothing dropped", 0, dut->pcm_drops_o - drops, 0);
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, false);
        cyc(200);
    }

    void a_pdu_no_input_accepts_then_one_they_do() {
        std::printf("\n[FO7] a 4-channel PDU inputs 0 and 1 discard, then an 8-channel one, back to back\n");
        const Snap b = snap();
        const Pdu rejected = payload();
        std::vector<Pdu> sent;
        sent.push_back(payload());
        feed(aaf(0, 4, rejected), 2);
        feed(aaf(0, 8, sent.back()));
        cyc(400);
        flush_iv();
        for (int s : {0, 1}) {
            received("[FO7] the 8-channel PDU:", s, b, sent);
            ck("[FO7] the 4-channel PDU counts UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF) - b.uf[s], 1);
        }
    }

    void a_frame_ending_on_its_match_beat_then_a_full_one() {
        std::printf("\n[FO8] a 64-byte frame of the stream, then a full PDU with no gap between them\n");
        const Snap b = snap();
        Pdu cut = payload();
        std::vector<uint8_t> f = aaf(0, 8, cut);
        f.resize(64);                             // eight beats: the parser matches on the last
        std::vector<Pdu> sent;
        sent.push_back(payload());
        feed(f, 0);
        feed(aaf(0, 8, sent.back()));
        cyc(400);
        flush_iv();
        for (int s : {0, 1}) {
            ck("[FO8] both PDUs are judged (the short one counts in FRAMES_RX)", s, accepts[s] - b.acc[s], 2);
            ck("[FO8] only the full PDU reaches the depacketizer's output", s,
               static_cast<long>(got[s].size() - b.pdus[s]), 1);
            ck("[FO8] ...with its own payload", s,
               got[s].size() > b.pdus[s] && got[s][b.pdus[s]] == sent[0] ? 1 : 0, 1);
        }
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    FanOut h;
    return h.run();
}
