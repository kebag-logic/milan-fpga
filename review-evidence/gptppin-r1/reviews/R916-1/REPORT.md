[R916] NEGATIVE - exact head bbfdb6746d585e490508783dc8a88c79fbab02c0

Round R916-1, external independent review of issue #994 and PR #995. One MAJOR finding remains: the adopted behavior has no defect-detecting platform regression. Two deliberately restored defects pass both existing platform slices. No production RTL defect was found in this review. One wording residue is listed separately.

## Scope and reconstruction

Reviewed only `300da99beed5bb1c77e4b04af0bb4f9369856e0d..bbfdb6746d585e490508783dc8a88c79fbab02c0`: four commits, twenty paths. The reviewed tree is `eb8282dfbfa9d8dc2e1c87bc3c09b5c010d30263`. The composed train in PR #988 is outside this review.

Read the repository operating contract and CONTRIBUTING, the documentation index, #994's frozen acceptance, requirements and integration authorities, then the delta/history and executable evidence. The public author packet is [gptppin-r1/author at 37794460](https://github.com/kebag-logic/milan-fpga/tree/3779446004dfb5ea4b18088bed83637e49139754/review-evidence/gptppin-r1/author). No private author material or other review report was read. `independent-pass.md` records the verdict and ledger before the PR discussion reconciliation.

The three frozen issue criteria are evidenced: current pins agree; consumer suites and both requested integration legs have passing author receipts; both selected release routes fit and meet #818. The additional mandatory verification bar remains unmet by F1. A passing existing suite is not coverage of the changed behavior.

## Findings

### R916-1-F1 | MAJOR | Conformance, Robustness, Tests

**Artifact:** `tb/verilator/gptp_plane/sim_main.cpp:506`, `tb/verilator/gptp_shadow/sim_main.cpp:1311`, `tb/verilator/milan_dp/sim_gptp.cpp:2057`; PR #995, Known limitations, “No platform test is added.”

**Authority/evidence:** CONTRIBUTING.md section 3 requires self-checking tests for functional RTL changes and favors real integration wiring. REQ-PTP-05 covers the fabric engine, receipt timers and PHC servo. The changed contracts at `docs/design/GM_LOSS_RECOVERY.md:46` and `docs/design/GPTP_PLANE.md:94` promise an immediate first Announce and oscillator-rate mastership. The review scope explicitly requires platform coverage of both.

The existing PHC slice waits for mastership and checks eventual frame contents. The shadow slice permits up to 2,000,000 clocks for the first Announce stamp. The datapath leg scans eventual Announce traffic and clockQuality after a long ride; it does not grade the receipt-deadline/re-election race. The parent tests do not assert the takeover rate and resulting real-counter slope after nonzero slave trim.

Independent disposable probes restore (a) the old 2 ms first-Announce arm and END at SELF, and (b) word 3 applying only during an active slew. These correspond to the donor's own #106/#107 defect controls. Both remain green in the parent suites:

| Disposable case | PHC slice `run` | Shadow slice `run` | Observed master addend, Q8.24 |
|---|---:|---:|---:|
| Exact-head control | 31/31, rc 0 | 326/326, rc 0 | 0 |
| Delayed first Announce | 31/31, rc 0 | 326/326, rc 0 | 0 |
| Retained slave rate | 31/31, rc 0 | 326/326, rc 0 | 13,414 |

The last column comes from a separate observation-only print after mastership; its patch and logs are included. It demonstrates an active rate defect, not merely a mutation that never executes. The original tests and their expected values were unchanged. These are focused `run` targets, not the full default mutation campaigns. `probe.py`, `follow_probe.py`, the case patches, logs and return-code files reproduce the evidence.

**Impact:** the platform regression can remain green when either behavior this adoption exists to deliver is broken. Donor-only coverage cannot prove the parent's transport and PHC consume the corrected behavior.

**Required outcome:** add a platform regression through parent transport and the real PHC. Grade the first master Announce before queued re-election at the receipt deadline, including cadence and transmit-credit behavior. Establish nonzero slave trim, take mastership, and grade rate zero and oscillator counter advance without a phase step; cover settled and slewing cases, both rate signs, and repeated mastership/no-new-slave-rate behavior. The existing donor controls provide useful negative cases, but do not replace this platform test.

**Verification:** the exact corrected head passes these platform assertions; restoring the delayed Announce and conditional rate-write defects makes the relevant assertions fail. Re-run the affected consumer gates and `milan_dp` gptp/gptp-lat legs. Moving the missing regression to another issue does not resolve this finding.

### R916-1-R1 | RESIDUE | Docs

**Artifact:** PR #995 Description, commit table, `973f2f20` row; public packet `author/PR-BODY.md`, same row.

