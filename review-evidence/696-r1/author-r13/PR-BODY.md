[A570]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Local validation complete on `696-maap-annexb` against `dev`: 62/62 suites, 2,187,183 checks, zero in-suite failures. New-head review remains pending.
Current local head: `313616d1a18549d41907db389d378f0beb9bc543`.
This is an unpublished update for PR #706.

## Linked Issue / roles

Closes #696

Executor: `[A570]`
Internal independent reviewer: `[R558]`
External independent reviewer: `[R559]`

R558-12 and R559-9 are POSITIVE at `26e2748f47b0d8fa533f53203264d9f31fc13c48`.
Their verdicts precede this merge round; new-head review remains pending.

## Description

The fabric MAAP allocator now samples the programmed identity and clock at first enable.
The remaining assigned Annex B corrections have clause-based checks and planted defects.

| Item | Result | Authority |
|---|---|---|
| M1 | Apply reversed-octet MAC ordering in the two missing conflict cells | Table B.7 note d; B.3.6.4 |
| M2 | DEFEND echoes the triggering requested start and all count bits | B.3.6.6 |
| M3 | Maximal 32-bit generator; seed from MAC plus local clock; retain the documented pool-mapping bias | B.3.6.1 |
| M4 | Sample on first enable; separate the first claims and intervals under the recorded criterion | B.3.4 NOTE; B.3.6.1; issue comment 6102832618 |
| M5 | Existing operational link return revokes validity and starts four fresh PROBEs | B.3.5.9; Table B.7 |
| M6 | Preserve one pending response while PROBE/ANNOUNCE drains; preserve the active frame | Table B.7; B.3.6.6; shared-buffer ruling 6079087547 |
| M7 | Refuse a supplied range outside the dynamic pool | B.4; Table B.9 |
| M8 | Discard incomplete PDUs without state, timer or transmission effects; counting withdrawn by ruling | B.2; issue comment 6076940309 |

### Round: merge dev e81ce82f

Assignment: [issue comment 6142198285](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6142198285).

Merge commit `313616d1a18549d41907db389d378f0beb9bc543` has ordered parents
`26e2748f47b0d8fa533f53203264d9f31fc13c48` and `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`.
Its tree is `8eb5d868bfac1973ba1d82b0665aabae07d9494c`, exactly the mechanical merge result.
There were no conflicts. No manual source change accompanies the merge.
MAAP RTL, integration wiring, harnesses, mutation table, differential sources and contract remain byte-identical to the reviewed head.
The imported changes belong to dev, including the duration-based worker split and stream-counter corrections.
Candidate and dev memory images have identical hashes. Their generated top-level HDL is identical after removing comments and normalizing build roots; the raw difference is hierarchy-comment ordering. The only functional input differences from dev are the existing MAAP RTL and its integration.

| Check | Result at the merged head |
|---|---|
| Worker split self-test | PASS, rc 0 |
| MAAP duration and owner | 1,375 s; worker 1/5 |
| Predicted worker time | 4,205 s <= 4,320 s, the 60 percent bound |
| All worker predictions | 4,204 / 4,205 / 4,203 / 4,205 / 2,877 s; every worker within the bound |
| Static checks | 28 checks pass; three initial environment refusals passed after selecting the existing YAML-capable environment |
| Parser ratchet | PASS, zero findings |
| MAAP OOC ceiling | 446 LUT / 340 FF; +7 / +60 against `6aa25dec`'s 439 / 280 |
| Candidate shipping route | PASS: 49,277 LUT / 53,419 FF; WNS +0.242 ns, WHS +0.017 ns; complete route; resource check rc 0 |
| Standalone 1×1 endpoint | PASS: 23,179 LUT / 19,779 FF; unchanged; resource check rc 0 |
| Standalone 8×8 endpoint | PASS: 30,135 LUT / 27,380 FF; unchanged; resource check rc 0 |
| Shipping comparison against dev | PASS: candidate 49,277 LUT / 53,419 FF vs dev 49,427 / 53,378; delta −150 LUT / +41 FF; both routes pass |
| Fresh recipe records and input recheck | PASS: four external `record --write` calls; 378 input-file checks unchanged |
| MAAP unit and campaign | PASS: 186 clean checks; 63 named defect rejections and two clean controls; zero failures |
| MAAP datapath and coverage | PASS: five integration checks; line-coverage gate 225/225 |
| MAAP differential | PASS: 12 cases; 17/17 planted defects caught |
| Behavior gate | PASS: 14 features, 406 scenarios, 1,977 steps; no failures or skips |
| Portability | PASS: 58 top-level checks, tied-input and observer/stream-binding gates |
| Processor regressions | PASS: 1,028,250 checks, zero failing |
| gPTP regressions | PASS: full `make -j8 tb`, rc 0 |
| Auxiliary checks | Eight commands rc 0; all required builder elaboration arms pass; historical calibration gate 11 is not run (see limitations) |
| Firmware regressions | PASS: required RV32 execution and self-tests, two jobs, rc 0 |
| Full local simulations | PASS: all five shards rc 0; exact 62-suite union; 2,187,183 checks, zero failures; canonical tally rc 0 |

