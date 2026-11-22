[A820] REVIEW READY
Commits, both local; the manager pushes:
- milan-fpga `pf-972-1` at `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b`: six commits on `dd163e41`, code head `48c39b5b`, the tsn-c-stack gitlink unchanged at `715589c1`.
- tsn-c-stack `970-gm-change-draw-kind` at `61a504e`: one commit on main `715589c1`, no `src/` or `include/` change.

Round-1 branch `pf-970-1` is not continued, following the ruling on #970.

#972, cause (from the code, measured in the split boot simulation):
- `milan_mac_link_status` resets to link up. The PHY poll's first publication came only with the first probe's miss, 27.3 ms after reset at 1x1, so until then the datapath's effective link was up: the gPTP plane's port, the fabric MAAP engine and the mailbox LINK level all followed it.
- The poll then restarted autonegotiation at every boot whatever the PHY held. Anything sent on the link formed before the restart went out on a link that then dropped. ADP's LINK_UP came only after the renegotiation.

Changed (`sw/firmware/ctrl/plat/ctrl_plat_phy.c:38-41`, docs in `ctrl_plat_phy.h` and the platform README):
- The arm publishes link down before its first frame: at 2.636 ms at 1x1 and 4.434 ms at 8x8. The datapath therefore sees no link until a poll publishes the PHY's verified one, and ADP starts DOWN.
- The arm owes the advertisement without its restart. At boot, as after a loss, registers 9 and 4 are written and read back, and negotiation restarts only where they did not hold it, so the boot forms the link once.
- THE OUTCOME is unchanged, so #840's link speed is unchanged: 1000BASE-T full duplex only, and a 100BASE-TX-only partner gets no link.
- A bus without MDIO publishes nothing.

Tests:
- Host P19: a PHY holding the advertisement, linked before the boot, is never restarted and its link is published once.
- P20: the arm publishes link down before any frame.
- P21: THE OUTCOME still restarts a held advertisement whose 100 Mb/s negotiation is in force.
- P11 restated; P9: no MDIO, nothing published.
- L4: the gPTP port enable is down from the arm to the first poll.
- L2, L3 and L5 restated: the boot moves each AVB_INTERFACE link counter once, as a boot whose PHY has no link at its first poll already did.
- The boot simulation's PHY grade requires the arm's publication, with a new plant `phy-arm-unpublished`.
- Plants: `plat-phy-boot-restarts-whatever-held` (the old behaviour) and `plat-phy-arm-publishes-nothing`, plus a P21 kill on `plat-phy-outcome-unchecked`.

#970, salvaged after its ruling: group G in `test_adp.cpp`, on the unchanged core, against Milan's literal draws:
- G1/G5: 64 LINK_UPs, each first ENTITY_AVAILABLE within its 0 to 4 s draw, each quarter of the range holding at least 8; available_index +1 per frame.
- G2: 32 startups, within 0 to 2 s, each half holding at least 8.
- G3: a grandmaster change inside the delay re-arms nothing, and the frame carries the new grandmaster.
- G4: the bench's order, a change 4.5 s after LINK_UP, announced by a new ENTITY_AVAILABLE with the new gptp_grandmaster_id and the next index, its delay the 0 to 4 s kind.
- Plants, in a new `adp_first_mutants.py`: 5 new (`link-up-draws-half-a-second` among them, round 1's narrowing as a defect) and 3 moved with G kills added.
- FR_NFR 2.1.1 derives the declared 6.0 s discovery time term by term: 250 + 0 + 30 + 4,000 + 30 + 1 = 4,311 ms. The ADP slice and the tests cite it.

tsn-c-stack (R887-1-F1): A2 asserts that GM_CHANGE in WAITING enters DELAY with the 0 to 4 s kind. The plant `gm-change-draws-startup-kind` passes all 10 binaries at the base and is caught at `61a504e`.

Validation:

| Gate | Result |
|---|---|
| Firmware gate, four shards, at `48c39b5b` | PASS: 75 of 75 suite verdicts; control campaign 832 of 832 caught; AECP 385 and SRP 543 `[ok]`; 0 escaped |
| `fw_coverage` | PASS, 40 files |
| Twin and its three plant and map legs, at `48c39b5b` | PASS, 0 findings |
| Split boot simulation at `ba0f80ed` | 1x1 and 8x8 PASS; the arm's link down at 2.636 / 4.434 ms, before the first frame at 27.125 / 66.186 ms; self-test 6 of 6 native controls, 7 of 7 plants |
| `plat_ledger` on base and head | PASS, RAMB36 45 / 46 / 58 / 63 unchanged, rom +16 B |
| Image diff | `ctrl_plat_phy.o` alone in the platform images, the size fixtures byte-identical |
| CPU budget legs, 9 groups, 1x1/1if and 8x8/1if | the harness images are byte-identical to the base; every figure of the 63 probes equal, 0 verdicts changed, 0 misses |
| Docs workflow steps at `0f508a01` | 104 of 104, tracked files unchanged |
| Builder leg 0 at `ba0f80ed`, leg 1 at `0f508a01` | PASS, each with the one NOT RUN arm the tree declares on this host |
| tsn-c-stack `validate.py --graphs` and `baremetal.py` at `61a504e` | rc 0 (28 of 28) and rc 0; 478 of 478 plants caught |

The commits after `48c39b5b` change only the boot simulation's stand-in and README and the documentation audit; the firmware gate, the twin and the images read none of them.

Acceptance criteria (#972):
- The boot path forms the link once: met (P19, P11; `plat-phy-boot-restarts-whatever-held` caught).
- The datapath does not transmit before the firmware has published the link: met from the arm on (P20, L4, the boot simulation's grade and plant). The window before it is in open question 1.
- A host test or the split boot simulation covers both the restart and no-restart paths, with planted defects: met (P11, P14, P17 for the restart; P19, P21 for none; the boot simulation the restart path).
- #840's link-speed behaviour unchanged: met (P11 to P18 and P21 pass; THE OUTCOME unchanged).
- The bench, first ENTITY_AVAILABLE within the declared discovery time at 1x1/1if and 8x8/1if: not run here (no bench access). It is the manager's re-run after merge, with FR_NFR 2.1.1 as the derivation.

Open risks and questions:
1. From the datapath's reset to the arm, 2.6 ms at 1x1 and 4.4 ms at 8x8, the word holds its reset value, link up. A power-up's or a REBOOT's PHY has no link then. A gateware reload that keeps the PHY's link could let a frame out in that window. Closing it needs the word's reset value at link down (`milan_soc.py`), which is gateware (RTL) and outside this lane. Decision needed.
2. The release (all-fabric) image's PHY init still restarts at every boot; #972 is the split's boot path.
3. The two branches are independent, and either can merge first. The tsn-c-stack branch changes no source, so the parent needs no pin move for it.
