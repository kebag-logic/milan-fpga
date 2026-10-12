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

Round 6 local source head: `12f00129349c889e6dbbb7de11529ab38c9d164d`.
Focused local validation passes; two new commits await publication.
`726-stream-counters` targets `dev`.
Independent re-review and merge-turn acceptance remain required.

Round 5 published source head: `e7d604faa0472d505d6459883b382c2b237ad06d`.
Focused local validation passes; both Round 5 commits are published.
The prior Round 4 hosted shard 4/5 succeeded at `1add0cfb`.
Its `suite-logs-4` contains all four counters legs' `RESULT: PASS`.
That prior result does not establish hosted acceptance for this head.

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
The existing scheduler retains Milan spacing and the interface throttle.

### Round 6

R628-5-F1 removes measured service from the refresh verdict.
Every consecutive gap and final wait must be at most 1025 ms.
Ruling 6134121887 fixes the service ceiling at 25 ms.
Its source is the prior 1012.029 ms maximum gap, plus margin.
Measured service remains descriptive and cannot enlarge that ceiling.
Spacing remains at least the Milan rate limit.

The standing parent egress plant delays eligible frames by 900 ms.
It runs at both shapes, fails CADENCE, and escapes without CADENCE.
All three unchanged review probes also fail CADENCE at both shapes.
Each of those six runs passes with only CADENCE omitted.
All measurement starts through one second retain the same verdict.
The mailbox fixture keeps its stricter 1003 ms ceiling.

R628-5-R1 through R5 correct counter comments, historical wording,
and the two clause tags without changing assertions or production behavior.
R628-5-R6 and R629-5-R01 correct the Round 5 publication status above.
No production RTL logic, firmware implementation or submodule changes this round.

## Authoritative references

- Issue #726 acceptance and assignment 6125784157.
- Counter ruling 6125741685 and addendum 6125845117.
- Corrected cadence ruling 6132483068 and fixed-ceiling precision 6134121887.
- Reviews R628-5, comment 6134115312, and R629-5, comment 6134076275.
- IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157 and 7.159.
- Milan v1.2 Table 5.4 reset and 5.4.5.2 Table 5.22 spacing.
- `docs/testing/726_STREAM_COUNTERS.md` and `docs/reference/REGISTER_MAP.md`.

## How to get into the same state

```sh
git switch 726-stream-counters
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Use runtime 3.12.3 and pinned simulator release 5.050.
Set VERILATOR to that executable and TMPDIR to disk scratch.
Use two compiler workers and at most two concurrent simulation builds.
Install the pinned documentation and firmware test dependencies.
Both Round 6 commits remain local pending authorized publication.

## How to validate

```sh
make -j8 -C tb/verilator/milan_dp counters
make -C tb/verilator/milan_dp counters-mutants
make -C tb/verilator/milan_dp counters-f5
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --variant before
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --variant before
make -j8 -C tb/verilator/avtp_rxmon run
make -j8 -C tb/verilator/crf_rx unit
make -j8 -C tb/verilator/crf_rx discontinuity
make -j8 -C tb/verilator/crf_rx talker_step
make -j8 -C tb/verilator/crf_rx mutants
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/lint_rtl.py --check --jobs 2
python3 scripts/check_nvm_capture.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
cd tests
python3 -m behave --no-capture -f plain
cd ..
python3 tb/tools/torture_campaign.py --self-test
git diff --check c6bd08c6 HEAD
```

Expected result: every driver returns zero.
Planted defects fail their named check and pass its omission control.
The long mutation target ran as bounded foreground driver groups.
Unit recipes used identical source inputs in disk scratch.
The evidence packet records every actual command and result.

| Round 6 validation | Result |
|---|---|
| Recursive counters | Four RESULT: PASS legs |
| Uncertain / frames-only | 58/247 and 70/301 checks, shipping/largest |
| Baseline controls | 12/54 required TX, RX and CADENCE failures; drivers pass |
| Standing parent and mailbox plants | Fifteen detection/omission pairs pass |
| Unchanged reviewer probes | Six CADENCE detections and clean omission escapes |
| Receive regression | 97 single-sink, 119 NxN, 36+36 lockstep; four plants caught |
| CRF regression | 14,287 unit, 2,201 discontinuity, 69 talker-step; ten campaign checks |
| Behavior / grader | 406 scenarios, 1,977 steps; 80 self-tests |
| Sources, lint, capture, language and documentation | Final gates return zero; budgets unchanged |
| Whitespace | Working-tree and committed-range checks pass |

| Shape, either output condition | Consecutive gaps | Minimum | Maximum | Measured service maximum |
|---|---:|---:|---:|---:|
| Shipping | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Every corrected gap and final wait satisfies the fixed 1025 ms bound.
Input rows have four notifications; output rows have five.
Baseline input rows have one notification followed by silence.
Frames-only output TU/MR counters and wire bits stay zero.
The mailbox gaps remain 1000-1002 ms, including the injected stall.
Fixed bins are descriptive; completion-stamp drift can leave bins empty.
The packet retains 660 per-second rows and 528 notification timestamps.

## Known limitations / out of scope

- Independent re-review, authorized publication and hosted acceptance remain required.
- After publication, the trusted current-dev workflow replica must precede hosted inspection.
- The current-dev candidate bank remains required; prior banks are earlier-head evidence.
- Physical cadence, reference-peer reset comparison and controller display belong to the merge turn.
- Finite compressed-time runs cover two recipients, not maximum fanout.
- The mailbox fixture injects change events; production caller integration is unproved.
- Production inputs are unchanged, so image and capture remeasurement are not triggered.
- Retained routed area: 49,427 LUT (+35 against 49,392), 53,378 FF, 87.5 BRAM tiles.
- Retained constrained WNS/WHS: +0.451/+0.036 ns; external-I/O limitations remain.

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
