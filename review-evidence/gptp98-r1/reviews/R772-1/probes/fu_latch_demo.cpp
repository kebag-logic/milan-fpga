// Reviewer probe: two Follow_Ups whose malformed TLV header sits ahead of a
// well-formed information TLV, so a walk that forgets the refusal would
// re-synchronise on the information TLV and accept. 802.1AS-2011 11.4.2.2 /
// IEEE 1588-2008 5.3.8 and the issue's acceptance item 2 make both refusals.
//   A: {tlvType 0x000A, lengthField 0x0100} (value past messageLength), then
//      the information TLV, messageLength = every octet carried (80)
//   B: {tlvType 0x000A, lengthField 0x0001} (odd), then the information TLV
// Expected on correct RTL: no event and one drop each. Prints one line each.
#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "VKL_gptp_rx_parser.h"

static VKL_gptp_rx_parser *dut;
static int ev = 0;
static void tick() {
  dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
  if (dut->ev_valid_o) ev++;
}
static void p16(std::vector<uint8_t> &v, unsigned x) { v.push_back(x >> 8); v.push_back(x & 0xFF); }

static std::vector<uint8_t> frame(unsigned bad_len) {
  std::vector<uint8_t> f;
  for (int i = 0; i < 6; i++) f.push_back(0x01);
  for (int i = 0; i < 6; i++) f.push_back(0x22);
  p16(f, 0x88F7); f.push_back(0x18); f.push_back(0x02); p16(f, 0);
  f.push_back(0); f.push_back(0); p16(f, 0);
  for (int i = 0; i < 12; i++) f.push_back(0);
  for (int i = 0; i < 8; i++) f.push_back(0xAA);
  p16(f, 1); p16(f, 0x9898); f.push_back(2); f.push_back(0xFD);
  for (int i = 0; i < 10; i++) f.push_back(0x10 + i);
  p16(f, 0x000A); p16(f, bad_len);                       // malformed header
  p16(f, 0x0003); p16(f, 28);                             // information TLV
  const uint8_t v[] = {0x00, 0x80, 0xC2, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x07};
  for (uint8_t b : v) f.push_back(b);
  while (f.size() < 14 + 44 + 4 + 32) f.push_back(0);
  const unsigned L = unsigned(f.size()) - 14;
  f[16] = uint8_t(L >> 8); f[17] = uint8_t(L);
  return f;
}

static void feed(const char *tag, const std::vector<uint8_t> &f) {
  ev = 0;
  const unsigned d0 = dut->drop_cnt_o;
  for (size_t i = 0; i < f.size(); i++) {
    dut->rx_valid_i = 1; dut->rx_data_i = f[i];
    dut->rx_sof_i = (i == 0); dut->rx_eof_i = (i + 1 == f.size()); dut->rx_err_i = 0;
    tick();
  }
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
  for (int i = 0; i < 3; i++) tick();
  const unsigned drops = uint16_t(dut->drop_cnt_o - d0);
  printf("%s: messageLength %zu, events %d, drops %u -> %s\n", tag, f.size() - 14, ev, drops,
         (ev == 0 && drops == 1) ? "refused (expected)" : "ACCEPTED (defect)");
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_gptp_rx_parser;
  dut->local_clock_valid_i = 1;
  dut->rst_n = 0; for (int i = 0; i < 4; i++) tick();
  dut->rst_n = 1; for (int i = 0; i < 2; i++) tick();
  feed("A overrunning TLV ahead of the information TLV", frame(0x0100));
  feed("B odd-length TLV ahead of the information TLV", frame(0x0001));
  delete dut;
  return 0;
}
