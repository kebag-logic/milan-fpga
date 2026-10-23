// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The slot-MSB pin decoder of one TDM interface (#632): it reads only that
// interface's bclk, fsync and (for a render interface) data pins. The rise
// that reads fsync high is the frame's sync instant; slot k's MSB is sampled
// (k x word_bits + d) rises later, d the data delay, and the slot's
// data_bits bits MSB first from there. sim_pins.cpp grades capture stamps
// against the MSB instants; sim_render.cpp grades rendered samples by their
// decoded value against those instants.
#pragma once

#include <array>
#include <cstdint>
#include <deque>

namespace milan::tb {

struct SlotMsbDecoder {
    SlotMsbDecoder(int s, int dd, double hz) : slots(s), data_delay(dd), bit_hz(hz) {}
    int slots;
    int data_delay;
    double bit_hz;
    static constexpr int kWordBits = 32;
    static constexpr int kDataBits = 24;

    //! one frame: its sync instant, each slot's MSB instant and value
    struct Frame {
        double sync = 0;
        std::array<double, 32> msb{};
        std::array<uint32_t, 32> value{};
        int got = 0;       //!< slots whose MSB was sampled
        int valued = 0;    //!< slots whose data bits are all in
    };
    std::deque<Frame> frames;
    //! frames whose every slot's data is in, oldest first (the render
    //! grader drains it; the capture grader never reads it)
    std::deque<Frame> done;
    long rise = -1;        //!< rises since the latest sync
    int prev_bclk = 0;

    //! slot k's MSB after the frame's sync instant, ns
    double slot_offset(int k) const { return (k * double(kWordBits) + data_delay) * 1e9 / bit_hz; }

    //! one pin sample at t_ns; data is the interface's serial data pin
    void on_edge(int bclk, int fsync, int data, double t_ns) {
        const bool r = bclk && !prev_bclk;
        prev_bclk = bclk;
        if (!r) return;
        if (fsync) {
            frames.push_back(Frame{});
            frames.back().sync = t_ns;
            if (frames.size() > 64) frames.pop_front();
            rise = 0;
        } else if (rise >= 0) {
            ++rise;
        }
        if (rise < 0 || frames.empty() || rise < data_delay) return;
        const long pos = rise - data_delay;
        const long k = pos / kWordBits;
        const long b = pos % kWordBits;
        if (k >= slots) return;
        Frame& f = frames.back();
        if (b == 0) {
            f.msb[static_cast<size_t>(k)] = t_ns;
            f.got++;
        }
        if (b < kDataBits) {
            uint32_t& v = f.value[static_cast<size_t>(k)];
            v = (v << 1) | static_cast<uint32_t>(data & 1);
            if (b == kDataBits - 1 && ++f.valued == slots) done.push_back(f);
        }
    }
};

}  // namespace milan::tb
