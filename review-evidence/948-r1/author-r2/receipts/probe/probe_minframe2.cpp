// probe_minframe2.cpp (scratch, not a repository test): the shortest frame whose PDU the receive stack delivers,
// through avtp_rxmon_nx_wrap's parser, monitor and depacketizer, using only ports every revision of the wrap has
// (15168e14, 4ceba3d4, the head): input 0 bound through its ACMP alias, its format in fmt0_i; "accepted" counts
// pdu_accept_p_o, "delivered" counts the depacketizer's emitted-PDU total (pcm_pdus_o). Each length is sent three
// times with a gap, untagged and behind a C-VLAN tag; the payload is one INT_16BIT channel of n/2 samples (n octets),
// and the Milan v1.2 1-channel 48 kHz Base format (INT_32BIT, six samples, 24 octets) is sent as itself.
#include <cstdint>
#include <cstdio>
#include <memory>
#include <vector>

#include "Vavtp_rxmon_nx_wrap.h"
#include "verilated.h"

namespace {
constexpr uint64_t kTalker = 0x0202DEADBEEF0001ull;

class Probe {
 public:
    int run() {
        d->bound0_i = 0; d->sid0_i = kTalker; d->fmt0_i = 0;
        d->tbl_wr_en_i = 0; d->lctx_wr_en_i = 0; d->lctx_rd_en_i = 0; d->route_wr_en_i = 0;
        d->ptp_now_i = 0xA55AC33CUL - 1000000; d->pres_ofs_i = 2000000; d->clk_src_i = 0; d->servo_conv_i = 0;
        d->s_tvalid_i = 0; d->resetn = 0;
        cyc(6); d->resetn = 1; cyc(4);
        for (bool vlan : {false, true}) {
            for (unsigned n = 2; n <= 80; n += 2) one(vlan, 0x04, 16, n / 2, n);
            one(vlan, 0x02, 32, 6, 24);   // Milan v1.2 Table 6.1, 1 channel at 48 kHz
        }
        return 0;
    }

 private:
    std::unique_ptr<Vavtp_rxmon_nx_wrap> d = std::make_unique<Vavtp_rxmon_nx_wrap>();
    long accepts = 0;
    uint8_t seq = 0;
    void cyc(int k = 1) {
        for (int i = 0; i < k; i++) {
            d->clk = 0; d->eval(); d->clk = 1; d->eval();
            if (d->pdu_accept_p_o) accepts++;
        }
    }
    void one(bool vlan, uint8_t format, uint8_t depth, unsigned spf, unsigned n) {
        d->bound0_i = 0; cyc(200);
        d->fmt0_i = (0x02050000ull | (uint64_t(format) << 8) | depth) << 32 | (1u << 22) | (spf << 12);
        d->bound0_i = 1; cyc(200);
        const long a0 = accepts;
        const unsigned p0 = d->pcm_pdus_o;
        const unsigned o = vlan ? 18 : 14;
        std::vector<uint8_t> f(o + 24 + n, 0);
        if (f.size() < 60) f.resize(60, 0);                 // the Ethernet minimum, padded after the payload
        for (int k = 0; k < 3; k++) {
            for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
            if (vlan) { f[12] = 0x81; f[13] = 0x00; f[14] = 0x60; f[15] = 0x02; }
            f[o - 2] = 0x22; f[o - 1] = 0xF0;
            f[o] = 0x02; f[o + 1] = 0x81; f[o + 2] = seq++;
            for (int i = 0; i < 8; i++) f[o + 4 + i] = uint8_t(kTalker >> (8 * (7 - i)));
            f[o + 12] = 0xA5; f[o + 13] = 0x5A; f[o + 14] = 0xC3; f[o + 15] = 0x3C;
            f[o + 16] = format; f[o + 17] = 0x50; f[o + 18] = 1; f[o + 19] = depth;
            f[o + 20] = uint8_t(n >> 8); f[o + 21] = uint8_t(n);
            for (unsigned i = 0; i < n; i++) f[o + 24 + i] = uint8_t(k * 31 + i + 1);
            const size_t beats = (f.size() + 7) / 8;
            for (size_t b = 0; b < beats; b++) {
                uint64_t w = 0; unsigned v = 0;
                for (unsigned j = 0; j < 8 && b * 8 + j < f.size(); j++, v++) w |= uint64_t(f[b * 8 + j]) << (8 * j);
                d->s_tdata_i = w; d->s_tkeep_i = v == 8 ? 0xFF : ((1u << v) - 1);
                d->s_tvalid_i = 1; d->s_tlast_i = b + 1 == beats;
                cyc();
            }
            d->s_tvalid_i = 0; d->s_tlast_i = 0;
            cyc(60);
        }
        cyc(400);
        std::printf("PROBE vlan=%d format=%u octets=%u frame_bytes=%zu frame_beats=%zu accepted=%ld delivered=%u\n",
                    vlan ? 1 : 0, format, n, f.size(), (f.size() + 7) / 8, accepts - a0,
                    unsigned(uint16_t(d->pcm_pdus_o - p0)));
    }
};
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Probe p;
    return p.run();
}
