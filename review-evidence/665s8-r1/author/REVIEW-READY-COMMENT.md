[A758b] REVIEW READY
Commit: `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` (branch `665-s8-wire-timing`: round 1's `086e186e` and six round 2 commits on dev-soft-core `1d6bf555`)

Changed:
- `tb/verilator/milan_dp/tb_split_top.sv`, `Makefile`: the split top and its recipe at a shape and an interface count (`SPLIT_SHAPE`, `SPLIT_STREAMS`, `SPLIT_IF`). Interface 0 goes through `KL_mbx_cdc` to the 8x8 datapath. Interface 1 is driven from the bench as S2 drives `KL_mbx`: link up, frames, the commit acknowledged at the bound, windows idle. It is not a second datapath. With the defaults, the 1x1 split leg and the twin are byte-identical. `milan_soc.CtrlMailbox`, `sw/mailbox/mailbox.yaml` and production RTL are unchanged.
- `tb/verilator/ctrl_wire_timing/`:
  - the 8x8/2if point;
  - S2's composed load per measured channel, offered before each draw and 200 us before every MAAP and ADP deadline;
  - grades for ACMP (Table 5.26), the AECP response time (240 ms), MAAP's probe and announce intervals (B.3.4.2, B.3.4.1) with egress and interval error under the 11 ms reserve, and ADP (Table 5.50);
  - a 33-control self-test, and two plants on every run's own log.
- CI: a `wire-timing` job in rtl-fast. Its one step is `python3 tb/verilator/ctrl_wire_timing/run.py --ci`. The fast verdict requires it, and `scripts/ci_events.py` pins it.
- Docs: the harness page, milan_dp's README, `docs/testing/CI_WORKFLOWS.md`, and the `sw/firmware/ctrl/maap/README.md:47` note, now closed with the measured egress error.

Validation (one pass, clean clones of the head):
- Workflows, every `run:` step:
  - rtl-fast, 18 jobs: 56 rc 0, 64 not run with a stated reason.
  - docs, 9 jobs: 64 rc 0, 31 not run with a reason.
  - elaborate, 6 jobs: 13 rc 0, 33 not run with a reason. The LiteX aggregate was killed twice at its 900 s member wall clock under host load (rc 92, result unknown). Re-run uncontended: 8 of 8 passed.
  - rtl: `full-ci-gate` and `yosys-shards` 0 to 3, rc 0 each.
  - 0 steps failed.
- The CI step: `PASS`, `33 controls, 0 failed`, both runs `0 finding(s)`, both plants caught. Results and logs are byte-identical to the measurement.
- The full sweep as four shard units: 65 of 65 suites, 2,192,857 checks in the sweep. `capture_coherence` was killed at its 2,400 s wall clock on CPUs another sweep shared (rc 92). Re-run uncontended with the sweep's own command: rc 0 in 2,262 s, 0 failures.
- Firmware and builder gates:
  - firmware self-test, four shards: rc 0, control mutants 570 of 570;
  - `fw_coverage.py --check`: PASS;
  - tally mutants: 18 of 18;
  - saved-state self-test: 109 of 109;
  - `test_builder.py --require-rv32`: rc 0. Two arms were not run: a mutant with no effect on this make, and a check that needs a placed implementation report;
  - behave: 508 scenarios passed;
  - `git diff --check` against the merge base: rc 0.
- S2's harness at 1x1/1if and 8x8/2if: rc 0, 0 refusals.
- Wire timing at 8x8/2if, without and with the load: rc 0, 0 findings, byte-identical to the measurement.
- `physical-gptp` is not run on a pull request, but was run anyway. Step 11 stopped twice in its cancellation preflight (#833; both results kept). The same preflight passed at this head in all four sweep shards.

Acceptance criteria:
1. Met. The slowest ACMP transaction is the loaded 8x8 bind at 17.7 ms, 182.3 ms inside Table 5.26's 200 ms. Measured at 1x1 and 8x8/2if, without and with the load.
2. Met.
   - Probe intervals are 512.9 to 583.7 ms, strictly inside B.3.4.2.
   - Announce intervals are 31,956.5 to 31,958.2 ms, inside B.3.4.1. These come from the local campaign: 4 units, seeds 1 to 4, each to its second ANNOUNCE.
   - Egress is at most 2.46 ms and each interval is within 1.7 ms of its draw, inside the 11 ms reserve.
   - The `maap/README.md:47` note is closed.
3. Met.
   - The AECP response is at most 20.6 ms in the 16-draw runs and 6.7 ms over the campaign's 1,368 draws, against 240 ms.
   - ADP advertise periods are 5,363.0 to 8,387.6 ms, inside Table 5.50's 5 to 9 s (the 5,000 ms timer plus a 0 to 4,000 ms delay). Each ENTITY_AVAILABLE leaves within 2.2 ms of its delay.
4. Met. On every run's own log, the egress-past-the-reserve plant and the shifted-clock grader are both caught, and the self-test has controls of both.
5. Met locally. It is one step of an existing dev-soft-core workflow, in a job with a 30-minute timeout. The step took 578 s on four CPUs. In the gate pass it took 2,317 s, on CPUs that other work kept fully busy.

Open risks/questions:
- Ruling item 3. A MAAP or ADP deadline's burst leaves out ACMP's and AECP's records. The whole burst fills ACMP's 12-record ring, and `KL_mbx` then drops a draw's frame, as the first campaign measured. Under the whole burst the timers still measured inside their clauses. A decision is requested if the timers' loaded figures must carry those records.
- Item 5's hosted wall time comes from the first hosted run.
- Two existing members are close to their wall clocks even uncontended on four CPUs: `capture_coherence` at 2,262 of 2,400 s, and `test_soc_timing_cuts` at 832 of 900 s.
