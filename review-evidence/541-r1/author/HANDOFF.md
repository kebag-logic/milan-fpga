[A304] Author handoff for #541

Closes #541

Status: local author work complete; ready for assigned independent review.
Branch: `541-crf-unlock`
Base: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`
Head: `2734b771bcf0b383ea62ef05744452827bafe9e4`

Assignment: https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5827373589
Roles: author [A304], internal reviewer [R322], external reviewer [R323].

Scope: verify Milan v1.2 Section 5.3.8.10 / Table 5.6 and the cited CRF
media-clock rules. If a validation error requires unlock, stop and report the
clause on #541. Otherwise correct the header and CRF_CTRL description, add a
locked-sink validation-error check and a killing mutant, and retain the graded
100 ms timeout. No functional RTL change.

Clause evidence: see CLAUSE-EVIDENCE.md. No immediate-unlock requirement was
found; the 100 ms timeout is the existing implementation policy. Public
takeover and clause conclusion:
https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5827406716

Changed files: `hdl/ieee1722/crf/KL_crf_rx.sv` (header only),
`docs/reference/REGISTER_MAP.md` (CRF_CTRL row),
`tb/verilator/crf_rx/sim_discontinuity.cpp` (locked reject, interval count,
resume and silence checks), `tb/verilator/crf_rx/mutants.py` (named rejection
of a mutant that clears lock on format failure).
Validation: all 16 assigned gate invocations passed with exit code zero.
See [VALIDATION.md](VALIDATION.md) for exact commands, environment and results;
`gate-results.json` also records each command and exit status.
Receiver: 13,836 unit checks, 1,932 discontinuity checks, 69 connected checks,
and nine mutation controls; zero failures. Servo: 85 unit, eight playback,
and 113 PHC-step checks; zero failures. The new unlock-on-error mutant exited
one at the required named assertion, while its clean control exited zero.
The new counter, lock-retention, resume and silence-timeout assertions pass.
The no-Git documentation mode ran on a temporary archive of the committed
head outside the output directory; that temporary tree was removed.
Comment-stripped receiver RTL matches the base exactly.
Acceptance: all assigned author criteria met. The normative stop condition
does not apply. The header and register row agree with the timeout policy,
identify the interval counter and its views, and the new test detects the
forbidden immediate unlock. Existing #546 tests and silence checks remain.

Public review-ready evidence: #541; exact body in
[REVIEW-READY.md](REVIEW-READY.md), posted as the final session action.
Prepared pull-request text: [PR-BODY.md](PR-BODY.md).
Open implementation risks/questions: none within this assignment.
Next owner action: assigned independent reviews of the exact local head.
No review verdict is claimed by this handoff.

Restrictions: local work only; no push, pull-request operations, merge,
delegation, other checkout, or hardware activity.