The current accepted resource record describes `bee1b0d7`, before these dev imports.
It is not labelled as a measurement of this merge.
This round measures the candidate and dev separately for attribution.
The accepted baseline stays at its recorded input head under `docs/design/AREA_BUDGET.md:453` (D7) and `:530` (inherited Mark II movement). Fresh measurements are compared with that policy and written through `record --write` to an external measurement copy; the improvement recommendation does not authorize replacing the repository baseline.


## Authoritative references

- IEEE 1722-2016 Annex B: B.2, Table B.7 and note d, B.3.4, B.3.5.9, B.3.6.1, B.3.6.4, B.3.6.6 and B.4/Table B.9.
- [Requirements](../REQUIREMENTS.md), [MAAP contract](../docs/design/MAAP_FABRIC.md), [resource policy](../docs/design/AREA_BUDGET.md), and [measurement recipe](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md).
- Issue #696 rulings: 6076940309 (M8), 6079087547 (shared response storage), 6089712293 (timing floor), 6102832618 (first-draw criterion), 6142198285 (this merge round).

## How to get into the same state

After publication of this head:

```sh
git fetch origin
git checkout 313616d1a18549d41907db389d378f0beb9bc543
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
: "${WORK:?Set an empty disk-backed scratch directory}"
: "${VERILATOR:?Select the pinned 5.050 executable}"
: "${MILAN_RV32_CC:?Select the verified RV32 compiler}"
export TMPDIR="$WORK" VERILATOR VERILATOR_JOBS=2 MILAN_RV32_CC
```

Use the pinned documentation environment and matching coverage reader.
Build the packet generator at the revision pinned by `.github/workflows/rtl.yml`.
Point `TSN_GEN_ROOT` to that clean checkout.

## How to validate

```sh
python3 scripts/suite_shards.py --selftest
make -j8 -C tb/verilator/maap MDIR="$WORK/unit"
make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration"
(cd "$WORK/integration" && ./maap_integration)
make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage"
python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"
bash scripts/run_all_suites.sh "$WORK/parent-logs"
bash syn/yosys/run.sh --results "$WORK/portability-results"
python3 scripts/lint_rtl.py --check --self-test --jobs 2
(cd tests && python3 -m behave --no-capture -f plain)
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base e81ce82f
python3 scripts/measure_test_evidence.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration
```

Measure the recipe's three endpoints using `--single-thread-synthesis`,
with `--integrated-clock` for both standalone endpoints.
Serialize each synthesis and route under the exclusive lock; keep simulations separate.

```sh
python3 syn/ooc/pp_resource_gate.py check "$ROUTE" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_1X1" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_8X8" --endpoint ooc-8x8
```

Expected results: every gate exits 0; MAAP reports 186 clean checks and 65 campaign rows
(63 named defect rejections and two clean controls); the datapath reports five clean checks;
line coverage is 225/225; the differential passes 12 cases and catches 17 defects.
The full sweep passed with `--shard 0/5` through `--shard 4/5` in separate checkouts at the same head. All five exit codes are zero, their exact disjoint union matches the default 62-suite inventory, and the repository tally over the combined logs passes.
The first launcher inherited ignored HUP and failed the cancellation preflight; restoring normal signal dispositions made it pass. The later serial run was cancelled after 19 passing suites to use the parallel distribution; its partial results do not count.
The coverage table in HANDOFF.md identifies each planted defect and its required named rejection. Its command ledger and bounded receipts include every completed command, the processor and gPTP banks, the auxiliary gates, source hashes and resource records.
The MAAP counts above are completed merged-head results. The parent sweep, focused gates and eight auxiliary commands have also completed; the builder coverage limit is stated below.

## Known limitations / out of scope

- Full Annex B conformance is not claimed. The pool fold/clip remains biased.
- M6 holds one pending or transmitting response. Further PROBEs while occupied remain unsupported, including during DEFEND.
- First-claim separation covers nonzero seeds a power of two apart and blocks of 1..8 addresses. Other seed pairs can overlap.
- Every-seed checks use the reviewed linear structure, learned maps and sampled linearity checks; they do not exhaust arbitrary nonlinear functions.
- Optional earlier suggestions about later Begin! draws and other block sizes at the pool clip remain outside this round.
- M8 discard accounting requires a separate register-map decision and remains withdrawn from this lane.
- Tagged reception remains outside scope.
- The FF allowance is fully used.
- Builder gate 11, the unchanged legacy estimator calibration, did not run because its historical placement report is absent. The builder command exits 0 with every required elaboration arm covered; the skipped arm is not claimed as passed.
- Validation resource exception: the service recorded an earlier 10.56 GB peak, above the requested 9 GB limit, without an out-of-memory event. A hard 8.9 GB limit now guards the remaining jobs.
- Acceptance 4, reference-peer bench interoperability, belongs to the post-merge bench lane.
- New-head independent review, publication, hosted acceptance and the local workflow replica remain pending. The previous head's passes are not relabelled as new-head evidence.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (bench acceptance is separately assigned)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes at the merged head
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal independent review covers this merged head
- [ ] External independent review covers this merged head
- [ ] Blocking and major findings are fixed and re-reviewed at the candidate
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
