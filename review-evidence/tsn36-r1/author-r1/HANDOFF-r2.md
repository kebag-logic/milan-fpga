# HANDOFF r2 — #972 (and the #970 salvage) ([A820])

STATUS (18:40 CET 2026-11-22): **REVIEW READY**. milan-fpga `pf-972-1` at `0f508a01`; tsn-c-stack
`970-gm-change-draw-kind` at `61a504e`. Every gate passes (section 5). ETA: none, round done. No unit of this lane is
left running. Nothing pushed; no PR opened (the manager's: PR-BODY.md, PR-BODY-stack.md).
Posted: `[A820] TAKEN` on #972, issuecomment-7080869589 (TAKEN-972-comment.md), and `[A820] REVIEW READY` on #972
issuecomment-7082983553 (REVIEW-READY.md).

Round 2 follows the [A10] ruling on #970 (issuecomment-7080789556):
- the narrowed first draw of round 1 is not conformant;
- tsn-c-stack#35 is closed without merge;
- round-1 branch `pf-970-1` is not to be merged and is left as it was. Its tsn-c-stack branch `970-first-advertise`
  stays local and unused.

## Branches (local commits only)
milan-fpga `pf-972-1`, from `dd163e41`, with the tsn-c-stack gitlink unchanged at its pin `715589c1`:
- `1d8bcfa2`: #972, the boot path forms the link once and publishes link down at the arm; host tests, plants, the
  boot simulation's grade and plant, the platform README.
- `e69e20d4`: #970's grandmaster-order tests (group G) on Milan's literal draws, with their plants.
- `48c39b5b`: FR_NFR 2.1.1, the declared 6.0 s discovery time derived; the ADP slice and the change log cite it.
- `3cfc2cd8`: the boot simulation's native-control stand-in prints the arm's publication its grade now requires.
- `ba0f80ed`: the boot simulation README: the grade, the new plant, this head's figures.
- `0f508a01`: the documentation audit regenerated for FR_NFR's new references (`docs_inventory.py --write`).

tsn-c-stack `970-gm-change-draw-kind`, from main `715589c1`: `61a504e` (R887-1-F1). It lives in the lane's submodule
repository (`third_party/tsn-c-stack`), with a worktree at `/data-2/milan/tmp/970-a820/stack-wt`. The submodule's
checkout itself stays detached at the pin.

## 1. #972: cause and fix
Before this change the boot path had two faults. Both come from the code and are measured in the split boot
simulation:
- `milan_mac_link_status` resets to link up (`sw/litex/milan_soc.py`, MilanMAC). The poll's first publication came
  only with the first probe's miss, 27.3 ms after reset at 1x1 and just before READY. Until then the datapath's
  effective link was up. That link drives the gPTP plane's port enable, the fabric MAAP engine and the mailbox LINK
  level (`hdl/milan/milan_datapath.sv` `eff_link_w`). ADP even drew a startup delay on it.
- The poll restarted autonegotiation at every boot whatever the PHY held (`adv = OWED | RENEGOTIATE` at the arm).
  Any frame sent on the link formed before the restart went out on a link that then dropped. ADP's LINK_UP came
  only after the renegotiation.

The fix:
- `sw/firmware/ctrl/plat/ctrl_plat_phy.c:38-41`: `ctrl_plat_phy_arm` writes link down to the word first, right after
  the identity check and before any frame, then owes the advertisement without its restart (`ADV_OWED`).
  - The restart decision at `ADV_SET_LOCAL` (`:225-232`, unchanged code, comment restated) now applies at boot as
    after a loss: a restart only where registers 4 and 9 did not hold the advertisement.
  - THE OUTCOME (`GIG_PEER`) is unchanged: a negotiation in force that shares no 1000BASE-T mode is published down
    and restarted. So #840's behaviour stands: 1000BASE-T full duplex only, and a 100BASE-TX-only partner gets no
    link (P21, P17, P18).
  - A bus with no MDIO pair returns before the write and keeps the reset value, the only link such a board has (P9).
- Docs: `ctrl_plat_phy.h:47-73` (THE ADVERTISEMENT restated; THE LINK BEFORE THE FIRST POLL, new), the `adv` field and
  `ctrl_plat_phy_arm` comments; `sw/firmware/ctrl/plat/README.md` (the new bullet, THE ADVERTISEMENT, the `platboot`
  test list).

Measured in the split boot simulation:
- the arm's link down is published at 2.636 ms (1x1) and 4.434 ms (8x8);
- that is before the first frame (27.125 and 66.186 ms) and before READY (27.978 and 67.228 ms);
- the base `dd163e41` published nothing before its first frame.

Consequences, stated and tested:
- The boot's publications move the AVB_INTERFACE LINK_DOWN and LINK_UP counters once each, and the gPTP port enable
  falls at the arm and rises at the first poll. A boot whose PHY has no link at its first poll (power-up, REBOOT)
  already moved them so at the base. L2, L3 and L5 are restated against that; L4 checks the port enable.
- A PHY at its defaults (10/100 advertised) is still written and restarted once (P11, P14), as #840 requires. The
  renegotiation now comes before the first publication, so nothing is sent on the link it drops.

Residual, an open decision and not changed here: from the datapath's reset to the arm, 2.6 ms at 1x1 and 4.4 ms at 8x8,
the word holds its reset value, link up. A power-up's or a REBOOT's PHY has no link then. A gateware reload that keeps
the PHY's link could let a frame out in that window. Closing it needs the word's reset value at link down in
`milan_soc.py`, which is gateware (RTL) and outside this lane. The reset value also serves boards with no MDIO.

## 2. #970's salvage (the ruling, item 4)
`sw/firmware/ctrl/test/test_adp.cpp:555-852` holds group G; the tests are at `:939-952`. It runs on the unchanged core.
The literals are `kLinkUpDrawMaxMs` 4000 (Milan 5.6.3.5.3), `kStartupDrawMaxMs` 2000 (5.6.3.5.2), `kDelayMaxMs` 4000 and
`kDiscoveryMs` 6000 (FR_NFR 2.1.1).

| Test | Holds | Measured at the head |
|---|---|---|
| G1/G5 `WithinTheLinkUpDrawOfEveryLinkUp` | 64 LINK_UPs: each first ENTITY_AVAILABLE within its draw (+2 ms of passes), inside 6.0 s; each quarter of 0 to 4 s holds at least 8 of 64; available_index +1 per frame across link-ups; the TMR_ADVERTISE delays 0 to 4 s, each quarter at least 8 | latest 3,990 ms; quarters 17/9/19/19; TMR_ADVERTISE 18/11/15/20 |
| G2 `WithinTheStartupDraw` | 32 startups (32 entity IDs): within 0 to 2 s; each half at least 8 of 32 | latest 1,981 ms; halves 18/14 |
| G3 `AGrandmasterChangeBeforeItIsCarriedByIt` | a change inside the delay re-arms nothing: the frame leaves at the LINK_UP's own deadline (the model's timer log) and carries the new GM | latest 3,649 ms |
| G4 `AGrandmasterChangeAfterItIsAnnounced` | the bench's order, a change 4.5 s after LINK_UP, in WAITING: a delay at once; a new ENTITY_AVAILABLE with the new GM and the next index within 4 s; the change's delay passes 2 s across 32 link-ups (its 0 to 4 s kind) | new GM within 3,994 ms |

