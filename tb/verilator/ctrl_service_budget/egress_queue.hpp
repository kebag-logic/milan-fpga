// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The transmit queue below the mailbox at a 100 Mb/s point, which decides the mailbox's tx_ready each cycle
// (#1004's egress gate; PR #1020's 100 Mb/s ruling, item 3: the census runs with egress drained at link rate through
// the shipping queue). Its stages, each one in the order a control frame meets it:
//   - the control lane's byte crossing (`ctl_tx_cdc`, milan_soc.py), lane_bytes deep, a byte visible to the packer
//     cross_dp datapath cycles after the mailbox hands it over;
//   - KL_ctrl_split's packer, one byte a datapath cycle while it holds no finished beat, so eight bytes in nine cycles;
//   - the control lane's min-IFG gasket (`ctl_ifg`, milan_datapath.sv), gap_dp cycles after a frame's last beat;
//   - the merges with the shape's SR stream and its gPTP frames, a frame at a time, alternating when both wait;
//   - MilanMAC's store-and-forward FIFO, sf_beats words and sf_frames frames, each frame held from its first beat to
//     its last octet on the wire, and released whole;
//   - the wire: preamble, the frame padded to min_frame, its FCS, then gap_octets of inter-frame gap.
// egress_mii.py states every parameter from its source and is the same model in Python, which its grade checks this
// one against. Each control frame's departure prints one EGRESS line: the sys cycle its last byte left the mailbox,
// its channel, its length, and the picosecond its last beat entered the FIFO and its last octet left the wire.
#pragma once
#include <cstdint>
#include <cstdio>
#include <deque>
#include <utility>
#include <vector>

struct EgressParams {
    std::uint64_t sys_ps = 0;            // one mailbox clock
    std::uint64_t dp_ps = 0;             // one datapath clock
    std::uint64_t octet_ps = 0;          // one octet on the wire
    unsigned lane_bytes = 0;             // the byte crossing's depth
    unsigned cross_dp = 0;               // its latency, datapath cycles
    unsigned gap_dp = 0;                 // a control frame's last beat to the next one's first, datapath cycles
    unsigned sf_beats = 0;               // the store-and-forward FIFO's words
    unsigned sf_frames = 0;              // and frames
    unsigned preamble = 0;               // preamble and start delimiter
    unsigned fcs = 0;                    // the frame check sequence
    unsigned gap_octets = 0;             // inter-frame gap
    unsigned min_frame = 0;              // a frame's least length without its FCS
    std::vector<unsigned> sr_bytes;      // the SR streams' frames, one a talker
    std::uint64_t sr_period_ps = 0;      // and their period
    std::vector<unsigned> gptp_bytes;    // the gPTP frames sent together
    std::uint64_t gptp_period_ps = 0;    // and their period
};

class EgressQueue {
public:
    // A point at gigabit rate states no queue (octet_ps 0), and its testbench prints nothing of one.
    explicit EgressQueue(EgressParams p) : p_(std::move(p)) {
        if (p_.octet_ps == 0) return;
        std::printf("EGRESSQ sys_ps=%llu dp_ps=%llu octet_ps=%llu lane=%u cross=%u gap=%u sf=%u/%u frame=%u/%u/%u/%u"
                    " sr=%zu/%llu gptp=%zu/%llu\n", ull(p_.sys_ps), ull(p_.dp_ps), ull(p_.octet_ps), p_.lane_bytes,
                    p_.cross_dp, p_.gap_dp, p_.sf_beats, p_.sf_frames, p_.preamble, p_.fcs, p_.gap_octets,
                    p_.min_frame, p_.sr_bytes.size(), ull(p_.sr_period_ps), p_.gptp_bytes.size(), ull(p_.gptp_period_ps));
    }

    // Whether the crossing takes a mailbox byte at the next edge.
    bool ready() const { return lane_.size() < p_.lane_bytes; }

    // A mailbox byte taken at sys cycle `sys`; the record's last byte names its channel.
    void take(std::uint64_t sys, bool last, unsigned ch) {
        lane_.push_back({sys * p_.sys_ps + p_.cross_dp * p_.dp_ps, last, ch, sys});
    }

    // Every datapath cycle up to the end of sys cycle `sys`.
    void advance(std::uint64_t sys) {
        const std::uint64_t until = sys * p_.sys_ps;
        while (next_dp_ <= until) {
            cycle(next_dp_);
            next_dp_ += p_.dp_ps;
        }
    }

private:
    enum class Lock { none, control, other };
    struct Byte { std::uint64_t at; bool last; unsigned ch; std::uint64_t sys; };
    struct Held { unsigned beats; std::uint64_t end; };

