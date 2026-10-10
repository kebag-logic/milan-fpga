// Reviewer probe (R558-6): the first Begin! offset and first probe interval of
// KL_maap for pairs of stations under identical reset/enable timing and equal
// local clock, differing only in the station MAC. Prints offset_o after the
// first enable, the claimed block's overlap, and the first PROBE-to-PROBE
// interval. Build: verilator --cc --exe --build -GCLK_FREQ_HZ_P=10000
//   --top-module KL_maap KL_maap.sv first_draw_probe.cpp
#include "VKL_maap.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

namespace {
struct Result { unsigned offset; long interval; };

Result run(uint64_t mac, uint32_t clock) {
    VKL_maap dut;
    long now = 0;
    auto cyc = [&]() { dut.clk_i = 0; dut.eval(); dut.clk_i = 1; dut.eval(); ++now; };
    dut.enable_i = 0; dut.port_operational_i = 1; dut.count_i = 8;
    dut.realtime_ns_i = clock; dut.station_mac_i = mac;
    dut.seed_offset_i = 0; dut.seed_valid_i = 0;
    dut.m_axis_tready = 1; dut.rx_tvalid_i = 0; dut.rx_tready_i = 1;
    dut.rx_tdata_i = 0; dut.rx_tkeep_i = 0; dut.rx_tlast_i = 0;
    dut.rst_n = 0; for (int i = 0; i < 6; ++i) cyc();
    dut.rst_n = 1; for (int i = 0; i < 100; ++i) cyc();
    dut.enable_i = 1; cyc(); cyc();
    Result r{dut.offset_o, -1};
    long starts[2] = {-1, -1}; int seen = 0; bool prev = false;
    for (long i = 0; i < 20000 && seen < 2; ++i) {
        const bool start = dut.m_axis_tvalid && !prev;
        prev = dut.m_axis_tvalid && !(dut.m_axis_tlast && dut.m_axis_tready);
        if (start) starts[seen++] = now;
        cyc();
    }
    if (seen == 2) r.interval = starts[1] - starts[0];
    return r;
}

void pair(const char* what, uint64_t a, uint64_t b, uint32_t clock) {
    const Result ra = run(a, clock), rb = run(b, clock);
    const long d = static_cast<long>(ra.offset) - static_cast<long>(rb.offset);
    const bool overlap = (d < 0 ? -d : d) < 8;
    std::printf("%-34s mac %012llx -> offset 0x%04x, first interval %ld | mac %012llx -> offset 0x%04x, "
                "first interval %ld | 8-address blocks %s\n",
                what, static_cast<unsigned long long>(a), ra.offset, ra.interval,
                static_cast<unsigned long long>(b), rb.offset, rb.interval,
                ra.offset == rb.offset ? "IDENTICAL" : overlap ? "OVERLAP" : "disjoint");
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    pair("adjacent MACs, clock 0", 0x020000000001ULL, 0x020000000002ULL, 0);
    pair("MACs differ in bit 16 only, clock 0", 0x020000000001ULL, 0x020000010001ULL, 0);
    pair("MACs differ in octet 4 only, clock 7", 0x0200000a1234ULL, 0x0200005b1234ULL, 7);
    pair("MACs differ in octet 3 only, clock 0", 0x020011001234ULL, 0x020022001234ULL, 0);
    return 0;
}
