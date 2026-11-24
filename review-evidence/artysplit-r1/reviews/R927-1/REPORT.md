[R927] NEGATIVE - exact head 248d85c1453213b0f1642967a4046f395c82c56b

# R927-1: internal cleared-context review of PR #1004 (Closes #878)

- Head: `248d85c1453213b0f1642967a4046f395c82c56b`, tree `ad0444dbf9089b90ac3693c0bc46421894cfadeb`.
- Base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6` (`dev-soft-core`). Four commits; 86 files, +2443/-288.
- Role: internal independent reviewer, cleared context. Reconstructed from AGENTS.md, CONTRIBUTING.md,
  docs/README.md, the #878 body and its public rulings, the diff, and the public evidence packet
  `review-evidence/artysplit-r1` at `0723eba4`. No private author material was read.
- Prior public review findings on this PR: none exist at review time. The PR thread carries the
  bench report and two review-start notices only. Nothing to resolve or retain.
- Verdict: **NEGATIVE.** Three MAJOR findings (F1 to F3) and three MINOR findings (F4 to F6) are open. RTL is covered clean.

Every receipt named below is under `receipts/` in this packet and listed in `MANIFEST.sha256`.
Probes ran on disposable copies under `scratch/` (never published); the review clone was never written.

## What was confirmed (independent execution at the exact head)

| Check | Result | Receipt |
|---|---|---|
| PLL contract: Arty 80 MHz sys/CPU, VCO 800 MHz, divisors 10/32/16/4, `margin=0`, 83,333,000 and 80,000,001 Hz refused | PASS | `raw/timing-grade-pll.log` |
| Arty owner model (`arty_grade.py`): load 0.49667711, txL 48.74 ms, last 121.84 ms, ACMP 28.82 ms, slice 950 us, pace 9 ms | PASS, figures equal the PR's | `raw/arty-grade.log` |
| Owner-bound boundary controls (`arty_grade.py --selftest`) | 8/8 PASS | `raw/arty-grade-selftest.log` |
| Service-budget self-test (`selftest.py`), every check and every grader mutant | rc 0: 1034 checks PASS, 0 FAIL; 297 of 297 mutants caught, 0 escaped; "self-test: 0 failures" | `raw/service-selftest.log` |
| The eight `clock:` mutants, the two Arty ones included, re-run alone; `egress_ledger.py --selftest`; `record_classes.py --selftest` | 8/8 caught, unmutated 0 failing; 18 ledger mutants, 0 failures; 26/26 controls and 9/9 Arty record checks | `raw/service-new-mutants.log`, `raw/egress-ledger-selftest.log`, `raw/record-classes-selftest.log` |
| Builder export identity, base vs head, all-fabric and split | AX7101 1x1/1if and 8x8: 4 of 4 sets IDENTICAL (44 files); Arty sets differ only in the clock | `raw/ax-identity.log` |
| AX7101 split product firmware ELF, base vs head, identical inputs | 1x1/1if and 8x8/1if IDENTICAL | `raw/ax-firmware-identity.log` |
| Committed generated `adp_shape_defaults.svh` (Arty split) equals the builder's emission | equal, both placements | `raw/generated-svh-compare.log` |
| Selected builder gates (36, 36a writable key, MAC/entity, audio rates, 23n placement, build.sh argv) | 6/6 PASS | `raw/builder-selected.log` |
| `gptp_txts` `run-latw` (both link shapes) | 921 checks, 0 failures | `raw/gptp-txts-latw.log` |
| `gptp_shadow` default and its controls | 326 checks; 9 controls, 0 failures | `raw/gptp-shadow.log` |
| `milan_dp` `gptp-latw` through the real CSR block | 237/237 PASS | `raw/milan-dp-gptp-latw.log` |
| `milan_dp` `gptp-lat` (constant pair, the AX7101 path) | 212/212 PASS | `raw/milan-dp-gptp-lat.log` |
| `ctrl_region_decode` committed `run.py --self-test`, Arty shape and default AX7101 shape | PASS at both | `raw/region-arty.log`, `raw/region-ax.log` |
| `ctrl_split_boot` committed `run.py`, Arty shape | PASS, 0 findings; ready at 28.732 ms (2,298,548 cycles at 80 MHz); longest PHY frame 14,487 cycles | `raw/boot-arty.log` |
| `platmii` arm as committed | 8/8 PASS | `raw/probe-mii-clean.log` |
| RTL lint ratchet | PASS, 89 <= 89 | `raw/lint-rtl.log` |
| `check_sweep_shape.py` | OK | `raw/check-sweep-shape.log` |
| em-dash, `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `git diff --check` | PASS | `raw/docs-*.log` |
| docs-workflow read-only checks, base vs head side by side | two head-only regressions (F2, F3) | `raw/docs-sweep-base.txt`, `raw/docs-sweep-head.txt` |
| Evidence packet integrity (`MANIFEST.json`, 1836 entries) | 0 published-hash mismatches | `raw/evidence-manifest-verify.log` |
| Review clone after every probe: HEAD, tree, index tree, clean status, six gitlinks | exact head bytes, 0 porcelain lines | `raw/clone-verify.log` |

