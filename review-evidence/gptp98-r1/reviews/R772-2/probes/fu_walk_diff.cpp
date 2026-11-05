// Reviewer probe (independent of the repository harness): random Follow_Up
// TLV chains fed byte-serially into KL_gptp_rx_parser, each verdict compared
// with a reference model written from IEEE 802.1AS-2011 11.4.1, 11.4.2.2,
// 11.4.4.3 / Table 11-10 and IEEE 1588-2008 5.3.8 / 14.1:
//   - messageLength L counts header (34) + body (10) + every TLV octet;
//     L < 76 (Table 11-9) or a frame shorter than L+14 octets is refused;
//   - the chain is walked from octet 44 to L; fewer than 4 octets left is a
//     cut header (refused); an odd lengthField is refused; a value that runs
//     past L is refused; any other TLV is skipped by its lengthField;
//   - the first TLV with tlvType 3, lengthField 28, organizationId 00-80-C2,
//     organizationSubType 1 is the information TLV; word 11 is
//     {csro, gmTimeBaseIndicator, 16'd0} from its octets 10..15;
//   - accept iff the walk completes and found the information TLV;
//   - octets past L (physical padding) are never walked.
// Also checked: one drop per refusal, no event on refusal, w4/w5/w11 on
// acceptance, no w11 write before a refusal that precedes any info TLV, and a
// constant EOF-to-event latency.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <random>
#include <string>
#include <vector>
#include <verilated.h>
#include "VKL_gptp_rx_parser.h"

static VKL_gptp_rx_parser *dut;
static std::map<uint32_t, uint64_t> bank;
static int ev_n = 0, ev_code = 0, ev_seq = 0;
static long cyc = 0, ev_cyc = -1;
static int w11_writes = 0;

static void tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  cyc++;
  if (dut->bank_we_o) {
    bank[dut->bank_addr_o] = dut->bank_wdata_o;
    if (dut->bank_addr_o == 11) w11_writes++;
  }
  if (dut->ev_valid_o) { ev_n++; ev_code = dut->ev_code_o; ev_seq = dut->ev_seq_o; ev_cyc = cyc; }
}

struct Model { bool accept; uint64_t w11; const char *why; bool info_first; int ntlv_before; };

static Model model(const std::vector<uint8_t> &f) {
  Model m{false, 0, "", false, 0};
  const size_t N = f.size();
  const unsigned L = (f[16] << 8) | f[17];
  if (L < 76) { m.why = "short-L"; return m; }
  if (L > 1500) { m.why = "long-L"; return m; }
  if (N < L + 14) { m.why = "truncated"; return m; }
  const size_t end = 14 + L;            // one past the last declared octet
  size_t p = 58;
  bool found = false;
  int idx = 0;
  while (p < end) {
    if (end - p < 4) { m.why = "cut-header"; return m; }
    unsigned t = (f[p] << 8) | f[p + 1];
    unsigned l = (f[p + 2] << 8) | f[p + 3];
    if (l & 1) { m.why = "odd-length"; return m; }
    if (p + 4 + l > end) { m.why = "past-L"; return m; }
    if (!found && t == 3 && l == 28 && f[p + 4] == 0x00 && f[p + 5] == 0x80 &&
        f[p + 6] == 0xC2 && f[p + 7] == 0 && f[p + 8] == 0 && f[p + 9] == 1) {
      found = true;
      uint64_t w = 0;
      for (int k = 10; k < 16; k++) w = (w << 8) | f[p + k];
      m.w11 = w << 16;
      m.info_first = (idx == 0);
      m.ntlv_before = idx;
    }
    idx++;
    p += 4 + l;
  }
  if (!found) { m.why = "no-info"; return m; }
  m.accept = true; m.why = "accept";
  return m;
}

static std::mt19937_64 rng(0x98987772ull);
static unsigned rnd(unsigned n) { return static_cast<unsigned>(rng() % n); }