G4's split by halves was 6 to 26. It is not used as a uniformity check: uniformity is held by G1, G5 and G2. G4 holds
the kind.

Plants, in `sw/firmware/ctrl/test/adp_first_mutants.py` (new). Three plants with G kills added were moved out of
`ctrl_mutants.py`, which was at the idiom ratchet's 1,000-line module limit (now 989 lines):

| Plant | Caught by | Failing words |
|---|---|---|
| `gm-change-ignored` (moved; new kill) | walk GM_CHANGE_x_WAITING; adp G4 | "GM_CHANGE x WAITING"; "G4 a grandmaster change after the first ENTITY_AVAILABLE starts a delay at once" |
| `link-up-draws-startup-kind` (moved; new kill) | walk LINK_UP_x_DOWN; adp G1 | "LINK_UP x DOWN"; "G1 the LINK_UP delay is spread over 0 to 4 s" |
| `draw-kinds-merged` (moved; new kill) | adp A9; adp G2 | "A9 every startup draw"; "G2 the first ENTITY_AVAILABLE, index 0, leaves within its 0 to 2 s draw" |
| `link-up-draws-half-a-second` (round 1's narrowing as a defect) | adp G1 | "G1 the LINK_UP delay is spread over 0 to 4 s" |
| `first-delays-not-drawn` | adp G2 | "G2 the startup delay is spread over 0 to 2 s" |
| `gm-change-in-delay-restarts-the-delay` | adp G3 | "G3 a grandmaster change before the first ENTITY_AVAILABLE re-arms nothing" |
| `gm-change-draws-the-startup-kind` | adp G4 (the stack's suite does not see it: R887-1-F1) | "G4 the grandmaster change's delay is the 0 to 4 s draw" |
| `link-loss-resets-the-index` | adp G1 (the only test that sees it) | "G1 each ENTITY_AVAILABLE carries the next available_index, across every link-up" |

#972's plants (`plat_mutants.py`):

| Plant | Caught by | Failing words |
|---|---|---|
| `plat-phy-boot-restarts-whatever-held` (the old behaviour; replaces `plat-phy-boot-restart-dropped`, which planted the fix) | P19; P11 | "P19 the boot restarts no negotiation the PHY already holds"; "P11 a PHY that holds the advertisement at boot is not restarted" |
| `plat-phy-arm-publishes-nothing` | P20; L4 | "P20 arming publishes link down"; "L4 the port enable falls as the poll arms and rises with its first publication" |
| `plat-phy-outcome-unchecked` (existing; new kill) | P18; P21 | "P18 no link at 100 after recovery"; "P21 THE OUTCOME owes the restart the boot did not take" |
| boot simulation `phy-arm-unpublished` (new) | the PHY grade | "PHY: no link down published before the first MDIO frame" |
| boot simulation `phy-unadvertised` (anchor moved) | the PHY grade | as before |

The control campaign goes from 826 to 832 plants, and each is caught: shard 1, 832 of 832.

## 3. FR_NFR 2.1.1: the declared discovery time
`docs/reference/FR_NFR.md:199-220`. Each term is cited:

| Term | Bound |
|---|---:|
| The link publication (the release's bound, graded by the boot simulation) | 250 ms |
| The PHY link time (the link guard's 41.94 ms settle, inside the publication) | 0 added |
| The LINK event to TMR_DELAY armed (ADP's row bound) | 30 ms |
| TMR_DELAY, uniform (Milan 5.6.3.5.3, Table 5.50; IEEE 1722.1-2021 6.2.4.2.2) | 4,000 ms |
| The expiry to the frame (ADP's row bound) | 30 ms |
| `CTRL_LOOP_T_EGRESS_MS` | 1 ms |
| **Sum** | **4,311 ms**, 1,689 ms under 6.0 s |

The startup draw (2 s) is less, and a grandmaster change adds nothing. The boot path adds nothing (#972). The
all-fabric placement is not claimed. "Its use where the declared discovery time is stated": no file in the tree stated
it before. It is stated here, and cited by the ADP slice (`docs/design/MAILBOX_SPLIT.md:536-539`), the G tests
(`kDiscoveryMs`) and CHANGELOG.

## 4. tsn-c-stack `970-gm-change-draw-kind` (`61a504e`)
- A2 in `AdpCore.A0toA2Schedule` (`tests/test_adp.cpp:139-141`): after `adp_gm_change` in WAITING, the machine is in
  DELAY with `ADP_DRAW_DELAY` and an armed delay at most 4,000 ms, a literal.
- The new plant `gm-change-draws-startup-kind`.
- `docs/TESTS.md` and `TRACEABILITY.md` regenerated by their generators; VERIFICATION.md 474 core plants; CHANGELOG.
- No `src/` or `include/` change.
- Sensitivity: the plant on the base `715589c1` passes 10 of 10 binaries (R887-1-F1 reproduced). At `61a504e`,
  `adp_tests` fails with "A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)".

## 5. Gate table
milan-fpga: the code head is `48c39b5b`. After it, `3cfc2cd8` changes only the boot simulation's stand-in,
`ba0f80ed` its README and `0f508a01` the documentation audit; the firmware gate, the twin and the images read none of
them.

| Gate | Result |
|---|---|
| Firmware gate, 4 shards (`--require-rv32 --self-test`) at `48c39b5b` | PASS: 75 of 75 suite verdicts; control campaign 832 of 832 caught; AECP 385 `[ok]`; SRP 543 `[ok]`; 0 escaped |
| `fw_coverage.py --selftest`, `--check` at `48c39b5b` | PASS (40 files) |
| Twin, twin-plants, twin-maps, twin-maps-plants at `48c39b5b` | PASS: 0 findings, every plant refused |
| Split boot simulation 1x1, 8x8, `--self-test` | at `48c39b5b`: 1x1 and 8x8 PASS, every plant caught (`phy-arm-unpublished` among them); its native controls failed (0 of 6), the stand-in lacking the arm's publication (fixed by `3cfc2cd8`; `--native-controls` then 6 of 6). At `ba0f80ed`: 1x1 and 8x8 PASS (ready 27.978 / 67.228 ms; base 27.952 / 67.223), the arm's link down at 2.636 / 4.434 ms; self-test 6 of 6 native controls, 7 of 7 plants, 0 placement controls wrong |
| Platform images (`plat_ledger.py`), base and head | PASS both; RAMB36 45 / 46 / 58 / 63 unchanged; rom +16 B at every point, sram unchanged |
| Image diff, 8 pairs | platform images: only `ctrl_plat_phy.o`, `.text.ctrl_plat_phy_arm` 176 -> 192 B. The canonical listings differ by the new `ctrl_plat_io_write32(link_status, 0)` call, the owed flag (1, was 3) and one callee-saved register. The size-fixture images are byte-identical |
| CPU budget legs, 9 groups, base vs head, 1x1/1if and 8x8/1if | the harness's images are byte-identical (it links no platform PHY code): 63 of 63 probes paired at each point, every figure equal, 0 verdicts changed, 0 misses |
| Docs workflow steps | at `0f508a01`: PASS, 104 of 104, tracked files unchanged. At `ba0f80ed`: 103 of 104, `docs_inventory.py --check` stale for FR_NFR's new references, regenerated by `0f508a01` |
| Builder legs | leg 0 at `ba0f80ed` and leg 1 at `0f508a01`: PASS, each with the one NOT RUN arm the tree declares on this host (leg 0 the MAKEFLAGS note; leg 1 gate 11, the mf48 build tree not on this host). Neither reads the audit `0f508a01` changes |
| tsn-c-stack `validate.py --graphs`, `baremetal.py` at `61a504e` | rc 0 (28 of 28 gates), rc 0; mutation 478 of 478 caught |

Not run: the full Verilator sweep (no RTL or harness change; the round's gate list does not name it); Vivado (no RTL;
RAMB36 unchanged).

## 6. Open questions
1. The window before the arm (section 1): it needs a gateware decision (the link word's reset value). It is reported,
   not changed.
2. The release (all-fabric) image's PHY init still restarts at every boot. #972 is the split's boot path, so the
   release is not changed.
3. The bench re-run of the discovery scenarios is the manager's, after merge.

## 7. Receipts and posting
- `receipts/` (INDEX.md generated from the files present; host paths replaced by placeholders; nothing over 200 KB).
  The spec is `receipts/tools/receipts_spec_r2.py.txt`.
- `[A820] TAKEN`: #972 issuecomment-7080869589.
- `[A820] REVIEW READY`: #972 issuecomment-7082983553 (the text is REVIEW-READY.md).
- Nothing else posted; no existing comment edited. Nothing pushed.

REVIEW READY 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b
