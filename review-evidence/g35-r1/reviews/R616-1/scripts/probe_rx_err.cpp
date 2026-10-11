// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe for FPGA-gPTP #35 (rx_err_i on any byte refuses the frame).
// Independent of the parser suite: its own frame builders and its own
// sampling. Built against any KL_gptp_rx_parser.sv (base or head).
//
// Lines:  RESULT <name> PASS|FAIL <detail>
//         INFO   <name> <detail>
// Last:   N probes: P PASS, F FAIL
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>
#include <verilated.h>
#include "VKL_gptp_rx_parser.h"

static VKL_gptp_rx_parser *dut;
static int probes = 0, fails = 0;
static int writes = 0, events = 0;
static uint8_t last_code = 0;
static uint16_t last_seq = 0;
static const uint64_t LOCAL = 0x02A1B2FFFEC3D4E5ull;

static void result(const std::string &n, bool ok, const std::string &d) {
  probes++; if (!ok) fails++;
  printf("RESULT %s %s %s\n", n.c_str(), ok ? "PASS" : "FAIL", d.c_str());
}

static void tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  if (dut->bank_we_o) writes++;
  if (dut->ev_valid_o) { events++; last_code = dut->ev_code_o; last_seq = dut->ev_seq_o; }
}

static void idle(int n) {
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0; dut->rx_err_i = 0;
  for (int i = 0; i < n; i++) tick();
}

struct B {
  std::vector<uint8_t> b;
  void u8(uint8_t v) { b.push_back(v); }
  void u16(uint16_t v) { u8(v >> 8); u8(v); }
  void u32(uint32_t v) { u16(v >> 16); u16(v); }
  void u48(uint64_t v) { u16(v >> 32); u32(v); }
  void u64(uint64_t v) { u32(v >> 32); u32(v); }
};

// Ethernet II + 34-octet PTP header, messageLength = 34 + body
static B hdr(uint8_t mt, uint16_t seq, uint16_t body) {
  B f;
  for (int i = 0; i < 6; i++) f.u8(0x01);
  for (int i = 0; i < 6; i++) f.u8(0x22);
  f.u16(0x88F7);
  f.u8(0x10 | mt); f.u8(0x02); f.u16(34 + body);
  f.u8(0); f.u8(0); f.u16(0x0200); f.u64(0); f.u32(0);
  f.u64(0x00AABBFFFECCDDEEull); f.u16(1); f.u16(seq); f.u8(0); f.u8(0xFD);
  return f;
}
static B sync_f() { B f = hdr(0x0, 0x7100, 10); f.u48(0x1234); f.u32(0x100); return f; }
static B fu_f() {
  B f = hdr(0x8, 0x7108, 42); f.u48(0x1234); f.u32(0x200);
  f.u16(0x0003); f.u16(28); f.u8(0x00); f.u8(0x80); f.u8(0xC2);
  f.u8(0); f.u8(0); f.u8(1);
  for (int i = 0; i < 4 + 2 + 12 + 4; i++) f.u8(0);
  return f;
}
static B pdreq_f() { B f = hdr(0x2, 0x7102, 20); for (int i = 0; i < 20; i++) f.u8(0); return f; }
static B pdresp_f(uint8_t mt, uint16_t seq) {
  B f = hdr(mt, seq, 20); f.u48(0x55); f.u32(0x66); f.u64(0x0011FFFE2233ull); f.u16(1);
  return f;
}
static B sig_f() { return hdr(0xC, 0x710C, 0); }
static B ann_f(bool path) {
  const uint64_t gm = 0x001122FFFE334455ull;
  B f = hdr(0xB, 0x710B, path ? 30 + 12 : 30);
  for (int i = 0; i < 10; i++) f.u8(0);
  f.u16(37); f.u8(0); f.u8(248); f.u32(0xF8FE436A); f.u8(248);
  f.u64(gm); f.u16(0); f.u8(0xA0);
  if (path) { f.u16(0x0008); f.u16(8); f.u64(gm); }
  return f;
}
static B padded_sync() { B f = sync_f(); f.u8(0); f.u8(0); return f; }

// stream one frame; err raised on bytes [from,to] (from > to: none).
// own = writes sampled after the first flagged byte's own edge.
struct Out { int drops, ev, after, own; uint8_t code; };
static Out feed(const B &f, size_t from, size_t to, bool idle_after = true) {
  uint16_t d0 = dut->drop_cnt_o; int w0 = writes, e0 = events, wflag = -1, wpre = 0;
  for (size_t i = 0; i < f.b.size(); i++) {
    dut->rx_valid_i = 1; dut->rx_data_i = f.b[i];
    dut->rx_sof_i = i == 0; dut->rx_eof_i = i + 1 == f.b.size();
    dut->rx_err_i = (i >= from && i <= to);
    if (i == from) wpre = writes;
    tick();
    if (i == from) wflag = writes;
  }
  if (idle_after) idle(4);
  Out o;
  o.drops = (uint16_t)(dut->drop_cnt_o - d0); o.ev = events - e0; o.code = last_code;
  o.after = wflag < 0 ? 0 : writes - wflag;
  o.own = wflag < 0 ? 0 : wflag - wpre;
  (void)w0;
  return o;
}

