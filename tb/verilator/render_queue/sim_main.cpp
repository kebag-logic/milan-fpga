// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_render_queue harness (#632): the listener render path's presentation
// stage.
//
// The harness plays the depacketizer's read side (each PDU's header with tv
// and avtp_timestamp, then, PAY_LEAD cycles later, its payload beats) and the
// domain's media event: one pulse every 100 cycles carrying the frame's
// instant on an exact 48 kHz grid (thirds of a nanosecond kept, so Ps =
// 62,500 / 3 ns has no drift). Every sample names its stream, PDU, event and
// wire channel. A reference model states the law independently of the RTL:
//
//   * a PDU's event k belongs to frame n + round((ts - E_n) / Ps) + k, n the
//     latest event at its header (IEEE 1722-2016 7.5), for a PDU of any
//     length (the [long] phase: 40 and 300 events);
//   * at event n each interface i is handed frame n + K_i, every stream in
//     index order, ceil(N_CH / 2) beats each in the clone format, lanes
//     without a sample zero, tlast on the last beat, its render tick one
//     cycle after its last beat; frame n + K_min is then consumed;
//   * late: an event whose frame is consumed is dropped, a PDU with any
//     counted once, whatever its timestamp: a PDU stamped behind the latest
//     event still presents its events ahead of the consumed frame (the
//     [behind] phase, up to the longest PDU, 504 one-channel events); early:
//     an event 128 frames or more past the consumed one is dropped, counted
//     likewise; a PDU with either counted once as refused; untimed: tv = 0,
//     or the payload before the frame is known, counted once, nothing
//     written;
//   * a consumed frame's row reads silence a lap later; a flush empties the
//     stream; a gap in a presenting stream and a PDU starting on a frame its
//     stream already wrote are slips;
//   * lead_o is the stream's newest frame less the consumed one, idle_o its
//     last read empty, pop_p_o one pulse per read with a sample, converged_o
//     after 100 ms of reads with samples.
//
// Every beat of every read is compared byte-exact with the model, attributed
// to the phase it falls in, and each phase is one named check. The build's -G
// shape reaches this file as -D constants from the Makefile's single
// statement of it.
#include "../../common/verilator_harness.hpp"
#include "VKL_render_queue.h"
#include "verilated.h"

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

