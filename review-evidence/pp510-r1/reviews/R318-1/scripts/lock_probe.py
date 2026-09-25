#!/usr/bin/env python3
"""Disposable harness probe (never committed): copy <base> to <dst> and add an
M4L arm to tb/pp_top MilanInfoPhase. Controller 1 takes the ENTITY lock; a
second controller then sends the complete SET_SYSTEM_UNIQUE_ID and
SET_MEDIA_CLOCK_REFERENCE_INFO commands. 06 section 6.9 / F06.9 claim both take
the unsupported-command path without a lock check, i.e. MVU status 1 with the
command echoed (Milan Table 5.19 has no ENTITY_LOCKED code). Then unlock."""
import shutil, sys, pathlib
base, dst = sys.argv[1:3]
d = pathlib.Path(dst)
if d.exists():
    shutil.rmtree(d)
shutil.copytree(base, dst, ignore=shutil.ignore_patterns('.git', 'obj_dir', 'obj_vid'))
f = d / 'tb/pp_top/sim_main.cpp'
s = f.read_text()
call = "    m4_the_waived_pairs_and_a_reserved_command_type();\n"
assert s.count(call) == 1
s = s.replace(call, call + "    r318_m4l_waived_sets_under_a_foreign_lock();\n")
anchor = "  // ---- M5: the r field is compared, the reserved field is not -----------"
assert s.count(anchor) == 1
probe = r'''  void r318_m4l_waived_sets_under_a_foreign_lock() {
    const uint64_t P2_MAC = 0x0202C2C2C2C2ull;
    std::vector<uint8_t> lock(16, 0);            // flags 0 = LOCK, ENTITY 0
    h.q_aecp.clear();
    h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, 0xD001, 0x0001, lock));
    auto got = h.wait_any(h.q_aecp, 200);
    CHECK(got.size() > 17 && (got[16] >> 3) == 0, "M4L: controller 1 could not lock");
    for (uint16_t ct : {uint16_t(0x0001), uint16_t(0x0003)}) {
      auto payload = mvu_cmd_pl(MVU_PID_LO, ct, ct == 1 ? 16 : 80);
      if (ct == 1) putbe(&payload[8], 0x0123456789ABCDEFull, 8);
      else { payload[8] = 3; payload[11] = 0x5A; }
      const uint16_t seq = uint16_t(0xD010 + ct);
      h.q_aecp.clear();
      h.feed(aecp_frame(OWN_MAC, P2_MAC, VU_COMMAND, 0, EID, CTLR2_EID, seq,
                        MVU_PID_HI, payload));
      got = h.wait_any(h.q_aecp, 200);
      const auto want = aecp_frame(P2_MAC, OWN_MAC, VU_RESPONSE,
                                   AECP_NOT_IMPLEMENTED, EID, CTLR2_EID, seq,
                                   MVU_PID_HI, payload);
      CHECK(got == want, "M4L: MVU 0x%04x from a foreign controller under lock "
            "is not the NOT_IMPLEMENTED echo (status %u)", ct,
            got.size() > 16 ? unsigned(got[16] >> 3) : 99u);
      h.run_ms(20);
      CHECK(h.q_aecp.empty(), "M4L: MVU 0x%04x produced an extra AECP frame", ct);
    }
    lock[3] = 1;                                 // UNLOCK
    h.q_aecp.clear();
    h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, 0xD002, 0x0001, lock));
    got = h.wait_any(h.q_aecp, 200);
    CHECK(got.size() > 17 && (got[16] >> 3) == 0, "M4L: controller 1 could not unlock");
    std::printf("R318 M4L probe ran: lock, 2 foreign waived SETs, unlock\n");
  }

'''
s = s.replace(anchor, probe + anchor)
f.write_text(s)
print("probe inserted")
