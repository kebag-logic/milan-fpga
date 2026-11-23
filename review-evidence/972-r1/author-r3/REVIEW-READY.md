[A820] REVIEW READY
Commits, both local; the manager pushes:
- milan-fpga `pf-972-1` at `77a74b2f4e289c5a5a89687e07a6925cfedf6860`: nine commits on round 2's head `0f508a01` (PR #974). The code head is `93d9eaaf`; the five commits after it add the `linkreset` leg, documentation, comment corrections and idiom fixes in test code, and change no firmware or gateware code. The tsn-c-stack gitlink is unchanged at `715589c1`.
- tsn-c-stack `970-gm-change-draw-kind` at `55852269db3554900d2b71e6f9a7b153cff69e14`: one commit on round 2's `61a504e` (PR #36). No `src/` or `include/` change.

Findings and their fixes:
- R890-1-F2 / R889-1-F2, per the [A10] scope decision on #972. `milan_soc.py`'s MilanMAC now resets `milan_mac_link_status` to link down (`0xC` at the two shipping shapes) where firmware owns the PHY: the split placement with an MDIO pair. The reset values live in a new LiteX-free `sw/litex/mac_link_status.py`. All-fabric builds, and any board without an MDIO pair, keep `0xD`, link up, as named there and in the register map.
  - The effective link is that word AND `LINK_CTRL[0]` AND the link guard's estimate. The gPTP port enable and the mailbox LINK level read it; the split's firmware MAAP, ADP and SRP follow the LINK level. The split builds no fabric MAAP engine.
  - So nothing is qualified from reset until the PHY poll's verified publication: after a reload that kept the PHY's link, and on a boot refused at the CSR identity check.
  - Both routed images carry `milansoc_milanmac_link_status_storage = 4'd12`, at reset too. The all-fabric export carries `4'd13`.
- R890-1-F1 / R889-1-F1 (#840). The boot's and a loss's no-restart path now also needs BMCR as read negotiating: 0.12 set, 0.15 and 0.10 clear (`ctrl_plat_phy.c`, `negotiating()`).
  - A PHY that is forced (100, 10 or 1000 Mb/s), isolated or resetting is restarted at the boot's first poll, whatever registers 4 and 9 hold.
  - BMCR not negotiating at the poll's resolution, on a PHY the advertisement is for, is published down and renegotiated, counted. So a forced mode is never published up, a lost restart included.
  - A 10/100 PHY, which the advertisement is not for, keeps the release's forced-mode words.
  - The change first took the 8x8/1if rom 48 B past its 58 RAMB36. Sharing the MDIO command's address bits between reads and writes, and one renegotiation site, brought it back to exactly its 34 tiles.
- R890-1-F3 / R889-1-F3: `adp_first_mutants.py:40` reads `# #970:`.
- R891-1-F1 (stack): A2 now also requires a fresh draw, `a.draws == draws + 1u`. A new plant, `gm-change-rearms-without-a-draw`, re-arms with `last_draw_ms` and no draw. It escapes `61a504e` (ctest 10 of 10 pass) and is caught at `5585226` by A2's message. TESTS and TRACEABILITY are regenerated (479 plants); VERIFICATION says 475 core plants.
- R891-1-F2 (stack): the changelog names no review finding.

Tests and plants (milan-fpga):
- P22: the reviewers' forced scenario as a regression, then BMCR 0x2100, 0x0000, 0x0140, 0x1400 and 0x9000 at boot, and a loss with BMCR forced.
- P23: a forced mode or isolate with no loss; a lost boot restart on a forced PHY; a PHY the advertisement is not for.
- At `0f508a01`'s `ctrl_plat_phy.c`, P22 fails 27 checks and P23 13; here both pass. P19 still proves a PHY holding 4, 9 and BMCR 0x1000 is not restarted.
- The host fixtures start at the split's reset, read from `mac_link_status.py`. L2, L4 and B11 are restated: LINK_UP moves once at boot, the port enable is down from reset, and an identity refusal never qualifies the link.
- Five new plants (`plat-phy-held-ignores-bmcr`, `-isolate-negotiates`, `-reset-negotiates`, `-forced-published`, `-forced-on-unadvertised`); control campaign 837 of 837 caught.
- `linkreset` (`tb/verilator/milan_dp`, `make linkreset linkreset-plants`): `milan_datapath` split, gPTP plane on, each shape's export parameters, from reset with the PHY's link retained. The word is modelled at `mac_link_status.py`'s reset behind MultiReg's two flops. The firmware's own `ctrl_plat_csr.c` writes the boot's policy through the CSR window. Both shapes: 0 frames before the publication at 1,500 ms, and the gPTP plane's first Pdelay_Req 0.032 ms after it; a refused boot, 0 frames in 1,600 ms. The plant (the helper's reset at link up) is caught at both shapes: a Pdelay_Req at the plane's 1,200 ms boot cadence. Each arm also checks `LINK_CTRL[0]` and the guard qualify throughout.

Validation:

