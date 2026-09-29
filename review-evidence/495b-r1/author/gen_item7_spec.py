#!/usr/bin/env python3
"""Write mutants/item7.json: R382-4's MD and ME, the pre-item-7 probe under
both, and ordering mutants of the #395 hooks, for mutate.py.

MD and ME are receipt 07's edits of sw/litex/clock_constraints.py, verbatim
(review-evidence/607-r1/reviews/R382-4/scripts/merge_mutants.py on branch
607-review-evidence at 14d271cc).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = "$LANES/495-builder-residue"
CHECK = ["python3", str(HERE / "run_ship_probe.py"), LANE]
CC = "sw/litex/clock_constraints.py"
PLAT = "sw/litex/platforms/alinx_ax7101.py"
PROBE = "sw/builder/test_shipping_clock_constraints.py"
ANCHOR = "    toolchain.bitstream_commands.append(\n        \"report_clock_interaction"
MD = {"path": CC, "old": ANCHOR, "new": "    toolchain.bitstream_commands = []\n" + ANCHOR}
ME = {"path": CC, "old": ANCHOR,
      "new": "    from litex.build.generic_toolchain import GenericToolchain  # noqa\n"
             "    toolchain.pre_placement_commands.__init__()\n" + ANCHOR}
REPORTS = '            "kl_timing_grade_reports {build_name}_signoff",\n'
LIST_END = '            "set_property CONFIG_VOLTAGE 3.3 [current_design]",\n        ]\n'
BEFORE = {"path": PROBE, "base": "eb23f044"}

mutants = [
    {"name": "control", "expect": "pass", "edits": []},
    {"name": "control 1x1 e2", "expect": "pass", "check": CHECK + ["ax7101_1x1_tdm8", "e2"], "edits": []},
    {"name": "control 8x8 e1", "expect": "pass", "check": CHECK + ["ax7101_8x8", "e1"], "edits": []},
    {"name": "BEFORE probe (eb23f044) under MD: gap", "expect": "pass", "edits": [BEFORE, MD]},
    {"name": "BEFORE probe (eb23f044) under ME: gap", "expect": "pass", "edits": [BEFORE, ME]},
    {"name": "MD 607 hook overwrites bitstream_commands", "edits": [MD]},
    {"name": "ME 607 hook overwrites pre_placement_commands", "edits": [ME]},
    {"name": "MD on 8x8 e2", "check": CHECK + ["ax7101_8x8", "e2"], "edits": [MD]},
    {"name": "ME on 8x8 e2", "check": CHECK + ["ax7101_8x8", "e2"], "edits": [ME]},
    {"name": "MF configure moved after placement",
     "edits": [{"path": PLAT, "old": "            self.toolchain.pre_placement_commands.append(",
                "new": "            self.toolchain.pre_routing_commands.append("}]},
    {"name": "MG reports moved before routing",
     "edits": [{"path": PLAT, "old": REPORTS, "new": ""},
               {"path": PLAT, "old": LIST_END, "new": LIST_END +
                "        self.toolchain.pre_routing_commands.append(\"kl_timing_grade_reports {build_name}_signoff\")\n"}]},
    {"name": "MI reports moved after write_bitstream",
     "edits": [{"path": PLAT, "old": REPORTS, "new": ""},
               {"path": PLAT, "old": LIST_END, "new": LIST_END +
                "        self.toolchain.additional_commands.append(\"kl_timing_grade_reports {build_name}_signoff\")\n"}]},
    {"name": "MH configure duplicated by the 607 hook",
     "edits": [{"path": CC, "old": ANCHOR,
                "new": "    toolchain.pre_placement_commands.append(\"kl_timing_grade_configure {{dup}}\")\n" + ANCHOR}]},
]
spec = {"check": CHECK, "cwd": ".", "timeout": 1200, "mutants": mutants}
(HERE / "mutants" / "item7.json").write_text(json.dumps(spec, indent=1) + "\n")
print(f"{len(mutants)} entries")
