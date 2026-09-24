#!/usr/bin/env python3
"""Adds a probe phase to a SCRATCH copy of protocol-processor
tb/pp_top/sim_main.cpp: MVU command_types 0x0001, 0x0003 and 0x0004 with
their Milan v1.2 Figure 5.5/5.6/5.7 payload lengths must each be answered
with the byte-exact NOT_IMPLEMENTED echo (the shape M4 grades for 0x0002).

A negative control proves the compare is discriminating: the real 0x0003
response is compared against a copy with one payload byte flipped and must
NOT be equal. A second negative control requires the real 0x0003 response
NOT to equal a SUCCESS-status version of the same echo.

Usage: patch_pp_mvu_probe.py <scratch sim_main.cpp>
"""
import sys

ANCHOR_CALL = "    m4_an_mvu_command_type_this_build_does_not_implement();\n"
ANCHOR_DEF = "  // ---- M5: the r field is compared, the reserved field is not -----------\n"

PROBE = r'''  // ---- R274 PROBE (scratch only): 0x0001 / 0x0003 / 0x0004 ------------
  void r274_probe_other_mvu_commands() {
    // SET_SYSTEM_UNIQUE_ID, Figure 5.5: pid_lo, r+ct, reserved, 64-bit id
    std::vector<uint8_t> p1(16, 0);
    putbe(&p1[0], MVU_PID_LO, 4); putbe(&p1[4], 0x0001, 2);
    for (int i = 0; i < 8; ++i) p1[8 + i] = uint8_t(0xA0 + i);
    // SET_MEDIA_CLOCK_REFERENCE_INFO, Figure 5.6: 80 bytes from @24
    std::vector<uint8_t> p3(80, 0);
    putbe(&p3[0], MVU_PID_LO, 4); putbe(&p3[4], 0x0003, 2);
    putbe(&p3[6], 0x0000, 2);          // clock_domain_index
    p3[8] = 0x03;                      // flags: both VALID bits
    p3[10] = 0x00; p3[11] = 0x80;      // default (ignored), user prio
    const char* nm = "R274-PROBE-DOMAIN";
    for (int i = 0; nm[i]; ++i) p3[16 + i] = uint8_t(nm[i]);
    // GET_MEDIA_CLOCK_REFERENCE_INFO, Figure 5.7: pid_lo, r+ct, index
    std::vector<uint8_t> p4(8, 0);
    putbe(&p4[0], MVU_PID_LO, 4); putbe(&p4[4], 0x0004, 2);
    putbe(&p4[6], 0x0000, 2);
    struct Pc { uint16_t ct; uint16_t seq; std::vector<uint8_t>* pl;
                const char* what; };
    Pc cases[] = {{0x0001, 0xC0A1, &p1, "SET_SYSTEM_UNIQUE_ID"},
                  {0x0003, 0xC0A3, &p3, "SET_MEDIA_CLOCK_REFERENCE_INFO"},
                  {0x0004, 0xC0A4, &p4, "GET_MEDIA_CLOCK_REFERENCE_INFO"}};
    std::vector<uint8_t> got3;
    for (auto& c : cases) {
      uint16_t c0 = d->dbg_aecp_cmd_o, r0 = d->dbg_aecp_resp_o;
      h.q_aecp.clear();
      h.feed(aecp_frame(OWN_MAC, CTLR_MAC, VU_COMMAND, 0, EID, CTLR_EID,
                        c.seq, MVU_PID_HI, *c.pl));
      auto got = h.wait_any(h.q_aecp, 200);
      auto want = mvu_expect(AECP_NOT_IMPLEMENTED, c.seq, *c.pl);
      std::printf("R274PROBE ct=0x%04x %s: got %zu B, want %zu B, %s\n",
                  c.ct, c.what, got.size(), want.size(),
                  got == want ? "BYTE-EXACT NOT_IMPLEMENTED ECHO" : "MISMATCH");
      CHECK(!got.empty(), "R274PROBE: ct 0x%04x got silence", c.ct);
      CHECK(got == want, "R274PROBE: ct 0x%04x echo is not byte-exact", c.ct);
      if (!got.empty() && got != want) { dump("got ", got); dump("want", want); }
      CHECK(d->dbg_aecp_cmd_o == c0 + 1 && d->dbg_aecp_resp_o == r0 + 1,
            "R274PROBE: ct 0x%04x counters did not move once", c.ct);
      if (c.ct == 0x0003) got3 = got;
    }
    // negative controls: the compare must be able to fail
    auto flipped = p3; flipped[20] ^= 0x01;
    auto wrong_pl = mvu_expect(AECP_NOT_IMPLEMENTED, 0xC0A3, flipped);
    auto wrong_st = mvu_expect(AECP_SUCCESS, 0xC0A3, p3);
    std::printf("R274PROBE negative control (one payload byte flipped): %s\n",
                got3 != wrong_pl ? "DETECTED" : "NOT DETECTED");
    std::printf("R274PROBE negative control (status SUCCESS): %s\n",
                got3 != wrong_st ? "DETECTED" : "NOT DETECTED");
    CHECK(got3 != wrong_pl, "R274PROBE: flipped-byte control not detected");
    CHECK(got3 != wrong_st, "R274PROBE: SUCCESS-status control not detected");
  }

'''


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if src.count(ANCHOR_CALL) != 1 or src.count(ANCHOR_DEF) != 1:
        raise SystemExit("patch anchors not found exactly once")
    src = src.replace(ANCHOR_CALL, ANCHOR_CALL +
                      "    r274_probe_other_mvu_commands();\n")
    src = src.replace(ANCHOR_DEF, PROBE + ANCHOR_DEF)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print("patched", path)


if __name__ == "__main__":
    main()
