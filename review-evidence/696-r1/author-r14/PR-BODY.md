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

GREEN: Round 14 local validation passed on `696-maap-annexb` against `dev`: 38,218 checks in seven selected default suites, unchanged from Round 13.
Local head: `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`.
The published PR #706 head remains `313616d1a18549d41907db389d378f0beb9bc543` until the manager publishes this merge.

## Linked Issue / roles

Closes #696

Executor: `[A570]`
Internal independent reviewer: `[R558]`
External independent reviewer: `[R559]`

R558-13 and R559-10 are POSITIVE at `313616d1`.
Those verdicts precede this merge; independent review of this head remains pending.

## Description

The fabric MAAP allocator samples the programmed identity and clock at first enable.
The assigned Annex B corrections retain their clause-based checks and planted defects.

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

### Round 14: merge the shared-stack candidate

Assignment: [issue comment 6148294623](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6148294623).

Merge `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` has ordered parents
`313616d1a18549d41907db389d378f0beb9bc543` and
`d40e4e9827be2516f8f34b9d65f0a483fff2194c` (PR #705, `697-consume`).
The resulting tree is `295aadcc963e941f2fcc97b27d497aa787da0d86`.
Until #705 merges, PR #706's diff shows 697c's commits.
No additional dev merge was made.

There is one conflicted file: `sw/firmware/ctrl/test/maap_differential.py`.
Its resolution retains the shared stack pin proof in both command modes,
the stack-built C core and object/library link order, and the Annex B differential's
optional RTL source, 17 planted defects and named MAC/phase rejection.
The stack remains pinned at `405dc68310a18f669049ffc10cc23eef7300dcff`.
Every other path equals the automatic merge result; no other imported file was edited by hand.
The MAAP RTL, integration wiring, unit/integration harnesses, mutation table and Annex B contract are unchanged from Round 13.

| Gate | Round 13 | Round 14 |
|---|---|---|
| MAAP unit | 186 checks | 186, zero failures, rc 0 |
| MAAP campaign | 63 rejected defects, 2 clean controls | Identical totals; zero failures, rc 0 |
| Datapath integration | 5 checks | 5, zero failures, rc 0 |
| Line coverage | 225/225 | 225/225 eligible lines; rc 0 |
| Differential | 12 cases, 17/17 rejected defects | 12 clean cases; 17/17 rejected defects; rc 0 |
| Documentation and static gates | 28 passing commands | 28 passing commands |
| Shipping route | 49,277 LUT / 53,419 FF; WNS +0.242 ns; WHS +0.017 ns | Identical figures; complete route; rc 0 |
| Standalone resource endpoints | Both pass | Both pass with identical figures; rc 0 |
| Firmware parent campaign | 506/506 rejected defects | 506/506; full firmware command rc 0 |
| Store gate | Not separately recorded | 435 tests across 5 shapes; rc 0 |
| Coverage self-test | Not separately recorded | 29/29 planted cases; rc 0 |
| Firmware coverage | Not separately recorded | 30 files pass after declared exclusions; rc 0 |
| Shared-stack boundary | Not separately recorded | 117 boundary, 120 pin and 4 figure controls; zero findings/misbehavior; rc 0 after environment correction |
| Other merge-touched suites | Seven selected suites: 38,218 checks | Same 38,218 checks; all final gate commands rc 0 |

The accepted source baseline remains at its recorded input head under the resource policy's D7 rule. Fresh measurements are checked against that policy and written through `record --write` to an external measurement copy. This merge changes no baseline policy or accepted source record.

All six shipping memory-image hashes equal Round 13's. The three measurement records were written successfully, and all 251 measured input-file checks remained unchanged.

The first boundary attempt refused the documentation interpreter because `migen` was absent. Repeating the full gate with the installed build interpreter passed; no source changed. The refused attempt remains in the evidence packet.

Portability passed 58/58 tops. Behavior passed 14 features, 406 scenarios and 1,977 steps. Control-memory checks caught 44 planted defects; sharding retained 916 invocations with no omissions or duplicates. The builder command exited 0 with every required elaboration arm run; its unchanged historical calibration arm remains explicitly not run.

Round 13's full 62-suite total of 2,187,183 checks belongs to `313616d1`.
It is not a fresh execution at this merge head.

## Authoritative references

- IEEE 1722-2016 Annex B: B.2, Table B.7 and note d, B.3.4, B.3.5.9, B.3.6.1, B.3.6.4, B.3.6.6, and B.4/Table B.9.
- [Requirements](../REQUIREMENTS.md), [MAAP contract](../docs/design/MAAP_FABRIC.md), [resource policy](../docs/design/AREA_BUDGET.md), and [measurement recipe](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md).
- Issue #696 rulings: 6076940309 (M8), 6079087547 (shared response storage), 6089712293 (timing floor), 6102832618 (first-draw criterion), 6148294623 (Round 14).

## How to get into the same state

After the manager publishes this head:

```sh
git fetch origin
git checkout e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
: "${WORK:?Set an empty disk-backed scratch directory}"
: "${VERILATOR:?Select the pinned 5.050 executable}"
: "${MILAN_RV32_CC:?Select the verified RV32 compiler}"
: "${MILAN_LITEX_PYTHON:?Select the installed build interpreter}"
export TMPDIR="$WORK" VERILATOR VERILATOR_JOBS=2 MILAN_RV32_CC MILAN_LITEX_PYTHON
"$MILAN_LITEX_PYTHON" -c 'import migen, litex, litex_boards, yaml'
```

Use the pinned documentation environment and matching coverage reader.
Before commands within a submodule, verify its top-level directory matches its checkout.

## How to validate

```sh
make -j8 -C tb/verilator/maap MDIR="$WORK/unit"
make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration"
(cd "$WORK/integration" && ./maap_integration)
make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage"
python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 2
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2
"$MILAN_LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
"$MILAN_LITEX_PYTHON" sw/litex/test_ctrl_memory.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration
make -j8 -C tb/verilator/milan_dp
make -j8 -C tb/verilator/mbx
make -j8 -C tb/verilator/pp_shadow
make -j8 -C tb/verilator/capture_coherence
make -j8 -C tb/verilator/milan_dp_mclk
make -j8 -C tb/verilator/milan_dp_render
bash syn/yosys/run.sh --results "$WORK/portability-results"
python3 scripts/lint_rtl.py --check --self-test --jobs 2
(cd tests && python3 -m behave --no-capture -f plain)
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base e81ce82f
python3 scripts/measure_test_evidence.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Run the resource recipe separately from simulation and compilation.
Use `--single-thread-synthesis`, `--integrated-clock` for standalone endpoints,
and the exclusive synthesis/route lock. Write measurement copies through `record --write`.

```sh
python3 syn/ooc/pp_resource_gate.py check "$ROUTE" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_1X1" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_8X8" --endpoint ooc-8x8
```

Expected: every gate exits 0; the MAAP totals match Round 13.
HANDOFF.md records each imported path, the resolution, test-to-defect coverage and exact command results.

## Known limitations / out of scope

- Builder gate 11, historical estimator calibration, did not run because its reference report is absent; this unchanged arm is not counted as covered.
- Full Annex B conformance is not claimed. The pool fold/clip remains biased.
- M6 holds one pending or transmitting response. Further PROBEs while occupied remain unsupported, including during DEFEND.
- First-claim separation covers nonzero seeds a power of two apart and blocks of 1..8 addresses. Other seed pairs can overlap.
- Every-seed checks use the reviewed linear structure, learned maps and sampled linearity checks; they do not exhaust arbitrary nonlinear functions.
- Optional earlier suggestions about later Begin! draws and other block sizes at the pool clip remain outside this round.
- M8 discard accounting requires a separate register-map decision and remains withdrawn from this lane.
- Tagged reception remains outside scope. The FF allowance is fully used.
- Acceptance 4, reference-peer bench interoperability, belongs to the post-merge bench lane.
- Independent review of this head, publication, hosted acceptance and workflow replication remain manager duties.

## Definition of Done

- [x] Linked Issue non-bench acceptance criteria are satisfied (bench acceptance is separately assigned)
- [x] New or changed behavior has self-checking tests
- [x] Required Round 14 local verification passes at the merged head (historical calibration exception disclosed above)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal independent review covers this merged head
- [ ] External independent review covers this merged head
- [ ] Blocking and major findings are fixed and re-reviewed at the candidate
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
