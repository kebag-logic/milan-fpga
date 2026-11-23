STATUS (2026-11-23 07:45 CET): DONE. REVIEW READY posted on #972 (issuecomment-7093468235), naming both local
heads: milan-fpga `pf-972-1` at `77a74b2f4e`, tsn-c-stack `970-gm-change-draw-kind` at `5585226`. Every gate passes
(receipts/FINAL-GATES.txt). The host crashed at 00:39 during the native sweep: shard 2/4, cut before its verdict, was
rerun whole from a cleaned clone (05:47 to 07:33, 17 of 17 suites, 284,336 checks, 0 failures); the sweep is 65 of 65
suites, 2,713,969 checks. Nothing else was cut: shards 0, 1, 3 and every other gate had finished with recorded
verdicts before 00:39. Nothing pushed; the manager pushes. PR bodies: PR-BODY.md (#974), PR-BODY-stack.md (#36).

Scope interpretation: the manager requires the **effective link** unqualified from reset. The MAC
status bit supplies that qualification barrier. LINK_CTRL[0] and the guard retain their values; the
integration leg observes both and demonstrates that they cannot override the down MAC status.
The split has no fabric MAAP engine: firmware MAAP follows mailbox LINK. This is an implementation
of the published effective-link requirement, not a proposed acceptance exception.

## Findings and fixes

| Finding | Cause and correction | Evidence |
|---|---|---|
| R890-1-F1 / R889-1-F1 | Retained ANAR/GCTRL did not prove BMCR enabled negotiation. Require AN enabled and reset/isolate clear before skipping a restart; refuse forced publication on the managed gigabit PHY. | P22/P23 fail 27/13 checks against `0f508a01` and pass here; the exact reviewer probe passes here. Healthy P19 retains zero redundant restarts. |
| R890-1-F2 / R889-1-F2 | Reset-up MAC status enabled the datapath before the arm. Reset the managed split status down; exercise retained clocks and refused publication at both shapes. | Four linkreset arms pass. Premature reset-up produces an early Pdelay_Req and fails both plants. Generated routed status is `4'd12`. |
| R890-1-F3 / R889-1-F3 | Review-label residue in the ADP plant comment. | Replaced with `# #970:`. |
| R891-1-F1 | A2 recorded draw kind without proving a fresh draw. | Stack `a.draws == draws + 1u`; the no-draw plant escapes `61a504e` and is caught at `5585226`. |
| R891-1-F2 | Review-label residue in the stack changelog. | Removed; stack privacy/docs gates pass. |
| R889-1-S1 (optional) | Fixed-seed spread checks are not a statistical proof. | No test change; document the finite regression scope. |

## Changed files and reasons

First changed line in each file relative to round 2; exact diffs belong in receipts/change/.

| File:line | Reason |
|---|---|
| `CHANGELOG.md:66` | Record the reset and BMCR contract. |
| `docs/design/CSR_REGISTER_NOTES.md:164` | Explain the split reset-down qualification. |
| `docs/reference/FR_NFR.md:217` | Apply reset-down and verified negotiation to the discovery derivation. |
| `docs/reference/REGISTER_MAP.md:522` | Regenerated MAC status descriptions. |
| `scripts/register_descriptions.json:1066` | Authoritative reset values by PHY ownership. |
| `sw/firmware/ctrl/plat/README.md:106` | Document the no-restart preconditions and reset-down state. |
| `sw/firmware/ctrl/plat/ctrl_plat_phy.c:38` | Check BMCR on both the skip and publication paths; share MDIO address bits and renegotiation code to preserve ROM fit. |
| `sw/firmware/ctrl/plat/ctrl_plat_phy.h:9` | Document BMCR, PHY publication and reset semantics. |
| `sw/firmware/ctrl/test/adp_first_mutants.py:40` | Remove the review label while retaining the #970 behavior explanation. |
| `sw/firmware/ctrl/test/phy_peer.hpp:70` | Start the host PHY fixture with the actual split reset value. |
| `sw/firmware/ctrl/test/plat_arms.py:85` | Import the product reset into both platform host-test shapes. |
| `sw/firmware/ctrl/test/plat_mutants.py:454` | Add five BMCR plants; update moved anchors and named kills. |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:97` | Check link qualification from reset and identity refusal; correct link-counter expectations. |
| `sw/firmware/ctrl/test/test_plat_phy.cpp:17` | Add P22/P23 and restate forced-mode/reset checks. |
| `sw/litex/mac_link_status.py:1` | Centralize reset fields; firmware-owned PHY starts down, other builds retain reset-up. |
| `sw/litex/milan_soc.py:47` | Apply the ownership-dependent reset to the actual MAC status CSR. |
| `tb/verilator/ctrl_split_boot/README.md:60` | Record measured reset-down boot behavior and figures. |
| `tb/verilator/ctrl_split_boot/boot_soc.py:25` | Use the product reset in the split boot stand-in. |
| `tb/verilator/ctrl_split_boot/run.py:34` | Align PHY-publication diagnostics and comments with reset-down. |
| `tb/verilator/milan_dp/Makefile:910` | Build and run the retained-link integration leg at both shipping shapes. |
| `tb/verilator/milan_dp/README.md:116` | Document the leg, parameters, measured outcomes and omitted components. |
| `tb/verilator/milan_dp/gen_gptp_leg_ucode.py:5` | Parameterize stream counts for the 8x8 leg. |
| `tb/verilator/milan_dp/linkreset_plants.py:1` | Plant premature status qualification and require actual early-transmit failures. |
| `tb/verilator/milan_dp/linkreset_probes.vlt:1` | Expose effective link, LINK_CTRL and guard observations without driving them. |
| `tb/verilator/milan_dp/sim_link_reset.cpp:1` | Observe MAC output and link qualification from reset through successful or refused publication. |

Stack correction: `tests/test_adp.cpp:138` requires one new draw; `tests/mutations.json:378` registers
`gm-change-rearms-without-a-draw`; `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated;
`docs/VERIFICATION.md:24` counts 475 core plants; `CHANGELOG.md:5` drops the review label.
No stack production source or constant changes. Parent gitlink remains `715589c1`.

## New checks, planted defects and required failing words

| Check | Plant | Failing words |
|---|---|---|
| P22 forced retained advertisement | `plat-phy-held-ignores-bmcr` | `P22 the boot's first poll restarts a forced PHY` |
| P22/P23 isolate | `plat-phy-isolate-negotiates` | `P22 the boot's first poll restarts a PHY not negotiating, case 3`; `P23 an isolated PHY is published down` |
| P22 reset | `plat-phy-reset-negotiates` | `P22 the boot's first poll restarts a PHY not negotiating, case 4` |
| P23 later forced mode / lost restart | `plat-phy-forced-published` | `P23 a forced mode on a PHY the advertisement is for is published down`; `P23 the forced link a lost restart left is published down` |
| P23 unmanaged advertisement compatibility | `plat-phy-forced-on-unadvertised` | `P23 a PHY the advertisement is not for: the forced mode BMCR names` |
| Retained-link integration, both shapes | `premature-qualification` | `no frame crosses the MAC boundary before the firmware's publication` |
| Stack A2 fresh GM_CHANGE draw | `gm-change-rearms-without-a-draw` | `A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)` |

The reviewer-supplied forced-speed failure at the preceding head is retained in `receipts/tests/reviewer-forced-at-0f508a01.txt`, with its report identity. Its matching current-head pass is in `receipts/tests/reviewer-forced-scenario.txt`. The P22/P23 old-code regression was separately reproduced in this lane.

The host L4/B11 checks start from reset and exercise identity refusal. The same reset-up defect
is observed at the actual transmit boundary by linkreset. P20 still detects removal of the arm's
write (`plat-phy-arm-publishes-nothing`: `P20 arming publishes link down`), covering CPU-only reset.
The earlier group G tests retain both GM orders, literal 4,000/2,000 ms bounds and available_index;
registered plants remain in the full firmware campaign.

## Gate table

| Gate | Head | Current result |
|---|---|---|
| Firmware gate, all four shards | `77a74b2f` | 0: PASS; 1: PASS; 2: PASS; 3: PASS |
| Parent default suite sweep, four shards | `77a74b2f` | PASS, 65 of 65 suites, 2,713,969 checks; shard 2 rerun after the host crash |
| Synthesis portability | `77a74b2f` | PASS |
| fw_coverage self-test/check | `d9e1d728` | PASS, 40 files; later changes do not touch covered firmware |
| Twin, plants, maps, map plants | `d9e1d728` | PASS, all four targets |
| Linkreset and premature qualification plants | `77a74b2f` | PASS, four arms and 2/2 plants |
| Split boot, both shapes and native controls/plants | `77a74b2f` | PASS, 6/6 native controls, 7/7 plants, 8/8 placement controls |
| Platform images, four ledger points | code `93d9eaaf` | PASS, RAMB36 45/46/58/63; ROM +40 B; size fixtures unchanged |
| CPU budget comparison, nine groups per shape | `fc7504f1` | PASS, 63 paired probes per shape identical; 0 changed verdicts or budget misses |
| Routes, three directives per shape | `93d9eaaf` | PASS, 6/6 meet #818 at all four corners; selected ExtraPostPlacementOpt at both shapes |
| Docs workflow | `77a74b2f` | PASS, 104/104; tracked files unchanged |
| Builder legs 0/1 | `d9e1d728` | PASS except one explicitly declared NOT RUN arm each |
| RTL lint / behavior scenarios / synthesis front end | `77a74b2f` | PASS, 89 findings within unchanged ratchet; 511/511 scenarios, 2,346 steps; front end 0 findings |
| Stack validate with graphs / baremetal | `5585226` | PASS, 28/28 gates, 479 CAUGHT, 0 ESCAPED, 0 ERROR; Debug/Release pass |

Completed evidence and commands are in [receipts/INDEX.md](receipts/INDEX.md); refreshed after the last gate.
The original documentation run found two idiom violations; commit `77a74b2f` fixed them and all
104 steps passed on rerun. An intermediate firmware layout exceeded its ledger; code sharing
in `93d9eaaf` restored fit without changing an approved bound.

## Limits and manager duties

- This is source-head validation. Hosted/act acceptance, correction review, candidate-merge
  validation, merge, containment and the physical discovery rerun remain with the manager.
- No bench or board was accessed. The 6.0 s physical discovery acceptance is not claimed passed.
- CPU harness images are byte-identical and their 63 probe values match. That harness excludes
  the platform PHY, so it is not a measurement of the changed PHY code. The split boot simulation
  measures that code's publication path separately.
- 8x8/1if ROM is exactly 139,264 bytes of 139,264. Its existing 58-RAMB36 firmware ledger is met;
  the recorded resource debt and routed fit/timing gates are retained.
- The linkreset model omits the physical PHY, CPU and mailbox, and models the existing two-flop
  status crossing. It executes the real datapath and firmware CSR policy, checks mailbox LINK
  output and actual MAC transmit output. It is invoked by name outside the hosted ordinary cases.
- All-fabric/no-MDIO builds retain reset-up; the all-fabric initialization path is unchanged.
- No push, PR creation/edit or merge is authorized or performed. The single round-3 REVIEW READY
  comment (issuecomment-7093468235) names both local heads.

## Local commits

```text
77a74b2f4e Hold the new test code to the idiom ratchets: one declarator a declaration, a documented main, a short line, the BMCR plants their own table (#840, #972)
1175c70ab9 Record the boot simulation's figures at the #840 BMCR rule's head in its README (#972, #840)
d9e1d72899 Name the split's MAAP as the firmware's, on the mailbox LINK level, where the docs listed a fabric engine (#972)
fc7504f133 State the split's link-down reset and #840's BMCR rule in the register map, CSR notes, FR_NFR, READMEs and change log (#972, #840)
3cfbc13290 Check from reset at 1x1/1if and 8x8/1if that the split datapath sends nothing before the link's publication, with a planted reset at link up (#972)
93d9eaaf32 Share the MDIO command's address bits and one renegotiation site, so 8x8/1if keeps its 58 RAMB36 (#840)
af7fd6e43f Drop a review label from a planted defect's comment (#970)
eeef34af54 Restart a PHY whose BMCR does not negotiate and never publish a forced mode up (#840, #972)
4f85fbd95f Reset the MAC link-status word to link down where the split's firmware owns the PHY (#972)
```

Stack: `55852269db3554900d2b71e6f9a7b153cff69e14` on `61a504e`.

REVIEW READY 77a74b2f4e289c5a5a89687e07a6925cfedf6860 55852269db3554900d2b71e6f9a7b153cff69e14