Timing on the selected directive (`ExtraTimingOpt`) was read from the published Vivado reports:

- `report_timing -delay_type min_max -slack_lesser_than 0` at Slow/0 C, Slow/85 C, Fast/0 C and Fast/85 C:
  "No timing paths found" in all four (Design State `Physopt postRoute`).
- `report_clock_interaction -delay_type min_max`: sys `clkout0` (12.50 ns) WNS 0.62 / WHS 0.02 ns;
  datapath `clkout2` WNS 1.21 / WHS 0.02 ns; every other timed pair positive.
  These corroborate the stated worst WNS +0.617 ns and WHS +0.017 ns to two decimals.
  WNS clears the +0.030 ns floor and WHS is non-negative at every corner.
- `clkout0` and `clkout2` (80 and 50 MHz) are "Ignored, Asynchronous Groups" in both directions.
  That is the same structure the base had at 83.333/50 MHz and the AX7101 has at 100/50 MHz.
- All 69,984 routable nets are routed, with 0 routing errors.
- `ExtraPostPlacementOpt` fails the floor (Slow WNS +0.009 ns) and was correctly not selected.
- Utilization (`*_utilization_place.rpt`, the source BUILDING.md names) is 33,411 LUT (52.70 %),
  40,479 FF (31.92 %), 78.5 BRAM tiles (58.15 %), 14,119 slices (89.08 %) and 11 DSP.
  This matches the PR. The firmware ledger (44/56 RAMB36) is consistent with the 78.5 tiles.

## Findings

### F1. MAJOR. The PR closes #878, but acceptance items 4 to 7 are not met at this image and no decision amends them

- Lenses: `Conformance`, `Docs`.
- Artifact: PR #1004 body (`Closes #878`), #878 acceptance 1 to 7, bench report issuecomment-7146699931.
- Authority and evidence: AGENTS.md section 4 freezes acceptance criteria for an active lane and
  section 6 `Conformance` asks that every criterion be actually satisfied. CONTRIBUTING.md 2.1 says a
  superseded issue is never quietly closed and its comment must name the unmet criteria.
- At this image:
  - Item 4 asks for offset and peer delay over at least 10 minutes. Peer delay is recorded. The offset is not.
  - Item 5 asks for frames checked on the capture. There was no tap ("No wire capture").
  - Item 6 asks for one hour with both connections up. The bench ran 1,046 s (17.4 min).
  - Item 7 asks for one saved descriptor change read back after a reset, with the save time measured.
    It was not run on this image. The earlier image measured no save time either.
  - Item 3 asks for byte identity with the all-fabric Arty image's descriptors, or each difference explained.
    The bench compared against this image's own AEM file. My builder exports show the all-fabric Arty
    AEM differs at ENTITY `firmware_version` ("3.96.0" against "2.96.0"). No report explains that difference.
  - Item 2's ident and mailbox `ID` are shown at image level only: the identity gate and the firmware's pre-ready check.
- The 2026-11-23 ruling lists the round's bench steps (boot, enumeration, link, one stream each way).
  It does not retire or amend items 4 to 7.
- The PR's own DoD leaves "Linked Issue acceptance criteria are satisfied" unchecked.
  The bench report's "Every step was met" refers to its own plan, not to #878's acceptance.