namespace {

constexpr int kStreams = N_STREAMS_TB;
constexpr int kCh = N_CH_TB;
constexpr int kIfs = N_IF_TB;
constexpr std::array<int, 2> kLead = {LEAD0_TB, LEAD1_TB};
constexpr int kPayLead = PAY_LEAD_TB;
constexpr int kMaxEv = MAX_EV_TB;            // the most events one PDU walks
constexpr long kClkHz = CLK_HZ_TB;
constexpr int kPairs = (kCh + 1) / 2;
constexpr long kPs3 = 62'500;                // Ps in thirds of a ns at 48 kHz
//! the frame whose instant the wrap phase puts 7 us before 2^32 ns
constexpr long kWrapAt = 3200;
constexpr long kTick = 100;                  // cycles per frame
constexpr long kPushAt = 40;                 // a frame's push window opens here
constexpr int kEvents = 6;

constexpr int kmin() { return kIfs > 1 ? std::min(kLead[0], kLead[1]) : kLead[0]; }
constexpr int kmax() { return kIfs > 1 ? std::max(kLead[0], kLead[1]) : kLead[0]; }
constexpr int kKMin = kmin();
constexpr int kKMax = kmax();
//! the depth, derived here from the hold and the event's latency
constexpr long span() {
    return ((static_cast<long>(MAX_HOLD_TB) + EV_LAT_TB) * 3 + kPs3 - 1) / kPs3 + 2;
}
constexpr int pow2ceil(long v) {
    int p = 1;
    while (p < v) p <<= 1;
    return p;
}
constexpr int kRows = pow2ceil(span());
static_assert(kRows == 128, "the [early] and [lap] phases place PDUs against 128 rows");
//! the stage's late reach in frames: the timestamp difference is read from
//! 2^31 ns + kLate frames behind to 2^31 ns - kLate frames ahead
constexpr long kLate = 3 * ((kMaxEv + 1) / 3);
constexpr long long kBiasNs = kLate * kPs3 / 3;
static_assert(kMaxEv == 504 && kLate == 504, "the [behind] phase places PDUs against a 504-frame late reach");

//! one sample: stream, PDU, event and wire channel, never zero
uint32_t sample_of(int s, int pdu, int k, int ch) {
    return (static_cast<uint32_t>(s & 1) << 23) | (static_cast<uint32_t>(pdu & 0x3F) << 17) |
           (static_cast<uint32_t>(k & 0x1FF) << 8) | (static_cast<uint32_t>(ch & 0xF) << 4) | 0x8u;
}

//! a wire-order S32BE beat, pad bytes as given
uint64_t beat_of(uint32_t s0, uint32_t s1, uint8_t pad) {
    uint64_t b = 0;
    b |= static_cast<uint64_t>((s0 >> 16) & 0xFF) << 0;
    b |= static_cast<uint64_t>((s0 >> 8) & 0xFF) << 8;
    b |= static_cast<uint64_t>(s0 & 0xFF) << 16;
    b |= static_cast<uint64_t>(pad) << 24;
    b |= static_cast<uint64_t>((s1 >> 16) & 0xFF) << 32;
    b |= static_cast<uint64_t>((s1 >> 8) & 0xFF) << 40;
    b |= static_cast<uint64_t>(s1 & 0xFF) << 48;
    b |= static_cast<uint64_t>(pad) << 56;
    return b;
}

//! one PDU the harness sends
struct Pdu {
    int stream = 0;
    int pdu = 0;
    int chans = kCh;
    int events = kEvents;
    long frame_off = 96;     //!< its first event's frame, relative to the header's event
    double phi = 0;          //!< its timestamp's offset from that frame, in Ps
    long ts_abs = -1;        //!< or this timestamp outright (ns, 64-bit)
    bool tv = true;
    int lead = kPayLead;     //!< cycles from its header to its first beat
    //! the refusal the phase builds it for, counted against late_o / early_o
    enum class Refusal { kNone, kLate, kEarly, kBoth } refusal = Refusal::kNone;
};

//! the model: the law stated on frames, one map entry per (stream, frame)
struct Model {
    long n = 0;
    long r = kKMin;
    std::map<std::pair<int, long>, std::array<int64_t, kCh>> rows;
    std::array<long, kStreams> lw{};
    std::array<bool, kStreams> lwv{};
    std::array<bool, kStreams> live{};
    std::array<long, kStreams> pops{};
    long late = 0;
    long early = 0;
    long refused = 0;
    long untimed = 0;
    long slips = 0;

    static std::array<int64_t, kCh> empty() {
        std::array<int64_t, kCh> e{};
        e.fill(-1);
        return e;
    }
    std::array<int64_t, kCh> frame(int s, long f) const {
        const auto it = rows.find({s, f});
        return it == rows.end() ? empty() : it->second;
    }
};

class RenderQueueHarness {
 public:
    RenderQueueHarness(VKL_render_queue* dut, milan::tb::Checker& check) : dut_(dut), check_(check) {}

    int run() {
        reset();
        phases();
        finish();
        return check_.report();
    }

 private:
    // ------------------------------------------------------------------ //
    // time: frame n's instant E(n), thirds of a ns kept
    long long e_ns(long n) const { return (e0_3_ + static_cast<long long>(n) * kPs3) / 3; }
    long long ts_of(long n_hdr, long off, double phi) const {
        const long long t3 = e0_3_ + static_cast<long long>(n_hdr + off) * kPs3 +
                             static_cast<long long>(phi * kPs3);
        return t3 / 3;
    }

    void reset() {
        dut_->rst_n = 0;
        for (int i = 0; i < 4; i++) cycle();
        dut_->rst_n = 1;
    }

    // ------------------------------------------------------------------ //
    // one clock cycle: inputs set for this edge, then the edge
    void cycle() {
        dut_->clk_i = 0;
        dut_->eval();
        dut_->clk_i = 1;
        dut_->eval();
        ++cyc_;
        observe();
    }

