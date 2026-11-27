[R927] NEGATIVE - exact head 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1

# R927-2: internal cleared-context re-review of PR #1004 (relates to #878)

- Head `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1`, tree `ee1b81d4fcd318aeca7c37c8096d35e0e056ea8a`. Source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`; PR base `dev-soft-core`, merged into the lane at `c34e7d8b0` by `49b534fc9`.
- Delta judged: `248d85c1..4adfa9dc`. That is the lane commits `c4ecb9d37..69d124a8d` (round 5), the merge `49b534fc9`, read with `--remerge-diff` for its conflict resolutions, and `c3cd51474..4adfa9dc8` (rounds 6 and 7). Code the delta does not touch keeps R927-1's lens verdicts.
- Evidence packet: `review-evidence/artysplit-r1/author-r7` at `907764eb`. The 147-case census (`census/`, 22,600 files, 3,957,281,806 bytes) is not published. Only its hashes are (`FILES.tsv`).
- Order kept: I finished my own pass over the diff, the issue, the rulings and the packet before I read the R927-1 and R928-1 findings. I resolve those findings below.
- **Verdict: NEGATIVE.** Three MINOR findings are open: F1, F2 and the narrowed R928-1-F1. Every one of the 11 prior findings that blocked merge or made a lens unclean is closed at this head, except the publication half of R928-1-F1. RTL is clean.

## What was confirmed at this head (own execution)

| Check | Result | Receipt |
|---|---|---|
| Regrade of all 12 published signoff reports, run by the head's `receipt_regrade.py --timing-only` | rc 0; output byte-equal to the author's first 13 lines. AltSpreadLogic_high / ExtraTimingOpt: Slow WNS +0.433 / WHS +0.138, Fast +1.606 / +0.050; ExtraPostPlacementOpt Slow +0.064 / +0.126. 0 failing setup or hold endpoints anywhere, floors +0.030 / 0 met | `receipts/timing-only-regrade.log` |
| Utilization in the published place reports | AltSpreadLogic_high and ExtraTimingOpt: 33015 LUT, 40369 FF, 13791 slices, 78 BRAM tiles (61 RAMB36 + 34 RAMB18). ExtraPostPlacementOpt: 33013 LUT, 13545 slices | `pkt/timing-r7/*/digilent_arty_utilization_place.rpt` |
| `arty_grade.py` at the head | PASS. Load 0.5004771140; ACMP 29.77, txL 48.82, last 117.47, tx 34.81 ms; slice 1250 us is the rule's (margin 0.00367), pace 10 | `receipts/arty_grade-inspect.log` |
| Standalone self-tests at the head | `rows_tiers` 1033/1033, `load_grade` 28/28, `egress_ledger` 21 mutants with 0 failures, `record_classes` 26/26 plus 9/9 Arty, `arty_grade` 8/8, `kept_grade` 32 checks (including Disposition's breach and alone paths): all rc 0 | `receipts/standalone-*.log` |
| Console (`lat`) and MII host arms, plus every `plat-lat-*` and `mii-*` mutant | both arms rc 0; **15 of 15 mutants caught**; checkout plat sources unchanged | `receipts/host-probe.log`, `scripts/host_probe.py` |
| Documentation and idiom gates at the head | docs_check, doc style, doc paths, gPTP docs, inventory, Python idiom, C++ idiom, em-dash (base `c34e7d8b0`), TOC check and anchors: all rc 0 | `receipts/doc-*.log` |
| Packet checks (19) | all PASS: FILES.tsv whole hash; 147 cases; every in-tree Arty statement equals the step-2 derived model; installed row = first choice; retry statements; owed exclusions only in `srp-kept`/`srp-bound`; identity IDENTICAL over 147 stimuli; regrade, control and before-fix outcomes | `receipts/packet-checks.log`, `scripts/packet_checks.py` |
| Full regrade over the published packet | rc 1, `FileNotFoundError: .../census/answering-every-port/notice-burst-0/manifest.json` | `receipts/full-regrade-published-packet.log` |
| Hosted contexts at the exact head | 0 check runs, combined status `pending`, no statuses | read-only API query; manager duty |

## The focus items

1. **The #969 disposition (11-23 amendment).**
   - The derivation recipe (`recipes/census7.py.txt`, `OWED_KEYS`) leaves out only owed kinds of `srp-kept` and `srp-bound`, and only those over the installed statement. That is the record apply, the tier-2 slice of records, the walk, the polls base and the build of one, in `srp-bound` only for the last three. This matches `kept_grade.OWED_KINDS`. The final census excludes 8 such measurements, all in `none/srp-kept` and `none/srp-bound` (`qualification/census.json`).
   - The recipe does not itself gate on `kept_grade`. The in-tree gate does. `run.py` and `receipt_regrade.py` both pass these lines through `kept_grade.Disposition`, which forgives an owed STATED or SHARE line only while `held()` finds nothing. Its self-test covers the breach path ("a condition broken in a log: the finding stays, nothing is owed") and the alone path, and I ran it at the head.
   - `step1-kept-grade.log` reports PASS: 0 findings and 5 owed. Kept is within bound with margins +6,144, +9,429 and +6,711 cycles. No work pass or idle run is over THE SHARE in either group. The `srp-bound` build of one is 56,255 cycles against 52,800 (owed).
   - The control packet without `srp-bound` is refused by name: "srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone" (`receipt-regrade-control.log`). Before the fix, the five owed lines were refused (`receipt-regrade-before-fix.log`).
   - The reading is consistent with "graded OWED to #977, not raised" and "the SRP unit not restated". The Arty point is not inside #977's acceptance, though: see **F1**.
2. **Step 2 regrades step 1's traces.**
   - `identity.log` ends IDENTICAL. It compares 8 variants' executables and ELFs, 23 recorded inputs each and 147 stimuli. Four dated inputs are compared with their date lines removed: `sim.v`, `libc.a`, `libcompiler_rt.a` and `flash_port.json`. `identity-raw.log` shows those raw 32 differences openly.
   - Only `CTRL_LOOP_TICK_US` moved in a firmware header at `74f942be5`. No firmware C file reads it: it is read in `ctrl_loop.h:412/521` and by the harness models only.
   - `build.reused()` refuses a build whose recorded `tree:firmware` differs from the checkout, so the step-2 build recorded the step-2 tree.
   - "Flash image identical" is vacuous: no variant records one (RS-D). The step-2 `census-build.log` is byte-identical to step 1's (SG-4).
   - Each copied trace is checked against step 1's recorded SHA256 before regrading (`recipes/reuse7.py.txt`).
3. **The receipt regrader.**
   - The published log shows 147 of 147 grades reproduced, cross-case PASS and the owner model equal to the published qualification.
   - The census extracts it reads are not published, so I could not rerun it beyond the timing part. That half of R928-1-F1 stays open.
   - Its timing selection differs from the image grader's (SG-1), and it has no self-test (SG-2).
4. **The route.**
   - AltSpreadLogic_high and ExtraTimingOpt are the same placed design. Both manifests are `1730c43f...`, with bitstream payload `8918ba7d...`. That explains the tie on every report.
   - My regrade confirms WNS +0.433 / WHS +0.050 ns, and the place reports confirm 33015 LUT / 40369 FF / 78.0 BRAM.
   - Against round 4's routed image (`248d85c1`: 33411 / 40479 / 78.5 / 14119) this is −396 LUT, −110 FF, −0.5 BRAM. The PR states it equals round 6's route. Round 6's reports are not in the published packet, so that equality, and the LUT-band rule against the previous routed image, cannot be checked from public evidence. Between this route's directives the spread is 2 LUT.

## Findings

### F1. MINOR. The Arty's #969 registration debt is "owed to #977", but #977's acceptance does not cover this point

- Lenses: `Conformance`, `Robustness`, `Docs`.
- Artifacts:
  - `docs/design/SPLIT_CONTROL_MEMORY.md:3518-3519` ("owed to #977 under #969's disposition, as at the other points ... and do not restate the row").
  - `validation/receipt-regrade.log` lines 161-170 (10 OWED lines) and `qualification/census.json` `owed_969` (8 exclusions, up to 495 us records and a 740 us build of one).
  - #977's issue body.
- Authority and evidence:
  - #969's 11-23 ruling (issuecomment-7116192252, item 2) makes the bound path's costs "the registration cost #977 owns". It says "#977 must clear both on the composed head".
  - #977's acceptance names only 1x1/1if and 8x8/1if: the measurement, and the bound "950 us at 1x1/1if, 1,475 us at 8x8/1if". Nothing on #977 mentions the Arty, `(1,1,2)`, #878 or #1004.
  - The PR body and HANDOFF state that without the disposition "the last queued notice is about 225 ms against its 140 ms owner bound". No published receipt shows that control derivation.
- Impact:
  - The Arty's owner-bound pass (last notice 117.47 ms) holds only with this debt excluded.
  - The issue named as the debt's owner can close without measuring or bounding this point. The owed lines would then have no owner, and the size of the debt has no published evidence.
- Required outcome:
  - A public record that a named issue carries the `arty-1x1` registration measurement and bound. That can be #977's acceptance amended, or a new issue that section 15 links.
  - Or a manager decision stating how this point's owed lines are discharged.
  - In either case, the no-disposition control derivation is published, so the debt's size is evidenced.
- Verification: the tracker's acceptance names `arty-1x1`. Section 15 cites it. The control derivation receipt is present.

### F2. MINOR. The service-budget README cites the superseded row's qualification as the Arty qualification

- Lens: `Docs`.
- Artifact: `tb/verilator/ctrl_service_budget/README.md:208-212`.
- Evidence:
  - It names "The published Arty qualification receipt", round 4's `build-corrected-final-census-qualification.json` at `0723eba4` (published `78be299b...`), which "records 145 measured cases".
  - That receipt qualified the 950 us / 9 ms / 30 ms row, which `f7b90e3b7` and `74f942be5` replaced.
  - The qualification of the installed row is `published-qualification.json` at `907764eb`: PASS, 147 groups, worst pass 142,775 cycles. Nothing in the tree cites it. Section 15 cites no receipt.
- Impact: a cold reader following the in-tree pointer audits the wrong qualification. It is a different row and a different case count. That is a verdict pointer, not wording.
- Required outcome: the README cites the qualification of the installed row by its published hash, or states that the cited receipt qualified the superseded row and names the current one.
- Verification: the cited file's `model` equals `arty_grade.py`'s output at the head, with 147 groups.

### R928-1-F1 (retained, narrowed). MINOR. The census observations behind the 147 grades are not public

- Lenses: `Conformance`, `Tests`, `Docs`. The RTL half is closed: see the resolution table.
- Artifacts:
  - The PR body, "Reproduce and inspect", and `receipts/INDEX.md` "Reproduce".
  - `FILES.tsv`: `census/` holds 22,600 files and 3,957,281,806 bytes, all unpublished.
- Evidence: the documented command fails on the published packet with `FileNotFoundError` on the first case manifest (`receipts/full-regrade-published-packet.log`). The case grades, observations, scenarios and stimuli exist only as hashes.
- Impact:
  - A cold reviewer cannot regrade any of the 147 cases or the cross-case step.
  - The qualification, and the step-2 regrade it rests on, are the author's execution evidence only.
- Required outcome, either of:
  - The extracts are published in an accessible archive whose hashes match `FILES.tsv`.
  - A public manager decision accepting hash-listed non-archival with access on request, and the PR's "Reproduce" text saying so.
- Verification: `receipt_regrade.py <packet>` exits 0 on the published archive, or the decision is linked from the PR.

### RESIDUE (wording only; exact fixes)

- **RS-A** `CHANGELOG.md:334`: "The split console's `milan_lat` writes the pair (#878)." `8e6001aa2` renamed the command, and `milan_lat` is now refused (`ctrl_plat_console.c:175-201`, `test_plat.cpp` K9). Fix: "The split console's `lat IIIII EEEEE` writes the pair (#878)."
- **RS-B** (R927-1 RS6, retained in a new form). The PR body says "Local head `4adfa9dc...`. Not pushed." It is the PR's head. Fix: "Head `4adfa9dc...` (the PR head)."
- **RS-C** The PR body says "Those are the totals of the previous route (round 6)". This reads as though the figures are not this route's, but they are (verified above). Fix: "These equal round 6's routed totals."
- **RS-D** The PR body "Validation" section and `receipts/INDEX.md` "Native census" say "every native executable, firmware ELF, flash image and all 147 stimuli are identical". No variant has a flash image (`identity.log`: `"flash": null` on both sides). Fix: "every native executable, firmware ELF and all 147 stimuli are identical; no variant builds a flash image".
- **R927-1 RS1 (retained)** `configs/endstation_arty_split.yaml:256-257`: "the manager verifies the split image on the bench after IMAGE READY". Fix: delete that clause.
- **R927-1 RS3 (retained)** Round labels stand in for decisions:
  - `docs/ENDSTATION_BUILDER.md:22` and `docs/integration/BUILDING.md:361`, "The owner's round-4 ruling".
  - `docs/integration/BUILDING.md:358`, "round 2's unachievable".
  - `tb/verilator/ctrl_service_budget/README.md:206`, "round-4 held-egress ruling".
  - Fix: cite [#878's held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930), and write "This replaces the unachievable 83,333,000 Hz request."
- **R927-1 RS4 (retained)** `docs/litex/CLOCK_DOMAINS.md:382`. Fix: "In VERSION `0x0002_0060` and a split image's `0x0003_0060`, ...".
- **R927-1 RS5 (retained)** `configs/endstation_arty_split.yaml:113`, "(N25Q128 QSPI)". Fix: "(S25FL128S QSPI)".
- No new source-comment instance of a lane label, review round, reviewer ID or comment ID was found in the delta's added code lines. The two in `ctrl_mutant_fixtures.py:9,30` were moved verbatim from `ctrl_mutants.py` (SG-8).

### SUGGESTION

- **SG-1** `receipt_regrade.py:164-168` breaks the WNS/WHS tie by directive name and prints `selected: ExtraTimingOpt`. `graded-images.json` selects AltSpreadLogic_high. Both are the same payload. Use the image grader's tie-break, or compare against `graded-images.json`'s `best`.
- **SG-2** `receipt_regrade.py` (new in this delta) has no `--selftest`. Planted controls could cover:
  - a part escaping its directory;
  - a part or whole hash mismatch;
  - a grade that differs;
  - `native_status != 0`;
  - an owner-model mismatch;
  - a Disposition breach.
  Its siblings all have one. Its only negative evidence is the author's runs on unpublished data.
- **SG-3** Step 2's derivation has two qualifying fixed points: (1250 us, 10 ms, 125 ms) and (950 us, 10 ms, 130 ms) (`derivation/model-installed-r7-step2.json`). The installed one is first by `derive-own.py`'s sort (pace, queued, slice) and is step 1's row. Section 15 should state that selection.
- **SG-4** Publish step 2's own build record, its `build.json` inputs and digests. The published step-2 `census-build.log` is step 1's file byte for byte, so "built at `74f942be5`" is evidenced only through `build.reused()`'s refusal logic.
- **SG-5** The census maxima and the #969 exclusion live in out-of-tree recipes (`census7.py`, `derive-own.py`). `STATED_NOW` is hard-coded to the step-2 statements, and step 1's version is unpublished. The in-tree gates enforce the upward direction and the slice, pace, queued and tx rules; "installed exactly as derived" is reproducible only from the recipes. Consider bringing them into the tree.
- **SG-6** ROM headroom: 125,572 live bytes against 126,976 in the 64+32+16+8+4 KiB banks (`product-size.json`), so 1,404 bytes before another bank. Worth a line in section 15.
- **SG-7** R927-1 SG1 (the `net_r` width guard), SG3 (`scripts/docs_inventory.json:236`, "retired DUT ... 83.333 MHz") and SG4 (`arty-1x1` bound to `endstation_arty_current`) are retained.
- **SG-8** `ctrl_mutant_fixtures.py:9,30` carries lane labels ("round 6 lane F2", "lane FC") moved from `ctrl_mutants.py`. Make sure #746's tracking follows the new path.

## Prior findings at this head

| Finding | Status at `4adfa9dc` | Evidence |
|---|---|---|
| R927-1 F1 MAJOR (closes #878 without items 4-7) | CLOSED | Ruling issuecomment-7153532537. The PR body says "Relates to #878". #878's item 3 all-fabric `firmware_version` difference stays with the open issue |
| R927-1 F2 MAJOR (stale `DOCUMENTATION_AUDIT.md`) | CLOSED | `docs_inventory.py --check` OK at the head (`receipts/doc-inventory.log`) |
| R927-1 F3 MAJOR (Python idiom ratchet) | CLOSED | `check_py_idiom.py` rc 0. The `2e2f1a34c` splits are pure moves and wraps; I compared added against removed lines |
| R927-1 F4 MINOR (MII guard untested) | CLOSED | `mii-publish-guard-removed` is caught by `ArtyPhy.AdvertisementDriftNeverPublishesUnsupportedMode`; `ForcedTen...` was added. The merge rewired the plant to `owed = true;`. My probe caught it |
| R927-1 F5 MINOR (`milan_lat` over FIFO) | CLOSED | `lat` is a fixed 15 bytes plus CR, `_Static_assert` against `CTRL_PLAT_RX_PER_PASS` (`ctrl_plat_console.c:175-201`). K9 drops every byte. The README requires a read-back check. 7/7 lat plants caught |
| R927-1 F6 MINOR (qualification hash unpublished) | CLOSED as raised | The README now relates `78be299b` to the local `f6f1d2f5`. That pointer is now stale: new **F2** |
| R927-1 RS1, RS3, RS4, RS5 | RETAINED | Listed above |
| R927-1 RS2 (`egress_ledger.py:13`) | CLOSED | Now "(#878)" |
| R927-1 RS6 (PR body stale) | RETAINED as RS-B | |
| R927-1 SG2 (MII retry uncounted) | CLOSED | The merge routes it through `renegotiate()` (`ctrl_plat_phy.c:134-140,346`) |
| R928-1 F1 MINOR (primary receipts absent) | PARTLY CLOSED | All 12 corner reports are published and regraded at the head. The census observations are still unpublished, so it is retained, narrowed |
| R928-1 F2 RESIDUE | CLOSED | `egress_ledger.py:13`, `yaml:142` and `yaml:155` read as fixed |
| R928-1 F3 MAJOR (bench acceptance) | CLOSED | Ruling issuecomment-7153532537: item 5 is a ruled deviation, item 4's offset stays on #878 via #1007, and items 6 and 7 are met. The PR relates rather than closes |

## Lens results

- **Conformance.** UNCLEAN: F1 and R928-1-F1.
  - The row matches the rule's choice: `arty_grade` checks slice, pace, queued and tx, and the qualification checks STATED. The owner bounds hold, and the five reported figures were reproduced.
  - The 80 MHz shape and the one-interface, one-source, two-sink shape are unchanged.
- **RTL.** CLEAN.
  - `git diff --stat` shows no `hdl/` or `sw/litex/` path in the lane commits, and none in the merge's conflict resolutions.
  - The routed image's 12 corner reports were regraded at the head, with 0 failing endpoints.
  - `check_timing` shows `no_clock` 0 and `unconstrained_internal_endpoints` 0.
  - Utilization was verified, and the two tied directives are one payload.
- **Robustness.** UNCLEAN: F1, the untracked registration debt at this point.
  - The `lat` parser's lost-byte and burst paths and the MII forced and drifted modes are covered by tests I ran and by plants.
  - The merge's `owed`/`renegotiate()` resolution is equivalent and counts the retry.
- **Tests.** UNCLEAN: R928-1-F1, the 147 grades cannot be regraded from public state.
  - Every in-tree grader self-test that the delta feeds passes at the head.
  - 15/15 focused plants were caught.
- **Docs.** UNCLEAN: F1, F2 and R928-1-F1.
  - Section 15's figures and tables match the receipts: the row, the retry fit 9767 / 1929 / 17193, the five owner figures, the ledger range 61.79729 to 63.29190, and the memory ledger against `product-size.json`.
  - All ten doc gates pass. RS-A through RS-D are recorded.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, R928-1-F1) | #878 body, rulings 7096503672, 7097204685, 7097474930, 7153532537; #969 rulings 7083542634 and 7116192252; #977 body; `ctrl_loop.h:400-417`; `arty_grade.py` run; `derivation/model-installed-r7*.json`; `qualification/qualification.json`; `recipes/census7.py.txt`, `derive-own.py.txt` | R927-2 | `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` |
| RTL | CLEAN | Lane and merge diff stats (no HDL); 12 `timing-r7/*/digilent_arty_signoff_*_timing.rpt` parts regraded at the head; `*_check_timing.rpt`; `*_utilization_place.rpt`; `graded-images.json`; `image/image_manifest.json` | R927-2 | `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` |
| Robustness | UNCLEAN (F1) | `ctrl_plat_console.c:141-201`; `ctrl_plat_phy.c:130-350` (merge resolution); `test_plat.cpp` K7/K9; `test_plat_phy_mii.cpp`; `kept_grade.py` `held`/`Disposition`; `step1-kept-grade.log`; host probe | R927-2 | `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` |
| Tests | UNCLEAN (R928-1-F1) | `receipt_regrade.py`; `plat_mutants.py` `lat_mutants`/`mii_mutants`; standalone self-tests (6) and host probe at the head; `receipt-regrade*.log`; `identity.log`, `identity-raw.log`, `reuse.log`, `recipes/reuse7.py.txt`, `identity7.py.txt`; full regrade over the published packet | R927-2 | `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` |
| Docs | UNCLEAN (F1, F2, R928-1-F1) | `SPLIT_CONTROL_MEMORY.md` section 15 (3486-3600); `tb/verilator/ctrl_service_budget/README.md:200-225`; `sw/firmware/ctrl/plat/README.md:60-80`; `CHANGELOG.md:322-335`; `BUILDING.md`; `ENDSTATION_BUILDER.md` row 33e; `GPTP_PLANE.md:484`; PR body; `receipts/INDEX.md`; 10 doc gates at the head | R927-2 | `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` |

## Real limits

- I regraded no census case. The extracts are unpublished, and I could not ask the manager for them in this session. The 147 grades, the step-2 regrade and the cross-case PASS rest on the author's logs, which are hash-bound to unpublished files.
- Round 6's route and its utilization are not in the published packet. "Equal to round 6" and the LUT-band comparison against it are unverified. The comparison against round 4 is computed above.
- I did not rerun the firmware shards, the Arty native boot or region simulations, the full 297-mutant service self-test, the census, routes or Vivado. I used the author's receipts at `74f942be5`. `2d911d2bf` and `4adfa9dc8` change only `docs/`, `receipt_regrade.py` and a README.
- No bench, flash or hardware step. The bench evidence (bench report rounds 1 and 2) is for the `248d85c1` image, not this one, and the PR says so. Physical calibration was NOT RUN.
- No manager source bank at this head is claimed or inferred.
- The `kept_grade` conditions were checked against the published log and the in-tree self-test. I did not plant a breach in a real packet.

## Pending manager duties

- Hosted contexts at the exact head: none recorded (0 check runs, status pending). The manager owns the hosted and act acceptance.
- Merge-candidate validation against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`: the builder and native banks.
- Decisions or records for F1 (the #977 scope at `arty-1x1`) and R928-1-F1 (census publication or accepted non-archival).
- Carry RS-A to RS-D and the retained R927-1 RS1, RS3, RS4 and RS5 to the residue checklist.
- Maintainer merge authorization and post-merge containment.
- The clone was restored and verified: worktree, index and tree equal to HEAD, and all six gitlinks at their HEAD commits (`receipts/restore-check.txt`).

R927-2 FINISHED