- Impact: merging as written records #878 as done while four acceptance items have no evidence on the image being merged.
- Required outcome: one of the following.
  - Evidence for items 4 to 7, and the item 3 all-fabric difference explained, on this image.
  - A public owner decision on #878 amending or deferring those items, with the PR text no longer
    claiming to close what it does not meet.
- Verification: a reviewer finds either the receipts or the recorded decision on #878 and a PR body consistent with it.

### F2. MAJOR. `docs_inventory.py --check` fails at the head: `docs/DOCUMENTATION_AUDIT.md` is stale

- Lenses: `Docs`, `Tests`.
- Artifact: `.github/workflows/docs.yml:424` runs `python3 scripts/docs_inventory.py --check`.
  `docs/DOCUMENTATION_AUDIT.md` rows 124, 152 and 277 are the stale ones (CHANGELOG.md, ENDSTATION_BUILDER.md, BUILDING.md).
- Evidence: the check passes at the base and fails at the head ("docs/DOCUMENTATION_AUDIT.md: STALE (3 lines differ)").
  On a disposable copy, `--write` regenerates exactly those three rows. The diff's own documentation edits
  change their evidence columns, for example BUILDING.md now cites Milan v1.2 and 802.1BA.
  Receipts: `raw/docs-inventory.log`, `raw/docs-inventory-base.log`, `raw/docs-inventory-regenerated.diff`.
- The author's "eleven final documentation gates" receipt (`build-corrected-docs-after-service-results.json`) does not include this check.
- Impact: the hosted docs workflow, and so the required `docs-check` context, goes red on this head. A generated artifact is out of date.
- Required outcome: the generated audit is regenerated by its generator, and `docs_inventory.py --check` passes at the new head.
- Verification: `python3 scripts/docs_inventory.py --check` exits 0.

### F3. MAJOR. The Python idiom ratchet fails at the head: 4 new over-long modules and 16 over-long lines

- Lens: `Tests`.
- Artifact: `.github/workflows/docs.yml:400` runs `python3 scripts/check_py_idiom.py`.
- Evidence: at the base it reports `long module 10 <= 10` and `over-long line 0 <= 0`. At the head it reports
  `FAIL: long module 14 > ratchet 10` and `FAIL: over-long line 16 > ratchet 0`.
  - New modules over 1000 lines: `sw/firmware/ctrl/test/ctrl_mutants.py`, `tb/verilator/ctrl_service_budget/rows_tiers.py`,
    `scenario.py` and `selftest.py`.
  - New lines over 120 columns in 11 files, among them `load_grade.py` (4).
    The `'arty-1x1': {...},'1x1/1if': ...` insertions at `load_grade.py:105,116`, `edit_rows.py:53`,
    `rows_grade.py:98` and `rows_tiers.py:102,137` account for several.
  - Receipts: `raw/py-idiom-list-base.log`, `raw/py-idiom-list-head.log`.
- Authority: CONTRIBUTING.md section 5 and CODE_QUALITY Rule 12. New Python complies immediately, and the ratchet only moves down.
- Impact: the docs workflow's Python idiom gate, and with it `docs-check`, fails. This is the same failure shape as this lane's earlier STOP (2026-11-11).
- Required outcome: the four modules are back at or under 1000 lines and no new line is over 120 columns,
  every check kept, with the ratchet unchanged. The gate passes.
- Verification: `python3 scripts/check_py_idiom.py` exits 0 at the new head.

### F4. MINOR. The MII publish guard has no test that can fail without it

- Lens: `Tests`.
- Artifact: `sw/firmware/ctrl/plat/ctrl_plat_phy.c:312-319`, the `CTRL_PLAT_PHY_100_ONLY` block
  "Never publish a lower-speed or half-duplex port as AVB-capable". Also `sw/firmware/ctrl/test/test_plat_phy_mii.cpp`.
- Evidence (portable probe `scripts/mii_guard_probe.py`):
  - Deleting the guard leaves all 8 shipped `ArtyPhy` cases green (`raw/probe-mii-noguard.log`, RC 0).
  - None of the 7 `mii_mutants` removes it.
  - An added case passes on the committed code (`raw/probe-mii-forcedten.log`, 9/9) and fails twice without the guard
    (`raw/probe-mii-forcedten-noguard.log`: "MII forced 10 Mb/s published up").
    In that case the PHY keeps autonegotiation off at 10 Mb/s full duplex and drops the BMCR restart.
  - The 10-only and half-duplex partner tests stay green without the guard: the advertisement alone leaves no common mode.
