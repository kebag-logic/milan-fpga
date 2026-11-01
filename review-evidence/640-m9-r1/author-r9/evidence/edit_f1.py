"""F1: docs/design/AREA_BUDGET.md agrees with NFR-RES-01; prose and status words only."""
import sys
p = "$LANES/640-mark2-charter/docs/design/AREA_BUDGET.md"
s = open(p, encoding="utf-8").read()
L = "[NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest)"
EDITS = [
 # 129-131 the target statement
 (f"{L} in the [requirements](../reference/FR_NFR.md) is the accepted headroom target.\n"
  "The baseline product must fit `xc7a100t` with at most 60 percent of its LUTs used.\n"
  "The adopted image does not meet it:\n",
  f"{L} in the [requirements](../reference/FR_NFR.md) is the accepted headroom target.\n"
  "Mark II must use fewer than 20,000 LUTs of `xc7a100t`.\n"
  "\n"
  "That replaces the earlier 60 percent target, 38,040 LUTs.\n"
  "The route below was 13,972 over it.\n"
  "\n"
  "The shipping image must fit the device.\n"
  "The resource gate holds it, with no other LUT bound:\n"),
 # 135 the target row
 (f"| Slice LUT | 63,400 | 52,012 | 82.04 % | {L}: at most 38,040 (60 %) | not met, 13,972 over |\n",
  f"| Slice LUT | 63,400 | 52,012 | 82.04 % | {L}: Mark II fewer than 20,000 (about 31.5 %); this image must fit the device | fits; no other LUT bound on this image |\n"),
 # 172-178 the acceptance bar and its history
 ("The wrapper alone exceeds that historical allocation.\n"
  f"The active [#640](https://github.com/kebag-logic/milan-fpga/issues/640) acceptance bar is the whole-image {L} target.\n"
  "\n"
  f"Meeting {L} with the rest of the image unchanged needs the wrapper at most 10,521 LUTs.\n"
  "That requires removing 13,972 LUTs, 57 % of the wrapper.\n"
  f"The [owner decided on 2026-10-03](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270) that {L} stays at 60 %.\n"
  "It is met by the [Mark II redesign plan](MARK_II_AREA_PLAN.md) ([#640](https://github.com/kebag-logic/milan-fpga/issues/640)).\n"
  "The [2026-10-05 schedule correction]",
  "The wrapper alone exceeds that historical allocation.\n"
  "\n"
  f"The active [#640](https://github.com/kebag-logic/milan-fpga/issues/640) acceptance bar is the {L} ceiling.\n"
  "That is fewer than 20,000 LUTs, with timing met.\n"
  "\n"
  "What follows is history, against the replaced 60 percent.\n"
  "The [owner kept that target on 2026-10-03](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270).\n"
  "\n"
  "All else unchanged, that needed a 10,521-LUT wrapper.\n"
  "That meant removing 13,972 LUTs, 57 % of the wrapper.\n"
  "\n"
  "The [Mark II redesign plan](MARK_II_AREA_PLAN.md) ([#640](https://github.com/kebag-logic/milan-fpga/issues/640)) answers the new ceiling.\n"
  "\n"
  "The [2026-10-05 schedule correction]"),
 # 186-188 the ledger is marked as the Mark I plan
 ("### Mark II planning ledger\n"
  "\n"
  "Round 1d uses",
  "### Mark II planning ledger\n"
  "\n"
  "This section is the Mark I plan, kept as history.\n"
  "Its target was 38,040 LUTs.\n"
  "\n"
  f"The [Mark II area plan](MARK_II_AREA_PLAN.md) supersedes its target and order.\n"
  f"{L} now sets the ceiling.\n"
  "\n"
  "Round 1d uses"),
 # 225
 ("| M9 closure and re-record | No assumed saving | Measured at closure | <= 38,040 LUT and timing met |\n",
  f"| M9 closure and re-record | No assumed saving | Measured at closure | {L} Mark II ceiling and timing met; formerly <= 38,040 LUT |\n"),
 # 349
 ("\n| Placement | Case | Estimated image LUT | Headroom to 38,040 | Headroom to 37,659 |\n",
  "\nThe two headroom columns are history.\n"
  "They measure the replaced 38,040 target and D8 margin.\n"
  "\n"
  "| Placement | Case | Estimated image LUT | Headroom to replaced 38,040 | Headroom to replaced 37,659 |\n"),
 # 378-381 D8 and the binding bar
 ("requires at least 1 percent planning margin.\n"
  "The integer ceiling is 37,659 LUTs.\n"
  "The binding bar remains 38,040 with timing met.\n"
  "[M0s](MARK_II_AREA_PLAN.md#lane-sequence) is owned",
  "requires at least 1 percent planning margin.\n"
  "The replaced target's integer ceiling was 37,659 LUTs.\n"
  "\n"
  "The binding bar was then 38,040 with timing met.\n"
  f"{L} has replaced it.\n"
  "\n"
  "[M0s](MARK_II_AREA_PLAN.md#lane-sequence) is owned"),
 # 497
 ("Growth remains visible across the default flip.\n"
  f"M9 re-records only after meeting {L} with timing met.\n"
  "An improvement recommendation",
  "Growth remains visible across the default flip.\n"
  "\n"
  f"M9 re-records only after meeting {L}'s Mark II ceiling.\n"
  "Timing must also be met.\n"
  "\n"
  "An improvement recommendation"),
]
for old, new in EDITS:
    if s.count(old) != 1:
        sys.exit(f"expected one match, found {s.count(old)}: {old[:90]!r}")
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
