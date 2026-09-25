// Reviewer probe (R322-1, #541): a LOCKED CRF sink fed ONLY matched-but-
// malformed PDUs at the 2 ms cadence must still unlock after 100 ms, count
// one MEDIA_UNLOCKED, and count UNSUPPORTED_FORMAT once per interval.
// Built at CLK_FREQ_HZ_P=200000 (TOUT = 20000 clk) and IVAL_CYC_P=200,
// the crf_rx Makefile parameters. Exit 0 = all checks pass.
#include "VKL_crf_rx.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

static VKL_crf_rx* d;
static int fails = 0;
static void tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
static void ck(const char* w, long long got, long long exp) {
    const bool ok = got == exp;
    if (!ok) ++fails;
    std::printf("[%s] %s got=%lld exp=%lld\n", ok ? "PASS" : "FAIL", w, got, exp);
}
static uint64_t ts = 10'000'000'000ULL;
static uint8_t seq = 0;
static const uint64_t kSid = 0x0200000000010001ULL;
static void fields() {
    d->seq_i = seq;
    d->fsh_i = (uint64_t{8} << 48) | (uint64_t{96} << 32) | (ts >> 32);
    d->fsh2_i = ts << 32;
    d->ptp_now_i = ts - 100'000;
}
// one PDU then idle to fill a 2 ms period (400 clk at 200 kHz)
static void pdu(bool good) {
    ts += 2'000'000;
    d->type_i = good ? 1 : 0;
    fields(); d->frame_p_i = 1; tick(); d->frame_p_i = 0;
    for (int n = 1; n < 400; ++n) tick();
    if (good) ++seq;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new VKL_crf_rx;
    d->rst_n = 0; d->en_i = 0; d->stop_i = 0; d->frame_p_i = 0;
    d->sid_i = kSid; d->sid_frame_i = kSid; d->subtype_i = 4; d->type_i = 1;
    d->pullbase_i = 48000; d->mr_i = 0; d->tu_i = 0;
    tick(); tick(); d->rst_n = 1; d->en_i = 1; tick();
    for (int n = 0; n < 20; ++n) pdu(true);
    ck("precondition locked", d->locked_o, 1);
    ck("precondition one lock event", d->cnt_locked_o, 1);
    const long long f0 = d->fmt_err_o, u0 = d->cnt_unlocked_o;
    // 49 malformed PDUs = 98 ms of malformed-only traffic: still locked
    for (int n = 0; n < 49; ++n) pdu(false);
    ck("malformed-only traffic < 100 ms keeps lock", d->locked_o, 1);
    // 6 more (110 ms total): the timeout must have expired
    for (int n = 0; n < 6; ++n) pdu(false);
    ck("malformed-only traffic >= 100 ms unlocks", d->locked_o, 0);
    ck("malformed-only drought scores one unlock", d->cnt_unlocked_o, u0 + 1);
    // 55 PDUs x 400 clk = 22000 clk = 110 intervals of 200 clk, each
    // containing a reject (one PDU every 2 intervals) -> ~55 commits
    const long long df = d->fmt_err_o - f0;
    std::printf("[INFO] fmt_err delta over 55 malformed PDUs: %lld\n", df);
    ck("UNSUPPORTED_FORMAT counts once per interval (one reject per 2 intervals)",
       df >= 54 && df <= 56, 1);
    for (int n = 0; n < 60; ++n) pdu(false);
    ck("continued malformed traffic never re-locks", d->locked_o, 0);
    ck("continued malformed traffic never recounts unlock", d->cnt_unlocked_o, u0 + 1);
    std::printf("drought probe: %d failures\n", fails);
    delete d;
    return fails ? 1 : 0;
}