- Authority: AGENTS.md section 6 `Tests`: each new test can fail for the defect it claims to detect, and negative paths are covered.
  BUILDING.md (added by this diff) states "Planted policy defects must fail the firmware gate".
- Impact: the one branch that keeps a non-AVB mode (IEEE 802.1BA-2011 Table 6-1) from being published up can be lost silently.
- Required outcome: a host case in which the resolved mode is not 100BASE-TX full duplex, and a planted defect removing the guard that the case catches.
- Verification: the plant is caught in the `platmii` arm.

### F5. MINOR. `milan_lat` is longer than the receive FIFO, so a dropped digit can write a different valid pair

- Lenses: `Robustness`, `Docs`.
- Artifact: `sw/firmware/ctrl/plat/ctrl_plat_console.c:141-196`, `ctrl_plat_console.h:46`
  (`CTRL_PLAT_RX_PER_PASS 16u`, "the UART's receive FIFO depth") and `sw/firmware/ctrl/plat/README.md:66-77`.
- Evidence:
  - `milan_lat 1409 100\r` is 19 bytes and the widest legal line is 22. The console drains at most 16 bytes a pass.
  - The qualified worst whole pass is 1.6813 ms. At 115200 baud that is about 19 byte times, and 16 bytes arrive in about 1.39 ms.
    So a line sent in one burst can overflow the FIFO during a long pass.
  - This lane's own earlier bench round on #878 (2026-11-12) recorded "a burst lost bytes and was refused" and
    "a robust fix ... for its own issue". No issue exists; a search for `milan_lat` finds only #878.
  - Losing a byte can also leave a well-formed line: losing the last `0` of `100` writes 1409/10. The
    command then writes that pair, and only the `GPTP_LAT=` read-back shows it.
  - The README states neither the hazard nor the operator's obligation to check the read-back.
- Impact: a wrong runtime gPTP correction can be applied during bench calibration, and the console gives no refusal for it.
- Required outcome: one of the following.
  - The console contract states the limit: paced input, and the read-back must equal the intended pair before the value is used.
  - The command refuses a line whose bytes may have been lost.
  - A public owner decision accepting the limit for this bench-only lever.
- Verification: the README or the code shows the chosen behaviour, and K7 or a new case covers it if the code changes.

### F6. MINOR. The cited qualification hash matches no published receipt

- Lens: `Docs`.
- Artifact: the #878 round-4 report (issuecomment of 2026-11-24 19:26) and `review-evidence/artysplit-r1/author/REPORT.md`.
  Both cite "service qualification receipt SHA256 `f6f1d2f5...86c`".
  `build-corrected-image-ready.json` and `build-corrected-qualification-parallel-audit.json` name the same hash.
- Evidence:
  - The packet's `MANIFEST.json` lists no file whose `original_sha256` is `f6f1d2f5...`.
  - The published `build-corrected-final-census-qualification.json` has original `0479a53e...` and published `78be299b...`.
    The image-ready receipt gives the cited file as 12,227 bytes; the published copy is 12,452 bytes after redaction.
  - The REPORT's verification table names a `.json.gz` receipt that is not in the packet.
- Impact: a cold reviewer cannot tie the cited qualification to a published file. Its content (PASS, 145 groups,
  the five bounds) is visible, but its identity is not.
- Required outcome: the cited file is published, or the reports cite the published receipt and state how the two relate.
- Verification: `sha256sum` of a published file equals the cited hash, or the citation names `0479a53e...` with its relation stated.

### RESIDUE (wording only; exact fixes)

- RS1. `configs/endstation_arty_split.yaml:256-257` says "#878 keeps this board's calibration; the manager verifies
  the split image on the bench after IMAGE READY." That is lane workflow in a source comment (owner comment rule).
  Fix: "#878 keeps this board's calibration."
- RS2. `tb/verilator/ctrl_service_budget/egress_ledger.py:13` says "(#878, round 4)", a review-round label in a source docstring.
  Fix: "(#878)".
