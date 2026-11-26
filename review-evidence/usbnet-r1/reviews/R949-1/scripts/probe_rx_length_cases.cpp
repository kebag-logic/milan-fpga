// Reviewer probe (appended to the head's tb/verilator/usbnet/sim_main.cpp in place of its main):
// the receive copy's record lengths against docs/design/USB_NET_PATH.md section 4, which gives
// a FRAME record "14 to 1518" octets in both directions. A received broadcast of each length is
// offered with a computer attached; reported: whether it was copied and the record's length field.

static void probe_rx_len(int len)
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    b->rx_q.push_back(frame(BCAST, PEER, 0x0800, len));
    for (int i = 0; i < 100000 && !b->rx_q.empty(); ++i) b->cycles(1);
    b->cycles(20000);
    bool ok; auto got = b->up_frames(&ok);
    int rec_len = b->up_words.empty() ? -1 : int(b->up_words[0] & 0xFFF);
    std::printf("  probe rx len=%d: copied=%zu record length field=%d verdict=%d\n", len, got.size(), rec_len,
                b->rx_verdicts.empty() ? -1 : b->rx_verdicts.back());
    CHECK(got.empty() || (rec_len >= 14 && rec_len <= 1518),
          "a FRAME record toward the computer is 14 to 1518 octets (USB_NET_PATH.md section 4): %d", rec_len);
    done(b);
}

int main(int argc, char **argv)
{
    std::setvbuf(stdout, nullptr, _IOLBF, 0);
    Verilated::commandArgs(argc, argv);
    for (int len : {1514, 1518, 1519, 1600, 2000, 2001}) {
        int before = fails();
        probe_rx_len(len);
        std::printf("%s rx_len_%d\n", fails() == before ? "PASS" : "FAIL", len);
    }
    std::printf("%s: %d failure(s)\n", fails() ? "FAIL" : "PASS", fails());
    return fails() ? 1 : 0;
}
