[A271] Discard CRF rate samples spanning talker discontinuities.

Closes #546

## Status

Round 2 is committed locally. All assigned local gates pass.
Independent re-review and publication remain pending.

## Description

A talker timestamp step contaminated the listener's 512 ms rate history.
The receiver now restarts that history on either `tu` edge, an adjacent
timestamp jump, or a sequence gap. The event timestamp seeds the history;
256 subsequent clean intervals restore validity. Full-width subtraction
catches both step signs without a 32-bit alias.

The media oscillator inherits the +/-100 ppm LocalClock bound from
Milan v1.2 Annex B.1.1. The remote talker is assumed to share this design's
PHC envelope: +/-200 ppm trim and less than 384 ns timestamp quantization.
The spacing bound is `ceil(2,000,000 * 300 / 999,900) + 2 * 384 = 1369 ns`,
rounded upward to 2,048 ns.

Receiver validity gates the servo's sample input. Invalid history holds
the integrator and lock state; local guards retain their behavior.
`CRF_RATE` holds the last clean measurement of talker media frequency
against gPTP. No CSR bit or counter is added.

## Round 2

Addresses R302-1 F1 and R303-1 F1-F3, plus assigned wording suggestions.
No RTL logic change was needed; RTL edits clarify comments.

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
servo-validity mutants. The committed ignored-validity control requires
the servo unit's named invalid-sample trim failure. Campaign output reports
its own verdict for the suite gate.

## How to reproduce

Establish CRF receiver and servo lock. Apply a marked +150 us talker step
or an unmarked -150 us step. Leave the listener PHC unchanged, or step
it 600 ms later, so contaminated history reaches a servo boundary.

## How to validate

Run the default receiver, servo and datapath suites, both archived review
campaigns, and the assigned documentation, source, idiom and behavior gates.

The clean connected harness passes 69 checks. Every event stays LOCKED,
with zero receiver unlocks and at most 0.020 ppm integrator movement.
Each discriminating case reaches one crossing boundary. Both-end cases
count exactly one local PHC step; 100 ms cases reach no crossing boundary.

The unchanged R302 campaign satisfies all 43 expectations. On `talker`,
clean passes; receiver-detection removal, jump removal, lower-bound removal
and ignored validity fail. Detection removal reproduces -115.762 ppm and
ACQUIRE. Both jump mutants reach +177.188 ppm and lose lock.
The unchanged R303 campaign satisfies all 23 cases, including connected
and listener-first mutation controls.

All assigned local gates return zero, including 344 behavior scenarios.

## Definition of done

- Crossing samples stay excluded through complete history refill.
- Connected positive and mutation controls discriminate the defect.
- Quiet traffic cannot satisfy withholding.
- Authoritative timing, recovery, register and test documentation agree.
- Local evidence is complete and the new head receives independent review.

Round 1 area evidence was +80 LUT, +35 flip-flops and +22 carry cells;
memory and multiplier usage were unchanged. Round 2 changes no RTL logic.
Physical calibration and timing closure are outside this evidence.
Receiver-discard telemetry remains outside this issue by assignment;
local PHC slew handling remains #545.
