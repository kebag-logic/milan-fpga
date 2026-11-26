// Reviewer probe (appended to the head's tb/verilator/usbnet/sim_main.cpp in place of its main):
// the arbiter's reset contract (KL_usbnet_tx_arb.sv RESETS paragraph). A reset of the tap's
// system-clock side alone, after an odd or even number of granted injections, with the
// transmit clock running and its side NOT reset; and the same with both sides reset.
// After the reset the computer re-announces itself, the datapath sends frames, then the
// computer sends frames. Reported: injections after the reset, datapath frame ends counted.

static void probe_reset(bool also_eth, int n_inject)
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    for (int i = 0; i < n_inject; ++i) b->rec(0, frame(PEER, HOST, 0x0800, 200, -1, {}, uint8_t(i)));
    b->drain_dn(); b->cycles(20000);
    size_t lo0 = 0; for (auto &s : b->out) lo0 += s.lo;
    CHECK(lo0 == size_t(n_inject), "before the reset: %zu injected of %d", lo0, n_inject);
    uint32_t tgl0 = b->tgl_flips;
    b->d->rst_ni = 0; if (also_eth) b->d->eth_rst_ni = 0;
    b->cycles(50);
    b->d->rst_ni = 1; b->d->eth_rst_ni = 1;
    b->cycles(50);
    b->host(HOST, 3); b->drain_dn();
    const int n_hi = 4;
    for (int i = 0; i < n_hi; ++i)
        b->hi_q.push_back({b->ncyc + 100 + 3000 * uint64_t(i), frame(PEER, DEVICE, 0x0800, 100 + i)});
    b->cycles(15000);
    for (int i = 0; i < 3; ++i) b->rec(0, frame(PEER, HOST, 0x0800, 150, -1, {}, uint8_t(50 + i)));
    b->drain_dn(); b->cycles(60000);
    size_t lo1 = 0, hi1 = 0; for (auto &s : b->out) { lo1 += s.lo; hi1 += !s.lo; }
    std::printf("  probe also_eth=%d n_inject=%d: datapath frames out %zu, datapath ends counted %u of %d, "
                "injected after the reset %zu of 3, passed=%u injected_ctr=%u\n",
                also_eth, n_inject, hi1, b->tgl_flips - tgl0, n_hi, lo1 - lo0,
                b->d->tx_passed_o, b->d->tx_injected_o);
    CHECK(lo1 - lo0 == 3, "after the reset the computer's frames are injected again (%zu of 3)", lo1 - lo0);
    CHECK(b->tgl_flips - tgl0 == uint32_t(n_hi), "after the reset every datapath frame end counts (%u of %d)",
          b->tgl_flips - tgl0, n_hi);
    done(b);
}

int main(int argc, char **argv)
{
    std::setvbuf(stdout, nullptr, _IOLBF, 0);
    Verilated::commandArgs(argc, argv);
    struct { const char *n; std::function<void()> f; } cases[] = {
        {"both_sides_reset_after_1", [] { probe_reset(true, 1); }},
        {"sys_side_reset_after_2",   [] { probe_reset(false, 2); }},
        {"sys_side_reset_after_1",   [] { probe_reset(false, 1); }},
    };
    for (auto &c : cases) {
        int before = fails();
        c.f();
        std::printf("%s %s\n", fails() == before ? "PASS" : "FAIL", c.n);
    }
    std::printf("%s: %d failure(s)\n", fails() ? "FAIL" : "PASS", fails());
    return fails() ? 1 : 0;
}
