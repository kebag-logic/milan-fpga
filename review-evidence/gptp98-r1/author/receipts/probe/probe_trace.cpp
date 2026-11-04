// Differential cycle trace of KL_gptp_rx_parser (scratch probe, #98).
// Feeds a fixed corpus back to back with two idle cycles between frames
// and prints every cycle that writes the bank, raises an event or moves
// the drop count, so base and head RTL traces can be diffed line by line.
#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "VKL_gptp_rx_parser.h"

namespace {
struct Frame {
  std::vector<uint8_t> b;
  void u8(uint8_t v) { b.push_back(v); }
  void u16(uint16_t v) { u8(v >> 8); u8(v & 0xFF); }
  void u32(uint32_t v) { u16(v >> 16); u16(v & 0xFFFF); }
  void u48(uint64_t v) { u16((v >> 32) & 0xFFFF); u32(v & 0xFFFFFFFF); }
  void u64(uint64_t v) { u32(v >> 32); u32(v & 0xFFFFFFFF); }
  void len() { uint16_t n = static_cast<uint16_t>(b.size() - 14); b[16] = n >> 8; b[17] = n & 0xFF; }
};
Frame hdr(uint8_t mt, uint16_t seq) {
  Frame f;
  for (int i = 0; i < 6; i++) f.u8(0x01);
  for (int i = 0; i < 6; i++) f.u8(0x22);
  f.u16(0x88F7); f.u8(0x10 | mt); f.u8(2); f.u16(0); f.u8(0); f.u8(0);
  f.u16(0x0008); f.u64(0x0000001234560000ull); f.u32(0);
  f.u64(0xAABBCCFFFE001122ull); f.u16(1); f.u16(seq); f.u8(5); f.u8(0xFD);
  return f;
}
void info(Frame &f) {
  f.u16(3); f.u16(28); f.u8(0); f.u8(0x80); f.u8(0xC2); f.u8(0); f.u8(0); f.u8(1);
  f.u32(0xFFFFF000); f.u16(7); for (int i = 0; i < 12; i++) f.u8(0); f.u32(0x123);
}
}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  VKL_gptp_rx_parser d;
  uint64_t cyc = 0;
  auto tick = [&]() {
    d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); cyc++;
    static uint16_t drops = 0;
    if (d.bank_we_o || d.ev_valid_o || d.drop_cnt_o != drops)
      printf("%6llu we=%d a=%2u d=%016llx ev=%d code=%u seq=%04x drops=%u\n",
             static_cast<unsigned long long>(cyc), d.bank_we_o, d.bank_addr_o,
             static_cast<unsigned long long>(d.bank_wdata_o), d.ev_valid_o, d.ev_code_o,
             d.ev_seq_o, d.drop_cnt_o);
    drops = d.drop_cnt_o;
  };
  d.rst_n = 0; d.local_clock_id_i = 0x02A1B2FFFEC3D4E5ull; d.local_clock_valid_i = 1;
  for (int i = 0; i < 4; i++) tick();
  d.rst_n = 1; tick(); tick();
  std::vector<std::pair<const char *, Frame>> corpus;
  { Frame f = hdr(8, 1); f.u48(0x12345678); f.u32(0x2FAF0800); info(f); f.len(); corpus.push_back({"plain Follow_Up", f}); }
  { Frame f = hdr(8, 2); f.u48(0x12345678); f.u32(0x2FAF0800); info(f); f.u16(8); f.u16(8); f.u64(0x3333333333333333ull); f.len(); corpus.push_back({"Follow_Up + trailing TLV", f}); }
  { Frame f = hdr(8, 3); f.u48(0x12345678); f.u32(0x2FAF0800); info(f); f.len(); for (int i = 0; i < 10; i++) f.u8(0); corpus.push_back({"Follow_Up + 10 padding", f}); }
  { Frame f = hdr(0, 4); f.u48(0x12345678); f.u32(0x1DCD6500); f.len(); f.u8(0); f.u8(0); corpus.push_back({"Sync padded to 60", f}); }
  { Frame f = hdr(3, 5); f.u48(0xABCD); f.u32(0x075BCD15); f.u64(0xDEADBEEFCAFEF00Dull); f.u16(1); f.len(); corpus.push_back({"Pdelay_Resp", f}); }
  { Frame f = hdr(0xA, 6); f.u48(0xABCD); f.u32(0x075BCD15); f.u64(0xDEADBEEFCAFEF00Dull); f.u16(1); f.len(); corpus.push_back({"Pdelay_Resp_Follow_Up", f}); }
  { Frame f = hdr(2, 7); for (int i = 0; i < 20; i++) f.u8(0); f.len(); corpus.push_back({"Pdelay_Req", f}); }
  { Frame f = hdr(0xB, 8); for (int i = 0; i < 10; i++) f.u8(0); f.u16(0xFFC4); f.u8(0); f.u8(248); f.u32(0xF8FE436A); f.u8(248);
    f.u64(0x00220FFFFE334455ull); f.u16(1); f.u8(0xA0); f.u16(8); f.u16(16); f.u64(0x00220FFFFE334455ull); f.u64(0x2222222222222222ull); f.len();
    corpus.push_back({"Announce, two-hop path", f}); }
  { Frame f = hdr(8, 9); f.u48(0x12345678); f.u32(0x2FAF0800); f.u16(3); f.u16(8); f.u32(0x123456AB); f.u32(0xCDEF55AA); info(f); f.len(); corpus.push_back({"Follow_Up, unknown TLV first", f}); }
  { Frame f = hdr(8, 10); f.u48(0x12345678); f.u32(0x2FAF0800); f.u16(8); f.u16(28); f.u8(0); f.u8(0x80); f.u8(0xC2); f.u8(0); f.u8(0); f.u8(1);
    for (int i = 0; i < 22; i++) f.u8(0); f.len(); corpus.push_back({"Follow_Up, tlvType 8", f}); }
  for (auto &[name, f] : corpus) {
    printf("-- %s (%zu bytes) starts at cycle %llu\n", name, f.b.size(), static_cast<unsigned long long>(cyc + 1));
    for (size_t i = 0; i < f.b.size(); i++) {
      d.rx_valid_i = 1; d.rx_data_i = f.b[i]; d.rx_sof_i = (i == 0); d.rx_eof_i = (i + 1 == f.b.size()); d.rx_err_i = 0;
      tick();
    }
    d.rx_valid_i = 0; d.rx_sof_i = 0; d.rx_eof_i = 0;
    for (int i = 0; i < 2; i++) tick();
  }
  for (int i = 0; i < 4; i++) tick();
  return 0;
}
