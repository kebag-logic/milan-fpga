[R730] POSITIVE - exact head 409c3075a6c5525d283de5a93584ad87a4528137

Independent delta review of FPGA-gPTP PR #95 / issue #94, round R730-2. Tree: `b552de2244475b15bfc430b683f8a4fe9c6a7db3`. Source base: `f97c18035be6ef5345e5af27db2124c5697c1b40`; previously reviewed head: `9d509029de967c50de7527edf2b8869aa9db9074`.

All three distinct prior behavioral findings are resolved. No open BLOCKER, MAJOR or MINOR was found in this delta. Prior accepted behavior remains covered. One source-comment RESIDUE and one publication SUGGESTION follow; neither changes the verdict.

## Scope and authority

The donor has no tracked AGENTS.md or CONTRIBUTING.md. The supplied workspace instructions, README, documentation map and current integration/development/test guides were examined. The documentation map makes RTL/generated microcode and executable tests authoritative over prose.

The binding public scope is [issue #94](https://github.com/Mister-M-alt/FPGA-gPTP/issues/94), its [assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/94#issuecomment-6489657856), and the [round-2 decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/94#issuecomment-6502549880). The latter requires each prior probe, permanent checks and controls, both complete mutation arms, and parent integration at the new gitlink.

The behavioral authorities are Milan v1.2 4.2.6.2.5 (toggle or countdown ends cease), 4.2.6.2.4 (fresh qualification), IEEE 802.1AS-2011 10.2.4.11 (effective portEnabled), and 11.2.15/Figure 11-8 with Cor1/Cor2 (NOT_ENABLED and INITIAL_SEND_PDELAY_REQ). Their relevant requirements are reproduced in the frozen public issue/decision. Parent REQUIREMENTS.md at `e06ade31` selects that edition and supplies REQ-PTP-05 and REQ-PTP-07; parent GPTP_PLANE.md defines transport and atomic publication ownership.

The base-to-head core diff and eleven-commit history were reconstructed; detailed review concentrated on the seven commits after `9d509029`. Changes outside the three causes and their dependencies retain the earlier accepted assessment. Prior public FINDINGS were read after the independent diff pass and explicitly reconciled below. The public packet is [pinned at 4c00cace](https://github.com/kebag-logic/milan-fpga/tree/4c00cace35fc573e7b0326b04d2d62d61c536fc9/review-evidence/gptp94-r1), specifically `author-r2/`. No private author material or another round-2 review was used.

## Prior finding resolution

| Prior finding | Status at this head | Cause and verification |
|---|---|---|
| R730-F1, previously MAJOR; all five lenses | RESOLVED | `hdl/wire/KL_gptp_tx_slot.sv:127` cancels only an unaccepted first byte and masks valid immediately. `hdl/top/KL_gptp_engine.sv:623` dispatches NOT_ENABLED ahead of results/queue without serializer-idle gating. The leg never builds or sends. The original stalled-first-byte probe reports flags `b`, valid 0, and zero completed frames after disabled ready release. Permanent phases additionally count every accepted SOF and verify completion after stalls at 1, 34 and 67 bytes. Controls restore missing cancellation, delayed valid, serializer wait and destructive mid-frame cancellation; each fails its named checks. Authority: 10.2.4.11 and the accepted-byte transmit contract. |
| R730-F2, previously MAJOR; R729-F2, previously MINOR; all five lenses | RESOLVED | `hdl/ucode/gen_gptp_ucode.py:2211` clears `S_RSPSEQ`; `S_PDGOT=1` prevents a new response arm. Existing disabled claim invalidation prevents late-t1 completion; the next request cancels the retained deferred pair. Zero cannot match the armed sequence representation, including sequence zero. Both public probes retain 601 ns and report zero Follow_Up completion commits. Permanent coverage adds a queued pre-fall Follow_Up and deferred t1, then requires two fresh exchanges. Separate controls fail each path. Authority: 11.2.15/Figure 11-8 NOT_ENABLED. |
| R730-F3, previously MAJOR; R729-F1, previously MINOR; all five lenses | RESOLVED | `hdl/top/KL_gptp_engine.sv:1124` makes the first post-reset sample the reference irrespective of level. A later rise after disabled release raises NOT_ENABLED and the request beat. Public reset probes report 0 ms and 245 cycles respectively to the first request. Permanent phase 51 and the restored-first-enable control distinguish the defect. A high-at-release sample remains suppressed, preserving cold/always-enabled reset publication behavior. Authority: Milan 4.2.6.2.5 and Figure 11-8. |

The integration and HDL guides now describe withdrawal before first acceptance, completion after first acceptance, priority disable dispatch, exchange disarm and the reset reference sample. These resolve the documentation portions of the prior findings.

## Reviewer execution and receipt verification

All independent builds and simulations ran in disposable trees under this packet's `scratch/`. The driver is a foreground process that joins its concurrent workers. Four builds at four jobs each respect the sixteen-job cap. No full donor/parent/builder bank or implementation build was run.

| Independent execution | Result | Receipt |
|---|---|---|
| Original R730 adversarial probe | 24/24, rc 0 | `r730-probe-run.log` |
| Original R730 accepted-behavior phases | 32/32, rc 0 | `r730-focused-run.log` |
| Original R729 reset, pairing and short-toggle probes | 122/122, rc 0 | `r729-probes-run.log` |
| Original R729 cadence-boundary sweep | 103/103, rc 0; 151 offsets, zero missing/duplicate requests | `r729-sweep-run.log` |
| Current permanent phases 44–51 with setup | 78/78, rc 0 | `permanent-run.log` |
| Documentation/diagram/source-anchor gates | rc 0; 20 exact anchors, zero findings | `docs-check.log` |
| Four tracked ROM configurations | Every byte identical after regeneration | `rom-regeneration.log` |

The two short-toggle probes observe one request at +289/+287 cycles; the independent R730 one-clock toggle observes +289 cycles. Ordinary cease exit, unchanged countdown, lost-response reset, disabled transmission, frame-built-across-fall and two-exchange qualification remain in the passing focused phases.

`check_evidence.py` verifies 211 downloaded files against the publication manifest's **published** SHA-256 values. It derives the 23 current port controls from reviewed source and checks every named expected failure against the corresponding raw campaign log. All 71 issue-specific checks have an actual FAIL line under a control. The campaign also includes existing lost-response and busy-serializer controls, for 25 campaigns total. Expected mutation failures are not counted as clean simulation passes.

The source-head public receipts, not a manager source bank, establish:

- Complete base and head mutation arms: **113/113** and **136/136**, with exact base/head identities and rc 0. Both clean controls pass.
- Head engine regression: **2048/2048 three times plus 60/60**, covering shipping, request-seeded, Sync-seeded and non-grandmaster-capable cases. This includes unaffected publication/BMCA/Announce/Sync behavior on which the delta depends.
- All thirteen fast source commands and both arm commands at base/head report rc 0. Other suite tallies remain unchanged.
- Current checks against round-1 RTL produce the published twelve failures at the three causes. Late-t1 invalidation already worked in round 1 and is separately mutation-proven now.
- ROM packing reports one additional word in all 3,000 sampled configurations, no packing regressions: 1,022 shipping and 1,023 seeded words. Independent regeneration verifies the committed images.

The immutable publication commit is **unsigned** according to its verification metadata, and no detached signature was found in the listed packet. `evidence-commit-verification.json` records this. Hash integrity was verified; cryptographic signer authenticity was not. This is not represented as a signed execution attestation.

## Parent companion and regression

The companion targets parent `e06ade312a80eb578579365134ab797cda90622b` and changes `gptp-processor` from the source base to exactly `409c3075a6c5525d283de5a93584ad87a4528137`. Independent verification fetched eight ordinary-file preimages, checked their blob IDs, applied the patch in a disposable subset, and checked every resulting blob ID (`evidence-check.log`).

The effective-link expression at parent `hdl/milan/milan_datapath.sv:3194` combines PHY link, software enable and link-guard health. The companion passes that level through the shadow in the same clock domain. The shadow's `tx_byte_w = eng_tx_valid_w & eng_tx_ready_w` and ticket ready/valid inputs consume accepted bytes only, so withdrawing an unaccepted first byte leaves no partial gearbox frame. Already accepted frames complete at the defined boundary.

Public author execution identifies parent snapshot `6c3246871647abbdcf7cf2505c184d55e06d426e`, based on `e06ade31` with the reviewed gitlink. Its 15 consumer commands return zero. Both `milan_dp` **gptp and gptp-lat pass 205/205**. Four parent controls have nonzero simulation results and named failures in `pm1.log`–`pm4.log`. Extra consumer receipts also report zero. The physical-simulation leg's extracted Pdelay/progress/verdict lines are byte-identical to base; this is simulation evidence, not physical measurement. No parent suite was independently rerun here, as prohibited by scope.

Published out-of-context results against the source base are LUTs 4,990 → 4,926, FFs 3,455 → 3,459, placed slices 1,663 → 1,634, and placed WNS +0.524 → +0.506 ns. These do not establish the final parent's routed area margin.

## Findings and publication notes

### R730-F4 — RESIDUE — stale phase number in control comments

- **All attributable lenses:** Docs.
- **Location:** `tb/verilator/engine/port_mutants.py:41` and `:46`.
- **Authority/evidence:** Both comments call the `{1,34,67}` byte-position cases “phase 49”; the harness identifies them as phase 50 immediately before `finish_a_frame_started_before_the_fall`. Phase 49 is the unaccepted first-byte case.
- **Impact:** Navigation wording only. No test name, operation, measurement, generated artifact, requirement claim or privacy rule changes.
- **Exact required outcome:** Replace `phase 49` with `phase 50` in those two comments/docstrings only.
- **Verification:** Comments agree with the harness; executable statements and named checks remain byte-identical.

No new prohibited bench-lane labels, reviewer identifiers, review rounds or issue-comment IDs were found in reviewed source-comment additions.

### R730-S1 — SUGGESTION — publish the prepared current-head PR description

- **All attributable lenses:** Docs, Tests.
- **Artifact:** Live PR #95 body captured in `public/pr.json`; replacement `public/author-r2/PR-BODY.md`.
- **Authority/evidence:** The live body's “this head” text still describes `9d509029`, including queued disable, dropped SENDs, first-enable suppression, 2,002-check passes, 128 controls and old area/ROM figures. The public exact-head packet and readiness comment already supply the corrected behavior and results verified above.
- **Impact:** Readers can mistake historical figures for the reviewed head. This is not classified as RESIDUE because updating it changes reported figures and behavior descriptions. It does not establish a missing executable acceptance gate: exact-head results are public and verified.
- **Requested outcome:** At publication, replace the live PR body with the prepared round-2 description, preserving historical records under their actual head.
- **Verification:** Live PR describes priority NOT_ENABLED, first-sample reference and withdrawal; results identify 2,048 ×3 +60, 136/136 and current ROM/area numbers.

## Reviewer-owned ledger

Every row below is for exact head `409c3075a6c5525d283de5a93584ad87a4528137`.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/decisions; Milan .4/.5; 10.2.4.11 and Figure 11-8 requirements; parent REQ-PTP-05/07; NOTEN/restart/countdown; all prior findings | R730-2 delta; prior accepted scope retained | 409c3075a6c5525d283de5a93584ad87a4528137 |
| RTL | CLEAN | Serializer cancellation; event priority/ownership; disarm and deferred timestamp gates; reset reference; ROMs; parent accepted-byte seam | R730-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Robustness | CLEAN | First-byte and started-frame stalls; queued/late pairing; disabled warm reset; short pulses and 151 cadence offsets; recovery qualification | R730-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Tests | CLEAN | Five independent probe executions; 71 checks/23 port controls; public 113/113 and 136/136 arms; source regression; parent 205/205 legs/four controls | R730-2 with round-1 regression retention | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Docs | CLEAN | Integration/HDL/test/source guides; diagram anchors; public readiness/packet/companion; F4 residue and S1 publication suggestion | R730-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |

## Limits, restoration and pending manager duties

This is a delta verdict, not full state-machine certification. Unchanged retained neighbor-rate history and sequence randomization are not newly certified. Disable is serviced after the current bounded handler; the tested prompt-clear bound is 2 ms, not combinational publication clearing. Already-started frames may finish, and changes entirely within reset are not observed. Accelerated three-second cease checks preserve the countdown algorithm; no new five-minute hardware run was performed.

Procedural limitation: prior public report bodies were returned after the independent diff pass, but before this final written verdict/ledger. Thus the stricter instruction to write a verdict/ledger before reading any other report was not met. No other round-2 review was read. The manager can assess that sequencing deviation separately from the independently executed behavioral results.

All **109 tracked blobs**, executable modes and index match the exact head; the donor has **no submodule gitlinks**. The companion donor gitlink was checked separately. The original clone was not edited; all probe changes, generated files and parent patch application stayed under `scratch/`. `integrity.log` and `tracked-index.txt` record final identity. No source fixes, commits, pushes, GitHub writes or hardware access occurred.

Exact-head hosted lookup returns **zero workflow runs** (`hosted-runs.json`); no skipped context is credited as execution. There is **no manager source-bank run at this head**, and none is inferred. Author source-head receipts and the parent companion snapshot are distinct from the final current-dev merge candidate.

The manager still owns hosted/local acceptance and merge-turn builder/native banks against live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`, and publication of their receipts. Parent adoption still owes the durable pin/companion, routed and out-of-context area acceptance and built-image link-toggle scenario. Physical calibration is **NOT RUN**; field skips and simulation do not constitute hardware proof. The manager should also publish the prepared PR description, carry F4 to the residue checklist, and resolve any expectation of a signed packet without treating the current checksum manifest as a signature.

Reproduction: run `python3 run_probes.py --repo /path/to/exact-head-clone --jobs 16`, `python3 check_evidence.py --repo /path/to/exact-head-clone`, and `python3 check_static.py --repo /path/to/exact-head-clone`. The probe runner accepts `--compiler` for the pinned compiler location. Public probe source bytes remain in `public/reviews/`; only the driver adapts head identity and execution placement. Every publishable receipt is listed in MANIFEST.sha256; `scratch/` is excluded.

R730-2 FINISHED
