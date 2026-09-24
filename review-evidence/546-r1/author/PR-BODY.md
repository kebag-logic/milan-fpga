[A264] Discard CRF rate samples spanning talker discontinuities.

Closes #546

## Status

Implementation committed locally and ready for independent review. All assigned local gates passed, including the default datapath sweep and mutation controls.

## Description

A talker timestamp step contaminated the listener's 512 ms rate history. The receiver now restarts that history on either `tu` edge, an adjacent timestamp jump, or a sequence gap. The event timestamp seeds the new history; 256 subsequent clean intervals restore validity.

The jump threshold is derived from the 2 ms cadence, legitimate media and PHC rate bounds, and timestamp quantization. Its value is 2,048 ns. Full-width subtraction catches forward and backward steps without a 32-bit alias.

The receiver's validity signal gates the servo's sample input. Invalid history holds the integrator and lock state. The servo's existing step and slew guards retain their behavior. `CRF_RATE` holds its last clean reading during refill; no CSR bit or counter is added.

## How to reproduce

Apply a 150 us talker timestamp step during a grandmaster transition, then step the listener PHC. Repeat with a negative unmarked talker step.

## How to validate

Run the receiver's default suite and its explicit `mutants` target, the servo and automatic-repair suites, and the default datapath sweep. Run the repository documentation, source, idiom and behavior gates recorded on the issue.

The connected scenarios preserve LOCKED throughout. The marked +150 us step leaves the integrator unchanged; the unmarked -150 us scenario stays within 0.020 ppm. Both return to valid clean rate samples without a counted receiver unlock.

## Definition of done

- Crossing samples are excluded through complete history refill.
- Ignored-tu and removed-jump mutants fail named checks.
- Refill, sampling-edge and ignored-validity controls also fail.
- Timing, recovery, register and test documentation describe the new contract.
- Local mapped area changes by +80 LUT, +35 flip-flops and +22 carry cells; memory and multiplier usage are unchanged.