    //! the beats and ticks of the edge just taken
    void observe() {
        if (!dut_->rst_n) return;
        for (int s = 0; s < kStreams; s++)
            if ((dut_->pop_p_o >> s) & 1) pops_seen_[static_cast<size_t>(s)]++;
        for (int i = 0; i < kIfs; i++) {
            if ((dut_->render_tick_p_o >> i) & 1) {
                ticks_[i]++;
                if (cyc_ - 1 != last_beat_cyc_[i]) tick_bad_++;
            }
        }
        const unsigned tv = dut_->m_tvalid_o;
        if (tv == 0) return;
        int itf = -1;
        int nset = 0;
        for (int i = 0; i < kIfs; i++)
            if ((tv >> i) & 1) { itf = i; nset++; }
        if (nset != 1) { mismatch("two interfaces strobed on one beat"); return; }
        if (expect_.empty()) { mismatch("a beat no read expects"); return; }
        const Beat e = expect_.front();
        expect_.erase(expect_.begin());
        if (e.itf != itf || e.stream != dut_->m_tuser_o || e.last != dut_->m_tlast_o || e.data != dut_->m_tdata_o) {
            mismatch("beat");
            if (shown_ < 6) {
                std::printf("  dbg: [%s] frame %ld if %d/%d stream %d/%u last %d/%u data %016llx exp %016llx\n",
                            phase_.c_str(), e.frame, itf, e.itf, e.stream, dut_->m_tuser_o, e.last,
                            dut_->m_tlast_o, static_cast<unsigned long long>(dut_->m_tdata_o),
                            static_cast<unsigned long long>(e.data));
                shown_++;
            }
        }
        if (e.last) last_beat_cyc_[itf] = cyc_;
    }
    void mismatch(const char*) { bad_[phase_]++; }

    // ------------------------------------------------------------------ //
    // a frame: its event at cycle 0, then the push window
    struct Beat {
        int itf;
        int stream;
        bool last;
        bool any;
        long frame;
        uint64_t data;
    };

    void frame(const std::vector<Pdu>& pushes = {}, int flush_stream = -1) {
        // the event: the model reads every interface, then consumes
        if (!expect_.empty()) mismatch("a read the stage never presented");
        expect_.clear();
        m_.n++;
        for (int i = 0; i < kIfs; i++) {
            for (int s = 0; s < kStreams; s++) {
                const long f = m_.n + kLead[static_cast<size_t>(i)];
                const auto lanes = m_.frame(s, f);
                bool any = false;
                for (int64_t v : lanes) any = any || v >= 0;
                for (int j = 0; j < kPairs; j++) {
                    const int64_t a = lanes[static_cast<size_t>(2 * j)];
                    const int64_t b = (2 * j + 1 < kCh) ? lanes[static_cast<size_t>(2 * j + 1)] : -1;
                    expect_.push_back(Beat{i, s, j == kPairs - 1, any, f,
                                           beat_of(a < 0 ? 0 : static_cast<uint32_t>(a),
                                                   b < 0 ? 0 : static_cast<uint32_t>(b), 0)});
                }
                if (i == 0) {
                    if (m_.live[s] && !any) m_.slips++;
                    m_.live[s] = any;
                    if (any) m_.pops[s]++;
                }
            }
            reads_[phase_]++;
        }
        m_.r = m_.n + kKMin;
        for (int s = 0; s < kStreams; s++) {
            m_.rows.erase({s, m_.r});
            if (m_.lwv[s] && m_.lw[s] <= m_.r) m_.lwv[s] = false;
        }
        dut_->ev_p_i = 1;
        dut_->ev_ns_i = static_cast<uint32_t>(e_ns(m_.n));
        cycle();
        dut_->ev_p_i = 0;
        long c = 1;
        // the push window
        for (const Pdu& p : pushes) {
            while (c < kPushAt) { cycle(); c++; }
            c += push(p);
        }
        while (c < kTick) {
            if (flush_stream >= 0 && c == kTick - 5) {
                dut_->flush_i = 1u << flush_stream;
                flush_model(flush_stream);
            }
            cycle();
            dut_->flush_i = 0;
            c++;
        }
        // the taps, against the model, at the frame's end
        for (int s = 0; s < kStreams; s++) {
            const long lead = m_.lwv[s] ? std::min(255L, m_.lw[s] - m_.r) : 0;
            if (static_cast<long>((dut_->lead_o >> (8 * s)) & 0xFF) != lead) tap_bad_[phase_]++;
            if (((dut_->idle_o >> s) & 1) != (m_.live[s] ? 0u : 1u)) tap_bad_[phase_]++;
        }
    }

    void flush_model(int s) {
        for (auto it = m_.rows.begin(); it != m_.rows.end();)
            it = it->first.first == s ? m_.rows.erase(it) : std::next(it);
        m_.lwv[s] = false;
        m_.live[s] = false;
    }

