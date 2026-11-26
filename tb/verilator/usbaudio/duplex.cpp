// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Independent bus, oscillator and media-grid drivers with exact sample scoring.
#include "VKL_usbaudio_bridge.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <stdexcept>
#include <string>
#include <vector>
#ifndef WINDOW_LOG2_TB
#define WINDOW_LOG2_TB 13
#endif

static uint32_t sample(uint32_t frame, unsigned channel) {
  return (frame * 0x1020305U) ^ (0x89abcdefU + channel * 0x31415927U);
}
static uint32_t swap_bytes(uint32_t value) { return __builtin_bswap32(value); }

struct Bench {
  milan::tb::Model<VKL_usbaudio_bridge> model;
  VKL_usbaudio_bridge &dut = *model;
  milan::tb::Checker checks{"usbaudio_duplex"};
  uint64_t steps = 0;
  uint64_t oscillator_phase = 0;
  uint64_t oscillator_cycles = 0;
  uint64_t bus_cycles = 0;
  uint64_t frames = 0;
  uint64_t next_reference = 2000;
  uint32_t reference_sequence = 0;
  uint32_t playback_sent = 0;
  uint32_t playback_seen = 0;
  uint32_t capture_seen = 0;
  uint32_t capture_first = 0;
  uint32_t last_status_epoch = 0;
  unsigned render_phase = 0;
  unsigned playback_pair = 0;
  unsigned capture_word = 0;
  unsigned status_word = 0;
  unsigned packet_words = 0;
  unsigned previous_status_sequence = 0;
  uint16_t capture_low = 0;
  uint32_t capture_frame_candidate = 0;
  bool capture_started = false;
  bool streaming = false;
  bool first_status = true;
  bool playback_started = false;
  uint16_t status[10]{};
  std::deque<uint16_t> incoming;
  uint32_t playback_epoch = 1;
  uint32_t capture_epoch = 1;
  uint64_t stream_start = 0;
  uint64_t next_pcm = 0;

  void check(bool value, const char *name) {
    if (!checks.that(name, value)) {
      checks.report();
      throw std::runtime_error(name);
    }
  }

  void push32(uint32_t value) {
    incoming.push_back(uint16_t(value)); incoming.push_back(uint16_t(value >> 16));
  }
  void state(unsigned count, unsigned flags = 7) {
    incoming.push_back(0x554f); incoming.push_back(uint16_t(count*32));
    push32(playback_epoch); push32(capture_epoch);
    incoming.push_back(uint16_t(flags)); incoming.push_back(0x84ff);
    for (unsigned f = 0; f < count; ++f, ++playback_sent)
      for (unsigned channel = 0; channel < 8; ++channel) push32(sample(playback_sent, channel));
  }
  void reference() {
    uint16_t count = uint16_t((reference_sequence*8) & 16383);
    incoming.push_back(0x5549); incoming.push_back(20); incoming.push_back(0x0801);
    incoming.push_back(count); push32(++reference_sequence); push32(count);
    incoming.push_back(reference_sequence == 1 ? 1 : 0); incoming.push_back(0x84ff);
  }
  void score_status() {
    status[status_word++] = dut.status_data_o;
    check(bool(dut.status_last_o) == (status_word == 10), "STATUS_TWENTY_BYTES");
    if (status_word != 10) return;
    status_word = 0;
    check(status[0] == 0x5541 && status[7] == 0x84ff, "STATUS_IDENTITY");
    check(status[4] == 48000 && status[5] == 0, "STATUS_RATE");
    if (!first_status) check(status[1] == uint16_t(previous_status_sequence+1), "STATUS_SEQUENCE");
    first_status = false; previous_status_sequence = status[1];
    last_status_epoch = uint32_t(status[8]) | uint32_t(status[9]) << 16;
    check((status[6] & 0xfff0U) == 0, "STATUS_RESERVED");
    if (status[6] & 1) check((uint32_t(status[2]) | uint32_t(status[3]) << 16) >= 0x5fff0,
                           "STATUS_MEASURED_FEEDBACK");
  }
  void score_capture() {
    check(last_status_epoch == capture_epoch, "CAPTURE_ACK_BEFORE_DATA");
    unsigned channel = (capture_word/2)%8;
    if (!(capture_word & 1)) capture_low = dut.capture_data_o;
    else {
      uint32_t value = uint32_t(capture_low) | uint32_t(dut.capture_data_o) << 16;
      if (!capture_started && channel == 0) {
        // Multiplication by this odd constant is invertible modulo 2^32.
        uint32_t inverse = 1;
        for (int n = 0; n < 5; ++n) inverse *= 2U-0x1020305U*inverse;
        capture_first = (value ^ 0x89abcdefU)*inverse;
        capture_started = true;
      }
      check(value == sample(capture_first+capture_seen, channel), "CAPTURE_ALL_BITS_ORDER");
      if (channel == 7) ++capture_seen;
    }
    ++capture_word; ++packet_words;
    if (dut.capture_last_o) {
      check(packet_words > 0 && packet_words <= 112 && packet_words%16 == 0, "CAPTURE_WHOLE_INTERVAL");
      packet_words = 0;
    }
  }
  void cycle() {
    ++steps;
    bool axis_rise = steps%2 == 0;
    bool bus_rise = steps%4 == 0;
    dut.media_clk_i = axis_rise;
    dut.bus_clk_i = steps%4 < 2;
    oscillator_phase += 24576000ULL*2*5;
    bool oscillator_rise = false;
    if (oscillator_phase >= 1000000000ULL) {
      oscillator_phase -= 1000000000ULL;
      dut.oscillator_clk_i = !dut.oscillator_clk_i;
      oscillator_rise = dut.oscillator_clk_i;
    }
    if (oscillator_rise && ++oscillator_cycles%512 == 0) {
      ++frames; render_phase = 1;
    }
    // Drive and score before the active edges; eval settles inputs first.
    dut.media_clk_i = 0;
    if (bus_rise) dut.bus_clk_i = 0;
    if (axis_rise) {
      dut.media_tick_i = render_phase == 1;
      dut.media_ns_i = uint32_t(frames*62500/3);
      dut.render_valid_i = render_phase >= 2 && render_phase <= 5;
      unsigned pair = render_phase >= 2 ? render_phase-2 : 0;
      dut.render_stream_i = 0;
      dut.render_data_i = uint64_t(swap_bytes(sample(uint32_t(frames), pair*2)))
          | uint64_t(swap_bytes(sample(uint32_t(frames), pair*2+1))) << 32;
      dut.render_last_i = render_phase == 5;
      dut.render_tick_i = render_phase == 6;
    }
    if (bus_rise) {
      ++bus_cycles;
      if (!dut.reset_i && bus_cycles >= next_reference && incoming.empty()) {
        reference(); next_reference += 50000;
      }
      if (streaming && bus_cycles >= next_pcm && incoming.empty()) {
        state(6); next_pcm += 6250;
      }
      dut.rx_valid_i = !incoming.empty() && bus_cycles%5 == 0;
      dut.rx_data_i = incoming.empty() ? 0 : incoming.front();
      dut.capture_ready_i = bus_cycles%3 != 0;
      dut.status_ready_i = bus_cycles%5 != 1;
    }
    dut.eval();
    if (axis_rise && !dut.reset_i && dut.pair_valid_o) {
      if (!playback_started && dut.pair_l_o != 0) playback_started = true;
      check(dut.pair_slot_o == playback_pair, "PLAYBACK_CHANNEL_PHASE");
      check(dut.pair_l_o == (playback_started ? sample(playback_seen, playback_pair*2) : 0), "PLAYBACK_LEFT_BITS");
      check(dut.pair_r_o == (playback_started ? sample(playback_seen, playback_pair*2+1) : 0), "PLAYBACK_RIGHT_BITS");
      if (++playback_pair == 4) { playback_pair = 0; if (playback_started) ++playback_seen; }
    }
    if (bus_rise && !dut.reset_i) {
      if (dut.rx_valid_i && dut.rx_ready_o) incoming.pop_front();
      if (dut.status_valid_o && dut.status_ready_i) score_status();
      if (dut.capture_valid_o && dut.capture_ready_i) score_capture();
    }
    if (axis_rise) {
      dut.media_clk_i = 1;
      if (render_phase) { if (++render_phase == 7) render_phase = 0; }
    }
    if (bus_rise) dut.bus_clk_i = 1;
    dut.eval();
  }
  void run(uint64_t bus_count) {
    uint64_t end = bus_cycles+bus_count;
    while (bus_cycles < end) cycle();
  }
};

