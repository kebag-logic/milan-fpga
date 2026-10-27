#!/usr/bin/env python3
"""Reviewer probe: plant wire-level talker-response checks into a COPY of tb/pp_top.

Usage: python3 -I pp_top_probe.py <tree>   (tree = a disposable copy of the processor)

Adds RV1..RV5 to the end of section T (TalkerStatePhase) of tb/pp_top/sim_main.cpp and a
'rvprobe' make target that builds and runs only the main DUT. Every edit must apply once.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sim = tree / "tb/pp_top/sim_main.cpp"
mk = tree / "tb/pp_top/Makefile"

RUN_OLD = ("    t1_each_listener_answers_its_own_flag();\n"
           "    t5_the_flag_is_read_live();\n"
           "  }\n")
RUN_NEW = ("    t1_each_listener_answers_its_own_flag();\n"
           "    t5_the_flag_is_read_live();\n"
           "    rv_reviewer_probe();\n"
           "  }\n"
           "\n"
           "  // ---- RV: reviewer probe, talker responses on the wire -------------\n"
           "  std::vector<uint8_t> rv_cmd(uint8_t msg, uint16_t tuid, uint64_t le,\n"
           "                              uint16_t lu, uint16_t seq, uint16_t fl) {\n"
           "    h.q_acmp.clear();\n"
           "    h.feed(acmp_frame(CTLR_MAC, msg, 0, 0, CTLR_EID, EID, le,\n"
           "                      tuid, lu, 0, 0, seq, fl, 0));\n"
           "    return h.wait_any(h.q_acmp, 400);\n"
           "  }\n"
           "  void rv_grade(const char* what, const std::vector<uint8_t>& f,\n"
           "                const std::vector<uint8_t>& want) {\n"
           "    CHECK(!f.empty() && f == want, \"%s byte-exact\", what);\n"
           "    if (!f.empty() && f != want) { dump(\"got\", f); dump(\"exp\", want); }\n"
           "    if (f.empty()) printf(\"RVINFO: %s no response\\n\", what);\n"
           "  }\n"
           "  void rv_reviewer_probe() {\n"
           "    const uint64_t LE = 0xF1E2D3C4B5A69788ull;\n"
           "    const uint16_t LU = 0x8C17;\n"
           "    // RV1 GET_TX_STATE, talker_unique_id 15 (out of range): Table 5.46\n"
           "    rv_grade(\"RV1 GET_TX_STATE unknown echoes listener fields\",\n"
           "             rv_cmd(4, 15, LE, LU, 0x5190, 0xFFFF),\n"
           "             acmp_frame(OWN_MAC, 5, 2, 0, CTLR_EID, EID, LE, 15, LU, 0, 0,\n"
           "                        0x5190, 0, 0));\n"
           "    // RV2 GET_TX_STATE success on source 0 with listener fields: Table 5.47\n"
           "    rv_grade(\"RV2 GET_TX_STATE success zeroes listener fields\",\n"
           "             rv_cmd(4, 0, LE, LU, 0x5191, 0),\n"
           "             tx_state_rsp(0x5191, 0));\n"
           "    // RV3 PROBE_TX unknown: Table 5.40 (flags 0 sent, so none echoed)\n"
           "    rv_grade(\"RV3 PROBE_TX unknown echoes listener fields\",\n"
           "             rv_cmd(0, 15, LE, LU, 0x5192, 0),\n"
           "             acmp_frame(OWN_MAC, 1, 2, 0, CTLR_EID, EID, LE, 15, LU, 0, 0,\n"
           "                        0x5192, 0, 0));\n"
           "    // RV4 DISCONNECT_TX unknown: Table 5.44\n"
           "    rv_grade(\"RV4 DISCONNECT_TX unknown echoes listener fields\",\n"
           "             rv_cmd(2, 15, LE, LU, 0x5193, 0xFFFF),\n"
           "             acmp_frame(OWN_MAC, 3, 2, 0, CTLR_EID, EID, LE, 15, LU, 0, 0,\n"
           "                        0x5193, 0, 0));\n"
           "    // RV5 GET_TX_CONNECTION on source 0: NOT_SUPPORTED, echo unchanged\n"
           "    rv_grade(\"RV5 GET_TX_CONNECTION echoes listener fields\",\n"
           "             rv_cmd(12, 0, LE, LU, 0x5194, 0),\n"
           "             acmp_frame(OWN_MAC, 13, 31, 0, CTLR_EID, EID, LE, 0, LU, 0, 0,\n"
           "                        0x5194, 0, 0));\n"
           "  }\n")

MK_ADD = ("\n# reviewer probe: the main DUT only\n"
          "rvprobe: ltn_rom.hex ucode.hex\n"
          "\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n"
          "\t./obj_dir/Vpp_top_sim\n")

text = sim.read_text()
assert text.count(RUN_OLD) == 1, f"run() anchor occurs {text.count(RUN_OLD)} times"
sim.write_text(text.replace(RUN_OLD, RUN_NEW, 1))
mk.write_text(mk.read_text() + MK_ADD)
print("probe planted in", tree)
