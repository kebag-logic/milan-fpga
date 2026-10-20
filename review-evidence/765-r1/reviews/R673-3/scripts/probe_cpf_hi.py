#!/usr/bin/env python3
"""Reviewer probe (disposable): patch a COPY of tb/verilator/avtp_rxmon/sim_main.cpp
so the flat AAF builder can set channels_per_frame[9:8] (byte O+17 [1:0]), and add a
case right after [28] that feeds counts whose low eight bits are zero or nonzero with
the high bits set. Each probe is checked by its frames_rx and UNSUPPORTED_FORMAT
deltas, so the binary's exit code and the [P*] lines say what the flat instrument does.

usage: probe_cpf_hi.py <copy-of-avtp_rxmon-dir>
"""
import pathlib, sys

d = pathlib.Path(sys.argv[1])
p = d / "sim_main.cpp"
s = p.read_text()

def sub(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)

sub("    uint8_t  chans    = 8;\n",
    "    uint8_t  chans    = 8;\n    uint8_t  chans_hi = 0;   // probe: channels_per_frame[9:8]\n")
sub("        f[o+17]=static_cast<uint8_t>(c.nsr<<4);\n",
    "        f[o+17]=static_cast<uint8_t>((c.nsr<<4)|(c.chans_hi&0x03));\n")
sub("        channel_freedom_accepts_every_count();\n",
    "        channel_freedom_accepts_every_count();\n        probe_cpf_high_bits();\n")
probe = r'''
    void probe_cpf_high_bits(){
        printf("\n[P] probe: channels_per_frame with bits [9:8] set\n");
        dut->bound_i=0; cyc(3); dut->bound_i=1; cyc(3);
        struct T { const char* n; uint8_t lo, hi; int acc; };
        const T t[] = { {"256", 0x00, 1, 0}, {"257", 0x01, 1, 1},
                        {"512", 0x00, 2, 0}, {"520", 0x08, 2, 1},
                        {"1023", 0xFF, 3, 1}, {"8", 0x08, 0, 1} };
        uint8_t seq = 0;
        for (const T& x : t) {
            long fr0 = dut->cnt_frames_rx_o, un0 = dut->cnt_unsupported_fmt_o;
            { AafCfg c; c.seq=seq++; c.chans=x.lo; c.chans_hi=x.hi; feed(build_aaf(stim, c)); }
            long dfr = dut->cnt_frames_rx_o - fr0, dun = dut->cnt_unsupported_fmt_o - un0;
            printf("     cpf=%s: frames_rx +%ld unsupported +%ld\n", x.n, dfr, dun);
            char lab[96];
            snprintf(lab, sizeof lab, "[P] cpf=%s frames_rx delta", x.n);
            ck(lab, dfr, x.acc);
            snprintf(lab, sizeof lab, "[P] cpf=%s UNSUPPORTED delta", x.n);
            ck(lab, dun, 1 - x.acc);
        }
        dut->fmt_i = FMT;
    }

    void channel_freedom_accepts_every_count(){'''
sub("\n    void channel_freedom_accepts_every_count(){", probe)
p.write_text(s)
print("patched", p)
