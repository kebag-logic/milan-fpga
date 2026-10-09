[R569] POSITIVE - exact head 62c261c2d1b899a9cf90c901b25b5a85846dfef6

Round R569-1, external independent review of PR #701 (Relates to #657).
Exact head 62c261c2d1b899a9cf90c901b25b5a85846dfef6, tree
a8ed9acaec2e3c7d0ff5ff1ea64ff68a4ab1027d; source base
5603c353137e90c1fa95429f6d00ef7a2298d9ee (one commit). The verdict and ledger
below were written from public state and own execution before any earlier
review comment on this PR was read. The disposition of earlier public
findings is a separate section, appended afterwards.

## Verdict basis

No BLOCKER, MAJOR or MINOR finding at this head. One SUGGESTION (S1). All five
lenses were applied and are covered clean at this exact head.

## Acceptance (issue #657 body, assignment 6082915356)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | `--epoch-only` clean leg passes, or its T30 checks are corrected to the declared law with the reason | MET by the first branch. The leg passes and the four T30 expectations are byte-unchanged (exact one-action) | `receipts/epoch-head.log`: 127 checks / 0 failures. `receipts/epoch-no-dwell.log` (only the new dwell line removed): 127 checks / exactly the four T30 failures, each `got=0 exp=1`. Campaign clean arm and both skew controls PASS (`receipts/campaign.log:941,948,949`) |
| 2 | "uncounted repeat" killed by a named check | MET | `receipts/campaign.log:955`: killed by `T6 UNDERRUN: every forced repeat is a counted underrun`. Probes: clean 66/0; burst disabled fails only `...forced repeated frames`; counter doubled fails only `...counted underrun got=11 exp=0` (`receipts/probe-results.json`) |
| 3 | `make -C tb/verilator/milan_dp_render tdm8render-mutants` rc 0 with the pinned Verilator | MET, 34/34 | `receipts/campaign.log` tail `34 checks: 34 PASS, 0 FAIL`; `receipts/campaign.rc` 0; 6027.6 s; Verilator 5.050, launcher sha256 905795b9... The count is the issue's 32 plus PR #672's two pull-in arms (the clean `--pullin` control and the missing-settle mutant, commit 540d7f65e). The tables hold 22 mutants, 3 clean controls, 3 leg defects and 6 positive-control modes, with identical names at base and head (`receipts/inventory-scope.json`, `receipts/inventory-history.txt`) |
| 4 | No RTL change | MET | `receipts/raw-delta.txt`: four paths, two docs and two harness/campaign files. No `hdl/`, generated-shape, Makefile or gitlink change |
| 5 | Default suite within its hosted budget, measured as PR #672 did; TESTING.md row updated | MET | Own cold default with serial outer `make -C`, four CPUs, `MAKEFLAGS` unset: 796.98 s, rc 0; 266/0, 71/0 and 5/5 (`receipts/default.json`; `receipts/default.log:574,1056,1066`). Author reports 809.21 s. Hosted render window at the exact-head synthetic merge d44e3e4 (parents 7c1b52be and 62c261c2): 1101.97 s, margins 338.03 s to 1440 s and 698.03 s to 1800 s (`receipts/hosted-render-timing.json`; raw job log sha256 f0583ebb...). TESTING.md:273 row and :349-361 timing paragraph updated |
| 6 | Builder bank and docs gates | Docs: MET | Own docs gates 8/8 rc 0 (`receipts/docs-local.json`). Hosted docs-check, docs-check-no-git, wire-accountability and bdd-conformance pass. Builder bank: author receipt only (rc 0, one historical placed-report calibration NOT RUN); not re-run by this round; manager candidate bank pending |

## Findings

S1 - SUGGESTION - Docs - docs/testing/TESTING.md:359-361 - hosted figure not
recorded.
Evidence: the paragraph says the candidate's hosted timing is pending. The
exact-head hosted render window now exists: 1101.97 s, run 37973662908, job
113966628806.
Impact: none on correctness. After merge the paragraph reads as permanently
pending.
Optional outcome: record the hosted window when the file is next touched,
following the PR #672 pattern ("these measurements cover <head>; later heads
still require hosted acceptance").
Verification: the paragraph cites the run, job and figure.

