#!/usr/bin/env python3
"""Reviewer probes for issue #206 at exact head c836105 (round R724-2).

Usage: python3 probes.py <processor clone> <output dir> <verilator> <jobs>

Reuses the clone's own tb/pp_top/gsi_mutants.py check_variant(): each arm is
built in a private temporary copy of hdl/, tb/common and tb/pp_top, so the
clone's tracked bytes are never edited. An arm with an expected check prefix
must fail that named check (killed); an arm with "" must PASS like the golden
(equivalent or unreachable mutant, a falsification probe of a stated claim).
"""

import json
import sys
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SEL0 = "4'd0: aecp_gsi_data_w = gsi_data_i & ~64'h0000_0000_5200_0000;"
SEL4 = "4'd4: aecp_gsi_data_w[63:16] = 48'd0;"
OTHER = ("GI GATE RESET solicited: every other flag the integrator claims "
         "passes for sink 0")
THREE = ("GI GATE RESET solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and "
         "STREAM_VLAN_ID_VALID clear for sink 0")


def sel0(mask: str) -> str:
    return SEL0.replace("64'h0000_0000_5200_0000", mask)


ARMS = [
    # over-clearing masks beyond the arms the author and the prior round ran
    ("P-overclear-msrp-failure-valid", SEL0, sel0("64'h0000_0000_5A00_0000"), OTHER),
    ("P-overclear-bit31", SEL0, sel0("64'h0000_0000_D200_0000"), OTHER),
    ("P-overclear-bit0", SEL0, sel0("64'h0000_0000_5200_0001"), OTHER),
    ("P-overclear-fast-connect", SEL0, sel0("64'h0000_0000_5200_0002"), OTHER),
    # under-clearing: STREAM_VLAN_ID_VALID left set while unsettled
    ("P-underclear-vlan-valid", SEL0, sel0("64'h0000_0000_5000_0000"), THREE),
    # the upper 32 bits of selector 0 never reach the wire (FMT_D @28):
    # expected equivalent, recorded so the "every bit" claim is bounded
    ("P-overclear-upper32-equivalent", SEL0, sel0("64'hFFFF_FFFF_5200_0000"), ""),
    # S1 claim: no graded unsettled response carries a non-zero failure code,
    # so zeroing selector 4's whole word while unsettled must survive
    ("P-sel4-whole-word-zero-survives", SEL4, "4'd4: aecp_gsi_data_w = 64'd0;", ""),
]


def main() -> int:
    clone, output, verilator, jobs = (Path(sys.argv[1]).resolve(),
                                      Path(sys.argv[2]).resolve(),
                                      sys.argv[3], int(sys.argv[4]))
    sys.path.insert(0, str(clone / "tb" / "pp_top"))
    sys.path.insert(0, str(clone / "tb" / "common"))
    import gsi_mutants  # noqa: E402
    from mutant_pool import in_order  # noqa: E402
    output.mkdir(parents=True, exist_ok=True)
    units = [("golden", None, "", output, verilator)]
    units += [(n, (TOP, old, new, 1), exp, output, verilator)
              for n, old, new, exp in ARMS]
    records = []
    with in_order(gsi_mutants.check_variant, units, jobs) as results:
        for r in results:
            r["expected"] = next((a[3] for a in ARMS if a[0] == r["variant"]), "")
            r["named_failures"] = r["named_failures"][:3]
            print(json.dumps(r), flush=True)
            records.append(r)
    (output / "probe-results.json").write_text(json.dumps(records, indent=2) + "\n")
    bad = [r["variant"] for r in records if not r["passed"]]
    print("PROBES:", "all verdicts as expected" if not bad else "UNEXPECTED " + " ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
