[A758c] REVIEW READY
Commit: `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` (branch `665-s8-wire-timing`: round 3's six commits on round 2's `bfb2df3707`, on dev-soft-core `1d6bf555`)

Changed (the round 3 ruling, issuecomment-6788719673; harness, grader, CI and docs only; firmware, RTL and the mailbox contract unchanged):
- Ruling 1 (R815 F3, R816 F1): each BIND_RX is paired with the first PROBE_TX after its own response and before the next draw's bind; a bind without one, a count of graded PROBE_TX transactions other than the draws, a non-SUCCESS BIND_RX_RESPONSE, and at `announces > 1` a missing advertise period (or a log that runs on 9,400 ms past its last ENTITY_AVAILABLE) are findings.
- Ruling 2 (R816 F2): the draw sends GET_AVB_INFO 0x0027 on AVB_INTERFACE 0 (IEEE 1722.1-2021 7.4.40.1: descriptor_type 9, descriptor_index 0). Each AEM command states its expected final status (SUCCESS); any other AEM or MVU final status is a finding.
- Ruling 3 (R815 F1): each MAAP echo keeps its own newest match as each frame is sent, so the ANNOUNCE is found whenever one has been sent; an echo skipped after its interface's first ANNOUNCE is a finding.
- Ruling 4 (R815 F2): the load is reported queued, delivered (frames that reached the MAC or the bench inside the run, by each offer's tag) and expiries met, apart; delivered load frames + 4 a draw must equal `rx_frames` + `bench_rx`, checked on every run.
- Ruling 5 (R815 F4, R816 F3): the reuse record holds the split recipe's own source list (`make print-split-srcs`), every file a Verilator run or the native compile read, the export's checkout modules, `milan_dp/Makefile` and the build's other tools, the shape's config and the firmware trees (tsn-c-stack and lwSRP among them).
- Ruling 6: `THE LOAD (#868):`; the advertise period's clause text carries 4,998 to 9,400 ms and its row the margin to the strict 9,000 ms. R815 S1: exit 2 on every refused path.
- Item 5, found this round: the `wire-timing` job's first hosted run (at `bfb2df3707`, job 130154674162) stopped at the build, `No module named 'pythondata_software_picolibc'`. The job now installs picolibc, compiler-rt and tapcfg at the bench venv's revisions; a replica of the job as a fresh runner does it passes, byte-identical to the bench venv's runs.
- Self-test: 49 controls (16 new), each refused or found by its own words.

Validation (one clean-clone pass at the head, 12:46-16:46 local; each workflow job on its own fresh clone; one build per point at that head):
- Workflows, every `run:` step: rtl-fast, 18 jobs: 56 rc 0, 65 not run with a stated reason; docs, 9 jobs: 64 rc 0, 31 not run; elaborate, 6 jobs: 13 rc 0, 33 not run (the LiteX aggregate 8 of 8); rtl: `full-ci-gate` and `yosys-shards` 0 to 3 rc 0. 0 steps failed. `physical-gptp` is not triggered by a pull request and was not run.
- The CI step in the pass: `PASS`, `49 controls, 0 failed`, both runs `0 finding(s)`, both plants caught; results and logs byte-identical to the measurement. 2,505 s on four contended CPUs.
- The full sweep as four shard units: 65 of 65 suites, 2,192,899 checks, 0 failed; cancellation preflight PASS in all four.
- Firmware self-test, four shards: PASS, control mutants 570 of 570; `fw_coverage.py --check` PASS; tally mutants 18 of 18; saved-state self-test 109 of 109; `test_builder.py --require-rv32` rc 0 (two arms not run: a mutant with no effect on this make, a check that needs a placed report); behave 508 scenarios; `git diff --check` against the merge base rc 0.
- S2's harness at 1x1/1if and 8x8/2if: rc 0, 0 refusals. Wire timing at 8x8/2if without and with the load: 0 findings, byte-identical to the measurement.
- Beside the pass: the `wire-timing` job replicated as a fresh runner (fresh venv by the job's own steps, the CPU netlist generated cold) at `fbe5acc983`: `PASS` in 1,299 s, byte-identical. Every reviewer probe named in R815-1 and R816-1, at the fixed head: R816 R0 passes; R1, R2, R4, R5 and R815's missing-PROBE_TX and no-advertise probes are found by their own words; both reuse probes report every edit refused.

Acceptance criteria:
1. Met. The slowest ACMP transaction is the loaded 8x8 bind at 18.3 ms, 181.7 ms inside Table 5.26's 200 ms; every bind has its own PROBE_TX and every BIND_RX_RESPONSE carries SUCCESS. Campaign: at most 6.7 ms over 1,368 draws.
2. Met. Probe intervals 513.1 to 583.7 ms over every run, strictly inside B.3.4.2; announce intervals 31,956.5 to 31,958.4 ms (the campaign, four units, seeds 1 to 4, to the second ANNOUNCE), inside B.3.4.1. MAAP egress 0.30 to 2.47 ms over 36 timer-driven frames, each interval within 1.82 ms of its draw, inside the 11 ms reserve; the `maap/README.md` note carries these figures.
3. Met. AECP response at most 24.5 ms in the 16-draw runs (the loaded 8x8's GET_AVB_INFO, now 0x0027 on AVB_INTERFACE 0; round 2's 20.6 ms was a GET_AS_PATH refusal) and 7.3 ms over the campaign, against 240 ms; every AEM and MVU response carries SUCCESS. ADP advertise periods 5,362.6 to 8,387.4 ms, 612.6 ms inside the strict 9 s and 1,012.6 ms inside the graded 9,400 ms; each ENTITY_AVAILABLE within 2.7 ms of its delay. The loaded campaign units now carry the MAAP records: 4,641 echoes found after the first ANNOUNCE, none skipped.
4. Met. On every run's own log the egress-past-the-reserve plant and the shifted-clock grader are caught; the self-test carries both.
5. Met locally: one step of the existing `rtl-fast` workflow, in a job with a 30-minute timeout, N = 16 draws a run. The job now installs the packages its first hosted run lacked; the fresh-runner replica took 1,299 s for the step. The hosted wall time comes from the first hosted run of this head.

Issue text: the issue body is the manager's to edit. Its GET_AVB_INFO figures, if quoted anywhere, are round 2's GET_AS_PATH refusal; the corrected figures are in the PR body and the harness page.

Open risks/questions:
- Item 5's hosted wall time (above).
- The CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`) sends 0x0028 the same way; outside this lane by ruling item 2, it needs its own Issue.
- The reuse guard digests the firmware trees whole, so an edit of any file in them, a README included, refuses a reused build: conservative by design.
- `dev-soft-core` moved on the remote during the round, to `764482b45f`; the lane's merge base is still `1d6bf555` (no rebase in this lane), so the candidate merge against the live base is the manager's.
