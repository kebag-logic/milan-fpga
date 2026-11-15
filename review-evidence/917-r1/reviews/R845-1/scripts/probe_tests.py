#!/usr/bin/env python3
"""Reviewer probe checks for #917, in a scratch copy of tb/verilator/mbx (never the tree): three checks
appended to the suite's HeldNotDropped group, built against the head RTL (must pass) and against RTL
copies carrying the probe defects that the shipped suite let escape (each should now fail).
Usage: python3 -I probe_tests.py <clone> <scratch-root>"""
import shutil, subprocess, sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve()
tb = root / "tb/verilator/mbx"
if root.exists():
    shutil.rmtree(root)
shutil.copytree(clone / "tb/common", root / "tb/common")
shutil.copytree(clone / "tb/verilator/mbx", tb, ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
ANCHOR = '    ck_.that("B4 whole, byte for byte", same_bytes(peek(ch).bytes, held));\n}\n'
PROBE = r'''    ck_.that("B4 whole, byte for byte", same_bytes(peek(ch).bytes, held));
    // ---- reviewer probe checks (scratch only) ----
    // RP1: a command the identity term refuses, and a runt, behind a held one count nowhere
    restart();
    open(1u << ch);
    for (std::uint32_t k = 0; k < burst + 1u; ++k) b_.send_frame(aecp_read(static_cast<std::uint16_t>(0x7600u + k)), 0);
    b_.drain_rx(40000);
    ck_.dec("RP1 the command past the burst is held", rx_pass(ch), burst);
    {
        const std::uint32_t m0 = mismatches();
        auto foreign = mbx_tb::aecp(0, kForeignEid, kForeignEid, kOwnMac, kReadDescriptor);
        b_.send_frame(foreign, 0);
        std::vector<std::uint8_t> runt(foreign.begin(), foreign.begin() + 14);
        b_.send_frame(runt, 0);
        b_.drain_rx();
        ck_.dec("RP1 a refused command and a runt behind the held one count in no RATE_DROP",
                rd(ch_reg(ch, MBX_CH_REG_RATE_DROP)), 0);
        ck_.dec("RP1 nor in RX_DROP", rd(ch_reg(ch, MBX_CH_REG_RX_DROP)), 0);
        ck_.dec("RP1 nor in FILTER_MISMATCH", (mismatches() - m0) & 0xFFFFu, 0);
        ck_.dec("RP1 nor set IRQ_STATUS.ERR", err(), 0);
    }
    b_.ms(refill);
    ck_.dec("RP1 the held one is committed at the refill", rx_pass(ch), burst + 1u);
    for (std::uint32_t k = 0; k < burst; ++k) release(ch, peek(ch));
    ck_.that("RP1 whole, byte for byte", same_bytes(peek(ch).bytes, aecp_read(static_cast<std::uint16_t>(0x7600u + burst))));
    // RP2: a frame held when its channel closes is still committed (MAILBOX_SPLIT.md, The held frame)
    restart();
    open(1u << ch);
    for (std::uint32_t k = 0; k < burst + 1u; ++k) b_.send_frame(aecp_read(static_cast<std::uint16_t>(0x7650u + k)), 0);
    b_.drain_rx(40000);
    ck_.dec("RP2 the command past the burst is held", rx_pass(ch), burst);
    wr(MBX_REG_FILTER_EN, 0u);
    b_.ms(refill);
    ck_.dec("RP2 a frame held when its channel closes is still committed at the refill", rx_pass(ch), burst + 1u);
    // RP3: a ring with room for one record only: the record is held, the frame behind it finds no room
    // past the held record (RX_DROP) and writes nothing over the oldest unread record
    restart();
    open(1u << ch);
    {
        const std::uint32_t words = 2u + static_cast<std::uint32_t>(aecp_read(0).size() + 3u) / 4u;
        std::vector<std::vector<std::uint8_t>> sent;
        auto room = [&]() { return MBX_CH_AECP_RX_WORDS - ((rx_head(ch) - rx_tail_[ch]) & 0xFFFFu); };
        while (room() >= 2u * words && sent.size() < 200u) {
            sent.push_back(aecp_read(static_cast<std::uint16_t>(0x7700u + sent.size())));
            const std::uint32_t before = rx_pass(ch);
            b_.send_frame(sent.back(), 0);
            b_.drain_rx();
            for (std::uint32_t w = 0; w <= refill && rx_pass(ch) == before; ++w) b_.ms(1);
        }
        ck_.that("RP3 the bucket's burst was spent filling the ring", sent.size() > burst);
        ck_.that("RP3 one record fits", room() >= words);
        const auto heldf = aecp_read(0x7800);
        b_.send_frame(heldf, 0);
        b_.drain_rx();
        ck_.dec("RP3 the record that fits is held", rx_pass(ch), static_cast<std::uint32_t>(sent.size()));
        b_.send_frame(aecp_read(0x7801), 0);
        b_.drain_rx();
        ck_.dec("RP3 the frame behind it finds no room past the held record: RX_DROP", rd(ch_reg(ch, MBX_CH_REG_RX_DROP)), 1);
        ck_.dec("RP3 and not RATE_DROP", rd(ch_reg(ch, MBX_CH_REG_RATE_DROP)), 0);
        ck_.that("RP3 the oldest unread record is intact", same_bytes(peek(ch).bytes, sent[0]));
        b_.ms(refill);
        ck_.dec("RP3 the held record is committed at the refill", rx_pass(ch), static_cast<std::uint32_t>(sent.size() + 1u));
        bool intact = true;
        for (const auto& s : sent) { const Record r = peek(ch); intact = intact && same_bytes(r.bytes, s); release(ch, r); }
        ck_.that("RP3 every unread record intact, in order", intact);
        ck_.that("RP3 the held record whole", same_bytes(peek(ch).bytes, heldf));
    }
}
'''
s = (tb / "suite.hpp").read_text()
assert s.count(ANCHOR) == 1
(tb / "suite.hpp").write_text(s.replace(ANCHOR, PROBE))
sys.path.insert(0, str(clone / "tb/verilator/mbx"))
import mutants as M  # noqa: E402
argv0 = M.recipe()
DEFECTS = {
    "head": None,
    "probe-release-gated-on-open": ("      rel_w[c]    = refill_w[c] && held_r[c];",
                                    "      rel_w[c]    = refill_w[c] && held_r[c] && open_i[c];"),
    "probe-refused-behind-held-counted": (
        "vd_rate_r <= hit_r && rule_pass_w && !bad_w && (tokens_r[ch_r] == 8'd0) && held_r[ch_r];",
        "vd_rate_r <= hit_r && !bad_w && (tokens_r[ch_r] == 8'd0) && held_r[ch_r];"),
    "probe-space-from-committed-head": ("    used_w       = wr_head_r[ch_r] - tail_w;",
                                        "    used_w       = head_r[ch_r] - tail_w;"),
}
for name, sub in DEFECTS.items():
    rtl = root / "rtl" / name
    shutil.copytree(clone / "hdl/milan/mailbox", rtl)
    if sub:
        t = (rtl / "KL_mbx_rx.sv").read_text(); assert t.count(sub[0]) == 1
        (rtl / "KL_mbx_rx.sv").write_text(t.replace(sub[0], sub[1]))
    (root / "obj" / name).mkdir(parents=True, exist_ok=True)
    argv = argv0 + ["-GHOST_P=0", "--Mdir", str(root / "obj" / name), "-j", "4",
                    *[str(rtl / f) for f in M.RTL_FILES], "tb_mbx_top.sv", "sim_main.cpp", "-o", "Vmbx"]
    b = subprocess.run(argv, cwd=tb, capture_output=True, text=True)
    if b.returncode:
        print(f"[BUILD-FAIL] {name}\n{b.stdout[-2000:]}{b.stderr[-2000:]}"); continue
    r = subprocess.run([str(root / "obj" / name / "Vmbx"), "0"], capture_output=True, text=True)
    lines = r.stdout.splitlines()
    rp = [l.strip() for l in lines if " RP" in l or l.strip().startswith("[FAIL]")]
    tally = [l for l in lines if "checks:" in l]
    print(f"== {name}: rc={r.returncode} {tally[-1] if tally else ''}")
    for l in rp:
        if "RP" in l or "[FAIL]" in l:
            print("   " + l)
    sys.stdout.flush()
