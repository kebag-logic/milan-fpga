#!/usr/bin/env python3
"""Anchor adapter for the unchanged round-1 campaign r329_mutants.py.

Usage: r329_mutants_adapter.py <tree> <outdir> [mutant ...]

Round 2 replaced the shadow's map term with the parent input amap_live_wr_i,
so the round-1 LIVE anchor no longer exists (the unchanged script REFUSES
those mutants). This adapter changes ONLY the anchor text: every round-1
replacement expression is kept byte-for-byte and substituted for the new
anchor. It also adds round-2 variants (prefix U) that re-express the same
defect classes on the new input, so each finding is also tested against the
shipping trigger rather than only against the superseded one:
  U1_drop_map          map term removed (the M1 class on the new input)
  U5_refused_live      M5 phase-4 trigger OR'd onto the shipping trigger
  U6_add_only          the shipping trigger gated off for REMOVE (M6 class)
  U8_input_only        the shipping trigger gated to input ports (M8 class)
  U11_unqualified_p5   the round-1 104c8a54 trigger (req && phase 5): every
                       phase-5 record, the R329-F3 over-report
Everything else (legs, verdict rules, source-identity check) is the
unchanged round-1 code imported from r329_mutants.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r329_mutants as m  # noqa: E402  (unchanged round-1 campaign)

NEW_LIVE = ("  assign aecp_live_wr_w = aecp_name_wr_w\n"
            "                        | amap_live_wr_i;")


def new(expr):
    return NEW_LIVE, f"  assign aecp_live_wr_w = {expr};"


adapted = {}
for name, spec in m.MUTANTS.items():
    if spec is not None and spec[0] == m.LIVE:
        adapted[name] = (NEW_LIVE, spec[1])     # anchor only; expression kept
    else:
        adapted[name] = spec
adapted.update({
    "U1_drop_map": new("aecp_name_wr_w"),
    "U5_refused_live": new("aecp_name_wr_w | amap_live_wr_i"
                           " | (amap_edit_req_o && (amap_edit_phase_o == 3'd4))"),
    "U6_add_only": new("aecp_name_wr_w | (amap_live_wr_i && !amap_edit_remove_o)"),
    "U8_input_only": new("aecp_name_wr_w | (amap_live_wr_i"
                         " && (amap_edit_desc_type_o == 16'h000e))"),
    "U11_unqualified_p5": new("aecp_name_wr_w | (amap_edit_req_o"
                              " && (amap_edit_phase_o == 3'd5))"),
})
m.MUTANTS = adapted

if __name__ == "__main__":
    m.main()
