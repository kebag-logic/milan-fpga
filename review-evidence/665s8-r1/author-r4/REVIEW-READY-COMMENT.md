[A758c] REVIEW READY
Commit: `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` (branch `665-s8-wire-timing`: round 4's one commit on round 3's `e3f96a67b5`, issuecomment-6800331535; merge base dev-soft-core `1d6bf555`)

Changed (the ruling on R815-2 and R816-2, issuecomment-6805224780: controls only; no harness behaviour, figure or firmware change):
- R815-2 F1: the clean loaded log (`clean-loaded`) gains a MAAP arm the same pass cancels before its deadline, as the firmware's final probe expiry does, its burst delivered whole and meeting no expiry, and a last offer the log ends inside, delivered in part. `LOADED` expects MAAP 5 queued, 4 delivered, 3 met and AECP 1 delivered whole, 1 in part, so a grader that counts a cancelled arm's burst as met, or no partial offer, fails it.
- R815-2 F1's option: a new control `load-offer-over-delivered`, a fourth frame under an offer's tag of three queued, found by `LOAD: 4 frames of offer 0 of load acmp were received, 3 were queued`.
- `received-frame-unaccounted`'s words follow the larger log (17 delivered load frames, 26 received). The harness page's control section says the same.
- Files: `tb/verilator/ctrl_wire_timing/wire_selftest.py`, `tb/verilator/ctrl_wire_timing/README.md`. Self-test: 50 controls.
- Not taken, as the ruling limits the round to controls: R815-2 S1 and S2. R1 (the PR body's 693 s sentence) is fixed in the PR body text for the manager.

Validation, at `dbe54e46f0`, each on its own fresh clean clone:
- the wire-timing self-test: rc 0, `50 controls, 0 failed`;
- `run.py --ci` as `rtl-fast / wire-timing`, every `run:` step: 4 rc 0, 10 not run with a stated reason, 0 failed; the step `PASS` in 564 s on four uncontended CPUs (build 80 s, netlist cached), both runs `0 finding(s)`, both plants caught, results and logs byte-identical to the measurement;
- the docs gates, `docs.yml` all 9 jobs: 64 steps rc 0, 31 not run with a stated reason, 0 failed;
- `git diff --check` against the merge base: rc 0.

R815-2 F1's Verification: its `delta_mutants.py`, unchanged, at `dbe54e46f0`: `expiry-met-ignores-arm` and `partial-offers-never-counted` KILLED (`clean-loaded` fails), the other 11 stay KILLED. `over-delivery-check-gone` now fails the self-test by `load-offer-over-delivered`, but the script scores it SURVIVED because it expects `clean-loaded`, which no clean log can fail for an over-delivery; with only that expectation changed, 14 of 14 KILLED.

Acceptance criteria: unchanged from round 3 (issuecomment-6800331535); round 4 changes no figure. 1 to 4 met; 5 met locally, its hosted wall time pending.

Open risks/questions:
- Item 5's hosted wall time: no hosted run has executed the step yet (R815-2's hosted state at `e3f96a67`: cancelled while building Verilator on a cache miss).
- The CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`) needs its own Issue (ruling item 2 of round 3).
- The candidate merge against the live `dev-soft-core` (`764482b45f`) is the manager's; the lane's merge base is `1d6bf555`.