- RS3. Round labels stand in for decisions in authoritative prose:
  - `docs/ENDSTATION_BUILDER.md:22`: "The owner's round-4 ruling".
  - `docs/integration/BUILDING.md:358`: "This replaces round 2's unachievable 83,333,000 Hz request."
  - `docs/integration/BUILDING.md:361`: "The owner's round-4 ruling".
  - `tb/verilator/ctrl_service_budget/README.md:206`: "(#878, round-4 held-egress ruling)".

  The held-egress ruling was issued on the round-3 STOP.
  Fix: cite the decision as SPLIT_CONTROL_MEMORY section 15 does, for example
  "[#878's held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930)".
  At BUILDING.md:358, write "This replaces the unachievable 83,333,000 Hz request."
- RS4. `docs/litex/CLOCK_DOMAINS.md:382`, a line this diff rewrites, reads "In VERSION `0x0002_0060`, `0x540`/`0x544`
  are readable shadow words:". The only build that sets the key is a split image, which reads `0x0003_0060`.
  Fix: "In VERSION `0x0002_0060` and a split image's `0x0003_0060`, ...".
- RS5. `configs/endstation_arty_split.yaml:113`, a new file, says "(N25Q128 QSPI)". The Arty's flash is the S25FL128S
  (`sw/litex/milan_soc.py:3888`). Fix: "(S25FL128S QSPI)".
- RS6. The PR #1004 body says "The branch has not been pushed." and "reviewer: pending assignment", and both are stale.
  Fix: state the pushed head and the assigned review sessions.

### SUGGESTION

- SG1. `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:310-320`: `net_r` is 18 bits signed. Nothing at elaboration requires
  `TXTS_CORR_NS_P` to fit 18 bits less 16; today's largest, MII about 3770 ns, fits easily.
  An `$error` guard beside the existing 16-bit pair guard would make the width a checked contract.
- SG2. `ctrl_plat_phy.c:315-318`: the MII outcome retry does not count `renegotiations`, unlike the 1000BASE-T path (line 285).
- SG3. `scripts/docs_inventory.json:236` still quotes the Arty recipe as a "retired DUT ... sys 83.333 MHz".
- SG4. `run.py`/`shape_costs.py` bind `arty-1x1` to `endstation_arty_current`, not the shipped `endstation_arty_split`.
  The harness image (`ctrl_srp_image.py`) is the same shape at both, and `arty_grade.py` checks that.
  Naming the shipped config would remove the question.

## Lens coverage (reviewer-owned ledger)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #878 acceptance 1-7 and its rulings; bench report issuecomment-7146699931; `configs/endstation_arty_split.yaml`; `ctrl_loop.h:401-413`; `arty_grade.py` run; PLL probe; `ctrl_plat_phy.c` 100-only policy against IEEE 802.1BA-2011 Table 6-1 via Milan v1.2 4.2.1; signoff and clock-interaction reports; AEM exports | R927-1 | `248d85c1453213b0f1642967a4046f395c82c56b` |
| RTL | CLEAN | `milan_datapath.sv:1863-1883` (latch on `s_axi_awready`, which is `wr_fire` = AW and W valid together, `milan_csr.sv:1140,1167`; full 16-bit address compare as in `is_plain_rw`); `milan_csr.sv:1593-1596,2053-2054`; `KL_gptp_shadow.sv:401-403` with the 16-bit guard at `:305`; `KL_gptp_txret.sv:310-320,639`; `milan_soc.py:273,5040-5050` (Arty-gated); clock-interaction report (no new crossing; the new flops are on `axis_clk`); lint 89/89; `gptp_txts` latw 921, `gptp_shadow` 326+9, `milan_dp` gptp-latw 237 | R927-1 | `248d85c1453213b0f1642967a4046f395c82c56b` |
| Robustness | UNCLEAN (F5) | `ctrl_plat_console.c` `number`/`lat` and K7 refusals; console FIFO and pass bound; `ctrl_plat_phy.c` 100-only paths (lost write, NAK, latched loss, forced mode; probe); latw mid-exchange write sweep (`gptp_txts`); held-egress ledger plants | R927-1 | `248d85c1453213b0f1642967a4046f395c82c56b` |
| Tests | UNCLEAN (F2, F3, F4) | `test_plat_phy_mii.cpp` and `plat_mutants.py` (guard probe); `test_plat.cpp` K7/K8; `gptp_txts/mutants.py` LATW; `sim_gptp.cpp` T-LATW; `egress_ledger.py`/`record_classes.py`/`arty_grade.py` controls; service self-test (full, 297/297 mutants); region decode at both shapes; split boot at Arty; builder gates; docs-workflow sweep base vs head | R927-1 | `248d85c1453213b0f1642967a4046f395c82c56b` |
| Docs | UNCLEAN (F1, F2, F5, F6) | `SPLIT_CONTROL_MEMORY.md` section 15; `CLOCK_DOMAINS.md`; `BUILDING.md`; `ENDSTATION_BUILDER.md` rows 33d/33e; `GPTP_PLANE.md`; `REGISTER_MAP.md` 0x540/0x544/0x7F0; `plat/README.md`; CHANGELOG; `DOCUMENTATION_AUDIT.md` (stale); PR body; evidence packet `MANIFEST.json` | R927-1 | `248d85c1453213b0f1642967a4046f395c82c56b` |