    //! one PDU: its header now, its beats lead cycles later; the model takes
    //! it at its header. Returns the cycles it took.
    long push(const Pdu& p) {
        const long long ts = p.ts_abs >= 0 ? p.ts_abs : ts_of(m_.n, p.frame_off, p.phi);
        const bool framed = p.tv && p.lead >= kPayLead;
        if (p.refusal == Pdu::Refusal::kLate || p.refusal == Pdu::Refusal::kBoth) declared_late_++;
        if (p.refusal == Pdu::Refusal::kEarly || p.refusal == Pdu::Refusal::kBoth) declared_early_++;
        if (p.refusal != Pdu::Refusal::kNone) declared_refused_++;
        model_push(p, ts, framed);
        dut_->hdr_p_i = 1;
        dut_->hdr_ts_ns_i = static_cast<uint32_t>(ts);
        dut_->hdr_tv_i = p.tv ? 1 : 0;
        cycle();
        dut_->hdr_p_i = 0;
        long c = 1;
        while (c < p.lead) { cycle(); c++; }
        const int total = p.events * p.chans;
        const int beats = (total + 1) / 2;
        for (int b = 0; b < beats; b++) {
            const int i0 = 2 * b;
            const int i1 = 2 * b + 1;
            const uint32_t s0 = sample_of(p.stream, p.pdu, i0 / p.chans, i0 % p.chans);
            const uint32_t s1 = i1 < total ? sample_of(p.stream, p.pdu, i1 / p.chans, i1 % p.chans) : 0;
            dut_->s_tdata_i = beat_of(s0, s1, 0xA5);
            dut_->s_tvalid_i = 1;
            dut_->s_tlast_i = b == beats - 1;
            dut_->s_tuser_i = static_cast<uint8_t>(p.stream);
            dut_->wire_chans_i = 0;
            for (int s = 0; s < kStreams; s++)
                dut_->wire_chans_i |= static_cast<uint32_t>(s == p.stream ? (p.chans & 0xF) : kCh) << (4 * s);
            cycle();
            c++;
        }
        dut_->s_tvalid_i = 0;
        dut_->s_tlast_i = 0;
        return c;
    }

    void model_push(const Pdu& p, long long ts, bool framed) {
        if (!framed) { m_.untimed++; return; }
        // the 32-bit difference, read in the stage's window
        const long long d = static_cast<long long>(static_cast<int32_t>(
                                static_cast<uint32_t>(ts) - static_cast<uint32_t>(e_ns(m_.n)) +
                                static_cast<uint32_t>(kBiasNs))) - kBiasNs;
        // round(3d / Ps3), half up, on the signed difference
        const long long num = 3LL * d + kPs3 / 2;
        const long long q = num >= 0 ? num / kPs3 : -((-num + kPs3 - 1) / kPs3);
        const long f0 = m_.n + static_cast<long>(q);
        bool late = false;
        bool early = false;
        const int s = p.stream;
        for (int k = 0; k < p.events; k++) {
            const long f = f0 + k;
            if (f <= m_.r) { late = true; continue; }
            if (f >= m_.r + kRows) { early = true; continue; }
            // the PDU's first event landing on a frame its stream wrote
            if (k == 0 && m_.lwv[s] && f <= m_.lw[s]) m_.slips++;
            auto it = m_.rows.find({s, f});
            if (it == m_.rows.end()) it = m_.rows.emplace(std::make_pair(s, f), Model::empty()).first;
            for (int ch = 0; ch < p.chans && ch < kCh; ch++)
                it->second[static_cast<size_t>(ch)] = sample_of(s, p.pdu, k, ch);
            if (!m_.lwv[s] || f > m_.lw[s]) m_.lw[s] = f;
            m_.lwv[s] = true;
        }
        m_.late += late;
        m_.early += early;
        m_.refused += late || early;
    }

    // ------------------------------------------------------------------ //
    int alt() const { return kStreams > 1 ? 1 : 0; }

    void run_frames(long count) {
        for (long i = 0; i < count; i++) frame();
    }

    //! a steady stream: a PDU every 6 frames, its first event off frames ahead
    void steady(int s, int pdus, long off, double phi = 0.0, int chans = kCh) {
        for (int j = 0; j < pdus; j++) {
            Pdu p;
            p.stream = s;
            p.pdu = ++pdu_id_;
            p.frame_off = off;
            p.phi = phi;
            p.chans = chans;
            frame({p});
            run_frames(kEvents - 1);
        }
    }