static int run(uint32_t target) {
  Bench b;
  b.dut.reset_i = 1; b.dut.media_locked_i = 0; b.dut.latency_qualified_i = 0;
  b.run(100); b.dut.reset_i = 0; b.dut.media_locked_i = 1;
  b.run((uint64_t(1U << (WINDOW_LOG2_TB-3))+16)*50000);
  b.check(!b.dut.locked_o, "PHYSICAL_QUALIFICATION_REQUIRED");
  b.dut.latency_qualified_i = 1; b.run(10);
  b.check(b.dut.locked_o, "COMPLETE_WINDOW_REQUIRED");
  b.check(b.dut.feedback_q16_o >= 0x5fff0 && b.dut.feedback_q16_o <= 0x60010, "FEEDBACK_MEASURED_RATE");
  while (!b.incoming.empty()) b.cycle();
  b.state(0); b.state(7); b.state(7); b.state(7); b.state(3);
  b.streaming = true; b.stream_start = b.bus_cycles; b.next_pcm = b.bus_cycles+6250;
  while (b.playback_seen < target) b.cycle();
  b.check(b.capture_seen > target-100, "CAPTURE_LONG_RUN_COUNT");
  b.check(!b.dut.error_o && b.dut.playback_drops_o == 0 && b.dut.playback_gaps_o == 0
        && b.dut.capture_drops_o == 0, "DUPLEX_ZERO_GAPS_DROPS");
  std::printf("PASS duplex: %u playback frames, %u capture frames, all eight channels and all 32 bits\n",
              b.playback_seen, b.capture_seen);
  std::printf("PASS qualified feedback: %08x, reference losses %u\n", b.dut.feedback_q16_o, b.dut.reference_losses_o);
  b.dut.media_locked_i = 0; b.run(20);
  b.check(!b.dut.locked_o && b.dut.feedback_q16_o == 0, "CLOCK_LOSS_NO_NOMINAL");
  std::puts("PASS clock loss clears feedback");
  return b.checks.report();
}

int main(int argc, char **argv) {
  try {
    return run(argc > 1 ? unsigned(std::strtoul(argv[1], nullptr, 10)) : 100000);
  } catch (const std::runtime_error &error) {
    std::fprintf(stderr, "CHECK %s\n", error.what());
    return 1;
  }
}