## Lens results (each at exact head 62c261c2)

[R569] PASS Conformance - sim_tdm8_render.cpp:3611-3637, :4448-4450; docs/design/MEDIA_CLOCK_FOLLOWING.md:1645-1659 - The four T30 #386 source-change recentre checks are byte-unchanged: trigger once, one pulse, one stage recentre, no second. The only epoch-only change is the existing `--crf-only` boot pull-in dwell (kBootPullInCycles at :1110, used identically at :4418, :4424, :4430 and :4441). The documented boot overshoot (MEDIA_CLOCK_FOLLOWING.md:1645-1652) and #629 A2-a justify it. The 120 ms figure matches `run_fed(12000000)` at :3615 under the 100 MHz model. The probe shows the dwell is load-bearing and nothing else differs (127/0 vs 127/4). The #645 settle recentre stays a separate action (`[PULLIN]` arms PASS). No setpoint, window, band or threshold changed.

[R569] PASS RTL - receipts/raw-delta.txt; hdl/ieee1722/aaf/KL_tdm_render_master.sv underrun counter (unchanged) - No RTL, interface, generated-shape or gitlink change. The harness change at sim_tdm8_render.cpp:407,412 scales only the modelled audio/serial clock accumulator. The kAudNum increment doubles and stays bounded by the kAudDen subtraction; it drives no DUT counter. Exact-head hosted verilator-lint, yosys-elaboration, Yosys shards 0-3 and elaborate pass.

[R569] PASS Robustness - sim_tdm8_render.cpp:2376-2413, :4450-4463 - The burst is bounded to two PDU periods after ten periods of real feed. The clock rate is restored (:2387) before any early return. In the full leg the burst runs after CRF, LAW, pull-in, CSR and reset; in `--serial-only` it runs after SERIAL. Both run while bound: the clean legs decode injected identities. The test grades nonempty routing, whole frames, first-frame identity, sample identity, zero padding, nonzero repeats, exact counted repeats and zero skips. The full leg still gives 266/0 with the bind-loss phase after the burst. Epoch-only keeps its reset/bind tests (127/0), and all six epoch-only mutants are still killed (campaign.log:957-962).

[R569] PASS Tests - receipts/campaign.log; receipts/probe-results.json; receipts/epoch-probe-results.json; tdm8_render_mutants.py:196, :503 - The new check fails for the defect it names: the frozen-counter mutant is killed by name, and a doubled counter fails got=11 exp=0. It is not vacuous: disabling the burst fails the forced-repeat precondition. The campaign arm's expected-check string uses the new name. The `--no-print-directory` fix is proven by running the campaign under an outer `make -C` (rc 0). The inventory is unchanged (34 at base and head). No check, arm or expectation was removed or relaxed.

