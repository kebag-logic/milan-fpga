[R890] NEGATIVE - exact head 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b

Round R890-1, external independent review of issue #972 / PR #974. Two MAJOR findings remain open. One source-comment RESIDUE is non-blocking. All five lenses were independently applied; none is clean because the findings cross their scopes.

Reviewed tree: `4a0fc0a2ee1159adffb276c1c00ef936c51b313f`. Reviewed delta: `dd163e41..0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b`, six commits and fifteen files. This is the requested source delta on the flip's reviewed head, not the larger PR comparison against its recorded branch base and not a current-dev merge candidate. The tsn-c-stack gitlink remains `715589c1db7cf67e2f3259fd7083ebc7f0923376`.

**Contract and independence**

The review reconstructed AGENTS.md and CONTRIBUTING.md, docs/README.md, the [issue acceptance and public scope](https://github.com/kebag-logic/milan-fpga/issues/972), the [#970 ruling](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556), REQUIREMENTS.md, FR_NFR, mailbox/platform interfaces and linked architecture, then the source delta and history, then the [published evidence packet](https://github.com/kebag-logic/milan-fpga/tree/7a5e1e9aec00736a7e7f5f3285d7f34448538e7e/review-evidence/972-r1). HANDOFF-r2.md was read only from that public packet. No private author material or other review report informed this verdict. The independent verdict and ledger were written before the final prior-findings reconciliation.

The ruling preserves Milan's 0..4,000 ms LINK_UP/GM_CHANGE draw and 0..2,000 ms startup draw, with the full-range distribution. It replaces the earlier one-second discovery acceptance with the declared discovery time. It does not waive #972's unpublished-link acceptance or [#840's gigabit-only requirement](https://github.com/kebag-logic/milan-fpga/issues/840). Both #972 author comments and the PR explicitly leave the pre-arm window as an open decision; no public maintainer waiver was present in the reconstructed contract.

**Findings**

**R890-1-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `sw/firmware/ctrl/plat/ctrl_plat_phy.c:41`, with the skip at lines 231-233 and forced-mode publication at lines 184-189; `test_plat_phy.cpp:864` (P19's retained-advertisement case).

The new boot state skips the BMCR write whenever registers 4 and 9 already advertise gigabit only. That establishes neither BMCR's autonegotiation enable nor an acceptable operating mode. A gigabit-capable PHY can retain `ANAR=0x0001`, `GCTRL=0x0200`, while `BMCR=0x2100` forces 100 Mb/s full duplex. The arm now owes no unconditional restart; both polls leave BMCR untouched, and CONTROL publishes `11` (link up, 100 Mb/s, full duplex). GIG_PEER's unchanged OUTCOME backstop is never reached because autonegotiation is disabled.

Authority/evidence: #972 requires #840's speed behavior unchanged; #840 requires gigabit-only operation because the MAC cannot operate the lower-speed link. IEEE 802.3 Clause 22 distinguishes BMCR enable (0.12), restart (0.9), speed and duplex from the advertisement registers used by Clauses 28/40. A [primary PHY register reference](https://www.ti.com/lit/ds/symlink/dp83561-sp.pdf) independently confirms those BMCR fields; it is corroboration of register semantics, not evidence about the DUT's physical PHY.

The disposable `forced-head` probe produces `BMCR=0x2100 publication=11 restarts=0 renegotiations=0` and fails both assertions. The identical scenario with only the PHY implementation replaced by its `dd163e41` bytes produces `BMCR=0x3100 publication=0 restarts=1` and passes. See `focused.py`, `receipts/forced-head.log` (exit 1) and `receipts/forced-base.log` (exit 0). All ordinary platform tests pass without this added scenario.

Impact: the boot can preserve and publish an unsupported forced-speed link indefinitely; the claimed preservation of #840's behavior is false. This is a firmware-to-datapath interface regression, an initial-state robustness gap, and a missing negative case in the new retained-advertisement tests. The PR's and header's broad gigabit-preservation claims consequently overstate the implementation.

Required outcome: establish acceptable BMCR operation as well as advertisement contents before publishing a gigabit-capable PHY's link. Preserve the healthy retained-gigabit no-restart path. Add the retained-advertisement/AN-disabled case, including lower-speed and relevant control-state boundaries, and align the contract description with the implemented distinction. If the literal no-restart acceptance needs a control-state qualification, record that decision publicly instead of silently changing it.

Verification: the supplied failing scenario must pass at the corrected head; healthy P19 must still show no redundant restart; changed advertisement and OUTCOME tests/plants must remain effective. Re-review every affected lens.

**R890-1-F2 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifacts: `sw/firmware/ctrl/plat/ctrl_plat_phy.c:40`; `sw/firmware/ctrl/plat/ctrl_plat.c:365`; `sw/litex/milan_soc.py:2024`; `hdl/common/csr/milan_csr.sv:1613`; `hdl/common/KL_link_guard.sv:163`; `hdl/milan/milan_datapath.sv:3407`; `tb/verilator/ctrl_split_boot/run.py:432`; `docs/reference/FR_NFR.md:217`.

The write closes the window from the arm onward, but the acceptance requires no datapath transmission before firmware publishes the link. Before the arm, the link-status reset is still up, LINK_CTRL[0] resets to one, and the guard assumes both clocks alive and resets to RUN. With retained PHY clocks, the guard supplies no intervening qualification barrier. `eff_link_w` reaches the gPTP port, MAAP and mailbox consumers unchanged. The arm follows banner output, identity checking and CSR policy writes; an identity refusal returns without it.

Authority/evidence: #972's frozen no-transmit acceptance and AGENTS.md sections 2/4 prohibit privately narrowing an acceptance criterion around an unresolved design choice. The public handoff measures the arm at 2.636 / 4.434 ms and explicitly acknowledges the retained-link reload case as an open decision. `guard_probe.py` compiles the exact-head link guard and drives retained clocks: all 221,700 cycles (4.434 ms at 50 MHz) have `link_est=1`, with zero cycles of MAC reset. See `receipts/guard.log`. This proves the guard does not close the window; it does **not** claim a measured Ethernet transmission.

The new P20 checks publication before an MDIO frame. L4 starts its qualification assertion at the arm. The split boot simulation has no product datapath/transmitter and grades PHYP against PHYF, also an MDIO frame. These checks cannot establish silence from reset on a retained physical link. FR_NFR's new statement that the datapath sees no link before a verified publication is therefore not true for the entire interval it describes.

Impact: an unpublished reset link can still enable the datapath, so the requested acceptance is neither enforced nor proved for the publicly identified warm-link case. Merely documenting it as outside a firmware-only change does not settle the issue's scope or earn clean lens coverage.

Required outcome: resolve the public scope/design decision and implement/prove the agreed reset-to-publication contract. Under the existing acceptance, keep the transmit paths unqualified from reset through verified publication, including retained-link reload and boot-refusal paths, while preserving the intentional no-MDIO configuration. Correct the unconditional documentation claim. Moving the same open defect to another issue does not resolve it.

Verification: a focused integration check must observe actual transmit admission/output from reset, with the PHY link retained, at both required shapes, and fail a planted premature qualification. Retain the arm publication checks. Any narrowed acceptance needs an explicit public authority decision before it can be reviewed as a different contract.

**R890-1-F3 | RESIDUE | Docs**

Artifact: `sw/firmware/ctrl/test/adp_first_mutants.py:40`.

Authority/evidence: the owner's source-comment rule forbids reviewer identities and review rounds in new source comments. The added comment contains `R888-1-F1`.

Impact: editorial provenance residue only; removing the identity changes no code, measurement, assertion, generated artifact or clause claim.

Exact required fix: replace `# #970, R888-1-F1:` with `# #970:` on that line. Keep the existing behavioral explanation. Verification: inspect the added source-comment delta. This residue does not independently make a lens unclean.

**Results by lens and executable evidence**

- Conformance: traced arm, advertisement writes/readback, restart choice, unchanged GIG_PEER OUTCOME, and the #840 requirement. The ordinary changed-advertisement and retained-gigabit paths are supported; F1/F2 prevent acceptance. ADP's production constants and stack pin are unchanged. Group G uses independent literal 4,000/2,000 ms bounds and tests both GM orders, wire GM identity and available_index.
- RTL: examined the actual SoC link CSR, synchronizers, CSR qualification reset, link guard and effective-link consumers. No RTL file changes or CDC changes occur in the reviewed delta. The changed firmware publication crosses through the existing synchronizers; the before-arm state is F2, and F1 changes the status delivered to the hardware interface.
- Robustness: examined no-MDIO, missing/NAKed PHY, latched loss, incomplete negotiation, failed advertisement writes, dropped restart, OUTCOME saturation, resumed polls, and room/wrap tests. The new forced-state probe establishes F1; retained-clock reset establishes F2's qualification exposure. Neither is a hardware measurement.
- Tests: independently ran the ADP arm (58 tests), platform boot/PHY arms at one and two interfaces (55 each), all eight relevant ADP plants and three PHY plants, including every named kill. All normal suites pass and all eleven plants are caught. Boot grader native controls pass 6/6. These successes establish the assertions they execute; they do not cover the missing F1/F2 scenarios. The initial ADP-plant wrapper invocation lacked its generated reuse include; adding the repository's `cut_reuse` preparation resolved that setup error before the successful full focused rerun.
- Docs: read every changed document and source-comment delta. `docs_check.py` independently reports zero findings; the source-comment residue still exists. FR_NFR 2.1.1 explicitly sums `250 + 0 + 30 + 4000 + 30 + 1 = 4311 ms`, leaving 1689 ms within the 6.0 s declaration. Its cited sources are #397's publication allowance, `CTRL_PLAT_PHY_POLL_US`, link-guard settle, the ADP service row/loop event bound, Milan's draw and `CTRL_LOOP_T_EGRESS_MS`. MAILBOX_SPLIT and G tests use the declaration. The sum is conditional on the qualified-link/service assumptions; F2's unconditional boot premise remains unresolved. The 41.94 ms settle is counted inside publication, not as an additional PHY autonegotiation measurement.

The independent G results match the published values: G1 latest 3990 ms, quarter counts 17/9/19/19; G2 latest 1981 ms, halves 18/14; G3 latest 3649 ms; G4's changed-GM advertisement latest 3994 ms. G4's halves 6/26 are not a uniformity assertion; that test checks the draw kind. The finite sample spread tests are regression evidence, not a statistical proof of every possible draw sequence.

All 101 entries in the public packet manifest match their published SHA-256. `receipts/public-evidence-audit.txt` records the examined author receipts and their identity:

- Firmware evidence at `48c39b5b`: four shards pass, 75 passing suite verdicts, 832/832 control plants, 385 AECP and 543 SRP successful plant rows; coverage passes for 40 files. Twin, plants and mapping legs complete with exit zero.
- Corrected boot evidence at `ba0f80ed`: both shapes pass; arm publication 2.636/4.434 ms precedes first MDIO frames 27.125/66.186 ms; six native controls and seven plants pass. The earlier native-control failure at `48c39b5b` is not counted as a pass; the stand-in correction is independently rerun here. Boot simulation exercises the restart path; host P19 covers no restart, as the acceptance permits.
- Image receipts: all four platform points retain 45/46/58/63 RAMB36 within their respective ordinary or explicitly ledgered limits; ROM increases 16 bytes. Platform differences are confined to `ctrl_plat_phy.o`; the four size fixtures are identical. CPU evidence has 63 paired probes per shape, zero changed verdicts or instruction counts, and identical harness images. That harness excludes the platform PHY, so it is not independent evidence of the new PHY boot behavior.
- Final-head docs evidence reports 104/104 steps. Builder receipts are the author's: leg 0 at `ba0f80ed`, leg 1 at `0f508a01`, each explicitly retaining its declared NOT RUN arm. Physical calibration was NOT RUN. No claim here converts those omissions or field skips into hardware proof.

Only boot run.py/README and the documentation audit changed after the firmware evidence head; only the audit changed after the corrected boot evidence head. These are scoped applicability checks, not a claim that full source banks executed again at this head. The separate stack test-only branch is not the parent's pin and supplies no substituted parent execution evidence.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #972 acceptance, #970 ruling, #840; ctrl_plat_phy.c:29/184/226/249; test_adp.cpp:555; FR_NFR.md:199 | R890-1 applied; no clean covering round | 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b |
| RTL | UNCLEAN (F1, F2) | milan_soc.py:2024/2051; milan_csr.sv:1613; KL_link_guard.sv:163/224/320; milan_datapath.sv:3407/9269; guard.log | R890-1 applied; no clean covering round | 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b |
| Robustness | UNCLEAN (F1, F2) | ctrl_plat_phy.c; test_plat_phy.cpp P1-P21; test_plat_boot.cpp L1-L6; forced-head/base logs; guard.log | R890-1 applied; no clean covering round | 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b |
| Tests | UNCLEAN (F1, F2) | adp_first_mutants.py; plat_mutants.py; test_adp.cpp G1-G5; run.py:432; receipts/adp, plat1, plat2, adp-plants, phy-plants, native-controls logs | R890-1 applied; no clean covering round | 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b |
| Docs | UNCLEAN (F1, F2; F3 is residue only) | FR_NFR.md:199-220; MAILBOX_SPLIT.md:534; ctrl_plat_phy.h; platform/boot READMEs; CHANGELOG; public handoff/receipts; docs-check.log | R890-1 applied; no clean covering round | 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b |

**Reproduction, limits and manager duties**

Run `python3 -B run_focused.py CHECKOUT` from this packet to reproduce the focused suites, named plants and forced-state comparison. Each task has its own log and exit-code file. `forced-head.rc=1` is the reproduced defect; `forced-base.rc=0` is its comparison control. `python3 -B guard_probe.py CHECKOUT` runs the isolated guard check. `python3 -B integrity.py CHECKOUT` verifies raw tracked bytes, executable modes, complete index entries and initialized submodule pins, without trusting status-cache flags. Builds and planted copies are confined to `scratch/`, excluded from publication.

The identity check used scoped Verilator 5.050, revision v5.050. Independent checks were coordinated in the foreground, with separate logs; there were no detached jobs. No candidate source was edited. Final raw-byte/index/mode validation passes for the parent and all five initialized submodules. The unused `external` gitlink remains unchanged and uninitialized. No GitHub write, source fix, commit, push, merge, full bank, shared installation, container execution or hardware action was performed.

There is no manager source-bank execution at this exact head. Full banks were not independently rerun, and exact-head hosted acceptance was not independently adjudicated. The manager still owns hosted/local-replica acceptance, the current-dev candidate build/native banks and their public receipts, subsequent containment, and the physical discovery rerun at 1x1/1if and 8x8/1if after an authorized merge. Live dev identified for that future merge turn is `e275d7950ef3385753e6a15d2e191ba855b171ed`; validation must use the then-current tip. Those duties do not resolve F1/F2 or supply this round's missing clean coverage. Bench discovery acceptance remains pending; this report is not hardware qualification or merge approval.

Prior-public-findings reconciliation: after this independent verdict and ledger were written, the PR's complete returned discussion contained only review-start comments `7083028799` and `7083035311`; review submissions and inline review threads were empty. The issue still contained only TAKEN and REVIEW READY. There were no prior public findings on PR #974 to resolve or retain. The #970 ruling remains the controlling public decision, already applied above. This check does not clear another review that remains in flight.

R890-1 FINISHED
