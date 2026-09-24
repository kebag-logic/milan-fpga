#!/usr/bin/env python3
"""Disposable probe patches for an exported protocol-processor tree (never the
review clone). Usage: pp_mvu_probe_patch.py <pp-tree> arms|mutant
  arms   : add a harness arm (after M4) sending MVU 0x0001, 0x0003 and 0x0004
           at the minimal 8-byte payload and at a representative size, each
           requiring the byte-exact MVU NOT_IMPLEMENTED echo that FR-MVU-02 and
           the compliance matrix state for all four commands.
  mutant : additionally make the engine's GET_MILAN_INFO match accept every
           command_type <= 0x0004 (a build that "serves" the four commands
           with the GET_MILAN_INFO body); M4 and the added arms must then fail.
Each substitution must match exactly once or the script refuses."""
import sys
tree, mode = sys.argv[1], sys.argv[2]

def sub_once(path, old, new):
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        sys.exit(f"REFUSED: anchor found {text.count(old)} times in {path}")
    open(path, "w", encoding="utf-8").write(text.replace(old, new))
    print(f"patched {path}")

sim = f"{tree}/tb/pp_top/sim_main.cpp"
sub_once(sim,
    "    m4_an_mvu_command_type_this_build_does_not_implement();\n",
    "    m4_an_mvu_command_type_this_build_does_not_implement();\n"
    "    r275_probe_the_other_three_mvu_command_types();\n")
sub_once(sim,
    "  // ---- M5: the r field is compared, the reserved field is not -----------\n",
    "  // ---- R275 disposable probe: 0x0001 / 0x0003 / 0x0004 -------------------\n"
    "  void r275_probe_the_other_three_mvu_command_types() {\n"
    "    struct Case { uint16_t ct; size_t bytes; const char* what; };\n"
    "    const Case cases[] = {\n"
    "      {0x0001,  8, \"SET_SYSTEM_UNIQUE_ID minimal\"},\n"
    "      {0x0001, 16, \"SET_SYSTEM_UNIQUE_ID with a u64 id\"},\n"
    "      {0x0003,  8, \"SET_MEDIA_CLOCK_REFERENCE_INFO minimal\"},\n"
    "      {0x0003, 80, \"SET_MEDIA_CLOCK_REFERENCE_INFO with a 64-byte name\"},\n"
    "      {0x0004,  8, \"GET_MEDIA_CLOCK_REFERENCE_INFO minimal\"},\n"
    "      {0x0004, 12, \"GET_MEDIA_CLOCK_REFERENCE_INFO with an index\"},\n"
    "    };\n"
    "    uint16_t seq = 0xC0A0;\n"
    "    for (const auto& c : cases) {\n"
    "      auto cmd = mvu_cmd_pl(MVU_PID_LO, c.ct, c.bytes);\n"
    "      auto got = mvu(MVU_PID_LO, c.ct, seq, c.bytes);\n"
    "      auto want = mvu_expect(AECP_NOT_IMPLEMENTED, seq, cmd);\n"
    "      CHECK(!got.empty(), \"R275: %s got silence\", c.what);\n"
    "      CHECK(got == want, \"R275: %s is not the byte-exact NOT_IMPLEMENTED echo\", c.what);\n"
    "      if (!got.empty() && got != want) { dump(\"got \", got); dump(\"want\", want); }\n"
    "      ++seq;\n"
    "    }\n"
    "  }\n\n"
    "  // ---- M5: the r field is compared, the reserved field is not -----------\n")
if mode == "mutant":
    sub_once(f"{tree}/hdl/aecp/KL_aecp_engine.sv",
        "&& (desc_ty_r  == MVU_GET_MILAN_INFO_C);",
        "&& (desc_ty_r  <= 16'h0004);")
elif mode != "arms":
    sys.exit("mode must be arms or mutant")