static void sweep(const char *tag, const B &f, uint8_t code) {
  const size_t n = f.b.size();
  size_t bad = 0, own_writes = 0; std::string miss;
  for (size_t p = 0; p < n; p++) {
    Out o = feed(f, p, p);
    if (o.drops != 1 || o.ev != 0 || o.after != 0) {
      bad++;
      if (miss.size() < 120) miss += " " + std::to_string(p) + ":d" + std::to_string(o.drops) +
                                     "e" + std::to_string(o.ev) + "w" + std::to_string(o.after);
    }
    own_writes += o.own;
  }
  result(std::string(tag) + "_every_byte", bad == 0,
         std::to_string(n) + " positions, " + std::to_string(bad) + " not refused cleanly" + miss);
  printf("INFO %s_flagged_edge_writes %zu of %zu positions issue a bank write on the flagged byte's own edge\n",
         tag, own_writes, n);
  Out h = feed(f, 0, n - 1);
  result(std::string(tag) + "_every_byte_flagged", h.drops == 1 && h.ev == 0,
         "drops " + std::to_string(h.drops) + " events " + std::to_string(h.ev));
  Out c = feed(f, 1, 0);
  result(std::string(tag) + "_clean_control", c.drops == 0 && c.ev == 1 && c.code == code,
         "drops " + std::to_string(c.drops) + " events " + std::to_string(c.ev) + " code " + std::to_string(c.code));
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_gptp_rx_parser;
  dut->local_clock_id_i = LOCAL; dut->local_clock_valid_i = 1;
  dut->rst_n = 0; idle(4); dut->rst_n = 1; idle(2);

  sweep("sync", sync_f(), 1);
  sweep("followup", fu_f(), 2);
  sweep("pdreq", pdreq_f(), 4);
  sweep("pdresp", pdresp_f(0x3, 0x7103), 5);
  sweep("pdrfu", pdresp_f(0xA, 0x710A), 6);
  sweep("signaling", sig_f(), 7);
  sweep("announce_nopath", ann_f(false), 3);
  sweep("announce_path1", ann_f(true), 3);
  sweep("sync_padded", padded_sync(), 1);

  // zero-gap neighbours: flagged frame then clean frame, no idle between
  const B s = sync_f(), q = pdreq_f();
  for (size_t k : {size_t(0), size_t(20), s.b.size() - 1}) {
    uint16_t d0 = dut->drop_cnt_o; int e0 = events;
    feed(s, k, k, false); feed(q, 1, 0, true);
    int d = (uint16_t)(dut->drop_cnt_o - d0), e = events - e0;
    result("zero_gap_flagged_then_clean_k" + std::to_string(k), d == 1 && e == 1 && last_code == 4,
           "drops " + std::to_string(d) + " events " + std::to_string(e) + " last code " + std::to_string(last_code));
  }
  // clean frame then a successor flagged on its first byte, no idle between:
  // the predecessor's deferred end-of-frame settles while the successor's
  // flagged sof is clocked
  for (size_t k : {size_t(0), size_t(1)}) {
    uint16_t d0 = dut->drop_cnt_o; int e0 = events;
    feed(q, 1, 0, false); feed(s, k, k, true);
    int d = (uint16_t)(dut->drop_cnt_o - d0), e = events - e0;
    result("zero_gap_clean_then_flagged_k" + std::to_string(k), d == 1 && e == 1 && last_code == 4,
           "drops " + std::to_string(d) + " events " + std::to_string(e) + " last code " + std::to_string(last_code));
  }
  // a valid byte outside any frame (no sof, after eof) carrying the flag
  {
    uint16_t d0 = dut->drop_cnt_o; int e0 = events;
    dut->rx_valid_i = 1; dut->rx_data_i = 0x5A; dut->rx_sof_i = 0; dut->rx_eof_i = 0; dut->rx_err_i = 1;
    tick(); idle(2);
    feed(s, 1, 0, true);
    int d = (uint16_t)(dut->drop_cnt_o - d0), e = events - e0;
    result("stray_flagged_byte_then_clean", d == 0 && e == 1 && last_code == 1,
           "drops " + std::to_string(d) + " events " + std::to_string(e));
  }
  // a one-byte frame (sof and eof together) carrying the flag: one drop
  {
    uint16_t d0 = dut->drop_cnt_o; int e0 = events;
    dut->rx_valid_i = 1; dut->rx_data_i = 0x01; dut->rx_sof_i = 1; dut->rx_eof_i = 1; dut->rx_err_i = 1;
    tick(); idle(4);
    int d = (uint16_t)(dut->drop_cnt_o - d0), e = events - e0;
    result("one_byte_frame_flagged", d == 1 && e == 0,
           "drops " + std::to_string(d) + " events " + std::to_string(e));
    feed(s, 1, 0, true);
    result("one_byte_frame_flagged_then_clean", events - e0 == 1 && last_code == 1,
           "events " + std::to_string(events - e0));
  }
  // flag held across an idle gap inside a frame and released before eof
  {
    uint16_t d0 = dut->drop_cnt_o; int e0 = events;
    for (size_t i = 0; i < s.b.size(); i++) {
      dut->rx_valid_i = 1; dut->rx_data_i = s.b[i];
      dut->rx_sof_i = i == 0; dut->rx_eof_i = i + 1 == s.b.size();
      dut->rx_err_i = (i == 30); tick();
      if (i == 30) { dut->rx_valid_i = 0; dut->rx_err_i = 1; tick(); tick(); }
    }
    idle(4);
    int d = (uint16_t)(dut->drop_cnt_o - d0), e = events - e0;
    result("flag_on_byte_then_idle_gap", d == 1 && e == 0,
           "drops " + std::to_string(d) + " events " + std::to_string(e));
  }
  printf("%d probes: %d PASS, %d FAIL\n", probes, probes - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}