    void phases() {
        // the wrap phase's frames straddle 2^32 ns
        e0_3_ = (4294967296LL - 7000) * 3 - static_cast<long long>(kWrapAt) * kPs3;

        phase_ = "boot";            // the reset walk: every read silent
        run_frames(20);

        phase_ = "place";           // the 2 ms default: 97 and 96 frames ahead
        for (int j = 0; j < 30; j++) {
            Pdu a;
            a.stream = 0; a.pdu = ++pdu_id_; a.frame_off = 97;
            frame({a});
            Pdu b;
            b.stream = alt(); b.pdu = ++pdu_id_; b.frame_off = 93 + 3 * (kStreams > 1);
            if (kStreams > 1) frame({b}); else frame();
            run_frames(kEvents - 2);
        }
        run_frames(110);

        phase_ = "round";           // every phase up to half a period: the nearest frame
        const std::array<double, 8> phis = {0.49, -0.49, 0.3, -0.3, 0.1, -0.1, 0.45, -0.45};
        for (double phi : phis) steady(0, 2, 96, phi);
        run_frames(110);

        phase_ = "chans";           // 6, 2, mono, 3, 12 wire channels and 8 again
        for (int c : {6, 2, 1, 3, 12, 8}) steady(alt(), 2, 96, 0.0, c);
        run_frames(110);

        refusal_phases();
        stream_phases();
    }

    //! the late, too-early and untimed rules
    void refusal_phases() {
        phase_ = "late";            // first two events on consumed frames; a timestamp 1 ms past
        {
            Pdu p;
            p.stream = 0; p.pdu = ++pdu_id_; p.frame_off = kKMin - 1; p.refusal = Pdu::Refusal::kLate;
            frame({p});
            run_frames(20);
            Pdu q;
            q.stream = 0; q.pdu = ++pdu_id_; q.frame_off = -48; q.refusal = Pdu::Refusal::kLate;
            frame({q});
            run_frames(140);
        }

        behind_phase();

        phase_ = "early";           // last three events past the queue; 3 ms ahead
        {
            Pdu p;
            p.stream = 0; p.pdu = ++pdu_id_; p.frame_off = kKMin + kRows - 3; p.refusal = Pdu::Refusal::kEarly;
            frame({p});
            run_frames(140);
            Pdu q;
            q.stream = 0; q.pdu = ++pdu_id_; q.frame_off = 145; q.refusal = Pdu::Refusal::kEarly;
            frame({q});
            run_frames(160);
        }

        phase_ = "untimed";         // no tv; and a payload before the frame is known
        {
            Pdu p;
            p.stream = alt(); p.pdu = ++pdu_id_; p.tv = false;
            frame({p});
            run_frames(10);
            Pdu q;
            q.stream = alt(); q.pdu = ++pdu_id_; q.lead = 4;
            frame({q});
            run_frames(110);
        }

        phase_ = "long";            // past eight events: 40 in stereo, the last ten past the queue; 300 and 504 mono
        {
            Pdu p;
            p.stream = 0; p.pdu = ++pdu_id_; p.chans = 2; p.events = 40; p.frame_off = kKMin + kRows - 30;
            p.refusal = Pdu::Refusal::kEarly;
            frame({p});
            run_frames(140);
            Pdu q;                  // events 120 on past the queue, and its frame numbers past their wrap
            q.stream = 0; q.pdu = ++pdu_id_; q.chans = 1; q.events = 300; q.frame_off = 10;
            q.refusal = Pdu::Refusal::kEarly;
            frame({q});
            run_frames(140);
            Pdu r;                  // the longest PDU, ten events in the queue: its frame numbers would pass
            r.stream = 0; r.pdu = ++pdu_id_; r.chans = 1; r.events = kMaxEv; r.frame_off = kKMin + kRows - 10;
            r.refusal = Pdu::Refusal::kEarly;   // half their wrap, misread late, without the hold
            frame({r});
            run_frames(140);
        }
    }

