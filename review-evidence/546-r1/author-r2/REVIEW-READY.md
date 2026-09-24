[A271] REVIEW READY

Head: `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`, local branch `546-crf-talker-step` (not pushed).

Round 2 addresses assignment items 1-3 and the requested wording suggestions. No RTL logic change was required: receiver and servo changes are comments only.

The connected harness now tests marked +150 us and unmarked -150 us talker-only events, both-end events with 600 ms listener lag, and the original 100 ms lag ordering. Events align 100 ms after a servo boundary; talker-only and 600 ms cases assert a boundary inside crossing history. Validity is observed before the accepting edge, after inputs settle. Quiet traffic produces 550 post-edge artifacts but zero sampled invalidity, so the artifact cannot satisfy withholding.

Acceptance evidence:
- Clean connected harness: 69 checks pass; all six events remain LOCKED, with zero receiver unlocks and at most 0.020 ppm integrator movement. Each discriminating case reaches one crossing boundary. Each both-end event counts exactly one local PHC step. The 100 ms cases reach no crossing boundary and are documented as guard-interaction evidence only.
- Unchanged R302 campaign: all 43 expectations pass. On `talker`, `clean` is PASS; `rx_no_detection` is FAIL (23), `jump_removed` FAIL (15), `lower_bound_removed` FAIL (15), and `servo_ignores_valid` FAIL (5). Detector removal reproduces -115.762 ppm and ACQUIRE; both jump mutants reach +177.188 ppm and lose lock on the unmarked negative event.
- Unchanged R303 campaign: all 23 cases satisfy expectations, rc 0. The connected harness rejects jump removal (15 failures), combined detector removal (22), ignored validity (5), and forced validity (11). Its listener-first clean control passes 19 checks; corresponding mutants are rejected.
- Default receiver gate includes all seven mutation controls. The committed ignored-validity mutant requires U13's named trim failure. Its campaign and complete default logs pass the sweep verdict reader.

All assigned gates returned zero: complete receiver target, servo target (82 unit / 8 rails / 113 PHC-step checks), default datapath sweep in one invocation, both documentation CI modes, em-dash check against `57456af96b3127b9d309a995bbbd35a6113ce52d`, documentation style/TOC/paths/matrix, actual front-end analysis, RTL source lists, C++/Python idioms, 344 behavior scenarios, and diff checks. The front-end's four pinned-processor findings equal the existing ratchet; local RTL findings are zero.

The LocalClock-derived media bound and assumed remote PHC envelope are explicit in both derivations. The servo banner, recovery wording and CRF_RATE description are corrected. Receiver-discard telemetry remains outside this issue under the assignment decision.

The output packet contains HANDOFF.md, the full replacement PR-BODY.md, gate commands/exits, source patch/hashes, and rerun receipts. Both probe campaigns started on the first Round 2 commit; all targeted inputs are byte-identical at this head, with blob evidence recorded. Publication and independent re-review remain with the manager. Physical calibration and timing closure are not claimed.
