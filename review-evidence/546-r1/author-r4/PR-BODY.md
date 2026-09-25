[A294]

Discard CRF rate samples spanning talker discontinuities.

Closes #546

## Status

Round 4 is committed locally at `f5532c4c3f94a516b748cc4627dc5f78d05fa73e`.
All 15 assigned local command invocations returned 0 at this head.
Publication and independent review of the merge delta remain pending.

## Description

A talker timestamp step contaminated the listener's 512 ms rate history.
The receiver now restarts that history on either `tu` edge, an adjacent
timestamp jump, or a sequence gap. The event timestamp seeds the history;
256 subsequent clean intervals restore validity. Full-width subtraction
catches both step signs without a 32-bit alias.

The media oscillator is assumed to meet the +/-100 ppm LocalClock
frequency-accuracy bound in IEEE 802.1AS Annex B.1.1.
Milan v1.2 section 7.4 requires media-source oscillators better than
+/-50 ppm; using 100 ppm retains conservative margin.
The remote talker is assumed to share this design's PHC envelope:
+/-200 ppm trim and less than 384 ns timestamp quantization.
The spacing bound is `ceil(2,000,000 * 300 / 999,900) + 2 * 384 = 1369 ns`,
rounded upward to 2,048 ns.

Receiver validity gates the servo's sample input. Invalid history holds
the integrator and lock state; local guards retain their behavior.
`CRF_RATE` holds the last clean measurement of talker media frequency
against gPTP. No CSR bit or counter is added.

## Round 2

The connected harness covers marked +150 us and unmarked -150 us steps:

- Talker only, requiring receiver isolation independently.
- Both ends, with 600 ms listener lag and a crossing-history boundary.
- Both ends, with the original 100 ms lag for guard interaction.

Events align 100 ms after a servo boundary. The first two scenarios
explicitly require a boundary within 256 source intervals. Validity is
captured before the accepting edge, after inputs settle. The quiet control
observes 550 post-edge artifacts but zero sampled invalidity, so those
artifacts cannot satisfy withholding.

The default receiver gate includes detector, refill, accept-edge and
servo-validity mutants. The ignored-validity control requires the servo
unit's named invalid-sample trim failure. The campaign reports its own
verdict for the suite gate.

## Round 3

Addresses R302-2 F1 and R303-2 F1, plus R303-2 S1 and S2.
The receiver comment, timing design document and this description now
name both clock authorities and the conservative media-clock assumption.
The false claim that no independent media-clock clause exists is removed.

Comment-free RTL is unchanged from
`d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` across all 72 tracked HDL files
under `hdl/`.
Both revisions elaborate `RATE_DRIFT_NS_C` to 601 ns and
`TS_JUMP_NS_C` to 2048 ns. The servo source is byte-identical.

U13 now follows invalid samples with a valid +10 ppm talker offset.
Within 24 ms, trim must increase by more than 5 ppm while retaining
LOCKED. Restoring the original rate must also retain LOCKED.
A new `servo_never_resumes` mutant latches PI off after invalidity.
The default mutation campaign requires its named resume-check failure.
The evidence-reader disposition now names both receiver and servo reads,
including ignored-validity and PI-resume defects.

## Round 4

Merged dev `c266432dcb0cdd464205823a3d82cad260eedde2` with a merge commit.
The recovery table retains the landed render, `mr`, MEDIA_RESET and
pending-restart wording, the receiver isolation and refill sentences,
and both receiver test rows. The gmstep row retains its three negative controls.
The five automatic overlaps agree with both changes. The recovery document
is the only manual merge resolution; no other content change was made.

## How to reproduce

Establish CRF receiver and servo lock. Apply a marked +150 us talker step
or an unmarked -150 us step. Leave the listener PHC unchanged, or step
it 600 ms later, so contaminated history reaches a servo boundary.

For the resume regression, invalidate the remote rate while locked.
Restore validity, then apply a small valid rate offset. A servo that
remains frozen must fail the trim-response check despite retaining LOCKED.

## How to validate

Run `make -C tb/verilator/crf_rx` and `make -C tb/verilator/mmcm_servo`.
The default receiver target includes the new resume mutant.
Run the assigned documentation, source, idiom and evidence gates.
Detailed command results belong in the review-ready evidence.

Round-3 simulation and source gates passed at `28b6bfd38300afd9b66c2e7893c30f6141521a38`.
The final commit only shortens two citation sentences in the timing document;
all other tracked files and dependency pins are identical. Documentation
gates and the RTL identity proof were rerun at the final head.

The clean connected harness passes 69 checks with zero receiver unlocks,
at most 0.020 ppm integrator movement, and one crossing boundary per
discriminating case. Both-end cases count exactly one local PHC step;
100 ms cases reach no crossing boundary. The default campaign passes eight
controls, including the required PI-resume mutant rejection.

Earlier review campaigns rejected receiver-detection removal, jump removal,
lower-bound removal and ignored validity. Detection removal reproduced
-115.762 ppm and ACQUIRE; jump mutants reached +177.188 ppm and lost lock.
Those broader reviewer campaigns and the prior 344 behavior scenarios
are prior-head evidence; they were not rerun for round 3.

## Definition of done

- Crossing samples stay excluded through complete history refill.
- Connected positive and mutation controls discriminate the defect.
- Quiet traffic cannot satisfy withholding.
- Valid remote samples resume PI after invalidity.
- Authoritative timing, recovery, register and test documentation agree.
- Assigned local gates pass and the new head receives independent review.
- Publication, required remote validation and merge checks are completed.

Round 1 area evidence was +80 LUT, +35 flip-flops and +22 carry cells;
memory and multiplier usage were unchanged. Rounds 2 and 3 change no
RTL logic. Physical calibration and timing closure are outside this evidence.
Receiver-discard telemetry remains outside this issue by assignment;
local PHC slew handling remains #545.
