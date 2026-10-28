#!/usr/bin/env python3
"""Instrument a disposable copy of tb/verilator/milan_dp/sim_gptp.cpp so the
GET_AS_PATH in-flight cut arm prints when the first path-entry request
(milan_datapath asp_resp_entry_w) fires relative to the cut's publication.

The RTL comment beside asp_resp_entry_w states that the cut must publish
after the count snapshot but before the first path-entry request, or an
all-old response is a false green. This probe measures that ordering.

Usage: probe_cut_timing.py <copy-of-clean-tree>
Then: make -C <copy>/tb/verilator/milan_dp gptp
"""
import sys
from pathlib import Path

OLD_DECL = "    bool withdrew_before_old_wire = false;\n"
NEW_DECL = ("    bool withdrew_before_old_wire = false;\n"
            "    bool probe_entry_seen = false;\n")
OLD_LOOP = ("      withdrew_before_old_wire =\n"
            "          dut->rootp->milan_datapath__DOT__gptp_pub_path_count_w"
            " == 1;\n    }\n")
NEW_LOOP = ("      if (dut->rootp->milan_datapath__DOT__asp_resp_entry_w &&\n"
            "          !probe_entry_seen) {\n"
            "        probe_entry_seen = true;\n"
            "        printf(\"PROBE first entry request at cut-loop cycle %d,"
            " before the cut commit\\n\", n);\n"
            "      }\n"
            "      withdrew_before_old_wire =\n"
            "          dut->rootp->milan_datapath__DOT__gptp_pub_path_count_w"
            " == 1;\n"
            "      if (withdrew_before_old_wire)\n"
            "        printf(\"PROBE cut commit at cut-loop cycle %d,"
            " entry request seen before it: %d\\n\", n,"
            " int(probe_entry_seen));\n"
            "    }\n")


def main() -> int:
    path = Path(sys.argv[1]) / "tb/verilator/milan_dp/sim_gptp.cpp"
    src = path.read_text(encoding="utf-8")
    for old in (OLD_DECL, OLD_LOOP):
        if src.count(old) != 1:
            print(f"anchor matches {src.count(old)} times", file=sys.stderr)
            return 2
    src = src.replace(OLD_DECL, NEW_DECL).replace(OLD_LOOP, NEW_LOOP)
    path.write_text(src, encoding="utf-8")
    print("instrumented", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