| Gate | Head | Result |
|---|---|---|
| Firmware gate, four shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`) | `77a74b2f` | PASS: 75 of 75 suite verdicts; control campaign 837 of 837 caught (round 2's 832 and the five BMCR plants); no `[FAIL]` or escaped line |
| Native suite sweep, four shards (`scripts/run_all_suites.sh --shard k/4`) | `77a74b2f` | shards 0, 1 and 3 PASS; shard 2 rerun whole after the host crash, PASS (17 of 17). In all: 65 of 65 suites (15, 17, 17, 16), 2,713,969 checks, 0 in-suite failures, 0 timed out |
| `linkreset` and `linkreset-plants` | `77a74b2f` | 4 of 4 arms PASS; 2 of 2 plants caught |
| Split boot simulation, both shapes and `--self-test` | `77a74b2f` | 1x1 and 8x8 PASS: ready 27.940 / 67.214 ms; the arm's link down at 2.637 / 4.437 ms, before the first frame at 27.096 / 66.163 ms; 6 of 6 native controls, 7 of 7 plants, 8 of 8 placement controls |
| The reviewers' forced scenario (`focused.py`) | `77a74b2f` | PASS here; their receipt fails it at `0f508a01` |
| fw_coverage `--selftest`, `--check` | `d9e1d728` | PASS, 40 files |
| Twin, `twin-plants`, `twin-maps`, `twin-maps-plants` | `d9e1d728` | PASS, 0 findings |
| `plat_ledger` and the image diff against round 2 | `fc7504f1` | PASS; RAMB36 45 / 46 / 58 / 63 unchanged; rom +40 B at each point; only `ctrl_plat_phy.o` differs; size fixtures identical |
| CPU budget legs, 9 groups, 1x1/1if and 8x8/1if | `fc7504f1` | harness images byte-identical to round 2; 63 of 63 probes equal at each shape; 0 verdicts changed; 0 misses |
| Routes, three directives at each shape (the gating recipe) | `93d9eaaf` | all six meet #818 at every corner. 1x1: ExtraPostPlacementOpt +0.331 / +0.031 ns (best), AltSpreadLogic_high +0.130 / +0.036, ExtraTimingOpt +0.133 / +0.036. 8x8: ExtraPostPlacementOpt +0.176 / +0.036 (best), AltSpreadLogic_high +0.150 / +0.036, ExtraTimingOpt +0.059 / +0.036 (worst-corner WNS / WHS). Routed `link_status_storage` `4'd12` in all six |
| Synthesis portability (Yosys) | `77a74b2f` | PASS |
| RTL lint, behaviour scenarios, xvlog | `77a74b2f` | lint PASS (89 of ratchet 89); 511 of 511 scenarios; xvlog 0 findings |
| Docs workflow steps | `77a74b2f` | 104 of 104 |
| Builder legs 0 and 1 | `d9e1d728` | PASS, each with the one NOT RUN arm the tree declares on this host (as round 2) |
| tsn-c-stack `validate.py --graphs`, `baremetal.py` | `5585226` | rc 0, 28 of 28 gates; 479 of 479 plants caught; rc 0 |

Heads: the commits after the code head `93d9eaaf` change test code, the leg, documentation and comments, no firmware or gateware code. The commits after `fc7504f1` and `d9e1d728` change no file those gates read but comments, READMEs and test-only idiom fixes; the gates that read them ran at `77a74b2f`. The host crashed at 00:39 during the native sweep; shard 2, cut before its verdict, was rerun whole from a cleaned clone, and only that rerun is counted.

Acceptance criteria (#972):
- The boot path forms the link once: met (P19, P11; `plat-phy-boot-restarts-whatever-held` caught). Holding it now needs BMCR negotiating (P22, P23 and five plants).
- The datapath does not transmit before the firmware publishes the link: met from reset in split builds (the word's reset; the `linkreset` leg at both shapes with its plant; L4, B11; the routed images' `4'd12`). Configurations without firmware PHY management keep reset-up, named.
- A host test or the split boot simulation covers both the restart and no-restart paths, with planted defects: met.
- #840's link-speed behaviour: kept and tightened. 1000BASE-T full duplex only; now no forced mode is published up either (P22, P23).
- The bench check, the first ENTITY_AVAILABLE within the declared discovery time at 1x1/1if and 8x8/1if: not run here (no bench access). It is the manager's re-run after merge, against FR_NFR 2.1.1.

Open risks and questions:
1. The effective link is held down by the MAC status reset. `LINK_CTRL[0]` and the guard retain their existing resets; the integration leg observes that both qualify while the status bit still holds every effective-link consumer down. This implements the manager's effective-link requirement without an acceptance exception.
2. The `linkreset` leg is outside the hosted case inventory (`ORDINARY_CASES`): joining it needs a hosted timing measurement. It runs by name.
3. The 8x8/1if image's rom is exactly at its 34 tiles (139,264 of 139,264 B; round 2 left 40 B). It is inside its 58-RAMB36 ledger, with no headroom.
4. R889-1-S1 (the spread checks on a fixed seed) is not taken.
5. The two branches are independent; the stack branch changes no source, so the parent needs no pin move for it.
