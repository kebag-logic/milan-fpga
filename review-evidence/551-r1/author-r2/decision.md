[A10] DECISION (manager) on R296-1 F1 = R297-1 F1: fix the stale grant where it is owned

Both reviews show that `sr_admitted_o` is not a trusted verdict in the first admission round after a re-declaration: the slope pipeline still holds the previous TSpec. A refused re-declaration therefore keeps about one round of licence.

The fix belongs to the processor, which owns the admission verdict: Mister-M-alt/protocol-processor-control-plane-avb-milan#112. After a (re)declaration, the grant stays low until the new TSpec has been evaluated. No new port. This follows option (a) of both findings. A parent-side delay would have to mirror the processor's round timing, and that is not allowed.

Sequence:
1. The processor fix (#112) merges.
2. A parent processor-pin PR adopts processor main: #92, #93 and #94 already merged, plus #112, and #43/#49 if merged by then.
3. #553 then merges dev and adds the unwarmed-pipeline fixture: the refused TSpec differs from the source's previous one. That fixture shows no licence pulse, and the docs' "cannot open" claims become true.

Meanwhile the next #553 round fixes the findings that do not depend on it:
- F2 (both reviews): the BDD scenario pins ACTIVE AND the real grant.
- F3: the generator output (my commit `0bf22c93`) is re-checked.
- F4 (both reviews): the Q-9/Q-10 module mapping, status mark, caveat and rationale are restored; Q-9 claims only what `crflic` shows; the remaining ACTIVE-only descriptions are corrected.
- The latency statement covers the 4-cycle case R296-1 measured.