[R569] PASS Docs - docs/testing/TESTING.md:273, :349-361, :614; docs/design/MEDIA_CLOCK_FOLLOWING.md:1653-1659; tdm8_render_mutants.py:80 docstring - The campaign row names the manager merge bank, per the assignment, and the new invocation. The inventory sentence (32 + #672's 2 = 34) and the T6 UNDERRUN description match the code and campaign output. The outer `make -C` claim matches the build() change and this round's run. The epoch-history paragraph states the reason and keeps the law. Own docs gates 8/8 rc 0. Only S1 (optional).

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | sim_tdm8_render.cpp T30 :3595-3640, run() :4400-4465; MEDIA_CLOCK_FOLLOWING.md :1636-1659; issue #657 acceptance; epoch dwell probe | R569-1 | 62c261c2d1b899a9cf90c901b25b5a85846dfef6 |
| RTL | CLEAN | raw base-to-head delta; harness clock model :404-416; unchanged render-master counter; hosted lint, elaboration and Yosys | R569-1 | 62c261c2d1b899a9cf90c901b25b5a85846dfef6 |
| Robustness | CLEAN | prove_serial_underruns_are_counted :2376-2413; sequencing :4450-4463; default 266/71/5 logs; epoch-only arms | R569-1 | 62c261c2d1b899a9cf90c901b25b5a85846dfef6 |
| Tests | CLEAN | campaign 34/34 log and rc; underrun probes; epoch dwell probe; tdm8_render_mutants.py diff; inventory tables | R569-1 | 62c261c2d1b899a9cf90c901b25b5a85846dfef6 |
| Docs | CLEAN (S1 optional) | TESTING.md :273, :349-361, :614; MEDIA_CLOCK_FOLLOWING.md :1653-1659; docs gate receipts | R569-1 | 62c261c2d1b899a9cf90c901b25b5a85846dfef6 |

## Execution receipts (this round)

- Cold default, serial outer make, four CPUs: rc 0, 796.98 s (`receipts/default.*`).
- Full campaign, `make -j16 -C tb/verilator/milan_dp_render tdm8render-mutants`: rc 0, 34/34, 6027.6 s (`receipts/campaign.*`). An external session limit cut the first campaign attempt at 20 graded arms, all PASS. That attempt was discarded and the target re-run from a cleaned build directory (`scripts/run_campaign.py`).
- Underrun probes (`scripts/probe_underrun.py`) and the epoch dwell probe (`scripts/probe_epoch_dwell.py`) ran on a disposable copy. The copy was restored and proven byte-identical (`receipts/probe-tree-restored.json`, `receipts/epoch-probe-tree-restored.json`).
- Docs gates 8/8 rc 0 (`receipts/docs-local.json`, `receipts/docs-*.log`).
- Review clone after all work: 1232 blobs, modes and index match head tree a8ed9aca. Gitlinks protocol-processor 2ad2f845, gptp-processor 5dce647a and third_party/verilog-axis 48ff7a7e verified. external and third_party/lwSRP are not required and not initialized (`receipts/final-tree.json`).

## Hosted state at exact head (read only)

Re-queried (`receipts/hosted-checks-recheck.json`): rtl-fast, verilator-lint,
yosys-elaboration, firmware-unit, elaborate, docs-check, docs-check-no-git,
bdd-conformance, wire-accountability, changes, full-ci-gate, Yosys shards
0-3 and Verilator shards 0, 2, 3 and 4 are SUCCESS. Verilator shard 1/5 was
still IN_PROGRESS at re-query. Physical gPTP is SKIPPED (a nightly/manual
context, not executed). The render suite passed in shard 0 at the synthetic
merge with current dev, not at the source head alone.

## Real limits

- No manager source bank exists at this head; none is claimed or inferred.
- Builder bank not re-run by this round; author receipt only.
- Hosted verilator-suites was not complete at re-query (shard 1/5 in progress).
- Local timing used four build workers; the author's figure used two.
- Physical calibration NOT RUN. Skipped field/physical contexts are not hardware proof.
- `tdm8render-law-boundary` and `tdm8render-pullin` were not re-run by this round. The campaign exercises the shared `build()` change.

## Pending manager duties

- Hosted/act acceptance, including verilator-suites completion (shard 1/5).
- Current-dev merge candidate (base 5603c353, live dev 7c1b52be): builder and native banks, and the candidate campaign per the TESTING.md:273 manager-bank row.
- Optionally carry S1.

## Earlier public findings (read after the verdict above)

PR #701 holds two review-start notices (6086958823, 6086965984) and one
earlier review, R568-1 (comment 6088670254, POSITIVE at this exact head). It
has no review object and no inline comment. R568-1 records no BLOCKER, MAJOR,
MINOR or RESIDUE, so none is open to resolve or retain.

- R568-1 S1 (SUGGESTION, Docs, TESTING.md:360-361, hosted window not yet
  recorded): independently found by this round as S1. Retained as an optional
  item at this head; it does not affect coverage or the verdict.

The verdict stands unchanged.

R569-1 FINISHED
