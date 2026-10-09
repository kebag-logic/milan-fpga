[A567]
Closes #168

Return zero talker identifiers on successful UNBIND, retain ACMP status across retries, use CONTROLLER_NOT_AUTHORIZED (16) for lock refusals, and return TALKER_UNKNOWN_ID for invalid DISCONNECT sources. Keep all 16 received VLAN bits in listener and input-stream readback. Check probe responses against the controller of the probe actually sent, and preserve that probe on retry after a same-talker rebind. The parent VID output keeps its existing width and meaning.

## Round 2

Main `09e357fb` is merged. The selected reduction compares before selection and selects the controller byte before its source, retaining all six corrections and their checks. The fresh 1x1 result is 21,614 → 21,643 LUT (+29) and 18,908 → 18,922 FF (+14), within both +40 limits. The six individual deltas sum to +27 LUT / +4 FF; the unreduced combined change was +127 / +14.

Validation: all 33 processor suites pass at baseline and head (1,028,293 and 1,028,384 checks), along with lint, repository checks, matrix consistency and portability synthesis. All 13 affected campaigns and all 17 scratch-parent consumer commands return zero at both revisions. All 18 added controls fail their required checks; the complete ACMP campaign kills 51 controls and passes six goldens. Record comparisons permit only the documented clause-required differences.

The parent report-calibration arm remains unrun because its historical placement report is absent; it is not counted as an executed check.

## Round 3

Align the authoritative ACMP behavior, compliance claims and operator diagram with the corrected source validation and retry-status retention. Document the private sent-controller overlay, regenerate the 16-bit VLAN record figure, and state input selector 6 ownership consistently: the processor supplies the settled VLAN or zero, while the integrator supplies the lower 48 bits and handshake. The public VID output remains 12 bits. This round changes documentation only.

Fresh validation: all documentation gates and the explicit module-matrix check pass at the Round 3 baseline and final tree. The scratch-parent documentation consumer also passes at both pins with identical records. Existing documentation negative fixtures pass; the stale record figure fails freshness before regeneration and passes afterward. Both changed figures were inspected, including two distinct fonts for the record layout. No test expectation or mutation control changes. The Round 2 implementation, area and execution evidence above is retained for unchanged source, rather than represented as rerun in this round.

## Round 4

Correct §7 of the AECP architecture page for R552-2-F1. The committed status compare pushes only when the byte changes. A discovered retry and its delay expiry retain status and push nothing; a retry with the talker gone pushes; an unchanged repeated double timeout does not. A different-talker re-bind from PRB_W_RESP that changes started/stopped uses only that trigger when no status is retained; with retained status both terms fire on the same write and produce one frame. Authority: Milan v1.2 §5.5.3.5.30, §5.5.3.5.10, §5.5.3.5.17 and Table 5.22.

Fresh validation: the documentation gates and explicit module-matrix check pass at the Round 4 baseline and final tree, with identical records apart from parallel completion order. Existing documentation negative fixtures pass. Only this section changes; no test expectation or automated check is added. The two related RTL comments remain on the manager's residue checklist under the assignment. The scratch-parent documentation consumer also passes at both pins with byte-identical records. Earlier implementation, campaign and area evidence remains historical.
