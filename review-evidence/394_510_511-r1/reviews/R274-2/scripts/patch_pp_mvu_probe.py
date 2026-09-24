#!/usr/bin/env python3
"""Disposable probe patch for the protocol-processor pp_top suite (pin 424c688).

Usage: patch_pp_mvu_probe.py <exported-pp-root> [--mutant]

<exported-pp-root> is a `git archive` export of the pinned processor
(hdl/ and tb/pp_top/), never the superproject's submodule checkout.

Always: extends pp_top's M4 with arms that send every other Milan v1.2
Table 5.18 command type this build does not serve (0x0001, 0x0003, 0x0004,
plus 0x0002 at a longer payload) and require the byte-exact MVU
NOT_IMPLEMENTED echo (Table 5.19), the fallback the PR's compliance-matrix
rows state.

--mutant: additionally widens the engine's GET_MILAN_INFO decode to accept
command_type 0x0003, a decode defect the new 0x0003 arms must catch.
"""
import sys

ARMS = r'''
    // [R274-2 probe] every other Table 5.18 command this build does not serve
    struct ProbeArm { uint16_t ct; size_t bytes; uint16_t seq; const char* what; };
    static const ProbeArm probe_arms[] = {
      {0x0001,  8, 0xC0A1, "SET_SYSTEM_UNIQUE_ID 8B"},
      {0x0001, 12, 0xC0A2, "SET_SYSTEM_UNIQUE_ID 12B"},
      {0x0002, 12, 0xC0A3, "GET_SYSTEM_UNIQUE_ID 12B"},
      {0x0003,  8, 0xC0A4, "SET_MEDIA_CLOCK_REFERENCE_INFO 8B"},
      {0x0003, 80, 0xC0A5, "SET_MEDIA_CLOCK_REFERENCE_INFO 80B"},
      {0x0004,  8, 0xC0A6, "GET_MEDIA_CLOCK_REFERENCE_INFO 8B"},
      {0x0004, 12, 0xC0A7, "GET_MEDIA_CLOCK_REFERENCE_INFO 12B"},
    };
    int probe_n = 0;
    for (const auto& x : probe_arms) {
      auto pl = mvu_cmd_pl(MVU_PID_LO, x.ct, x.bytes);
      auto got2 = mvu(MVU_PID_LO, x.ct, x.seq, x.bytes);
      auto want2 = mvu_expect(AECP_NOT_IMPLEMENTED, x.seq, pl);
      CHECK(!got2.empty(), "M4x: %s got silence", x.what);
      CHECK(got2 == want2, "M4x: %s is not the byte-exact NOT_IMPLEMENTED echo", x.what);
      ++probe_n;
    }
    std::printf("[R274-2 probe] M4x arms executed: %d\n", probe_n);
'''

ANCHOR = '    CHECK(got == want, "M4: the unimplemented-MVU echo is not byte-exact");\n'
DECODE = "                                && (desc_ty_r  == MVU_GET_MILAN_INFO_C);"
MUTANT = ("                                && ((desc_ty_r == MVU_GET_MILAN_INFO_C)"
          " || (desc_ty_r == 16'h0003));")


def patch(path, old, new):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if text.count(old) != 1:
        sys.exit(f"anchor count {text.count(old)} != 1 in {path}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))
    print(f"patched {path}")


def main():
    root = sys.argv[1]
    patch(f"{root}/tb/pp_top/sim_main.cpp", ANCHOR, ANCHOR + ARMS)
    if "--mutant" in sys.argv[2:]:
        patch(f"{root}/hdl/aecp/KL_aecp_engine.sv", DECODE, MUTANT)


if __name__ == "__main__":
    main()
