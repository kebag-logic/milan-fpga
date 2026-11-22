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
//   [FO9] eight inputs on one stream: a full PDU, six such frames with no
//         gap, then two full PDUs: the burst fills the engine's ring with
//         lost PDUs behind the committed one's verdicts, and each input
//         receives exactly the three full PDUs, its FRAMES_RX counting
//         exactly the PDUs it accepted
//   [FO10] eight inputs on one stream, thirty full PDUs with no gap: each
//         frame is read out eight times, so the store overflows; every PDU
//         an input accepted is delivered to it, in order, or counted as one
//         of its own DEPKT drops, and each input counts the same drops
//   [FO11] a PDU whose stream_data_length is not the input's frame size
//         (channels x samples_per_frame x sample octets, IEEE 1722-2016
//         7.3.5 and I.2.4.1) is off-format: each input bound to its stream
//         counts it in UNSUPPORTED_FORMAT and receives none of it, and the
//         valid PDUs around it arrive whole, in order, under each input's
//         index (Milan v1.2 4.4.2.2); 65 octets is the review's case. Two
//         inputs with different frame sizes on one stream each take only
//         the PDUs of their own size
//   [FO12] formats whose frame size is not a multiple of eight, every
//         remainder 1 to 7, untagged and behind a C-VLAN tag, two inputs on
//         one stream and a third input on another between them: each PDU
//         reaches each input as one frame of ceil(length/8) beats,
//         zero-padded, with one tlast, and the other stream's PDUs keep
//         their own boundaries and index
//   [FO13] frames that end short of their stream_data_length, by words and
//         by one octet: each input counts the PDU (its header is whole) but
//         receives none of it, the frame is one DEPKT drop for each, and
//         the PDUs around it arrive whole
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
//! an AAF PCM format: the sample format (IEEE 1722-2016 Table 9), bit depth, channels and samples per frame
struct Fmt {
    uint8_t format, depth;
    unsigned ch, spf;
    unsigned octets() const { return ch * spf * (format == 0x03 ? 3u : format == 0x04 ? 2u : 4u); }
    uint32_t hi() const { return 0x02050000u | (static_cast<uint32_t>(format) << 8) | depth; }
    uint32_t lo() const { return (ch << 22) | (spf << 12); }
};
constexpr Fmt kPcm32x8{0x02, 32, 8, 6};               // fmt(8): 192 octets
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
        a_burst_of_frames_ending_on_their_match_beat_to_eight_inputs();
        a_dense_burst_to_eight_inputs_overflows_the_store();
        a_pdu_off_its_inputs_frame_size_is_discarded_whole();
        payload_tails_that_are_not_whole_beats();
        frames_short_of_their_payload();
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
        return aaf_as(t, Fmt{0x02, 32, ch, 6}, p, false, skip);
    }
    // the same in format `fm`, behind a C-VLAN tag when `vlan`; its stream_data_length is the payload's size
    std::vector<uint8_t> aaf_as(int t, const Fmt& fm, const Pdu& p, bool vlan, unsigned skip = 0) {
        const int o = vlan ? 18 : 14;
        std::vector<uint8_t> f(static_cast<size_t>(o) + 24 + p.size(), 0);
        for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
        if (vlan) { f[12] = 0x81; f[13] = 0x00; f[14] = 0x60; f[15] = 0x02; }   // PCP 3, VID 2
        f[o - 2] = 0x22; f[o - 1] = 0xF0;
        const uint64_t id = t == 0 ? kTalkerA : kTalkerB;
        seq[t] = static_cast<uint8_t>(seq[t] + skip);
        f[o + 0] = 0x02;                          // AAF
        f[o + 1] = 0x81;                          // sv, tv
        f[o + 2] = seq[t]++;
        for (int i = 0; i < 8; i++) f[o + 4 + i] = static_cast<uint8_t>(id >> (8 * (7 - i)));
        f[o + 12] = 0xA5; f[o + 13] = 0x5A; f[o + 14] = 0xC3; f[o + 15] = 0x3C;
        f[o + 16] = fm.format;
        f[o + 17] = 0x05 << 4;                    // 48 kHz
        f[o + 18] = static_cast<uint8_t>(fm.ch);
        f[o + 19] = fm.depth;
        f[o + 20] = static_cast<uint8_t>(p.size() >> 8);
        f[o + 21] = static_cast<uint8_t>(p.size());
        for (size_t i = 0; i < p.size(); i++) f[o + 24 + i] = p[i];
        return f;
    }
    // a payload of `n` octets, every byte naming the PDU it belongs to
    Pdu payload(unsigned n) {
        Pdu p(n);
        for (unsigned i = 0; i < n; i++) p[i] = static_cast<uint8_t>(pdu_no * 29u + i * 3u + 1u);
        pdu_no++;
        return p;
    }
    // what the depacketizer emits for payload `p`: whole beats, the last zero-padded
    static Pdu padded(const Pdu& p) {
        Pdu q = p;
        q.resize((p.size() + 7) / 8 * 8, 0);
        return q;
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
    void set_format(int s, const Fmt& fm) {
        if (s == 0) {
            dut->fmt0_i = (static_cast<uint64_t>(fm.hi()) << 32) | fm.lo();
            cyc();
        } else {
            lctx_wr(s, W_FMT_LO, fm.lo());
            lctx_wr(s, W_FMT_HI, fm.hi());
        }
    }
    // rebind inputs `ins` to talker `t` at format `fm` (each unbound while its format is written)
    void rebind_as(std::initializer_list<int> ins, uint64_t id, const Fmt& fm) {
        for (int s : ins) bind(s, id, false);
        cyc(200);
        for (int s : ins) set_format(s, fm);
        for (int s : ins) bind(s, id, true);
        cyc(200);
    }

    struct Snap {
        std::array<long, kStreams> acc;
        std::array<size_t, kStreams> pdus;
        std::array<uint32_t, kStreams> frx, depkt, ddrop, sm, si, uf;
    };
    Snap snap() {
        Snap n{};
        n.acc = accepts;
        for (int s = 0; s < kStreams; s++) {
            n.pdus[s] = got[s].size();
            n.frx[s] = lctx_rd(s, W_FRX);
            n.depkt[s] = lctx_rd(s, W_DEPKT) & 0xFFFF;
            n.ddrop[s] = (lctx_rd(s, W_DEPKT) >> 16) & 0xFFFF;
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

    void a_burst_of_frames_ending_on_their_match_beat_to_eight_inputs() {
        std::printf("\n[FO9] eight inputs on one stream: a full PDU, six 64-byte frames with no gap, then two full PDUs\n");
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, true);
        cyc(200);
        const Snap b = snap();
        // the full PDU is committed and its eight verdicts outlast the burst behind it; each queued 64-byte frame is
        // gone before its PDU is queued, and once the engine's ring is full the later ones are not queued at all, so
        // three PDUs wait at once behind the committed one's verdicts and none of the short frames reaches an input
        std::vector<Pdu> sent;
        sent.push_back(payload());
        feed(aaf(0, 8, sent.back()), 0);
        for (int k = 0; k < 6; k++) {
            std::vector<uint8_t> f = aaf(0, 8, payload());
            f.resize(64);
            feed(f, 0);
        }
        cyc(3000);
        for (const Pdu& p : send(0, 2, 600)) sent.push_back(p);
        flush_iv();
        for (int s = 0; s < kStreams; s++) {
            ck("[FO9] only the three full PDUs reach the depacketizer's output", s,
               static_cast<long>(got[s].size() - b.pdus[s]), 3);
            long exact = 0;
            for (size_t k = 0; k < sent.size() && b.pdus[s] + k < got[s].size(); k++)
                if (got[s][b.pdus[s] + k] == sent[k]) exact++;
            ck("[FO9] ...each its own payload, in order", s, exact, 3);
            ck("[FO9] FRAMES_RX counts exactly the PDUs the input accepted", s,
               lctx_rd(s, W_FRX) - b.frx[s], accepts[s] - b.acc[s]);
        }
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, false);
        cyc(200);
    }

    void a_dense_burst_to_eight_inputs_overflows_the_store() {
        std::printf("\n[FO10] eight inputs on one stream: thirty full PDUs with no gap, more than the store holds\n");
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, true);
        cyc(200);
        const Snap b = snap();
        std::array<long, kStreams> drops_before{};
        for (int s = 0; s < kStreams; s++) drops_before[s] = (lctx_rd(s, W_DEPKT) >> 16) & 0xFFFF;
        const long drops = dut->pcm_drops_o;
        // each frame is read out eight times, eight times slower than the wire brings it, so the store fills and
        // drops whole frames; every PDU an input accepted is then either delivered to it or one of its own drops
        std::vector<Pdu> sent;
        for (int k = 0; k < 30; k++) {
            sent.push_back(payload());
            feed(aaf(0, 8, sent.back()), 0);
        }
        cyc(20000);
        flush_iv();
        ck("[FO10] the store dropped frames (the case is live)", 0, dut->pcm_drops_o - drops > 0 ? 1 : 0, 1);
        long dropped0 = -1;
        for (int s = 0; s < kStreams; s++) {
            const long delivered = static_cast<long>(got[s].size() - b.pdus[s]);
            const long dropped = static_cast<long>((lctx_rd(s, W_DEPKT) >> 16) & 0xFFFF) - drops_before[s];
            ck("[FO10] every accepted PDU is delivered to the input or one of its DEPKT drops", s,
               delivered + dropped, accepts[s] - b.acc[s]);
            ck("[FO10] the input counts drops", s, dropped > 0 ? 1 : 0, 1);
            if (s == 0) dropped0 = dropped;
            ck("[FO10] each input counts the same drops (one frame, one drop for each input that accepted it)", s,
               dropped, dropped0);
            long in_order = 0;
            size_t k = 0;
            for (size_t m = b.pdus[s]; m < got[s].size(); m++) {
                while (k < sent.size() && got[s][m] != sent[k]) k++;
                if (k < sent.size()) { in_order++; k++; }
            }
            ck("[FO10] each delivered payload is a sent one, in order", s, in_order, delivered);
        }
        for (int s = 2; s < kStreams; s++) bind(s, kTalkerA, false);
        cyc(200);
    }

    void a_pdu_off_its_inputs_frame_size_is_discarded_whole() {
        std::printf("\n[FO11] inputs 0 and 1 at 8 channels (192 octets): PDUs of 65, 64, 200 and 191 octets between valid ones\n");
        const Snap b = snap();
        const long drops = dut->pcm_drops_o;
        std::vector<Pdu> sent;
        // the review's 65-octet probe, then an aligned but wrong size, a longer one and one octet short; each
        // carries the stream's own header fields, so only its length is off. A gap after each, then back to back.
        for (int headroom : {60, 2}) {
            for (unsigned n : {65u, 64u, 200u, 191u}) {
                sent.push_back(payload());
                feed(aaf(0, 8, sent.back()), headroom);
                feed(aaf_as(0, kPcm32x8, payload(n), false), headroom);
            }
        }
        sent.push_back(payload());
        feed(aaf(0, 8, sent.back()));
        cyc(400);
        flush_iv();
        for (int s : {0, 1}) {
            received("[FO11] the 192-octet PDUs:", s, b, sent);
            ck("[FO11] the off-size PDUs count UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF) - b.uf[s] > 0 ? 1 : 0, 1);
            ck("[FO11] ...and are no SEQ_NUM_MISMATCH: a discarded PDU still advances the sequence (#775)", s,
               lctx_rd(s, W_SM) - b.sm[s], 0);
            ck("[FO11] ...and no DEPKT drop", s, ((lctx_rd(s, W_DEPKT) >> 16) & 0xFFFF) - b.ddrop[s], 0);
        }
        ck("[FO11] nothing dropped by the store", 0, dut->pcm_drops_o - drops, 0);

        std::printf("  input 1 at 8 channels of seven samples (224 octets), input 0 at six (192)\n");
        const Fmt spf7{0x02, 32, 8, 7};
        rebind_as({1}, kTalkerA, spf7);
        const Snap c = snap();
        std::vector<Pdu> six, seven;
        for (int headroom : {60, 2, 2, 60}) {
            six.push_back(payload(192));
            feed(aaf_as(0, kPcm32x8, six.back(), false), headroom);
            seven.push_back(payload(224));
            feed(aaf_as(0, spf7, seven.back(), false), headroom);
        }
        cyc(400);
        flush_iv();
        received("[FO11] input 0 takes the 192-octet PDUs:", 0, c, six);
        received("[FO11] input 1 takes the 224-octet PDUs:", 1, c, seven);
        for (int s : {0, 1})
            ck("[FO11] ...and counts the other size as UNSUPPORTED_FORMAT", s, lctx_rd(s, W_UF) - c.uf[s] > 0 ? 1 : 0, 1);
        rebind_as({1}, kTalkerA, kPcm32x8);
    }

    void payload_tails_that_are_not_whole_beats() {
        std::printf("\n[FO12] frame sizes that are not whole beats: inputs 0 and 1 on talker A, input 2 on talker B between\n");
        bind(2, kTalkerB, true);
        cyc(200);
        // every remainder 1 to 7: the final beat lies wholly in the depacketizer's hold untagged at a remainder of 1
        // or 2 octets, behind a C-VLAN tag at 1 to 6. Each frame is at least 13 beats, long enough for its PDU to be
        // queued in its flight ([FO8] holds the frames that are not)
        const Fmt tails[] = {
            {0x03, 24, 3, 9},    // INT_24BIT, 81 octets: remainder 1
            {0x03, 24, 2, 11},   // 66 octets: remainder 2
            {0x03, 24, 3, 11},   // 99 octets: remainder 3
            {0x03, 24, 4, 5},    // 60 octets: remainder 4
            {0x03, 24, 1, 31},   // 93 octets: remainder 5
            {0x04, 16, 5, 7},    // INT_16BIT, 70 octets: remainder 6
            {0x03, 24, 3, 7},    // 63 octets: remainder 7
        };
        for (const Fmt& fm : tails) {
            rebind_as({0, 1}, kTalkerA, fm);
            for (bool vlan : {false, true}) {
                std::printf("  %u octets (%u ch x %u samples, format %u)%s\n", fm.octets(), fm.ch, fm.spf, fm.format,
                            vlan ? ", tagged" : "");
                char tag[96];
                std::snprintf(tag, sizeof tag, "[FO12] %u octets%s:", fm.octets(), vlan ? " tagged" : "");
                const Snap b = snap();
                std::vector<Pdu> sa, sb;
                for (int headroom : {60, 2, 2}) {
                    const Pdu p = payload(fm.octets());
                    sa.push_back(padded(p));
                    feed(aaf_as(0, fm, p, vlan), headroom);
                    sb.push_back(payload());
                    feed(aaf_as(1, kPcm32x8, sb.back(), vlan), headroom);
                }
                cyc(800);
                flush_iv();
                for (int s : {0, 1}) received(tag, s, b, sa);
                char tb[120];
                std::snprintf(tb, sizeof tb, "%s talker B's input between them:", tag);
                received(tb, 2, b, sb);
            }
        }
        rebind_as({0, 1}, kTalkerA, kPcm32x8);
        bind(2, kTalkerB, false);
        cyc(200);
    }

    void frames_short_of_their_payload() {
        std::printf("\n[FO13] inputs 0 and 1: 192-octet PDUs whose frames end early, between whole ones\n");
        const Snap b = snap();
        const long drops = dut->pcm_drops_o;
        std::vector<Pdu> sent;
        int cut = 0;
        for (bool vlan : {false, true}) {
            for (size_t len : {size_t{150}, size_t{0}}) {   // 0: one octet short
                sent.push_back(payload());
                feed(aaf_as(0, kPcm32x8, sent.back(), vlan), 2);
                std::vector<uint8_t> f = aaf_as(0, kPcm32x8, payload(), vlan);
                f.resize(len ? len : f.size() - 1);
                feed(f, 2);
                cut++;
            }
        }
        sent.push_back(payload());
        feed(aaf(0, 8, sent.back()));
        cyc(800);
        flush_iv();
        for (int s : {0, 1}) {
            char t[120];
            ck("[FO13] each PDU is judged, the short ones too (FRAMES_RX)", s, lctx_rd(s, W_FRX) - b.frx[s],
               static_cast<long>(sent.size()) + cut);
            ck("[FO13] only the whole PDUs reach the depacketizer's output", s,
               static_cast<long>(got[s].size() - b.pdus[s]), static_cast<long>(sent.size()));
            long exact = 0;
            for (size_t k = 0; k < sent.size() && b.pdus[s] + k < got[s].size(); k++)
                if (got[s][b.pdus[s] + k] == sent[k]) exact++;
            ck("[FO13] ...each its own payload, in order", s, exact, static_cast<long>(sent.size()));
            ck("[FO13] the DEPKT tally counts the whole ones", s, (lctx_rd(s, W_DEPKT) & 0xFFFF) - b.depkt[s],
               static_cast<long>(sent.size()));
            std::snprintf(t, sizeof t, "[FO13] each short frame is one of the input's DEPKT drops");
            ck(t, s, ((lctx_rd(s, W_DEPKT) >> 16) & 0xFFFF) - b.ddrop[s], cut);
        }
        ck("[FO13] the depacketizer counts each short frame as dropped", 0, dut->pcm_drops_o - drops, cut);
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    FanOut h;
    return h.run();
}
