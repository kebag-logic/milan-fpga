// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_depkt.cpp - KL_aaf_rx_depacketizer on its own (#948), N_STREAMS_P = 4:
// the frame boundaries of each PDU's output for every payload length, read out
// once for each input that accepted it.
//
// The harness plays the monitor: an enqueue pulse in the frame's flight (the
// parser matches on beat 7), then a done pulse naming the accepting inputs, in
// enqueue order, some cycles later (before or after the frame's end). The
// consumer stalls at random, or at each PDU's last two beats, or never.
//
//   [DT1] a 64-octet payload is eight beats with one tlast, and a 65-octet
//         one nine beats with one, its last beat lying in the hold
//   [DT2] every payload length 1..72 and 184..200, and 1000, 1001 and 1983,
//         untagged and behind a C-VLAN tag, with and without octets after
//         the payload, to one, two or four inputs or to none, each case
//         followed by an ordinary 192-octet PDU to another input. Each input
//         that accepted a PDU receives it as one frame of ceil(length/8)
//         beats, tlast on the last alone, tuser its own index throughout,
//         the payload byte for byte and zeros after it; the inputs' passes
//         come lowest first, and the next PDU keeps its own boundaries and
//         index. A stalled beat holds its data, tuser and tlast (AXI-Stream).
//         pdus_o and pdu_out_p_o count each delivered pass under its index,
//         and nothing is dropped
//   [DT3] frames that end short of their payload, by words or by octets of
//         the last beat, untagged and tagged: nothing of the PDU is read out,
//         drops_o counts the frame, drop_p_o names its accepting inputs, and
//         the next PDU arrives whole
//
// Usage: make -C tb/verilator/avtp_rxmon depkt

#include <cstdint>
#include <cstdio>
#include <deque>
#include <memory>
#include <vector>

#include "Vdepkt_top.h"
#include "verilated.h"

