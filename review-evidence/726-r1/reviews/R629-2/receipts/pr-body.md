[A605]

## Contents

- **[Status](#status)** -- Implementation and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent reviewers.
- **[Description](#description)** -- Counter and notification behavior.
- **[Authoritative references](#authoritative-references)** -- Rulings and contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Branch and dependencies.
- **[How to validate](#how-to-validate)** -- Reproducible checks.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Pending evidence and bench work.
- **[Definition of Done](#definition-of-done)** -- Remaining review and merge obligations.

## Status

Round 2 corrections on `726-stream-counters` -> `dev`.
Final local head: `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb`.
The behavior gate passes 405 scenarios with zero failures.
All nine parent and two mailbox mutation/omission pairs pass.
The shipping image remains 49,427 LUT (+35), 53,378 FF and 87.5 BRAM.
Its recorded input hashes match; this round changes tests and documentation.
Hosted checks require publication of the corrected head.

## Linked Issue / roles

Relates to #726

Physical cadence, the reference-peer reset comparison and controller display
remain merge-turn evidence. Complete acceptance is not claimed.

Executor: `[A605]`
Internal cleared-context reviewer: `[R628]`
External reviewer: `[R629]`

## Description

AAF and CRF transmit counters count every AVTPDU and reset at each start.
CRF receive counters count every accepted AVTPDU. Receive totals reset on
binding and survive unbind. The AAF pending batch uses all 32 bits.
Healthy input updates mark the descriptor dirty for rate-limited notifications.

### Round 2

The bind-era check now requires the six retained anomaly flags and all ten
counter resets. Its bind-only reset and lock-state checks remain intact.
The counter law table and receive-rate grader follow Table 7.157.
An interval-rate FRAMES_RX on a flowing stream now fails the behavior contract.
Single-snapshot TV/TNV comparisons remain diagnostic because publication is coalesced.

The parent fixture grades both shapes with only FRAMES_TX changing on outputs.
It verifies clear wire `tu`/`mr`, zero TU/MR counts, and no streaming transitions
after the initial start. Removing the packet-change event produces 16 named
`OUTPUT_CADENCE` failures and passes with only that check group omitted.
The baseline driver now requires named TX, RX and CADENCE failures.
Four obsolete suite passages are corrected, and the stale status sentence is removed.

## Authoritative references

- Issue #726 acceptance and assignment comment 6125784157.
- Counter ruling 6125741685, addendum 6125845117 and window ruling 6126028604.
- The latest Round 2 assignment and reviews R628-1 / R629-1.
- IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157 and 7.159.
- Milan v1.2 Table 5.4 reset and 5.4.5.2 Table 5.22 spacing.
- `docs/reference/REGISTER_MAP.md` and `docs/testing/726_STREAM_COUNTERS.md`.

## How to get into the same state

```sh
git switch 726-stream-counters
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Use CPython 3.12.3 and the pinned simulator, with disk scratch.
Set TMPDIR to scratch storage and VERILATOR to the pinned executable.
Use two compiler workers and at most two simultaneous simulation builds.

## How to validate

```sh
cd tests
python3 -m behave --no-capture -f plain
cd ..
python3 tb/tools/torture_campaign.py --self-test
make -C tb/verilator/milan_dp counters counters-f5 counters-mutants
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --variant before
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --variant before
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_nvm_capture.py
python3 scripts/lint_rtl.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
git diff --check
```

The behavior gate passes 405 scenarios; the grader passes 78 self-tests.
Parent checks pass 98/427 checks under the original uncertain condition and
110/481 with output FRAMES_TX alone changing. Every graded row-window holds
one notification. Minimum/maximum gaps are 1000.996/1001.867 ms at shipping
shape and 1000.982/1012.029 ms at largest shape, within measured service delay.
The original baseline has zero notifications in every graded input row-window.
Its outputs stamp `tu=1`, and periodic TU changes also mark them dirty.
The new frames-only runs stamp `tu=0` and keep `mr=0` on every output.

The counter targets are executed as separate foreground driver commands with
retained scratch builds. Each plant must fail by name and then escape with
its check omitted. The handoff records each command, result and artifact hash.
The original affected unit, parent integration, synthesis and image receipts
remain applicable to their unchanged production inputs.

## Known limitations / out of scope

- Windows 0 and 1 record startup; only steady windows 2 through 4 are graded.
- Protocol time is compressed; physical cadence and maximum fanout remain unmeasured.
- The reference-peer comparison and controller display require merge-turn bench work.
- Production RTL, firmware implementation and submodule pins are unchanged in Round 2.
- The saved-state capture guard passes; no new capture measurement is required.
- The full current-dev candidate bank, hosted checks and independent re-review remain required.
- Historical cross-device interval-comparison helpers remain outside this receive-rate correction.

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