## Notes on the focus items

- **Clock plan and CDC.** The PLL probe and the reports confirm the 80/25/50/200 MHz plan from an 800 MHz VCO at `margin=0`.
  The 80:50 ratio sits inside the envelope the shared CDC already serves (AX7101 100:50, the base Arty 83.333:50).
  `pp_mem_timeout_cycles` keeps milan slower than sys. The writable corrections add no crossing.
  The audio chain is clocked from `clk100` and is unaffected.
- **Owner bounds.** Load 0.4967 <= 0.70, txL 48.74 <= 49 ms (0.26 ms margin), last notice 121.84 <= 140 ms,
  ACMP 28.82 <= 30 ms, worst whole pass 134,507 cycles = 1.6813 ms <= 2 ms. These are reproduced from the model.
  The published qualification receipt shows 145 groups, 6/6 checks and 0 findings.
- **Retry and ledger arithmetic.** I recomputed them by the stated rule.
  Cold 9285 cycles gives 125 us, attempt 1947 gives 30 us and notice 17196 gives 230 us.
  The seven ledger figures equal 60 + 1.05 x (measured - 60), rounded up to 0.01 ms.
- **AX7101 shared-image regression.** None found.
  - Builder exports: 44 files identical.
  - Split product ELFs: identical at both AX shapes.
  - The default-off RTL paths elaborate the same constants. The 16-bit cast is guarded at `KL_gptp_shadow.sv:305`.
  - The `milan_dp` constant-pair leg passes 212/212.
  - Region decode passes at the default AX7101 shape after this diff's harness rework.
- **Bench notes.**
  - The new entity ID `024b4cfffe4b4c02` and MAC `02:4b:4c:4b:4c:02` match `platform.mac_address` and the builder's station-MAC table (`test_station_mac_ul_bit_warns`, PASS), as decided in #840.
  - The accumulated-latency observation is filed as #1006, which is open. It lies in shared split SRP code that this diff does not touch.
  - The `serial_number` "AX7101-0001" is inherited from the shared AEM image.

## Real limits

- No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the author's receipts plus the runs above.
- No hosted check run exists for this head (`check-runs` total 0). Hosted and act acceptance belong to the manager.
- The full 145-case native service campaign, the four firmware shards, Vivado routes and the boot self-test controls were not re-run here.
  The service-budget grader self-test was re-run in full (297/297 mutants caught); the native campaign it grades was not.
- The per-corner `*_signoff_*_timing.rpt` summaries are not in the packet; only their hashes are.
  Timing was corroborated from the published negative-slack and clock-interaction reports, to two decimals.
- AX bitstreams were not rebuilt by anyone. AX identity is at builder-export and ELF level.
- Physical calibration was NOT RUN. Bench results are the manager's bench report. No hardware was touched in this round.
- The forced-10 Mb/s MII case of F4 is a review probe, not a proposed test text.

## Pending manager duties

- Disposition of F1 with the owner (evidence or an amended or deferred acceptance on #878).
- Current-dev candidate merge validation (live dev `e275d795`) with the builder and native banks, and hosted contexts at the final head.
- Carrying RS1 to RS6 to the residue checklist.
- Re-review of F2 to F6 at the corrected head; every lens marked UNCLEAN above needs a covering round there.

R927-1 FINISHED
