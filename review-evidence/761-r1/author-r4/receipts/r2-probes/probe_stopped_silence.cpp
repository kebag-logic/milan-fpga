#include "VKL_crf_rx.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

int main() {
    int failures = 0;
    for (int stopped = 0; stopped <= 1; ++stopped) {
        VKL_crf_rx d;
        auto tick = [&]() { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); };
        d.rst_n = 0; d.en_i = 0; d.stop_i = 0; d.frame_p_i = 0;
        d.sid_i = 0x0200000000010001ULL;
        d.sid_frame_i = d.sid_i;
        d.subtype_i = 4; d.type_i = 1; d.pullbase_i = 48000;
        d.mr_i = 0; d.tu_i = 0;
        for (int i = 0; i < 8; ++i) tick();
        d.rst_n = 1; d.en_i = 1;
        for (int i = 0; i < 8; ++i) tick();
        uint64_t ts = 1000000000ULL;
        for (int i = 0; i < 10; ++i) {
            ts += 2000000;
            d.ptp_now_i = ts - 1000000;
            d.seq_i = i;
            d.fsh_i = (8ULL << 48) | (96ULL << 32) | (ts >> 32);
            d.fsh2_i = (ts & 0xffffffffULL) << 32;
            d.frame_p_i = 1; tick(); d.frame_p_i = 0;
            for (int k = 0; k < 4; ++k) tick();
        }
        if (!d.locked_o || d.cnt_intr_o != 0) { ++failures; std::puts("PRECONDITION FAIL"); }
        d.stop_i = stopped;
        for (int i = 0; i < 20010; ++i) tick();
        std::printf("STOPPED-SILENCE stopped=%d bound=%d locked=%d MEDIA_LOCKED=%u MEDIA_UNLOCKED=%u STREAM_INTERRUPTED=%u\n",
                    stopped, d.en_i, d.locked_o, d.cnt_locked_o, d.cnt_unlocked_o, d.cnt_intr_o);
        if (d.cnt_unlocked_o != 1 || d.cnt_intr_o != 1) {
            ++failures;
            std::puts("FAIL: bound input's silence unlock must count exactly one interruption under the frozen acceptance");
        }
    }
    std::printf("STOPPED-SILENCE failures=%d\n", failures);
    return failures ? 1 : 0;
}