    static unsigned long long ull(std::uint64_t v) { return v; }

    // One datapath cycle at picosecond t: arrivals, one beat into the FIFO, then the packer.
    void cycle(std::uint64_t t) {
        while (!fifo_.empty() && fifo_.front().end <= t) {
            used_ -= fifo_.front().beats;
            fifo_.pop_front();
        }
        while (p_.sr_period_ps != 0 && sr_next_ <= t) {
            for (const unsigned bytes : p_.sr_bytes) others_.push_back(bytes);
            sr_next_ += p_.sr_period_ps;
        }
        while (p_.gptp_period_ps != 0 && gptp_next_ <= t) {
            for (const unsigned bytes : p_.gptp_bytes) others_.push_back(bytes);
            gptp_next_ += p_.gptp_period_ps;
        }
        const bool held = beat_ready_;  // the packer's ready is the cycle's start value
        if (lock_ == Lock::none) grant(t, held);
        if (lock_ == Lock::control && held && used_ < p_.sf_beats) {
            ++used_;
            ++beats_;
            beat_ready_ = false;
            if (beat_last_) {
                complete(t, frame_len_, true);
                gap_until_ = t + p_.gap_dp * p_.dp_ps;
                lock_ = Lock::none;
            }
        } else if (lock_ == Lock::other && used_ < p_.sf_beats) {
            ++used_;
            ++beats_;
            if (--other_left_ == 0) {
                complete(t, others_.front(), false);
                others_.pop_front();
                lock_ = Lock::none;
            }
        }
        if (!held && !lane_.empty() && lane_.front().at <= t) pack();
    }

    // At a frame boundary: the control lane's frame or the next SR or gPTP frame, alternating when both wait, each
    // only with a frame slot free in the FIFO.
    void grant(std::uint64_t t, bool held) {
        const bool control = held && t >= gap_until_;
        const bool other = !others_.empty();
        if ((!control && !other) || fifo_.size() >= p_.sf_frames) return;
        lock_ = control && (!other || last_ != Lock::control) ? Lock::control : Lock::other;
        last_ = lock_;
        beats_ = 0;
        if (lock_ == Lock::other) other_left_ = (others_.front() + 7u) / 8u;
    }

    // The packer takes one byte; its eighth, or the frame's last, finishes a beat.
    void pack() {
        const Byte b = lane_.front();
        lane_.pop_front();
        ++beat_bytes_;
        ++frame_bytes_;
        if (b.last || beat_bytes_ == 8u) {
            beat_ready_ = true;
            beat_last_ = b.last;
            beat_bytes_ = 0;
            if (b.last) {
                frame_len_ = frame_bytes_;
                frame_ch_ = b.ch;
                frame_sys_ = b.sys;
                frame_bytes_ = 0;
            }
        }
    }

    // A frame whose last beat entered the FIFO at t: its turn on the wire, after the frames ahead of it.
    void complete(std::uint64_t t, unsigned len, bool control) {
        const std::uint64_t start = t > wire_free_ ? t : wire_free_;
        const unsigned octets = p_.preamble + (len > p_.min_frame ? len : p_.min_frame) + p_.fcs;
        const std::uint64_t end = start + octets * p_.octet_ps;
        wire_free_ = end + p_.gap_octets * p_.octet_ps;
        fifo_.push_back({beats_, end});
        if (control) {
            std::printf("EGRESS %llu %u %u %llu %llu\n", ull(frame_sys_), frame_ch_, len, ull(t), ull(end));
        }
    }

    EgressParams p_;
    std::deque<Byte> lane_;
    std::deque<unsigned> others_;
    std::deque<Held> fifo_;
    std::uint64_t next_dp_ = 0;
    std::uint64_t sr_next_ = 0;
    std::uint64_t gptp_next_ = 0;
    std::uint64_t gap_until_ = 0;
    std::uint64_t wire_free_ = 0;
    std::uint64_t frame_sys_ = 0;
    unsigned used_ = 0;
    unsigned beats_ = 0;
    unsigned other_left_ = 0;
    unsigned beat_bytes_ = 0;
    unsigned frame_bytes_ = 0;
    unsigned frame_len_ = 0;
    unsigned frame_ch_ = 0;
    bool beat_ready_ = false;
    bool beat_last_ = false;
    Lock lock_ = Lock::none;
    Lock last_ = Lock::none;
};
