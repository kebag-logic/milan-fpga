[A304] TAKEN

Branch: `541-crf-unlock`, based on `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
Author: [A304]. Internal reviewer: [R322]. External reviewer: [R323].

Authoritative references: Milan v1.2 Section 5.3.8.10 / Table 5.6,
Sections 7.3.2-7.3.4 / Table 7.1; IEEE 1722-2016 Clauses 10.4.3,
10.4.5, 10.6 and 10.7; `docs/design/TIME_SYNC.md` and
`docs/reference/REGISTER_MAP.md`.

Clause verification: read the original standards directly. Milan Table 5.6
(printed p. 37) says the definition of unsynchronized is manufacturer-owned:
“the definition of ‘unsynchronized’ is left open to each manufacturer.”
The analogous MEDIA_LOCKED entry also leaves synchronization criteria open.
The counter pair records state: equality while unlocked, a difference of one
while locked. UNSUPPORTED_FORMAT counts observation intervals containing a
format mismatch, with an interval no longer than one second.

Milan 7.3.2 (p. 113): “Each PDU shall contain 1 timestamp”. The surrounding
profile requires 48 kHz, interval 96, pull 0, audio-sample CRF and Class A
reservation. It adds no validation-error unlock requirement.

IEEE 1722-2016 10.6 (p. 119), on packet loss: “the media clock free-wheels
until the CRF stream resumes and new CRF timestamps are available.”
Clause 10.7 also permits free-wheeling while uncertain timestamps stabilize;
10.4.3 and 10.4.5 separately govern restart and uncertainty.

Conclusion: no clause requires immediate unlock on this validation error.
The stop condition is not met. The 100 ms timeout remains the documented
implementation policy, not a specification-prescribed duration.

Interpreted scope: correct the header and CRF_CTRL row, including the
UNSUPPORTED_FORMAT interval count, full-width output and truncated CSR;
add a locked-sink validation-error check and a named unlock mutant;
preserve graded silence unlock and all #546 discontinuity/servo legs.
No functional RTL change.

Validation plan: the assigned receiver and servo suites, receiver mutation
campaign, both documentation CI modes, em-dash check against the supplied
base, documentation style/contents/anchors/paths/matrix checks, HDL analysis,
language idioms, evidence ratchet and whitespace check. All commands run in
the foreground. No push, pull-request operations, merge or hardware activity.

Blockers: none.
