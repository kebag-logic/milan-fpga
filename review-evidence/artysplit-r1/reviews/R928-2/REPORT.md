[R928] NEGATIVE - exact head 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1

External independent review R928-2 of [PR #1004](https://github.com/kebag-logic/milan-fpga/pull/1004) / [issue #878](https://github.com/kebag-logic/milan-fpga/issues/878). Tree: `ee1b81d4fcd318aeca7c37c8096d35e0e056ea8a`. All five lenses were applied. Two MINOR evidence findings remain open. The focused checks establish no new functional implementation defect.

The public packet **P** is [review-evidence/artysplit-r1 at 907764ebbc99dad85babf522da92c13d92ab20aa](https://github.com/kebag-logic/milan-fpga/tree/907764ebbc99dad85babf522da92c13d92ab20aa/review-evidence/artysplit-r1); **E** means `P/author-r7/receipts`. Unprefixed source paths refer to the exact head above. Review receipts and scripts are relative to this report.

AGENTS.md, CONTRIBUTING.md, the documentation map, frozen issue acceptance and public decisions were reconstructed before the requirements, interfaces and diff. The original-base diff and history were inspected, concentrating on the delta from `248d85c1453213b0f1642967a4046f395c82c56b`, its merged platform dependency `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, and the final scheduler/receipt changes. Prior public findings were read only after an independent diff pass and provisional ledger. No private author material or another current reviewer's report was used.

**R928-2-F1 — MINOR — Conformance, Tests, Docs — the packet cannot reproduce the 147 grades or independently establish both steps' byte identity.**

Artifact: `E/FILES.manifest.json` and TSV parts; `E/census.json`; `E/validation/receipt-regrade.log`, `receipt-regrade-control.log`, `identity.log`; `tb/verilator/ctrl_service_budget/receipt_regrade.py:192`; PR “Reproduce and inspect”.

Authority/evidence: AGENTS.md sections 1, 6 and 7 require reconstructible evidence. This round explicitly requires reproduction of all 147 grades and verification of every executable, ELF, flash image and stimulus between the steps. The public manifest's 2,141 non-review files all verify. The separate full-campaign inventory lists 22,866 files: 266 are available and hash-correct, 22,600 are absent. The omitted `census/` directory includes the case manifests and text observations needed by the regrader, not just bulky raw simulator output.

Running the exact-head regrader against the published packet passes all twelve timing reports, then exits 1 on the first absent `census/answering-every-port/notice-burst-0/manifest.json`. No case grade was independently reproduced. The author log names all 147 unique indexed cases and a passing cross-case result; its missing-bound control log records refusal. These are consistent execution receipts, but are not the inputs needed to reproduce those results.

The identity receipt reports eight matching executable/ELF pairs and 147 matching stimuli. Its rows contain a single agreed hash for each product, not independently inspectable step-1 and step-2 product inventories. The comparison recipe and normalized-input rationale are present. Independent byte comparison remains unavailable. In these non-XIP native builds `flash: null` is expected: `build.py` emits a separate flash image only for XIP. This finding does not demand nonexistent native flash images.

The raw 3.7 GB census was explicitly declared unarchived. The requested remedy is access to retained extracts and paired identity evidence, not putting all raw output in Git. Those artifacts were requested during this review and were not supplied before the report closed. See `audit.log`, `missing-census.json`, `receipt-regrade.log` and `receipt-regrade.rc`.

Impact: measured qualification and safe reuse of step-1 traces cannot yet receive independent signoff. This is an evidence gap, not a claim that executions failed or products differ. It retains the execution-observation portion of R928-1-F1; that finding's raw-timing portion is now resolved.

Required outcome: provide an accessible, hash-bound archive of all 147 case manifests, observation extracts and grades, plus both steps' build/product and stimulus identities sufficient to verify the comparison. Preserve source/image binding and explain the null native flash field. An equivalent accessible archive is sufficient; no rerun is inherently required.

Verification: run the current regrader to reproduce all 147 grades and cross-case checks; run the missing-`srp-bound` control and require refusal; independently compare each step's executable, ELF, applicable flash image and every stimulus. Recheck conditional #969 exclusion against those observations.

**R928-2-F2 — MINOR — Conformance, RTL, Tests, Docs — the routed-total LUT comparison lacks routed utilization evidence.**

Artifact: `E/timing-r7/AltSpreadLogic_high/digilent_arty_utilization_place.rpt:10` and its table; PR “Source and image”; FILES inventory.

Authority/evidence: the requested owner area test is the routed-total LUT band of approximately 50 LUTs against the previous routed image. The report supplying 33,015 LUTs, 40,369 FFs and 78.0 BRAM tiles explicitly says `Design State : Physopt postPlace`; its command is `report_utilization ... utilization_place.rpt`. The PR correctly calls these post-placement figures, then says they equal the previous route's totals. Neither the previous round-6 routed utilization report nor a current post-route utilization report is supplied in this packet. Equality of post-placement totals does not establish the routed-total comparison. `audit.log` records report state and indexed utilization filenames.

Impact: setup/hold timing is independently supported, but the requested area comparison cannot be verified. No area overrun is asserted. The older 33,411-LUT image is not substituted for the specified round-6 reference.

Required outcome: provide utilization from the selected final routed implementation and the previous routed reference, with source/image or checkpoint identity, and calculate the routed-total LUT delta against the owner's band. If an owner decision authorizes a different measurement stage, link that explicit decision.

Verification: inspect both design states and bindings; recompute total LUT difference and report the actual comparison. Retained routed checkpoints are sufficient; this finding does not prescribe another implementation run.

**Prior public finding dispositions**

Prior reports: [R928-1](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7147188140) and [R927-1](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7147439126).

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R928-1-F1, missing primary receipts | Partly resolved; retained as F1 | Twelve full timing reports now reassemble, hash-verify and grade. Case extracts and paired identity evidence remain unavailable. |
| R928-1-F2, source chronology residue | Resolved | All three identified wording changes are present: egress-ledger header, MRP reset comment and reflash comment. |
| R928-1-F3 / R927-1-F1, frozen acceptance and premature issue closure | Resolved as scope findings | [Acceptance ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7153532537) accepts endpoint counters in place of capture, records soak/save evidence, retains missing offset measurement under #1007 and keeps #878 open. PR now says “Relates to #878”. This does not turn the previous bench image into current-head hardware evidence. |
| R927-1-F2, documentation inventory | Resolved | `python3 scripts/docs_inventory.py --check` passes; `docs-inventory.log`. |
| R927-1-F3, Python idiom ratchet | Resolved | Extracted helpers retain behavior; `python3 scripts/check_py_idiom.py` passes without ratchet weakening; `python-idiom.log`. |
| R927-1-F4, ineffective MII publication-guard test | Resolved | Removing the guard is caught by `AdvertisementDriftNeverPublishesUnsupportedMode` (four failed checks). `host-mii.log`, `host-plants.log`. The merged platform's repair path changes how the older forced-BMCR case reaches the guard; the advertisement-drift case directly protects it. |
| R927-1-F5, lossy oversized latency command | Resolved | `ctrl_plat_console.c`, `test_plat.cpp` and platform README specify `lat IIIII EEEEE\r`, exactly 16 bytes. Five-digit widths are mandatory; dropped data digits, unequal widths, extra data and values above 65535 are refused. Tests and plants pass. |
| R927-1-F6, qualification hash citation | Resolved | Service README lines 208–212 distinguish the earlier local citation from the published receipt identity. The old published qualification and manifest verify. Citation repair does not resolve F1. |

For the descriptor part of R927-1-F1, REQUIREMENTS.md assigns different major versions to split and all-fabric placement, with the same minor version for the same model. Thus `3.96.0` versus `2.96.0` is an explained firmware identity difference, not a changed descriptor layout; IEEE 1722.1 6.2.2.8 remains the model-identity authority.

**RESIDUE — Docs — exact wording fixes**

These change wording only, not code behavior, measurements, figures, generated artifacts, verdicts or normative requirements. They do not unclean a lens.

| ID | Artifact and evidence | Impact / required exact outcome | Verification |
|---|---|---|---|
| R928-2-RS1 (new) | `sw/firmware/ctrl/test/ctrl_mutant_fixtures.py:7` and `:30` introduce copied “Lane FC”, “Lane F3”, “round 6 lane F2” and “lane FC, rule 1” in a new file. Owner source-comment rule forbids these labels. | Replace lines 7–9 with “The open takes every interface's own MAC; boot composes ADP, ACMP and MAAP before opening (#665).” Replace line 30 with “802.1Q C-tag before it (#665, NFR-SCOUT-08).” Leave fixture strings unchanged. | Inspect comments and confirm fixture values are identical. |
| R927-1-RS1 retained | `configs/endstation_arty_split.yaml:256`–257 retain manager/IMAGE READY workflow. | Replace that clause with “#878 keeps this board's calibration.” | Comment-only diff. |
| R927-1-RS3 retained | `docs/ENDSTATION_BUILDER.md:22`, `docs/integration/BUILDING.md:361`, service `README.md:206` call the decision “round-4”; BUILDING line 358 says “round 2's”. | Cite [#878's held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930) by decision; at line 358 write “This replaces the unachievable 83,333,000 Hz request.” | Same limits/decision, chronology removed. |
| R927-1-RS4 retained | `docs/litex/CLOCK_DOMAINS.md:382` names only VERSION `0x0002_0060` above the correct optional-key behavior. | Write “In VERSION `0x0002_0060` and a split image's `0x0003_0060`, ...”. This clarifies the version display without changing the register contract below it. | Check version constants. |
| R927-1-RS5 retained | `configs/endstation_arty_split.yaml:113` says “N25Q128 QSPI”. | Replace with “S25FL128S QSPI”, as the board implementation identifies it. | Comment-only diff; generated settings unchanged. |
| R927-1-RS6 partly retained | PR “Source and image” says “Local head ... Not pushed.” Roles are now correct. | Replace with “Published head `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1`.” Keep the image/source distinction. | Compare PR to its published head. |

R927-1-RS2 is resolved by the egress-ledger wording repair, also covered by R928-1-F2.

**SUGGESTIONS**

Each item is optional and leaves coverage unchanged.

| ID / lenses | Artifact, evidence and impact | Suggested outcome and verification |
|---|---|---|
| R928-2-SG1 / Tests | `ctrl_mutant_fixtures.py:55`, `scenario_types.py:48`, `selftest_trace.py:55`, `tier_design.py:43` have an extra blank line at EOF; `git diff --check 854bd7236792ce1adbd10c43b13a6a5002ad3bb6 HEAD` exits 2. Same result against the merged platform base. No behavioral effect. | Remove those blank lines and rerun. This is optional formatting: the mechanical hygiene policy distinguishes blank layout from trailing-whitespace debt; no mandatory `git diff --check` gate was established here. This is not a hosted-gate failure claim. |
| R927-1-SG1 retained / RTL, Robustness | `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:310`: signed 18-bit intermediate fits today's correction, but no elaboration assertion bounds the parameter plus maximum runtime correction. | Optionally assert the range and exercise accepted/refused boundaries. No present overflow found. |
| R927-1-SG3 retained / Docs | `scripts/docs_inventory.json:236` still uses retired 83.333 MHz Arty-recipe wording. | Update description and regenerate/check audit if needed. |
| R927-1-SG4 retained / Tests, Docs | `run.py` / `shape_costs.py` bind the Arty harness to `endstation_arty_current` rather than the shipped split config; checked shape and 80 MHz clock agree. | Optionally name the shipped config directly, retaining generated-input identity checks. |

R927-1-SG2 is resolved: the merged MII path uses common renegotiation accounting and tests cover repair/retry behavior.

**Conformance and scheduler examination**

The one-interface, one-AAF-talker, one-AAF-listener and CRF-input shape remains intact. The [entity/mode decision](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz decision](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), held-egress ruling, REQUIREMENTS.md and FR_NFR.md section 3.4.1 were checked against `configs/endstation_arty_split.yaml`, `ctrl_loop.h`, `arty_grade.py` and Arty model tables.

Reexecuting the published derivation recipe on its merged census reproduces the derived model and installed step-2 model exactly. All 42 census cost roundings reproduce: cycles at 80 MHz, plus five percent, rounded upward to 5 us. The installed row is a fixed point: slice 1250 us, pace 10 ms, queued bound 125 ms, transmit bound 35 ms, retry cold 130 us. Both MRPDU builds cost 1035 us, so `CTRL_LOOP_BUILD_MOST` is 2. Poll base 235, centisecond 160, LINK 190, MAAP 165 and withdrawal 95 us agree with the tables.

| Quantity | Result | Owner bound |
|---|---:|---:|
| Load, independently reproduced model | 0.5004771140350878 | 0.70 |
| ACMP, model | 29.77 ms | 30 ms |
| txL, model | 48.82 ms | 49 ms |
| Last queued notice, model | 117.47 ms | 140 ms |
| Whole-pass maximum, author measured receipt | 142775 cycles / 1.7846875 ms | 2 ms |

The whole-pass row is author observation evidence, not independently measured here. ACMP, txL and SHARE margins are 0.23, 0.18 and approximately 0.215 ms.

The [#969 amendment](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252) permits only owed SRP measurements, conditional on kept-record grading. `kept_grade.py`, `run.py` and the final receipt-regrader change preserve that condition. They require paired groups, compare kept against bound records with the allowed five percent, retain kept/idle/whole-build limits, and distinguish owed bound work from ordinary work. LINK/withdrawal costs from `srp-kept` and centisecond cost from `srp-bound` still contribute.

All 32 kept-grade controls pass, including missing pairs/observations, threshold equality/overrun, SHARE and ambiguous slice cases. Independently restoring all excluded owed costs to the derivation yields **NO QUALIFIED MODEL**, zero qualified choices. This is an arithmetic control, not a substitute for the missing-group receipt control: the latter's published log shows refusal, but F1 prevents rerunning it from observations.

The seven held-egress entries retain their ledger: 60 ms hold plus 1.05 times service behind it, rounded upward to 0.01 ms. They remain ordinary-budget misses with separate authorization; no new miss class is waived. Ledger and record controls pass.

**RTL and architecture examination**

The scheduling constants/helper extraction do not alter the 80/25/50/200 MHz plan, exact 800 MHz VCO divisions or margin-zero settings. Clock/correction paths were checked in `sw/litex/milan_soc.py`, `milan_datapath.sv`, `milan_csr.sv`, `KL_gptp_shadow.sv` and `KL_gptp_txret.sv` against clock-domain/register authorities. Existing asynchronous FIFO/mailbox crossings remain. Writable corrections and consumers remain together in the datapath domain; ingress snapshot and signed egress arithmetic are unchanged by the later delta. Prior clean coverage of unchanged constant-correction/default-off behavior is retained.

All twelve full timing reports reassemble and hash-check. Independently grading them yields:

| Directive | Slow 0/85 C WNS / WHS, ns | Fast 0/85 C WNS / WHS, ns | Result |
|---|---|---|---|
| ExtraTimingOpt | +0.433 / +0.138 | +1.606 / +0.050 | PASS |
| AltSpreadLogic_high | +0.433 / +0.138 | +1.606 / +0.050 | PASS |
| ExtraPostPlacementOpt | +0.064 / +0.126 | +1.606 / +0.050 | PASS |

Every report has zero failing setup/hold endpoints. AltSpreadLogic_high meets setup >= 0.030 ns and hold >= 0. The regrader chooses ExtraTimingOpt by tie-break; their graded metrics tie, so this is not a failure. Temperature labels are report metadata, not hardware measurements. F2 concerns the distinct resource comparison.

The post-place report gives 33,015 LUT, 40,369 FF, 78.0 BRAM and 13,791 slices. Product firmware receipt and memory ledger agree: text 113908, rodata 11558, data 100, bss 45136, stack 8192 bytes; live ROM 125572, SRAM 53456; allocation 31 + 13.5 = 44.5 of 56 RAMB36. Bitstream identity is `24a782c505c1ae4aea61d2abf1b1dd2e2cf0e5aa08e12a717e10cfddb37a871e`; ELF identity is `b6cfb9a4e051e865101ceb220a3dfe4f7c487938c97d3e764c0f7407085038d2`. These are published product identities, not locally rebuilt products.

Step 2's compiled-header change is `CTRL_LOOP_TICK_US` 150 -> 160; searches find no compiled firmware consumer. Other changes are grading/model tables. The author identity recipe compares generated dates separately from meaningful inputs. This supports trace reuse at source level; F1 reserves the independent byte comparison.

**Robustness and Tests examination**

The console accepts two five-digit decimal fields, retains 0..65535 bounds, rejects extra fields/lost data digits, and retains disabled-key refusal. The documented flow checks readback before using a correction. Both console configurations pass (13 and 14 tests), plus two MMIO tests. MII passes ten tests covering incompatible modes, lost writes, unacknowledged operations, budget refusal, latched loss and repair. All fifteen focused console/MII planted defects are caught, including publication-guard deletion.

Extracted scenario, tier-design, trace and mutation-fixture helpers preserve imports, case definitions and test meaning. Row controls pass 1033/1033; owner, kept, ledger and record controls pass. The receipt parser checks part/whole hashes and reparses observations rather than trusting grades. Its end-to-end measured-data claim remains limited by F1.

Author receipts provide four successful firmware shards, Arty boot/native controls and region controls at `74f942be516b84915f7d982fe1e3c65b497c227a`, plus 297/297 service mutation results in eight partitions. Later changes are documentation and the receipt regrader, whose current conditional disposition was inspected. Ten documentation/quality receipts identify the final head. These are author source-validation receipts. No manager source bank exists at this head and none is inferred.

The [second bench report](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7149406265) records 3683 seconds of concurrent-stream observations and timed descriptor save/reset/readback. It concerns the earlier image. The acceptance ruling accepts endpoint observations instead of capture and leaves true offset measurement outstanding. It does not establish current-image field/calibration performance.

**Documentation examination**

`docs/design/SPLIT_CONTROL_MEMORY.md` section 15, `docs/integration/BUILDING.md`, `docs/ENDSTATION_BUILDER.md`, `docs/litex/CLOCK_DOMAINS.md`, platform/service READMEs, CHANGELOG, generated audit and PR were checked against installed constants, optional correction interface, measured versus stated evidence and issue scope. Fixed-point/model and memory descriptions agree with published receipts. Inventory and Python gates pass. Remaining reproducibility/resource claims are F1/F2; wording residue and optional cleanup are collected above.

**Reviewer-owned ledger**

UNCLEAN means the lens was applied but cannot be banked clean. Every entry refers to this exact head; this ledger does not release a merge.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | #878 acceptance/rulings; #969 amendment; REQUIREMENTS.md; FR_NFR.md 3.4.1; split config; ctrl_loop.h; arty_grade.py; census/derivation; timing/resources | R928-2 | 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1 |
| RTL | UNCLEAN: F2 | milan_soc.py clock/CDC; milan_datapath.sv corrections; milan_csr.sv writes; KL_gptp_shadow.sv / KL_gptp_txret.sv arithmetic; twelve timing reports; utilization; memory ledger | R928-2 | 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1 |
| Robustness | CLEAN | ctrl_plat_console.c / test_plat.cpp loss/widths; ctrl_plat_phy.c / test_plat_phy_mii.cpp repair/publication; host-plants.log; kept_grade.py / egress_ledger.py controls; acceptance ruling | R928-2 | 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1 |
| Tests | UNCLEAN: F1, F2 | receipt_regrade.py; kept_grade.py; extracted helpers; identity manifests; checks.json; host-results.json; author gates-results.json; resource provenance | R928-2 | 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1 |
| Docs | UNCLEAN: F1, F2 | SPLIT_CONTROL_MEMORY.md section 15; BUILDING.md; ENDSTATION_BUILDER.md; CLOCK_DOMAINS.md; platform/service READMEs; DOCUMENTATION_AUDIT.md; PR; receipt inventory | R928-2 | 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1 |

[R928] PASS Robustness — `sw/firmware/ctrl/test/test_plat.cpp`, `test_plat_phy_mii.cpp`, `host-plants.log`, `kept-controls.log`, `ledger-controls.log` — applied loss, overflow, disabled-option, invalid-mode, failed-write, retry and bound-overrun checks against console/PHY contracts and #969/held-egress rulings; no open finding under this lens.

**Reproduction and final integrity**

Scripts take source checkout and output packet as positional arguments. `checks.py` and `audit.py` also take extracted public P as their third argument. Run with `python3 -B`. `host_checks.py` uses disposable copies under `scratch/host`, with bounded concurrent jobs. `integrity.py <source>` verifies raw tracked blob bytes, modes, index and initialized required submodule contents. All checks and campaigns were joined to completion; no process was left running.

`checks.json`, individual logs/return codes, `host-results.json`, `audit.log`, `derived-model.json`, `without-disposition.json`, `missing-census.json`, `diff-check.log` and `integrity.log` are the receipts. MANIFEST.sha256 lists publishable files. Local paths in text receipts are normalized to SOURCE/PACKET placeholders; results/diagnostics are unchanged. Provisional material and disposable trees are excluded.

Final integrity verifies 2,000 parent tracked entries, exact tree/index, empty status, and these required submodule gitlinks plus checked-out tracked bytes/modes:

| Submodule | Commit |
|---|---|
| protocol-processor | 801ef2283ec793e35a2590fc6593c90313a64041 |
| gptp-processor | 1213ac5b9e09b8759ba76cc70c53652b5e108996 |
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce |
| third_party/tsn-c-stack | 715589c1db7cf67e2f3259fd7083ebc7f0923376 |
| third_party/lwSRP | d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b |

Public manifest and part hashes verify. The evidence commit has no embedded cryptographic signature; this review claims hash/provenance verification, not verification of a cryptographic signer.

**Real limits and pending manager duties**

No full parent, processor, synthesis or builder banks, hardware work or implementation routes ran here. No full native census was repeated; the native simulator was not invoked by focused host probes. Physical calibration remains **NOT RUN**; skipped field gates are not hardware proof. Older bench results are not relabeled as execution on this image.

Hosted/local-replica acceptance remains the manager's responsibility; no claim is made about executed versus skipped hosted contexts. There is no manager source-bank result at this head. Source validation is distinct from final current-dev candidate validation: original source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`, stated live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`.

The manager must obtain F1/F2 artifacts and independent re-review, publish residue dispositions, run/link current-dev merge-candidate builder/native receipts, satisfy hosted/local-replica gates, obtain explicit maintainer merge authorization and perform post-merge containment. Keep #878 open for offset acceptance under #1007. This report supplies no merge authorization.

R928-2 FINISHED