    //! PDUs stamped behind the latest event: each event judged on its own
    //! frame, the ones still ahead of the consumed frame presented
    void behind_phase() {
        phase_ = "behind";
        //! (frame offset, phase in Ps, events, channels, refusal): a frame
        //! behind; 0.3 Ps behind; its control 0.3 Ps ahead (d >= 0, the same
        //! frames late); 250 frames behind, its last 47 events ahead; the
        //! longest PDU 200 behind, late, presented and past the queue in turn;
        //! the longest 500 behind, its last event ahead; the longest at the
        //! late reach and one frame past it, every event late
        using R = Pdu::Refusal;
        struct Shape {
            long off;
            double phi;
            int events;
            int chans;
            R refusal;
            long after;
        };
        const std::array<Shape, 7> shapes = {{{-1, 0.0, kEvents, kCh, R::kLate, 20},
                                              {0, -0.3, kEvents, kCh, R::kLate, 20},
                                              {0, 0.3, kEvents, kCh, R::kLate, 20},
                                              {-250, 0.0, 300, 1, R::kLate, 70},
                                              {-200, 0.0, kMaxEv, 1, R::kBoth, 140},
                                              {-500, 0.0, kMaxEv, 1, R::kLate, 20},
                                              {-kLate, 0.0, kMaxEv, 1, R::kLate, 20}}};
        for (const Shape& sh : shapes) {
            Pdu p;
            p.stream = 0; p.pdu = ++pdu_id_; p.frame_off = sh.off; p.phi = sh.phi;
            p.events = sh.events; p.chans = sh.chans; p.refusal = sh.refusal;
            frame({p});
            run_frames(sh.after);
        }
        Pdu q;                      // past the late reach: refused whole, every event late
        q.stream = 0; q.pdu = ++pdu_id_; q.frame_off = -kLate - 1; q.events = kMaxEv; q.chans = 1;
        q.refusal = Pdu::Refusal::kLate;
        frame({q});
        run_frames(140);
    }

    //! a frame read once a lap, the flush, the slips, the wrap, the observer
    void stream_phases() {
        phase_ = "lap";             // one PDU, then nothing for two laps: no replay
        {
            Pdu p;
            p.stream = alt(); p.pdu = ++pdu_id_; p.frame_off = 50;
            frame({p});
            run_frames(2 * kRows + 20);
        }

        phase_ = "flush";           // queued frames flushed before they play; then fresh
        {
            for (int j = 0; j < 3; j++) {
                Pdu p;
                p.stream = alt(); p.pdu = ++pdu_id_; p.frame_off = 90;
                frame({p});
                run_frames(kEvents - 1);
            }
            frame({}, alt());
            run_frames(12);
            steady(alt(), 3, 60);
            run_frames(110);
        }

        phase_ = "slip";            // a PDU on its predecessor's last frame; a frame left out
        {
            Pdu a;
            a.stream = 0; a.pdu = ++pdu_id_; a.frame_off = 60;
            frame({a});
            Pdu b;
            b.stream = 0; b.pdu = ++pdu_id_; b.frame_off = 60 + 5 - 1;
            frame({b});
            run_frames(4);
            //! a's frames n+60..65, b's n+65..70 (on a's last), c's from n+72:
            //! frame n+71 is left out
            Pdu c;
            c.stream = 0; c.pdu = ++pdu_id_; c.frame_off = 66;
            frame({c});
            run_frames(110);
        }

        phase_ = "wrap";            // the frame instants cross 2^32 ns
        wrap_ahead_ = m_.n < kWrapAt - 60;
        while (m_.n < kWrapAt - 60) frame();
        steady(0, 25, 96);
        run_frames(110);

        phase_ = "obs";             // 110 ms of steady presentation: converged
        steady(0, 185, 96);
        conv_after_steady_ = (dut_->converged_o & 1) != 0;
        run_frames(110);
        conv_after_stop_ = (dut_->converged_o & 1) != 0;
    }

