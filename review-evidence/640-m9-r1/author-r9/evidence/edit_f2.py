"""F2: each page states the transition and end state, or points at the split contract."""
import sys
ROOT = "$LANES/640-mark2-charter/"
HDR_OLD = ("This page describes the all-fabric shipping placement.\n"
 "[Mark II placement](../ARCHITECTURE_HW_SW_SPLIT.md#1-ownership-rule) is build-selectable per control function.\n"
 "Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.\n"
 "All-fabric remains supported and the shipping default until F2 to F5 acceptance.\n"
 "That acceptance covers all streams, counters and the audio soak.\n")
HDR_NEW = ("This page describes the all-fabric shipping placement.\n"
 "It stays the shipping default until F2 to F5 acceptance.\n"
 "\n"
 "That acceptance covers all streams, counters and the audio soak.\n"
 "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md#1-ownership-rule) defines the transition and end state.\n")
EDITS = {
 "docs/design/MAAP_FABRIC.md": [(HDR_OLD, HDR_NEW)],
 "docs/fpga/DATAPLANE_WALKTHROUGH.md": [(HDR_OLD, HDR_NEW)],
 "docs/fpga/FPGA_DESIGN.md": [(HDR_OLD, HDR_NEW)],
 "docs/overview/SYSTEM_DOMAIN_MAP.md": [(HDR_OLD, HDR_NEW)],
 "docs/litex/LITEX_SOC.md": [(HDR_OLD, HDR_NEW + "\n")],
 "docs/traceability/ieee8021q.md": [
  (HDR_OLD, HDR_NEW),
  ("  Mark II permits firmware placement while retaining one selected owner.\n",
   "- Mark II moves reservation to firmware after the switch-over.\n"),
 ],
 "README.md": [(
  "[Mark II](docs/ARCHITECTURE_HW_SW_SPLIT.md) selects each control function at build time.\n"
  "ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.\n"
  "AECP includes descriptor serving, unsolicited notifications and counter serving.\n"
  "Framing, timestamps, ingress filtering, gPTP and media remain in fabric.\n"
  "All-fabric stays supported and the shipping default until F2 to F5 acceptance.\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "F0/F1 are merged foundations; no shipping placement changes here.\n",
  "[Mark II](docs/ARCHITECTURE_HW_SW_SPLIT.md) firmware runs ADP, ACMP, AECP, MAAP and SRP.\n"
  "AECP includes descriptor serving, unsolicited notifications and counter serving.\n"
  "\n"
  "Until the switch-over, each has build-selectable placement with one owner.\n"
  "All-fabric stays the shipping default until F2 to F5 acceptance.\n"
  "\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "After the switch-over, no all-fabric build remains.\n"
  "\n"
  "Framing, timestamps, ingress filtering and media remain in fabric.\n"
  "gPTP stays in fabric until F6, then moves to firmware.\n"
  "\n"
  "F0/F1 are merged foundations; no shipping placement changes here.\n")],
 "docs/overview/FULL_FPGA_SOLUTION.md": [(
  "One bare-metal RV32 core boots and configures that image.\n"
  "Mark II defaults control protocols to the core through packet mailboxes.\n"
  "ADP, ACMP, AECP, MAAP and SRP remain selectable per function.\n"
  "Audio, gPTP, framing, timestamps and ingress filtering remain in fabric.\n"
  "All-fabric remains supported and the shipping default until F2 to F5 acceptance.\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines these requirements.\n"
  "The implementation inventory below describes the current shipping build.\n",
  "One bare-metal RV32 core boots and configures that image.\n"
  "\n"
  "Mark II firmware runs ADP, ACMP, AECP, MAAP and SRP.\n"
  "Packet mailboxes carry their frames to the core.\n"
  "\n"
  "Until the switch-over, each has build-selectable placement with one owner.\n"
  "All-fabric stays the shipping default until F2 to F5 acceptance.\n"
  "\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "After the switch-over, no all-fabric build remains.\n"
  "\n"
  "Audio, framing, timestamps and ingress filtering remain in fabric.\n"
  "gPTP stays in fabric until F6, then moves to firmware.\n"
  "\n"
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines these requirements.\n"
  "The implementation inventory below describes the current shipping build.\n")],
 "docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md": [(
  "The current shipping placement keeps control traffic in fabric.\n"
  "Mark II passes selected control frames through filtered packet mailboxes.\n"
  "ADP, ACMP, AECP, MAAP and SRP are selectable per function.\n"
  "Its default is bare-metal control; all-fabric remains supported.\n"
  "All-fabric stays the shipping default until F2 to F5 acceptance.\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md#packet-mailbox-interface) defines the mailbox boundary.\n"
  "Framing, timestamps, gPTP and media remain fabric responsibilities.\n"
  "The generic classifier/queue/CBS input remains inactive in today's shipping boundary.\n",
  "The current shipping placement keeps control traffic in fabric.\n"
  "It stays the shipping default until F2 to F5 acceptance.\n"
  "\n"
  "That acceptance covers all streams, counters and the audio soak.\n"
  "After the switch-over, no all-fabric build remains.\n"
  "\n"
  "Mark II passes selected control frames through filtered packet mailboxes.\n"
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md#packet-mailbox-interface) defines the mailbox boundary.\n"
  "\n"
  "Framing, timestamps and media remain fabric responsibilities.\n"
  "gPTP stays in fabric until F6, then moves to firmware.\n"
  "\n"
  "The generic classifier/queue/CBS input remains inactive in today's shipping boundary.\n"),
  ("Bare-metal firmware accesses the AXI-Lite Milan window for initialization,\n"
   "policy, state snapshots, and diagnostics. Interrupt status remains available\n"
   "in the CSR block. Media and gPTP progress remain firmware-independent.\n",
   "Bare-metal firmware accesses the AXI-Lite Milan window.\n"
   "It covers initialization, policy, state snapshots and diagnostics.\n"
   "\n"
   "Interrupt status remains available in the CSR block.\n"
   "Media progress remains firmware-independent.\n"
   "\n"
   "gPTP progress does too, until F6.\n"
   "\n"),
 ],
 "docs/GLOSSARY.md": [
  ("The current fabric placement serves the feature-ledger inventory; Mark II selects firmware or fabric, including notifications and counters.",
   "The current fabric placement serves the feature-ledger inventory; after the switch-over, Mark II firmware serves it, including notifications and counters."),
  ("| **gPTP** | IEEE 802.1AS generalized precision time protocol. The fabric plane is the sole product owner. |",
   "| **gPTP** | IEEE 802.1AS generalized precision time protocol. The fabric plane is the sole product owner until F6; firmware then owns the protocol and servo. |"),
 ],
 "docs/design/AREA_BUDGET.md": [(
  "All-fabric remains supported and remains the current shipping default.\n"
  "The flip requires F2-F5 suites and bench acceptance.\n"
  "[#664](https://github.com/kebag-logic/milan-fpga/issues/664) governs that qualification.\n"
  "Unqualified functions retain fabric placement.\n"
  "The hard-core port remains milestone 13.\n",
  "\n"
  "All-fabric remains the current shipping default until the flip.\n"
  "After the flip, no all-fabric build remains.\n"
  "\n"
  "The flip requires F2-F5 suites and bench acceptance.\n"
  "[#664](https://github.com/kebag-logic/milan-fpga/issues/664) governs that qualification.\n"
  "\n"
  "The hard-core port remains milestone 13.\n")],
 # Found by the sweep, not listed by the review: the same claim.
 "docs/ENDSTATION_BUILDER.md": [(
  "This page describes the current all-fabric shipping build.\n"
  "The [split target](ARCHITECTURE_HW_SW_SPLIT.md) adds selectable control placement.\n"
  "Its static control contexts use the same generated entity shape.\n"
  "The default changes only after F2 to F5 acceptance.\n",
  "This page describes the current all-fabric shipping build.\n"
  "The default changes only after F2 to F5 acceptance.\n"
  "\n"
  "The [split contract](ARCHITECTURE_HW_SW_SPLIT.md) defines the transition and end state.\n"
  "Split static control contexts use the same generated entity shape.\n")],
 "docs/integration/INTEGRATION_GUIDE.md": [(
  "The [split target](../ARCHITECTURE_HW_SW_SPLIT.md) selects each control owner.\n"
  "It preserves media and gPTP interfaces.\n",
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines the transition and end state.\n"
  "It preserves media interfaces, and gPTP interfaces until F6.\n")],
 "docs/design/GPTP_PLANE.md": [(
  "Fabric gPTP owns product time synchronization.\n",
  "Fabric gPTP owns product time synchronization until F6.\n"
  "The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines that transition.\n")],
}
pending = {}
for page, edits in EDITS.items():
    s = open(ROOT + page, encoding="utf-8").read()
    for old, new in edits:
        if s.count(old) != 1:
            sys.exit(f"{page}: expected one match, found {s.count(old)}: {old[:80]!r}")
        s = s.replace(old, new)
    pending[page] = s
for page, s in pending.items():
    open(ROOT + page, "w", encoding="utf-8").write(s)
print(" ".join(EDITS))
