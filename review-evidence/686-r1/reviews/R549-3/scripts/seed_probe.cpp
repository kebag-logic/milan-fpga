#include "VKL_maap.h"
#include "VKL_maap___024root.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

static unsigned checks = 0, failures = 0;
static void check(bool ok, const char* label) {
    ++checks;
    failures += !ok;
    std::printf("%s %s\n", ok ? "PASS" : "FAIL", label);
}
static void tick(VKL_maap& d) {
    d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval();
}
static uint16_t seed(const VKL_maap& d) {
    return d.rootp->KL_maap__DOT__lfsr_r;
}
static void reset(VKL_maap& d, uint64_t mac) {
    d.station_mac_i = mac; d.rst_n = 0; d.enable_i = 0;
    d.count_i = 8; d.seed_valid_i = 0; d.seed_offset_i = 0;
    d.rx_tvalid_i = 0; d.rx_tready_i = 1; d.rx_tlast_i = 0;
    d.rx_tdata_i = 0; d.rx_tkeep_i = 0; d.m_axis_tready = 1;
    for (unsigned i = 0; i < 4; ++i) tick(d);
}
static uint16_t next(uint16_t s) {
    return uint16_t((s << 1) | (((s >> 15) ^ (s >> 14) ^ (s >> 12) ^ (s >> 3)) & 1));
}
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    VKL_maap a, b;
    reset(a, 0); reset(b, 0);
    check(seed(a) == 0xACE1 && seed(b) == 0xACE1, "zero MAC at reset seeds both instances to ACE1");
    a.rst_n = b.rst_n = 1;
    a.station_mac_i = 0x020000000001ULL;
    b.station_mac_i = 0x020000000002ULL;
    uint16_t expected = 0xACE1;
    bool same = true;
    for (unsigned i = 0; i < 65535; ++i) {
        expected = next(expected); tick(a); tick(b);
        same &= seed(a) == expected && seed(b) == expected;
    }
    check(same, "different MAC writes after reset do not alter the shared free-running sequence");
    reset(a, 0x020000000001ULL); reset(b, 0x020000000002ULL);
    check(seed(a) == 0xACE0 && seed(b) == 0xACE3, "module samples distinct MAC values when supplied during reset");
    reset(a, 0x02000000ACE1ULL);
    check(seed(a) == 0xACE1, "MAC folding to zero takes nonzero fallback");
    a.rst_n = 1; tick(a);
    check(seed(a) == next(0xACE1) && seed(a) != 0xACE1, "fallback advances after reset");
    bool no_zero = true, only_zero_fixed = true;
    for (unsigned s = 1; s < 65536; ++s) {
        no_zero &= next(uint16_t(s)) != 0;
        only_zero_fixed &= next(uint16_t(s)) != s;
    }
    check(no_zero && next(0) == 0, "all 65535 nonzero states avoid zero in one step");
    check(only_zero_fixed, "zero is the only fixed point across all 65536 states");
    std::printf("seed probe: %u checks, %u failures\n", checks, failures);
    return failures ? 1 : 0;
}