    void finish() {
        run_frames(3);
        for (const auto& [ph, n] : reads_) {
            char what[200];
            const long bad = bad_.count(ph) ? bad_.at(ph) : 0;
            std::snprintf(what, sizeof what,
                          "[%s] every event presented to every interface is the frame the law names, byte-exact "
                          "(%ld reads, %ld mismatched beats)", ph.c_str(), n, bad);
            check_.that(what, n > 0 && bad == 0);
            const long tb = tap_bad_.count(ph) ? tap_bad_.at(ph) : 0;
            std::snprintf(what, sizeof what, "[%s] lead_o and idle_o follow the model at every frame end (%ld off)",
                          ph.c_str(), tb);
            check_.that(what, tb == 0);
        }
        char what[200];
        std::snprintf(what, sizeof what, "[late] late PDUs counted once each (%u, model %ld, phases %ld)",
                      dut_->late_o, m_.late, declared_late_);
        check_.that(what, dut_->late_o == static_cast<unsigned>(m_.late) && m_.late == declared_late_);
        std::snprintf(what, sizeof what, "[early] too-early PDUs counted once each (%u, model %ld, phases %ld)",
                      dut_->early_o, m_.early, declared_early_);
        check_.that(what, dut_->early_o == static_cast<unsigned>(m_.early) && m_.early == declared_early_);
        std::snprintf(what, sizeof what,
                      "[refused] PDUs with a late or too-early event counted once each in refused_o (%u, model %ld, "
                      "phases %ld)", dut_->refused_o, m_.refused, declared_refused_);
        check_.that(what, dut_->refused_o == static_cast<unsigned>(m_.refused) && m_.refused == declared_refused_);
        std::snprintf(what, sizeof what, "[untimed] untimed PDUs counted once each (%u, model %ld)",
                      dut_->untimed_o, m_.untimed);
        check_.that(what, dut_->untimed_o == static_cast<unsigned>(m_.untimed) && m_.untimed == 2);
        std::snprintf(what, sizeof what, "[slip] gaps and overlaps counted (%u, model %ld)", dut_->slips_o, m_.slips);
        check_.that(what, dut_->slips_o == static_cast<unsigned>(m_.slips));
        for (int s = 0; s < kStreams; s++) {
            std::snprintf(what, sizeof what, "[obs] stream %d: one pop per interface-0 read with a sample (%ld, model %ld)",
                          s, pops_seen_[static_cast<size_t>(s)], m_.pops[static_cast<size_t>(s)]);
            check_.that(what, pops_seen_[static_cast<size_t>(s)] == m_.pops[static_cast<size_t>(s)]);
        }
        check_.that("[obs] converged after 110 ms of steady presentation, and cleared by the gap after it",
                    conv_after_steady_ && !conv_after_stop_);
        check_.that("[wrap] the phase starts before its frame instants cross 2^32 ns, so its PDUs straddle the wrap",
                    wrap_ahead_);
        std::snprintf(what, sizeof what,
                      "[if] each interface's render tick comes one cycle after its last beat, once per event (%ld off)",
                      tick_bad_);
        bool ticks_ok = tick_bad_ == 0;
        for (int i = 0; i < kIfs; i++) ticks_ok = ticks_ok && ticks_[i] == m_.n;
        check_.that(what, ticks_ok);
        bool lanes_ok = true;
        for (int s = 0; s < kStreams; s++)
            lanes_ok = lanes_ok && ((dut_->m_wire_chans_o >> (4 * s)) & 0xF) == static_cast<unsigned>(2 * kPairs);
        std::snprintf(what, sizeof what,
                      "[if] every stream presents 2 x ceil(N_CH / 2) = %d lanes to its crossbar, the pad lane of an "
                      "odd count a channel never latched", 2 * kPairs);
        check_.that(what, lanes_ok);
    }

    VKL_render_queue* dut_;
    milan::tb::Checker& check_;
    long cyc_ = 0;
    long long e0_3_ = 0;
    Model m_;
    int pdu_id_ = 0;
    long declared_late_ = 0;
    long declared_early_ = 0;
    long declared_refused_ = 0;
    std::string phase_ = "boot";
    std::vector<Beat> expect_;
    std::map<std::string, long> reads_, bad_, tap_bad_;
    std::array<long, 4> ticks_{};
    std::array<long, 4> last_beat_cyc_{};
    long tick_bad_ = 0;
    std::array<long, kStreams> pops_seen_{};
    bool conv_after_steady_ = false;
    bool wrap_ahead_ = false;
    bool conv_after_stop_ = true;
    int shown_ = 0;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<VKL_render_queue> model;
    milan::tb::Checker check{"render_queue"};
    check.echo_passes();
    std::printf("== KL_render_queue: %d streams x %d lanes, %d interfaces (out-leads %d, %d), %d rows ==\n",
                kStreams, kCh, kIfs, kLead[0], kIfs > 1 ? kLead[1] : 0, kRows);
    RenderQueueHarness harness(model.get(), check);
    return harness.run();
}
