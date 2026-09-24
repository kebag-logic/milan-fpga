[A277]

## Status

Round 3 for `387-media-rebase` -> `dev`, head `0f003fab3303858ba4db955ad3c0512e67a8018b`.
The assigned local validation is green.
The corrected head still requires independent re-review and candidate validation.

## Linked issue and roles

Relates to #387: this is the datapath half of acceptance 3.
Acceptance 4, the two-board grandmaster-handover measurement, remains open.
That measurement stays with the manager's #117 bench step after merge.

Author: `[A277]`, round 3, under the [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975).
Internal and external reviewers: independent cleared-context re-reviews remain required.

## Description

A PHC step requests one media restart on every running Stream Output, irrespective of clock-source selection. The render stage re-centres once. The outgoing `mr` toggle contributes one MEDIA_RESET event. A restart already pending on a stream absorbs another request until the first PDU at its adopted level is reported. The eight-PDU hold remains per stream.

The step set comprises the fabric plane's step, a plane-off CLKV adjtime, and software settime. The render stage also re-centres after a settled clock-source change. Grandmaster identity alone no longer triggers that stage. CRF disruption and echo remain gated by CRF selection. The grid aligner and CRF servo retain their decided contracts.

The branch includes the gmstep integration leg, per-stream pending-window tests in tkdiag, option-off settime checks, mutation controls, builder contract checks, and the corresponding documentation.

Round 3 addresses [R276-5](https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5820231837) and [R277-4](https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5820575348):

- The `milan_dp` deadline is 3600 seconds. Its runner contract and mutation test pin that value. Hosted shards already allow 120 minutes.
- `gmstep_mutants.py` suppresses directory announcements when reading recipe inputs. Both gmstep and option-off positive controls reuse fresh binaries under nested recipes.
- The FPGA design, compliance matrix, and roadmap scope selection gating to CRF triggers. A PHC step toggles `mr` and counts MEDIA_RESET whatever the selection.
- The render-stage summary states the same trigger set as its banner and port contract. The restart-engine comment explains why stopping a stream on `hold_r == 0` follows the non-streaming target rule.
- `RENDER-SETTIME` issues an absolute settime through the live CSR path. It requires one render pulse and one counted re-base, then observes another 100 PDUs for a duplicate. A local control removing only settime from the render trigger fails these checks.

Round 3 changes harness and validation code; its RTL edits are comments only.

## Decisions and authoritative references

[Decision 5819379503](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819379503) selects the PDU report as the engine's launch boundary. A request between the actual launch and its report merges into the existing restart. This bounded residue is accepted and documented; no launch-port extension is required. The same decision keeps the three acceptance controls in the default sweep and leaves additional controls in `gmstep-mutants`.

[Decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308) raises the deadline after the prior margin fell below 10%. The windows run from `shard: 4/5` through `PASS milan_dp`:

| Sample | Window | Checks | Evidence |
|---|---|---|---|
| dev `9d3288107e` | 1296.1 s | 9635 | [hosted job](https://github.com/kebag-logic/milan-fpga/actions/runs/35981190398/job/107573353073) |
| PR head `a9636e0f` | 2264.9 s | 9775 | [hosted job](https://github.com/kebag-logic/milan-fpga/actions/runs/36025349467/job/107720800104) |
| PR head `a21cd358` | 2459.9 s | 9781 | [hosted job](https://github.com/kebag-logic/milan-fpga/actions/runs/36038109516/job/107763352706) |

The day's spread was 1296-2460 seconds. The `a21cd358` sample left 240.1 seconds, 8.9% of the former 2700-second budget. Against 3600 seconds it leaves 1140.1 seconds, 31.7% (approximately 32%). These are historical samples, not measurements of this corrected head. If a later exact-head sample leaves less than 10%, the next step is further sharding.

Other governing references:

- [Issue #387 decision part b](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5606198212), [owner step policy](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5794731090), [re-base and pending-restart ruling](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260), [wire-boundary ruling](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077), and [aligner decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282).
- IEEE 1722-2016 4.4.4.3 and 10.4.3; Milan v1.2 Table 5.4; REQ-PTP-08.
- `docs/design/GM_LOSS_RECOVERY.md`, `docs/design/TIME_SYNC.md`, and `docs/testing/CI_WORKFLOWS.md`.

## Reproduction and validation

Use the PR branch with the three required submodules initialized at their pins. Install the locked dependencies in `tools/markdown/requirements.txt`.

```sh
make -C tb/verilator/milan_dp run VERILATOR_JOBS=8
make -C tb/verilator/milan_dp gmstep-mutants VERILATOR_JOBS=8
make -C tb/verilator/tkdiag VERILATOR_JOBS=8
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/ci_events.py --check
python3 sw/builder/test_builder.py
(cd tests && behave --no-capture -f plain)
git diff --check
```

Expected command result: exit 0. Repeat `docs_check.py` from a tracked-tree export without Git metadata. Run the full builder with RV32 candidates unavailable for the assigned compiler-absent evidence; its final verdict explicitly excludes compiler-dependent instruments and hardware calibration.

The default sweep was executed in ordered chunks, preserving every expanded recipe command and recording each exit. All 44 commands exited 0: 9785 checks, 0 failures. The gmstep leg passed 48/48; the full gmstep campaign passed 13/13; tkdiag passed 96/96 with four mutants caught. The true-ratio leg passed 143/143. Both documentation modes and all listed static checks passed. The behavior suite passed 344 scenarios. The full compiler-absent builder rejected 189/189 applicable mutations and reported its two expected exclusions. The settime omission control failed the named new checks. The nested freshness repro passed for both positive legs.

## Limits and remaining merge work

Acceptance 4 remains open. No physical handover is claimed. The pending-restart interaction is tested on the engine; gmstep and option-off legs test its datapath trigger wiring. The render settime check runs on the option-off true-ratio leg. The Arty I2S element retains its existing grandmaster-identity trigger.

This round supplies local source-head evidence. Publication of the corrected branch, hosted checks, local workflow replication, full current-dev candidate validation, and independent review remain manager-owned next steps.

## Definition of Done

- [x] Assigned round-3 fixes and taken suggestions implemented.
- [x] Decisions and remaining scope documented.
- [x] Assigned local gates pass at the corrected head.
- [ ] Local evidence published for review.
- [ ] Two independent positive reviews, including one external.
- [ ] Reviewer-owned clean coverage ledger for all five lenses.
- [ ] No BLOCKER, MAJOR, or MINOR remains open within a covered lens.
- [ ] Required hosted and candidate-merge validation complete.
- [ ] No review round remains in flight.
- [ ] Authorized merge and post-merge containment complete.
- [ ] Issue #387 acceptance 4 measured and remaining issue work closed.
