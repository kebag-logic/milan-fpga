# [A271] Round 2 handoff

Status: implementation committed; all assigned gates and both review probe campaigns pass their expectations. Ready for independent re-review.
Issue #546, PR #554, branch `546-crf-talker-step`.
Starting head: `39a0171c8c39e68065b14b9178b30d708a9f7645`.
Current head: `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`.

Public references: [assignment](https://github.com/kebag-logic/milan-fpga/issues/546#issuecomment-5818237636),
[R302-1](https://github.com/kebag-logic/milan-fpga/pull/554#issuecomment-5817998312),
[R303-1](https://github.com/kebag-logic/milan-fpga/pull/554#issuecomment-5818230916).

## Changes and finding responses

| Assignment item | Response |
|---|---|
| R302-1 F1 / R303-1 F1 | Connected harness adds marked positive and unmarked negative talker-only steps, preserves both-end 100 ms lag cases, and adds both-end 600 ms lag cases. Event alignment and independent source-interval accounting require a servo boundary inside crossing history. |
| Sampling artifact | Validity is captured after input settling with clk_i low, before the accepting edge. The same observer handles quiet and step cases. Quiet post-edge artifacts are counted separately and cannot satisfy withholding. |
| R303-1 F2 / R302-1 S1 | RTL comment and TIME_SYNC state that the media oscillator inherits the LocalClock +/-100 ppm bound. The remote PHC envelope and quantization assumptions are explicit. |
| R303-1 F3 / R302-1 S2 | Default receiver target includes mutation controls. The committed ignored-servo-validity mutant reuses the servo unit build recipe and requires U13's trim failure. Campaign output is compatible with the sweep verdict reader. |
| R302-1 S3, S5 / R303-1 S2 | Servo banner includes remote-validity skipping; recovery grammar fixed; rate-register description again identifies talker media frequency measured against gPTP. |
| R302-1 S4 / R303-1 S1 | Receiver-discard telemetry remains outside this issue under the assignment decision; manager owns the #495 checklist item. |

No RTL logic change was required. Receiver and servo edits are comments only;
`rtl-comment-only.log` verifies equality after stripping comments and whitespace.
No reviewer verdict or clean-lens claim is made by this handoff.

## Completed acceptance evidence

- Complete default receiver gate: rc 0; 13,836 unit, 1,658 discontinuity,
  69 connected checks, and seven mutation controls. Its full log passes
  `scripts/suite_tally.py --verdict`.
- Every clean connected event stays LOCKED, with no receiver unlock and at
  most 0.020 ppm integrator movement. Each talker-only and 600 ms case
  reaches one crossing boundary. Each both-end event counts one local step.
- The 100 ms lag cases reach zero crossing boundaries: they exercise guard
  interaction, and do not independently prove receiver isolation.
- Quiet control: 550 post-edge artifacts, zero sampled invalidity. The
  unchanged standalone artifact probe still reproduces 300 false post-edge
  readings out of 300 clean PDUs.
- Complete servo gate: rc 0; 82 unit, 8 rail and 113 PHC-step checks.
- Both documentation modes, style, TOC, paths, matrix, source-list, idiom,
  behavior and diff checks pass. Behavior: 344 scenarios, 1,739 steps.
- Front-end analysis actually ran: zero local RTL findings, four pinned
  processor findings equal the existing ratchet, rc 0.
- Archived clean connected harness: 69 checks pass. Archived clean lag
  sweep: 36 checks pass; no-detection lag sweep: 13 expected failures.
- Archived `rx_no_detection` against the revised connected harness: FAIL,
  23 failures including lock and integrator checks. First talker-only
  positive step drives the integrator to -115.762 ppm and state ACQUIRE.
- Archived `servo_ignores_valid` against the revised connected harness:
  FAIL, five invalid-sample PI assertions.

## Completed probe validation

The default datapath sweep passed in one invocation, rc 0 (1810.05 s).
The archived R303 campaign completed all 23 cases, rc 0: four clean
controls pass, seventeen expected mutants are killed, and two informational
ignored-tu cases pass. Receipts are in `receipts/R303/`.
The full R302 campaign completed, rc 0, all 43 expectations satisfied.
Its shipped `talker` scenario reports clean PASS (69/0), `rx_no_detection`
FAIL (23), `jump_removed` FAIL (15), `lower_bound_removed` FAIL (15),
and `servo_ignores_valid` FAIL (5). Each removed jump check exposes the
unmarked negative event: up to +177.188 ppm and state ACQUIRE.
The original INFO case for a subthreshold unmarked 2,000 ns step still
fails lock, as documented by the reviewer; no RTL behavior changed there.
R302 receipts are preserved under `receipts/R302/`.
Every foreground command has completed. `gates.jsonl` records all gate commands
and exits. `PROBE-RESULTS.md` also enforces the stricter Round 2 expectations
for rows the original R302 runner labels informational.

## Probe provenance

Public review archives were fetched into temporary scratch only:
`3e1008b8bf4f20866051b5be66367fdb4ff11451` and
`8d2a18a9a9d975c36efbf70b06078aec8a6d1a50` on `546-review-evidence`.
Both reports equal their public comments apart from a trailing newline.
Both published manifests match (53 and 17 entries).
`archive-hashes.txt` records the original bytes.

The R302 runner is imported unchanged; only its pinned HEAD binding selects
this round's candidate. Scenarios, mutations, builds, grading and every
archived probe source byte remain unchanged. R303 uses its unchanged runner
directly. All scratch trees/builds are outside this output packet.

Both campaigns started on `8f432ba77548d0e3ff6f93fb87dd0323ca356d6e`.
The second commit only adjusts mutation-campaign reporting. All targeted
RTL, wrappers, harnesses and build recipes are byte-identical at the current
head; `probe-input-identity.txt` records the matching blobs.

## Setup retries and evidence limits

The system interpreter initially lacked the pinned Markdown renderer.
The existing pinned environment passed the TOC and em-dash gates.
The first probe-wrapper attempt tried to hash its generated cache directory;
that setup error was fixed before any campaign execution.
These nonzero attempts remain visible in `gates.jsonl`.
The initial connected run was exploratory; the clean rebuilt default receiver
run is the final local gate evidence.

Physical calibration, timing closure, hosted acceptance, current-dev candidate
validation, independent re-review and publication remain with the manager.
Local PHC slew handling remains #545. No push, PR edit, merge, hardware work,
other checkout or delegation was performed. The final issue handoff uses `REVIEW-READY.md`; publication of the branch
and replacement PR body remains with the manager.

`GATES.md` records all assigned gate commands, elapsed times, zero exits and receipts.

Temporary review archives, exported source trees and all probe builds were
deleted after both campaigns completed. This packet contains text artifacts
only, with no toolchain, SDK, environment or source-tree export.

Packet entry points: [gate table](GATES.md), [strict probe results](PROBE-RESULTS.md),
[replacement PR body](PR-BODY.md), [issue handoff](REVIEW-READY.md).