**Authority/evidence:** the table lists three commits after `973f2f20`, but its row says “the two later commits change no synthesis input.” The no-synthesis-input conclusion is correct; the count is stale.

**Impact:** wording only. It changes no measurement, test, generated artifact or conformance claim.

**Exact fix:** replace “the two later commits” with “the three later commits.”

**Verification:** compare the sentence with `git log 300da99b..bbfdb674`. This residue does not make Docs unclean.

## Results across all five lenses

**Conformance:** checked #994 against current pin sites, published tests and both route shapes; all three explicit criteria have evidence. Checked REQ-PTP-01/05/07 and the parent takeover contract against the imported delta. F1 leaves the required behavioral verification incomplete.

**[R916] PASS RTL - `gptp-processor/hdl/top/KL_gptp_engine.sv:958` and `:1283`; `gptp-processor/hdl/ucode/gen_gptp_ucode.py:1994`, `:2036`, `:2487`; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:717` and `:784`; `hdl/milan/milan_datapath.sv:3259` and `:9265` - imported control changes preserve parent ports, clock/reset assumptions and wiring.** The BECOME word has zero in its low half and the signed negated estimate in its high half. The rate write is unconditional; the wrapper latches it into the PHC path. The slave-rate-seen flag clears at mastership, avoiding a stale frequency-change report on repeated takeover. The signed multiply retains its existing scaling pipeline. SELF reaches ANNTX after publication; role, asCapable and credit gates remain. No new CDC, port, parameter or configuration interface is introduced. No changed source comment contains the prohibited review or bench identifiers.

**Robustness:** inspected reset/no-prior-rate and repeated-mastership handling, Announce expiry ordering, disabled role/asCapable paths, credit refusal and cadence re-arm, plus the shadow suite's malformed-frame, reset, ledger and backpressure assertions. Existing checks pass at the exact-head control. F1 leaves the changed deadline and rate-transition cases unprotected at platform level.

**Tests:** inspected the imported #106/#107 controls, parent PHC/shadow/datapath assertions, and author receipts. Ran the paired controls and faults above concurrently, with at most fifteen compiler jobs. Fault survival is a test weakness, not proof of a defect in the unmodified head. No full parent, processor, synthesis or builder bank was run by this reviewer.

**[R916] PASS Docs - `docs/reference/SUBMODULES.md:24` and `:949`, the four `docs/guides/gptp/` pages, `docs/design/GPTP_PLANE.md:33`, `docs/design/TIME_SYNC.md:118`, `docs/reference/STRICTER_READINGS.md:100`, `docs/traceability/ieee8021as.md:53`, `CHANGELOG.md:65`, both pin diagrams and `syn/yosys/rom_digests.tsv:17` - current pins and behavioral descriptions match the adopted revision.** Historical measurements retain their original pins. Both diagram generators pass their no-drift checks; PNG/source manifest hashes match, and both rendered PNGs were visually inspected. The regenerated default ROM has 1,013 real words and SHA-256 `4eb21cefc8d769df4a764402aead970b59be96cb3fa267d25af9d1857935f083`, equal to the tracked donor image and new ledger row. The live PR body differs from the packet only by the added stacking explanation; its measurements match the packet. R1 is wording residue only.

## Route and execution evidence audit

The adopted donor pin fast-forwards `1616fc8f`; its tree equals reviewed donor head `331e27de`, tree `7b579e33a97ff4f2bec8c0064f0f73c862bbb135`. The adoption's route receipts were produced at `973f2f20`; the consumer legs at `39e9c9d2`; the sweep at `8c5a51e1`. These are ancestor evidence, not executions on `bbfdb674`. Inspection confirms no intervening runtime/synthesis input change. The route base's `c2b2ba1a..300da99b` delta is documentation/tests and an AST-identical string rewrap in `sw/litex/ctrl_memory.py`.

| Selected release image | Base LUT | Adopted LUT | Delta | Worst WNS/WHS | #818 |
|---|---:|---:|---:|---|---|
| 8x8/1if, ExtraPostPlacementOpt | 46,621 | 46,246 | -375 | +0.066/+0.036 ns | PASS, all four corners |
| 1x1/1if, ExtraTimingOpt | 32,680 | 32,639 | -41 | +0.170/+0.024 ns | PASS, all four corners |

Both selected builds have rc 0 and published image-identity success receipts with bitstream/manifest/firmware hashes. BRAM/DSP remain 98.5/13 and 80.5/13. The first 1x1 placement misses setup at +0.007 ns; the selected +0.170 ns result exceeds the third directive's +0.072 ns. The 1x1 signoff text also prints `rc=1` for an additional WHS >= +0.030 test. That extra threshold is not #818: [the issue](https://github.com/kebag-logic/milan-fpga/issues/818) and `docs/integration/BUILDING.md:616` require WNS >= +0.030 and WHS >= 0. Recomputing those actual floors passes both selected images. No route or identity gate was rerun here, and the binary artifacts were not independently rehashed from their original build directories.

The [owner's donor decision](https://github.com/Mister-M-alt/FPGA-gPTP/pull/108#issuecomment-7121892317) accepts 43,022 -> 43,477 LUT, +455, on the older parent base. The adopted composed base measures -375; the +455 does not appear here. This is a different placement/mapping comparison, not demonstrated area recovery.

The author packet records gptp/gptp-lat at 212/212 each, with clockQuality `0xF822436A` and `0xF8FE436A`. The sweep records gptp_shadow, gptp_plane, gptp_tables and gptp_txts PASS. Its four shards total 65 suites and 2,715,829 checks, with 64 passing initially; the mailbox harness rerun passes with the documented make-output flag. The field campaigns were initially skipped and subsequently run: 675 gPTP and 164 AAF passes. The so-called physical simulation suite records 205 checks; its printed field exclusions remain exclusions.

The exact-final-head author synthesis receipt contains successful lint, selected elaboration/synthesis tops, OOC selftest and split-CDC results. The documentation-step receipt records 56 rc 0, 24 skipped steps and three SDK-provenance refusals; it is not an all-green executed workflow. Builder legs record one NOT RUN each. The public firmware comparison receipt states 24/24 hashes identical, with the ledger passing; this review did not rebuild those images or independently retrieve the base ledger. `artifact-audit.log` records the bounded checks and exact artifact identities.

## Prior public findings and scope decisions

After writing the independent verdict/ledger, read the merged PR discussion timeline. It contains two manager review-start comments, including [this round's start](https://github.com/kebag-logic/milan-fpga/pull/995#issuecomment-7128360806), and no prior findings or review verdicts. Issue #994 has no comments in the retrieved public snapshot. Thus there are no earlier PR #995 findings to resolve or retain at this head. No public decision waiving platform coverage was found. The PR body's deferral is an author statement, not such a waiver. `public-snapshot.json` preserves the retrieved body and relevant discussion/owner decision.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #994; REQUIREMENTS.md:172; SUBMODULES.md:24,949; route receipts; changed integration contract | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| RTL | CLEAN | imported engine:958,1283; generator:1994,2036,2487; shadow:717,784; milan_datapath:3259,9265 | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Robustness | UNCLEAN (F1) | deadline/credit and settled/slewing/repeated-mastership paths; parent shadow reset/backpressure cases; fault receipts | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Tests | UNCLEAN (F1) | PHC and shadow controls/faults; milan_dp/sim_gptp.cpp:2057; published sweep and leg receipts | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Docs | CLEAN (R1 residue) | twenty-path diff; current pin sites; both diagrams; ROM ledger; live PR body/public packet comparison | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |

## Limits and pending manager duties

This is source-delta review, not validation of a merge with live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. There is no manager source bank at this exact head, and none is claimed. Hosted job execution was not independently audited here; neither skipped contexts nor author local equivalents are counted as hosted execution. Hosted/local-replica acceptance remains with the manager.

Before merge: fix F1 and obtain corrected-head re-review, resolve the residue, finish both independent reviews and the coverage ledger, then validate the current-dev candidate with the required builder/native banks and publish those receipts. Preserve the distinction between inherited source receipts and candidate execution. Containment and issue completion remain post-merge duties.

Physical calibration was NOT RUN. Field skips, diagnostic traffic, software simulation and route timing are not hardware proof. No standards PDF was independently revalidated; clause interpretation was checked against the repository requirements and imported interface authorities.

All probe trees/builds are confined to `scratch/` and excluded from publication. Source checkout bytes were never edited. `integrity.log` proves raw blob bytes, executable modes and index entries against the exact head, plus every required submodule's bytes and gitlink. The historical unused external gitlink remains unchanged and uninitialized. The source status is clean. No commits, pushes, GitHub writes or merges were made.

Reproduction: run `probe.py`, then `follow_probe.py` with source checkout, packet directory and the pinned simulator as arguments; run `checks.py` and `review_audit.py` with source/packet arguments; run `integrity.py` with the source argument. The probe clones must be absent before rerunning those two creation steps. The initial audit-script attempt used a file hash for a raster hash; that reviewer-script error was corrected to decoded-raster hashing before the recorded passing audit. It was not a product finding. `package_receipts.py` normalizes host paths in logs and builds the publication manifest; behavioral outputs and return codes are preserved.

Only REPORT.md and files in MANIFEST.sha256 are publishable. The manifest includes the scripts, patches, raw command-output receipts with normalized host paths, return codes, public snapshot, independent-pass snapshot and final integrity proof.

R916-1 FINISHED