namespace {

constexpr int kInputs = 4;
using Bytes = std::vector<uint8_t>;

struct Rng {
    uint64_t s;
    uint64_t next() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
    unsigned below(unsigned n) { return static_cast<unsigned>(next() % n); }
};

//! one frame on the tap: its octets, whether its PDU is queued, and the accepting inputs
struct Frame {
    Bytes octets;
    bool queued;
    unsigned mask;
    Bytes payload;      // the stream_data_length octets, as the header names them
    bool whole;         // the frame holds them all
};

//! one output frame as the consumer saw it
struct Out {
    unsigned tuser;
    Bytes data;
    bool tuser_steady;
};

enum class Stall { kNone, kRandom, kTail };

class Depkt {
 public:
    int run() {
        reset();
        std::printf("== KL_aaf_rx_depacketizer, N_STREAMS_P=4, PAY_LEAD_CYC_P=%d (#948) ==\n", LEAD_TB);
        control_and_probe();
        every_length();
        frames_short_of_their_payload();
        std::printf("\n======================================================================\n");
        std::printf("DEPKT: %ld checks, %ld failures\nRESULT: %s\n", checks, fails, fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

 private:
    std::unique_ptr<Vdepkt_top> d = std::make_unique<Vdepkt_top>();
    long checks = 0;
    long fails = 0;
    Rng rng{0x9E3779B97F4A7C15ull};
    Stall stall = Stall::kNone;
    unsigned pdu_no = 0;

    // the consumer's view
    std::vector<Out> outs;                 // completed output frames, in order
    Out cur{0, {}, true};
    bool have_cur = false;
    unsigned beat_in_frame = 0;
    unsigned tail_beats = 0;               // the current PDU's beat count (for the tail stall)
    int hold = 0;                          // cycles of stall left
    bool stalled_seen = false;             // a stalled beat to compare on the next cycle
    uint64_t st_data = 0; unsigned st_user = 0; bool st_last = false;
    long axis_breaks = 0;
    std::vector<unsigned> out_idx;         // pdu_out_p_o's indices
    std::vector<unsigned> drop_masks;      // drop_p_o's masks

    // the monitor's done pulses still owed, in enqueue order: {cycle due, mask}
    std::deque<std::pair<long, unsigned>> owed;
    long now = 0;

    void ck(const char* t, long have, long exp) {
        checks++;
        if (have != exp) { fails++; std::printf("  [FAIL] %s got=%ld exp=%ld\n", t, have, exp); }
        else std::printf("  [ ok ] %s = %ld\n", t, have);
    }

    void reset() {
        d->rst_n = 0;
        d->s_tvalid_i = 0; d->s_tready_i = 1; d->s_tlast_i = 0; d->s_tkeep_i = 0; d->s_tdata_i = 0;
        d->pdu_enq_p_i = 0; d->pdu_done_p_i = 0; d->pdu_done_mask_i = 0;
        d->m_axis_tready = 1;
        for (int i = 0; i < 6; i++) cycle();
        d->rst_n = 1;
        for (int i = 0; i < 4; i++) cycle();
    }

    // one clock: drive the consumer's tready and the owed done pulse, sample the output, then the edge
    void cycle() {
        d->clk_i = 0;
        d->pdu_done_p_i = 0;
        if (!owed.empty() && owed.front().first <= now) {
            d->pdu_done_p_i = 1;
            d->pdu_done_mask_i = owed.front().second;
            owed.pop_front();
        }
        d->eval();
        // the consumer decides on this cycle's beat
        bool ready = true;
        if (d->m_axis_tvalid) {
            if (stall == Stall::kRandom) ready = rng.below(10) < 6;
            else if (stall == Stall::kTail) {
                if (hold == 0 && tail_beats >= 2 && beat_in_frame + 2 >= tail_beats && !stalled_seen) hold = 5;
                if (hold > 0) { ready = false; hold--; }
            }
        }
        d->m_axis_tready = ready;
        d->eval();
        if (d->m_axis_tvalid) {
            if (stalled_seen && (d->m_axis_tdata != st_data || d->m_axis_tuser != st_user ||
                                 static_cast<bool>(d->m_axis_tlast) != st_last))
                axis_breaks++;
            stalled_seen = false;
            if (d->m_axis_tready) {
                if (!have_cur) { cur = Out{d->m_axis_tuser, {}, true}; have_cur = true; }
                if (d->m_axis_tuser != cur.tuser) cur.tuser_steady = false;
                for (int k = 0; k < 8; k++) cur.data.push_back(static_cast<uint8_t>(d->m_axis_tdata >> (8 * k)));
                beat_in_frame++;
                if (d->m_axis_tlast) {
                    outs.push_back(cur);
                    have_cur = false;
                    beat_in_frame = 0;
                    hold = 0;
                }
            } else {
                stalled_seen = true;
                st_data = d->m_axis_tdata; st_user = d->m_axis_tuser; st_last = d->m_axis_tlast;
            }
        } else if (stalled_seen) {
            axis_breaks++;                 // a stalled beat withdrawn
            stalled_seen = false;
        }
        d->clk_i = 1;
        d->eval();
        if (d->pdu_out_p_o) out_idx.push_back(d->pdu_out_idx_o);
        if (d->drop_p_o) drop_masks.push_back(d->drop_mask_o);
        now++;
    }

    Bytes payload(unsigned n) {
        Bytes p(n);
        for (unsigned i = 0; i < n; i++) p[i] = static_cast<uint8_t>(pdu_no * 37u + i * 5u + 3u);
        pdu_no++;
        return p;
    }

    // an AAF frame carrying `p`, tagged when `vlan`, `extra` octets after the payload, cut to `cut` octets if set
    static Frame frame(const Bytes& p, bool vlan, unsigned extra, unsigned mask, size_t cut = 0) {
        const size_t o = vlan ? 18 : 14;
        Bytes f(o + 24 + p.size() + extra, 0xEE);
        for (size_t i = 0; i < o + 24; i++) f[i] = 0;
        for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
        if (vlan) { f[12] = 0x81; f[13] = 0x00; f[14] = 0x60; f[15] = 0x02; }
        f[o - 2] = 0x22; f[o - 1] = 0xF0;
        f[o + 0] = 0x02; f[o + 1] = 0x81;
        f[o + 12] = 0x12; f[o + 13] = 0x34; f[o + 14] = 0x56; f[o + 15] = 0x78;
        f[o + 16] = 0x02; f[o + 17] = 0x50; f[o + 18] = 8; f[o + 19] = 32;
        f[o + 20] = static_cast<uint8_t>(p.size() >> 8);
        f[o + 21] = static_cast<uint8_t>(p.size());
        for (size_t i = 0; i < p.size(); i++) f[o + 24 + i] = p[i];
        bool whole = true;
        if (cut) { f.resize(cut); whole = cut >= o + 24 + p.size(); }
        return Frame{f, true, mask, p, whole};
    }

    // the tap: one beat a cycle, the enqueue pulse on beat 8 (one after the parser's match on beat 7), the done
    // pulse `lag` cycles after it
    void feed(const Frame& fr, int lag, int gap) {
        const size_t beats = (fr.octets.size() + 7) / 8;
        for (size_t b = 0; b < beats; b++) {
            uint64_t w = 0;
            unsigned n = 0;
            for (unsigned k = 0; k < 8 && b * 8 + k < fr.octets.size(); k++, n++)
                w |= static_cast<uint64_t>(fr.octets[b * 8 + k]) << (8 * k);
            d->s_tdata_i = w;
            d->s_tkeep_i = n == 8 ? 0xFF : ((1u << n) - 1);
            d->s_tvalid_i = 1;
            d->s_tlast_i = b + 1 == beats;
            d->pdu_enq_p_i = fr.queued && b == 8;
            if (fr.queued && b == 8) owed.emplace_back(now + lag, fr.mask);
            cycle();
        }
        d->s_tvalid_i = 0; d->s_tlast_i = 0; d->pdu_enq_p_i = 0;
        for (int i = 0; i < gap; i++) cycle();
    }

    // until the output is idle for longer than the store takes to pass over a frame no input accepted (256 words)
    void drain() {
        int idle = 0;
        while (idle < 300) {
            cycle();
            idle = (d->m_axis_tvalid || !owed.empty()) ? 0 : idle + 1;
        }
    }

    // what the frames should have produced, in order: one output per accepting input, lowest first
    static std::vector<Out> expected(const std::vector<Frame>& fs) {
        std::vector<Out> e;
        for (const Frame& f : fs) {
            if (!f.queued || !f.whole) continue;
            Bytes q = f.payload;
            q.resize((q.size() + 7) / 8 * 8, 0);
            for (unsigned s = 0; s < kInputs; s++)
                if (f.mask & (1u << s)) e.push_back(Out{s, q, true});
        }
        return e;
    }

    // run frames back to back and grade the outputs; returns true when every output matched
    bool grade(const char* tag, const std::vector<Frame>& fs, int lag, bool print) {
        outs.clear(); out_idx.clear(); drop_masks.clear(); axis_breaks = 0;
        const unsigned pdus0 = d->pdus_o;
        const unsigned drops0 = d->drops_o;
        for (const Frame& f : fs) feed(f, lag, static_cast<int>(rng.below(3)));
        drain();
        const std::vector<Out> e = expected(fs);
        long exact = 0;
        bool order_ok = outs.size() == e.size();
        for (size_t k = 0; k < e.size() && k < outs.size(); k++) {
            if (outs[k].tuser == e[k].tuser && outs[k].data == e[k].data && outs[k].tuser_steady) exact++;
            else order_ok = false;
        }
        long idx_ok = out_idx.size() == e.size();
        for (size_t k = 0; k < e.size() && k < out_idx.size(); k++)
            if (out_idx[k] != e[k].tuser) idx_ok = 0;
        long short_q = 0;
        std::vector<unsigned> want_drops;
        for (const Frame& f : fs)
            if (f.queued && !f.whole) { short_q++; if (f.mask) want_drops.push_back(f.mask); }
        const bool ok = order_ok && idx_ok && axis_breaks == 0 &&
                        static_cast<uint16_t>(d->pdus_o - pdus0) == e.size() &&
                        static_cast<uint16_t>(d->drops_o - drops0) == short_q && drop_masks == want_drops;
        if (print || !ok) {
            char t[200];
            std::snprintf(t, sizeof t, "%s output frames, one per accepting input", tag);
            ck(t, static_cast<long>(outs.size()), static_cast<long>(e.size()));
            std::snprintf(t, sizeof t, "%s ...each its beats, its tlast, its index and its bytes, in order", tag);
            ck(t, exact, static_cast<long>(e.size()));
            std::snprintf(t, sizeof t, "%s pdu_out_p_o names each pass's input", tag);
            ck(t, idx_ok, 1);
            std::snprintf(t, sizeof t, "%s pdus_o counts each pass", tag);
            ck(t, static_cast<uint16_t>(d->pdus_o - pdus0), static_cast<long>(e.size()));
            std::snprintf(t, sizeof t, "%s drops_o counts each short frame", tag);
            ck(t, static_cast<uint16_t>(d->drops_o - drops0), short_q);
            std::snprintf(t, sizeof t, "%s drop_p_o names each short frame's accepting inputs", tag);
            ck(t, drop_masks == want_drops ? 1 : 0, 1);
            std::snprintf(t, sizeof t, "%s a stalled beat holds its data, tuser and tlast", tag);
            ck(t, axis_breaks, 0);
        }
        return ok;
    }

    void control_and_probe() {
        std::printf("\n[DT1] 64 and 65 octets, untagged, to input 0\n");
        for (unsigned n : {64u, 65u}) {
            outs.clear();
            feed(frame(payload(n), false, 0, 1), 3, 0);
            drain();
            char t[120];
            const unsigned beats = (n + 7) / 8;
            std::snprintf(t, sizeof t, "[DT1] a %u-octet payload: one output frame", n);
            ck(t, static_cast<long>(outs.size()), 1);
            std::snprintf(t, sizeof t, "[DT1] a %u-octet payload: %u beats, tlast on the last", n, beats);
            ck(t, outs.empty() ? 0 : static_cast<long>(outs[0].data.size() / 8), beats);
        }
    }

    void every_length() {
        std::printf("\n[DT2] every length, tagged and untagged, to none, one, two or four inputs, three consumers\n");
        std::vector<unsigned> lengths;
        for (unsigned n = 1; n <= 72; n++) lengths.push_back(n);
        for (unsigned n = 184; n <= 200; n++) lengths.push_back(n);
        for (unsigned n : {1000u, 1001u, 1983u}) lengths.push_back(n);
        const unsigned masks[] = {0x1, 0x5, 0xF, 0x8, 0x0};
        const Stall stalls[] = {Stall::kNone, Stall::kRandom, Stall::kTail};
        const char* sname[] = {"no stall", "random stalls", "stalls at the last two beats"};
        long cases = 0;
        long good = 0;
        for (int si = 0; si < 3; si++) {
            stall = stalls[si];
            for (bool vlan : {false, true}) {
                for (unsigned n : lengths) {
                    for (unsigned mask : masks) {
                        // a frame of the stream is at least nine beats with its PDU queued; a short payload carries
                        // octets after it, and every eighth case does
                        const size_t hdr = vlan ? 42 : 38;
                        unsigned extra = (hdr + n < 72) ? static_cast<unsigned>(72 - hdr - n) : 0;
                        if ((cases & 7) == 3) extra += 1 + rng.below(12);
                        tail_beats = (n + 7) / 8;
                        std::vector<Frame> fs;
                        fs.push_back(frame(payload(n), vlan, extra, mask));
                        // the next PDU, to another input: input 2, or input 0 after one to input 2 alone
                        const Frame next = frame(payload(192), false, 0, mask == 0x4 ? 0x1 : 0x2);
                        const bool fits = (fs[0].octets.size() + next.octets.size()) / 8 < 250;
                        char tag[120];
                        std::snprintf(tag, sizeof tag, "[DT2] %u octets%s, inputs %X, %s:", n, vlan ? " tagged" : "",
                                      mask, sname[si]);
                        const int lag = 2 + static_cast<int>(rng.below(40));
                        bool ok;
                        if (fits) {
                            fs.push_back(next);
                            ok = grade(tag, fs, lag, false);
                        } else {
                            ok = grade(tag, fs, lag, false) && grade(tag, {next}, lag, false);
                        }
                        cases++;
                        if (ok) good++;
                    }
                }
            }
        }
        stall = Stall::kNone;
        ck("[DT2] cases whose every output frame is whole, in order, under its index", good, cases);
    }

    void frames_short_of_their_payload() {
        std::printf("\n[DT3] frames that end short of their payload, then a whole PDU\n");
        for (bool vlan : {false, true}) {
            const size_t hdr = vlan ? 42 : 38;
            for (unsigned n : {192u, 65u, 66u}) {
                for (size_t short_by : {size_t{1}, size_t{7}, size_t{8}, size_t{9}, size_t{40}}) {
                    for (unsigned mask : {0x3u, 0x0u}) {
                        const Bytes p = payload(n);
                        std::vector<Frame> fs;
                        fs.push_back(frame(p, vlan, 0, mask, hdr + n - short_by));
                        if (fs[0].octets.size() < 72) continue;    // its PDU is queued on beat 8, in its flight
                        fs.push_back(frame(payload(192), false, 0, 0x4));
                        char tag[120];
                        std::snprintf(tag, sizeof tag, "[DT3] %u octets%s, %zu short, inputs %X:", n,
                                      vlan ? " tagged" : "", short_by, mask);
                        grade(tag, fs, 2 + static_cast<int>(rng.below(20)), true);
                    }
                }
            }
        }
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Depkt h;
    return h.run();
}