static void put16(std::vector<uint8_t> &v, unsigned x) { v.push_back(x >> 8); v.push_back(x & 0xFF); }

static void info(std::vector<uint8_t> &c, unsigned type, unsigned len, unsigned oui,
                 unsigned sub, uint32_t csro, uint16_t tbi) {
  put16(c, type); put16(c, len);
  std::vector<uint8_t> v = {uint8_t(oui >> 16), uint8_t(oui >> 8), uint8_t(oui),
                            uint8_t(sub >> 16), uint8_t(sub >> 8), uint8_t(sub)};
  for (int s = 24; s >= 0; s -= 8) v.push_back(uint8_t(csro >> s));
  v.push_back(tbi >> 8); v.push_back(tbi & 0xFF);
  while (v.size() < len) v.push_back(uint8_t(rnd(256)));
  v.resize(len);
  c.insert(c.end(), v.begin(), v.end());
}

static std::vector<uint8_t> gen(uint16_t seq) {
  std::vector<uint8_t> f;
  for (int i = 0; i < 6; i++) f.push_back(0x01);
  for (int i = 0; i < 6; i++) f.push_back(0x22);
  put16(f, 0x88F7);
  f.push_back(0x18); f.push_back(0x02);
  put16(f, 0);                                   // messageLength, set below
  f.push_back(0); f.push_back(0); put16(f, 0x0208);
  for (int i = 0; i < 8; i++) f.push_back(uint8_t(i));
  for (int i = 0; i < 4; i++) f.push_back(0);
  for (int i = 0; i < 8; i++) f.push_back(uint8_t(0xA0 + i));
  put16(f, 1); put16(f, seq); f.push_back(0x02); f.push_back(0xFD);
  for (int i = 0; i < 10; i++) f.push_back(uint8_t(0x50 + i));
  std::vector<uint8_t> c;
  const unsigned n = rnd(6);
  for (unsigned k = 0; k < n; k++) {
    const uint32_t csro = uint32_t(rng());
    const uint16_t tbi = uint16_t(rng());
    switch (rnd(12)) {
      case 0: case 1: case 2: info(c, 3, 28, 0x0080C2, 1, csro, tbi); break;
      case 3: info(c, 3, 28, 0x0080C2, 1 + 1 + rnd(3), csro, tbi); break;
      case 4: info(c, 3, 28, rnd(2) ? 0x001B19 : 0x0080C3, 1, csro, tbi); break;
      case 5: info(c, 3, 26 + 2 * rnd(4) + (rnd(2) ? 0 : 6), 0x0080C2, 1, csro, tbi); break;
      case 6: info(c, rnd(2) ? 8 : 0x8003, 28, 0x0080C2, 1, csro, tbi); break;
      case 7: { unsigned l = 2 * rnd(12); put16(c, rnd(0x10000)); put16(c, l);
                for (unsigned i = 0; i < l; i++) c.push_back(uint8_t(rnd(256))); } break;
      case 8: { put16(c, rnd(16)); put16(c, 0); } break;
      case 9: { unsigned l = 2 * rnd(8) + 1; put16(c, rnd(16)); put16(c, l);
                for (unsigned i = 0; i < l; i++) c.push_back(uint8_t(rnd(256))); } break;
      case 10: { // a near copy: 00-80-C2/1 at a shifted offset inside another TLV
                 put16(c, 3); put16(c, 30); c.push_back(0x12); c.push_back(0x34);
                 c.push_back(0x00); c.push_back(0x80); c.push_back(0xC2);
                 c.push_back(0); c.push_back(0); c.push_back(1);
                 for (int i = 0; i < 22; i++) c.push_back(uint8_t(rnd(256))); } break;
      default: { put16(c, 0x0008); put16(c, 8 * rnd(3));
                 for (unsigned i = 0; i < c[c.size() - 1]; i++) c.push_back(0x33); } break;
    }
  }
  if (rnd(6) == 0) { unsigned cut = 1 + rnd(3); for (unsigned i = 0; i < cut; i++) c.push_back(uint8_t(rnd(256))); }
  f.insert(f.end(), c.begin(), c.end());
  int L = int(f.size()) - 14;
  switch (rnd(10)) {
    case 0: L += 1 + int(rnd(8)); break;          // declared beyond the chain
    case 1: L -= 1 + int(rnd(8)); break;          // declared inside the chain
    default: break;
  }
  if (L < 0) L = 0;
  f[16] = uint8_t(L >> 8); f[17] = uint8_t(L);
  if (rnd(3) == 0) { unsigned pad = 1 + rnd(24); for (unsigned i = 0; i < pad; i++) f.push_back(uint8_t(rnd(256))); }
  if (rnd(12) == 0 && f.size() > 60) f.resize(f.size() - 1 - rnd(4));
  return f;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  const long iters = (argc > 1) ? atol(argv[1]) : 200000;
  dut = new VKL_gptp_rx_parser;
  dut->local_clock_id_i = 0x02A1B2FFFEC3D4E5ull;
  dut->local_clock_valid_i = 1;
  dut->rst_n = 0; for (int i = 0; i < 4; i++) tick();
  dut->rst_n = 1; for (int i = 0; i < 2; i++) tick();
  std::map<std::string, long> cov;
  long mism = 0, lat_bad = 0;
  long lat0 = -1;
  for (long it = 0; it < iters; it++) {
    const uint16_t seq = uint16_t(it);
    std::vector<uint8_t> f = gen(seq);
    const Model m = model(f);
    bank.clear(); ev_n = 0; w11_writes = 0; ev_cyc = -1;
    const uint16_t d0 = dut->drop_cnt_o;
    long eof_cyc = 0;
    for (size_t i = 0; i < f.size(); i++) {
      dut->rx_valid_i = 1; dut->rx_data_i = f[i];
      dut->rx_sof_i = (i == 0); dut->rx_eof_i = (i + 1 == f.size()); dut->rx_err_i = 0;
      tick();
      if (i + 1 == f.size()) eof_cyc = cyc;
    }
    dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
    for (int i = 0; i < 3; i++) tick();
    const bool acc = (ev_n == 1 && ev_code == 2 && ev_seq == seq);
    const unsigned drops = uint16_t(dut->drop_cnt_o - d0);
    bool bad = false;
    if (m.accept) {
      if (!acc || drops != 0 || !bank.count(11) || bank[11] != m.w11 ||
          bank[4] != 0x0000505152535455ull || bank[5] != 0x56575859ull) bad = true;
      if (acc) {
        const long lat = ev_cyc - eof_cyc;
        if (lat0 < 0) lat0 = lat;
        if (lat != lat0) lat_bad++;
      }
    } else {
      if (ev_n != 0 || drops != 1) bad = true;
    }
    std::string k = std::string(m.why) + (m.accept ? (m.info_first ? "/info-first" : "/info-after-unknown") : "");
    cov[k]++;
    if (bad) {
      if (mism < 10) {
        printf("MISMATCH it=%ld model=%s ev_n=%d drops=%u w11=%016llx exp=%016llx len=%zu L=%u\n  ",
               it, m.why, ev_n, drops, (unsigned long long)(bank.count(11) ? bank[11] : ~0ull),
               (unsigned long long)m.w11, f.size(), (f[16] << 8) | f[17]);
        for (size_t i = 58; i < f.size(); i++) printf("%02x", f[i]);
        printf("\n");
      }
      mism++;
    }
  }
  for (auto &kv : cov) printf("COVER %-28s %ld\n", kv.first.c_str(), kv.second);
  printf("LATENCY eof->event %ld cycles; latency deviations %ld\n", lat0, lat_bad);
  printf("RESULT iters=%ld mismatches=%ld\n", iters, mism);
  delete dut;
  return (mism || lat_bad) ? 1 : 0;
}
