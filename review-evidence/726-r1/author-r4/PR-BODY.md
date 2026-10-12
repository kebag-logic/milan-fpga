[A605]

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

Round 4 source head: `1add0cfbcc778c5292a5935631ca7b47c612b990`.
The corrected cadence criterion and recursive make fix are implemented.
`726-stream-counters` targets `dev`.
Required hosted shard 4/5 success remains outstanding at this head.
Independent re-review and merge-turn acceptance remain required.

## Linked Issue / roles

Relates to #726

Executor: `[A605]`
Internal cleared-context reviewer: `[R628]`
External reviewer: `[R629]`

## Description

AAF and CRF FRAMES_TX count every transmitted AVTPDU.
Stream Input FRAMES_RX counts accepted AVTPDUs.
Both wrap at 32 bits.
TX resets at talker start; RX resets on binding.
Unbind preserves RX totals; AAF pending totals use 32 bits.
Healthy counter updates mark their descriptor dirty.
The existing notification scheduler retains Milan spacing.
The interface throttle is unchanged.

### Round 4

R628-3-F2: both captured make exports suppress directory banners.
Inherited `-w` no longer enters compiler arguments.
Clean counter legs print `RESULT: PASS` into suite logs.
The direct inherited-flag command and recursive counters target pass.
The required hosted shard still needs its new-head result.
Its `suite-logs-4` artifact must contain the counter verdicts.

R628-3-F1: every consecutive notification gap is graded.
Grading starts with the first captured notification.
The final wait is bounded; insufficient observations fail.
There is no startup exclusion or fixed-bin criterion.
Frames after service measurement ends are excluded.
Both shapes retain the same verdict across every cycle
position through one simulated second: 1,000,001 starts per row.
Restoring fixed-bin grading fails PHASE and escapes without PHASE.
The mailbox fixture applies the same criterion and phase control.

R628-3-R1 and R629-3-R01: stale publication wording is removed.
The prior packet-law, reset, snapshot and cross-device fixes remain.
Production RTL, firmware implementation and submodule pins are unchanged
by Round 4.

## Authoritative references

- Issue #726 acceptance and assignment 6125784157.
- Counter ruling 6125741685 and addendum 6125845117.
- Corrected cadence ruling and Round 4 assignment 6132483068.
- Reviews R628-3, comment 6132474230, and R629-3, comment 6132316626.
- IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157 and 7.159.
- Milan v1.2 Table 5.4 reset and 5.4.5.2 Table 5.22 spacing.
- `docs/testing/726_STREAM_COUNTERS.md` and `docs/reference/REGISTER_MAP.md`.

## How to get into the same state

```sh
git switch 726-stream-counters
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Use runtime 3.12.3 and pinned simulator release 5.050.
Set VERILATOR to that executable and TMPDIR to disk scratch.
Use two compiler workers and at most two concurrent simulation builds.
Install the pinned dependencies from `.github/workflows/docs.yml`.

## How to validate

```sh
MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1
make -j8 -C tb/verilator/milan_dp counters
make -C tb/verilator/milan_dp counters-f5 counters-mutants
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --variant before
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --variant before
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/lint_rtl.py --check --jobs 2
python3 scripts/check_nvm_capture.py
cd tests
python3 -m behave --no-capture -f plain
cd ..
python3 tb/tools/torture_campaign.py --self-test
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
git diff --check c6bd08c6 HEAD
```

Run the remaining commands in the complete documentation workflow.
All 78 executable docs-check commands and three companion checks returned 0.
The full builder verdict excludes its 19 explicitly reported NOT RUN arms.
Its offline runner self-test belongs inside a disposable CI job.
The evidence packet records every command, result and limitation.

| Validation | Result |
|---|---|
| Inherited flag and recursive counters | Both rc 0; four recursive legs print RESULT: PASS. |
| Parent uncertain outputs | 58 shipping / 247 largest checks pass. |
| Parent frames-only outputs | 70 shipping / 301 largest checks pass. |
| Baseline controls | 12 / 54 required TX, RX and CADENCE failures; drivers pass. |
| Parent controls | Ten named detections and matching omission escapes pass. |
| Mailbox | Both shapes and three detection/omission pairs pass. |
| Separate start shifts | 0, 200, 300, 800, 900 microseconds and one second pass at both shapes. |
| Behavior / grader | 406 scenarios, 1,977 steps; 80 self-tests; zero failures. |
| Source inventories, lint, capture and documentation gates | All return 0; complete builder reports 19 optional NOT RUN arms. |
| Whitespace | Working-tree and base-to-head checks pass. |

| Shape | Consecutive gaps per condition | Minimum gap | Maximum gap | Maximum service |
|---|---:|---:|---:|---:|
| Shipping | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Every gap respects the rate limit and measured service bound.
Each corrected input row has four notifications; each output has five.
Baseline input rows have one notification, followed by silence.
The frames-only condition keeps output TU/MR counters and wire bits zero.
FRAMES_TX is its only changing output counter after the initial start.
Mailbox gaps are 1000-1002 ms, including the injected stall.

Fixed bins are retained only as descriptive measurements.
Shipping input 0, recipient 0, has an empty bin 1.
The largest shape has this empty bin for both recipients.
The scheduler stamps completion, causing drift against fixed bins.
These empty bins are neither excluded nor graded as failures.
The packet retains 660 parent bin rows and 528 notification timestamps.

## Known limitations / out of scope

- Hosted shard 4/5 at this source head remains unverified.
- Independent re-review and the current-dev candidate bank remain required.
- Physical cadence, reference-peer reset comparison and controller display belong to the merge turn.
- Finite compressed-time runs cover two recipients, not maximum fanout.
- The mailbox fixture injects change events; production caller integration is unproved.
- No production code changes in Round 4 trigger a new image or capture measurement.
- Retained routed area: 49,427 LUT (+35 against 49,392), 53,378 FF, 87.5 BRAM tiles.
- Retained constrained WNS/WHS: +0.451/+0.036 ns; external I/O limitations remain.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
